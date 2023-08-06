import codearchiver.core
import codearchiver.subprocess
import datetime
import functools
import hashlib
import itertools
import logging
import os
import shutil
import subprocess
import tempfile


_logger = logging.getLogger(__name__)


class GitMetadata(codearchiver.core.Metadata):
	fields = (
		codearchiver.core.MetadataField(key = 'Git version', required = True, repeatable = False),
		codearchiver.core.MetadataField(key = 'Based on bundle', required = False, repeatable = True),
		codearchiver.core.MetadataField(key = 'Ref', required = True, repeatable = True),
		codearchiver.core.MetadataField(key = 'Head', required = True, repeatable = False),
		codearchiver.core.MetadataField(key = 'Root commit', required = True, repeatable = True),
		codearchiver.core.MetadataField(key = 'Object', required = False, repeatable = True),
	)
	version = 0


class Git(codearchiver.core.Module):
	name = 'git'
	MetadataClass = GitMetadata

	@staticmethod
	def matches(inputUrl):
		return inputUrl.url.endswith('.git')

	def __init__(self, *args, extraBranches = {}, **kwargs):
		super().__init__(*args, **kwargs)
		self._extraBranches = extraBranches

	def process(self):
		with tempfile.TemporaryDirectory(prefix = 'tmp.codearchiver.git.', dir = os.getcwd()) as directory:
			bundle = f'{self._id}_git.bundle'
			if os.path.exists(bundle):
				_logger.fatal(f'{bundle!r} already exists')
				raise FileExistsError(f'{bundle!r} already exists')

			_, gitVersion, _ = codearchiver.subprocess.run_with_log(['git', '--version'])
			if not gitVersion.startswith('git version ') or not gitVersion.endswith('\n') or gitVersion[12:-1].strip('0123456789.') != '':
				raise RuntimeError(f'Unexpected output from `git --version`: {gitVersion!r}')
			gitVersion = gitVersion[12:-1]

			_logger.info(f'Cloning {self._url} into {directory}')
			startTime = datetime.datetime.utcnow()
			codearchiver.subprocess.run_with_log(['git', 'clone', '--verbose', '--progress', '--mirror', self._url, directory], env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0'})

			if self._extraBranches:
				for branch, commit in self._extraBranches.items():
					_logger.info(f'Fetching commit {commit} as {branch}')
					r, _, _ = codearchiver.subprocess.run_with_log(['git', 'fetch', '--verbose', '--progress', 'origin', commit], cwd = directory, check = False)
					if r == 0:
						r2, _, _ = codearchiver.subprocess.run_with_log(['git', 'update-ref', f'refs/codearchiver/{branch}', commit, ''], cwd = directory, check = False)
						if r2 != 0:
							_logger.error(f'Failed to update-ref refs/codearchiver/{branch} to {commit}')
					else:
						_logger.error(f'Failed to fetch {commit}')
				# This leaves over a FETCH_HEAD file, but git-bundle does not care about that, so it can safely be ignored.
			endTime = datetime.datetime.utcnow()

			_logger.info('Collecting repository metadata')
			_, refs, _ = codearchiver.subprocess.run_with_log(['git', 'show-ref'], cwd = directory)
			refs = list(map(str.strip, refs.splitlines()))
			_, rootCommits, _ = codearchiver.subprocess.run_with_log(['git', 'rev-list', '--max-parents=0', '--all'], cwd = directory)
			rootCommits = list(filter(None, rootCommits.splitlines()))
			_, objects, _ = codearchiver.subprocess.run_with_log(['git', 'cat-file', '--batch-check', '--batch-all-objects', '--unordered', '--buffer'], cwd = directory)
			objects = {oid: otype for oid, otype, osize in map(functools.partial(str.split, sep = ' '), objects.splitlines())}
			with open(os.path.join(directory, 'HEAD'), 'r') as fp:
				head = fp.read()
			if not head.startswith('ref: refs/heads/') or not head.endswith('\n'):
				raise RuntimeError(f'Unexpected HEAD content: {head!r}')
			head = head[:-1]  # Remove trailing \n

			# Check whether there are relevant prior bundles to create an incremental one
			commitsAndTags = {oid for oid, otype in objects.items() if otype in ('commit', 'tag')}
			basedOnBundles = {}  # dict to keep the order
			baseBundleObjects = set()
			if self._storage:
				_logger.info('Checking for previous bundles')

				# A note on dependency optimisation: we want the minimal set of previous bundles {B0, …, Bn} that maximises the cover with the current clone S.
				# In other words, in the general case, this is a set cover problem between I = S ∩ (B0 ∪ … ∪ Bn} as the universe and Bi ∩ I as the subsets.
				# Fortunately, solving the actual set cover problem is not necessary.
				# This is because the previous bundles must be disjoint: commit/tag objects are never duplicated. (Trees and blobs might be, but deduplicating those isn't possible.)
				# Therefore, any previous bundle that contains at least one commit or tag object in the current clone must be a dependency.

				for oldBundle in self._storage.search_metadata([('Module', type(self).name), ('Root commit', tuple(rootCommits))]):
					_logger.info(f'Previous bundle: {oldBundle!r}')
					with self._storage.open_metadata(oldBundle) as fp:
						idx = GitMetadata.deserialise(fp)
					isMatch = False
					oldObjects = set()  # commit and tag IDs in this bundle
					for key, value in idx:
						if key != 'Object':
							continue
						oid, otype = value.split(' ', 1)
						oldObjects.add(oid)
						if otype not in ('commit', 'tag'):
							continue
						if not isMatch and oid in commitsAndTags:
							isMatch = True
					if isMatch:
						basedOnBundles[oldBundle] = True
						baseBundleObjects |= oldObjects

			_logger.info(f'Bundling into {bundle}')
			cmd = ['git', 'bundle', 'create', '--progress', f'../{bundle}', '--stdin', '--reflog', '--all']
			objectsToExclude = baseBundleObjects & commitsAndTags
			input = ''.join(f'^{o}\n' for o in objectsToExclude).encode('ascii')
			status, _, stderr = codearchiver.subprocess.run_with_log(cmd, cwd = directory, input = input, check = False)
			if status == 128 and (stderr == 'fatal: Refusing to create empty bundle.\n' or stderr.endswith('\nfatal: Refusing to create empty bundle.\n')):
				# Manually write an empty bundle instead
				# Cf. Documentation/technical/bundle-format.txt and Documentation/technical/pack-format.txt in git's repository for details on the formats
				_logger.info('Writing empty bundle directly instead')
				with open(bundle, 'xb') as fp:
					fp.write(b'# v2 git bundle\n')  # bundle signature
					fp.write(b'\n')  # bundle end of prerequisites and refs
					packdata = b'PACK'  # pack signature
					packdata += b'\0\0\0\x02'  # pack version
					packdata += b'\0\0\0\0'  # pack number of objects
					fp.write(packdata)
					fp.write(hashlib.sha1(packdata).digest())  # pack checksum trailer
			elif status != 0:
				raise RuntimeError(f'git bundle creation returned with non-zero exit status {status}.')

			_logger.info('Indexing bundle')
			# Yes, this is stupid, but unfortunately, `git index-pack` can only read from stdin inside a repo and will still write the packfile to disk anyway.
			# So sadly, the only way here (for now) is to make a copy of the packfile and then run index-pack on it.
			with open(bundle, 'rb') as fpin:
				# Skip over header
				for line in fpin:
					if line == b'\n':
						break
				# Copy remainder (= packfile) to tmp.pack
				with open('tmp.pack', 'xb') as fpout:
					shutil.copyfileobj(fpin, fpout)
			codearchiver.subprocess.run_with_log(['git', 'index-pack', '-v', 'tmp.pack'])
			with open('tmp.idx', 'rb') as fp:
				_, index, _ = codearchiver.subprocess.run_with_log(['git', 'show-index'], input = fp)
			indexObjectIds = {l.rstrip('\n').split(' ', 2)[1] for l in index.splitlines()}
			try:
				indexObjects = {oid: objects[oid] for oid in indexObjectIds}
			except KeyError as e:
				# This should never happen since the bundle is created from the clone with exclusions...
				raise RuntimeError(f'Bundle {bundle} contains object not contained in the present clone') from e
			if objects.keys() - (baseBundleObjects | indexObjectIds) != set():
				# If there is at least one object in the clone that is not in the base bundles or the bundle index...
				raise RuntimeError('Object mismatch between clone and bundles')
			os.remove('tmp.pack')
			os.remove('tmp.idx')

			_logger.info('Checking for submodules')
			_, commitsWithSubmodules, _ = codearchiver.subprocess.run_with_log(['git', 'log', '--format=format:%H', '--diff-filter=d', '--all', '--', '.gitmodules'], cwd = directory)
			if commitsWithSubmodules:
				_logger.warning('Submodules found but extraction not supported')

		metadata = self.create_metadata(bundle, startTime, endTime)
		metadata.append('Git version', gitVersion)
		for oldBundle in basedOnBundles:
			metadata.append('Based on bundle', oldBundle)
		for line in refs:
			metadata.append('Ref', line)
		metadata.append('Head', head)
		for commitId in rootCommits:
			metadata.append('Root commit', commitId)
		for oid, otype in indexObjects.items():
			metadata.append('Object', f'{oid} {otype}')

		return codearchiver.core.Result(id = self._id, files = [(bundle, metadata)])

	def __repr__(self):
		return f'{type(self).__module__}.{type(self).__name__}({self._inputUrl!r}, extraBranches = {self._extraBranches!r})'

import abc
import codearchiver.core
import collections.abc
import contextlib
import glob
import logging
import os.path
import shutil
import typing


_logger = logging.getLogger(__name__)


class Storage(abc.ABC):
	@abc.abstractmethod
	def put(self, filename: str, metadata: typing.Optional['codearchiver.core.Metadata'] = None):
		'''Put a local file and (if provided) its metadata into storage. If an error occurs, a partial copy may remain in storage. If it completes, the local input file is removed.'''

	def put_result(self, result: 'codearchiver.core.Result'):
		'''Put a module's Result into storage. The semantics are as for `put`, and the exact behaviour regarding partial copies and leftover files on errors is undefined.'''
		for fn, metadata in result.files:
			self.put(fn, metadata)
		for _, subresult in result.submoduleResults:
			self.put_result(subresult)

	@abc.abstractmethod
	def search_metadata(self, criteria: list[tuple[str, typing.Union[str, tuple[str]]]]) -> collections.abc.Iterator[str]:
		'''
		Search all metadata in storage by criteria.
		Refer to `codearchiver.core.Metadata.matches` for the semantics of `criteria`.
		Yields all filenames where all criteria match in lexicographical order.
		'''

	@abc.abstractmethod
	@contextlib.contextmanager
	def open_metadata(self, filename: str) -> typing.TextIO:
		'''Open the metadata for a file in serialised form.'''

	@abc.abstractmethod
	@contextlib.contextmanager
	def open(self, filename: str, mode: typing.Optional[str] = 'rb') -> typing.Iterator[typing.Union[typing.BinaryIO, typing.TextIO]]:
		'''Open a file from storage. The mode must be r or rb.'''


class DirectoryStorage(Storage):
	def __init__(self, directory):
		super().__init__()
		self._directory = directory

	def _check_directory(self):
		exists = os.path.exists(self._directory)
		if exists and not os.path.isdir(self._directory):
			raise NotADirectoryError(self._directory)
		return exists

	def _ensure_directory(self):
		if not self._check_directory():
			os.makedirs(self._directory)

	def put(self, filename, metadata = None):
		self._ensure_directory()
		#FIXME: Race condition
		if os.path.exists((targetFilename := os.path.join(self._directory, os.path.basename(filename)))):
			raise FileExistsError(f'{targetFilename} already exists')
		_logger.info(f'Moving {filename} to {self._directory}')
		shutil.move(filename, self._directory)
		if not metadata:
			return
		metadataFilename = os.path.join(self._directory, f'{filename}_codearchiver_metadata.txt')
		# No need to check for existence here thanks to the 'x' mode
		_logger.info(f'Writing metadata for {filename} to {metadataFilename}')
		with open(metadataFilename, 'x') as fp:
			fp.write(metadata.serialise())

	def search_metadata(self, criteria):
		_logger.info(f'Searching metadata by criteria: {criteria!r}')
		# Replace this with `root_dir` when dropping Python 3.9 support
		escapedDirPrefix = os.path.join(glob.escape(self._directory), '')
		escapedDirPrefixLen = len(escapedDirPrefix)
		files = glob.glob(f'{escapedDirPrefix}*_codearchiver_metadata.txt')
		files.sort()
		for metadataFilename in files:
			metadataFilename = metadataFilename[escapedDirPrefixLen:]
			_logger.info(f'Searching metadata {metadataFilename}')
			with self.open(metadataFilename, 'r') as fp:
				idx = codearchiver.core.Metadata.deserialise(fp, validate = False)
			if idx.matches(criteria):
				_logger.info(f'Found metadata match {metadataFilename}')
				yield metadataFilename.rsplit('_', 2)[0]
		_logger.info('Done searching metadata')

	@contextlib.contextmanager
	def open_metadata(self, filename):
		with self.open(f'{filename}_codearchiver_metadata.txt', 'r') as fp:
			yield fp

	@contextlib.contextmanager
	def open(self, filename, mode = 'rb'):
		with open(os.path.join(self._directory, filename), mode) as fp:
			yield fp

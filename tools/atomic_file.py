"""Publish generated files only after their complete contents reach disk."""
from contextlib import contextmanager
import os
import shutil
import stat
import tempfile


@contextmanager
def atomic_open(path, mode='wb', **kwargs):
    """Write beside the destination, then replace it; failures preserve it."""
    destination = os.path.abspath(path)
    directory = os.path.dirname(destination)
    os.makedirs(directory, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + os.path.basename(path) + '.', dir=directory)
    try:
        if os.path.exists(destination):
            os.fchmod(fd, stat.S_IMODE(os.stat(destination).st_mode))
        with os.fdopen(fd, mode, **kwargs) as stream:
            fd = None
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if fd is not None:
            os.close(fd)
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_copy(source, destination):
    """Copy contents and metadata without truncating an existing destination."""
    with atomic_open(destination) as stream:
        with open(source, 'rb') as incoming:
            shutil.copyfileobj(incoming, stream)
        stream.flush()
        metadata = os.stat(source)
        os.fchmod(stream.fileno(), stat.S_IMODE(metadata.st_mode))
        os.utime(stream.fileno(), ns=(metadata.st_atime_ns, metadata.st_mtime_ns))

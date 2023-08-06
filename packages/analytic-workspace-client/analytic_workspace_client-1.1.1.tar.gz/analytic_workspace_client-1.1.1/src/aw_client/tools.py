import tempfile
import shutil
from pathlib import Path
from contextlib import contextmanager


@contextmanager
def get_temp_folder(remove_on_exit: bool = True) -> Path:
    """ """
    temp_folder = tempfile.mkdtemp()

    try:
        yield Path(temp_folder)
    finally:
        if remove_on_exit:
            shutil.rmtree(temp_folder, ignore_errors=True)

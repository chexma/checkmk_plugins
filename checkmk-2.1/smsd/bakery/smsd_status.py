from pathlib import Path
from typing import Any, Dict

from .bakery_api.v1 import FileGenerator, OS, Plugin, register

def get_smsd_status_files(conf: Dict[str, Any]) -> FileGenerator:
    yield Plugin(base_os=OS.LINUX,
                 source=Path("smsd_status"))

register.bakery_plugin(
    name="smsd_status",
    files_function=get_smsd_status_files,
)
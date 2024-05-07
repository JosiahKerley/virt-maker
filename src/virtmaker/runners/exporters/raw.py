import os
import shutil

from virtmaker.runners.exporters import Exporter
from virtmaker.runners.exporters.qcow2 import QCOW2
from virtmaker.utils.cmd import runCmd
from virtmaker.utils.qemu import qemu_img_list_snapshots


class Raw(QCOW2):
    _virt_sparsify_convert = 'raw'
    _spec_schema = QCOW2._spec_schema.copy()
    _spec_schema["title"] = f"export-{_virt_sparsify_convert}"

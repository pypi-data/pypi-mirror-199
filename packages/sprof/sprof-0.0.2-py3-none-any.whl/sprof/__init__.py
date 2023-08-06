# -*- coding: utf-8 -*-
from pathlib import Path

import sprof
from sprof.core.info import info
from sprof.core.init import init
from sprof.version import __version__

_template_path = Path(__file__).parent / "data" / "project_template"

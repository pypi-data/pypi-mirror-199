from setuptools import setup
from pathlib import Path

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
)

JS_DIR = Path(__file__).resolve().parent / 'js'

# Representative files that should exist after a successful build
jstargets = [JS_DIR / 'dist' / 'index.js']

data_files_spec = [
    ('share/jupyter/nbextensions/ipyd3', 'ipyd3/nbextension', '*.*'),
    ('share/jupyter/labextensions/ipyd3', 'ipyd3/labextension', '**'),
    ('share/jupyter/labextensions/ipyd3', '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'ipyd3.json'),
]

cmdclass = create_cmdclass('jsdeps', data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(JS_DIR, npm=['yarn'], build_cmd='build:prod'),
    ensure_targets(jstargets),
)

# See setup.cfg for other parameters
setup(cmdclass=cmdclass)

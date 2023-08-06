# ipyd3

Library for visualizing D3.js inside Jupyter.

## Installation

To install use pip:

    $ pip install ipyd3

For a development installation (requires [Node.js](https://nodejs.org) and [Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com//ipyd3.git
    $ cd ipyd3
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix ipyd3
    $ jupyter nbextension enable --py --sys-prefix ipyd3

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite ipyd3

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.

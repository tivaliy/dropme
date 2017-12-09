======
dropme
======

Command Line Interface tool to manage data in Dropbox workspace (based on official
`dropbox-sdk-python <https://github.com/dropbox/dropbox-sdk-python/>`_).

How to install
==============
1. Clone ``dropme`` repository: ``git clone https://github.com/tivaliy/dropme.git``.
2. Configure ``settings.yaml`` file (in ``dropme/settings.yaml``).

.. code-block:: yaml

    token: YOUR_DROPBOX_ACCESS_TOKEN

3. Create isolated Python environment ``virtualenv venv`` and activate it ``source venv/bin/activate``.
4. Install ``dropme`` with all necessary dependencies:

    ``pip install -r requirements.txt .``

5. (Optional) Add ``dropme`` command bash completion:

    ``dropme complete | sudo tee /etc/bash_completion.d/gc.bash_completion > /dev/null``

    Restart terminal and activate virtual environment once again.

Quick Start
===========

* as a standalone application:

.. code-block:: console

        $ dropme
        (dropme) whoami
        +--------------+------------------------+
        | Field        | Value                  |
        +--------------+------------------------+
        | user         | John Doe               |
        | e_mail       | j.doe@example.com      |
        | country      | UA                     |
        | account_type | basic                  |
        +--------------+------------------------+
        (dropme) ls -l
        +------+---------+---------------------+-----------------------------+
        | type | size    | last_modified       | name                        |
        +------+---------+---------------------+-----------------------------+
        | d    |         |                     | demo/                       |
        | d    |         |                     | foo/                        |
        | d    |         |                     | dummy/                      |
        | -    | 1.11 MB | 2017-10-29 11:12:54 | Start work with Dropbox.pdf |
        | -    | 19.0 B  | 2017-11-17 12:41:29 | bar.txt                     |
        +------+---------+---------------------+-----------------------------+

* as a command with respective sub-command arguments:

.. code-block:: console

        $ dropme df
        +-----------+-----------------+
        | Field     | Value           |
        +-----------+-----------------+
        | allocated | 2.0 GB          |
        | used      | 326.19 MB       |
        | available | 1.68 GB (84.1%) |
        +-----------+-----------------+

Common Usage
============

To get help on a specific :command:`dropme` command enter:

.. code-block:: console

   $ dropme COMMAND --help

All :command:`dropme` commands support several shared arguments:

.. code-block:: console

    usage: dropme [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

    CLI tool for managing Dropbox environment.

    optional arguments:
    --version            Show program's version number and exit.
    -v, --verbose        Increase verbosity of output. Can be repeated.
    -q, --quiet          Suppress output except warnings and errors.
    --log-file LOG_FILE  Specify a file to log output. Disabled by default.
    -h, --help           Show help message and exit.
    --debug              Show tracebacks on errors.

    Commands:
    complete       Prints bash completion command (cliff).
    cp             Copies a file or folder to a different location in the user’s Dropbox.
    df             Shows information about space usage of the current user's account.
    get            Downloads a file at a given local path.
    help           Prints detailed help for another command (cliff).
    ls             Lists directory content.
    mkdir          Creates a folder at a given path.
    mv             Moves a file or folder to a different location in the user’s Dropbox.
    put            Uploads a file to a specified directory.
    rm             Deletes a file or a folder at a given path.
    status         Shows status of a specified file or folder.
    whoami         Shows information about the current user's account.

Commands
========

The list of available :command:`dropme` commands:

.. toctree::
   :maxdepth: 2

   cli/index

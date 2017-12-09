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

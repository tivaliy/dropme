Common Usage
============

To get help on a specific :command:`dropme` command enter:

.. code-block:: console

   $ dropme COMMAND --help

All :command:`dropme` commands support several global arguments.

.. autoprogram-cliff:: dropme.app.DropboxClient
   :application: dropme

The :command:`dropme` client can run in two modes:

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

How to install
==============

**From PyPI (stable)**

1. Create isolated Python environment ``virtualenv venv`` and activate it:

    ``source venv/bin/activate``

2. Install ``dropme`` with ``pip``:

    ``pip install dropme``

3. Configure ``dropme`` client according to `Configuring`_ section

**From GitHub (latest)**

1. Clone ``dropme`` repository:

    ``git clone https://github.com/tivaliy/dropme.git``.

2. Configure ``settings.yaml`` file (in ``dropme/settings.yaml``) or see `configuring`_ section.

.. code-block:: yaml

    token: YOUR_DROPBOX_ACCESS_TOKEN

3. Create isolated Python environment ``virtualenv venv`` and activate it:

    ``source venv/bin/activate``

4. Install ``dropme`` with all necessary dependencies:

    ``pip install -r requirements.txt .``

Configuring
===========

To add ``dropme`` command bash completion:

    ``dropme complete | sudo tee /etc/bash_completion.d/gc.bash_completion > /dev/null``

Restart terminal and activate virtual environment once again.

There are several ways oh now to specify Dropbox access token (according to the search order):

- as an argument of a command:

    ``dropme ls -l --token YOUR_DROPBOX_ACCESS_TOKEN``

- as a environment variable:

    ``export DBX_AUTH_TOKEN=YOUR_DROPBOX_ACCESS_TOKEN``

- in ``~/.config/dropme/settings.yaml`` file
- in ``dropme/settings.yaml`` file

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

Command Bash Completion
-----------------------

To add ``dropme`` command bash completion:

    ``dropme complete | sudo tee /etc/bash_completion.d/gc.bash_completion > /dev/null``

Restart terminal and activate virtual environment once again.

Dropbox Access Token
--------------------

To use the ``dropme`` client, you'll need to register a new app in the
`App Console <https://www.dropbox.com/developers/apps>`_.
Select Dropbox API app and choose your app's permission. You'll need to use the app key created
with this app to access API v2. You have also to `generate an access token <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>`_
for your own account through the `App Console <https://www.dropbox.com/developers/apps>`_.

There are several ways to specify Dropbox access token in ``dropme`` (the order of search matters):

- as an argument of a command:

    ``dropme ls -l --token YOUR_DROPBOX_ACCESS_TOKEN``

- as a environment variable:

    ``export DBX_AUTH_TOKEN=YOUR_DROPBOX_ACCESS_TOKEN``

- in ``~/.config/dropme/settings.yaml`` file
- in ``dropme/settings.yaml`` file

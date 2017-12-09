#
#    Copyright 2017 Vitalii Kulanov
#

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'cliff.sphinxext'
]

# Options for cliff.sphinxext plugin
autoprogram_cliff_application = 'dropme'

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'dropme'

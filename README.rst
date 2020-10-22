.. image:: https://raw.githubusercontent.com/Nekmo/gkeep/master/logo.jpg
    :width: 100%

|

**DEVELOPMENT BRANCH**: The current branch is a development version. Go to the stable release by clicking
on `the master branch <https://github.com/Nekmo/gkeep/tree/master>`_.


Google Keep Cli
###############
Work with Google Keep on your terminal. To install this module
(`more options in the documentation <https://docs.nekmo.org/gkeep/installation.html>`_)::

    $ pip install -U gkeep


To get the available options use the ``--help`` parameter or
`see the documentation <https://docs.nekmo.org/gkeep/usage.html>`_::

    $ gkeep --help

For example **to search for notes**::

    $ gkeep notes search "Shopping list"

Gkeep allows you to use Google Keep **in your scripts**. For example to remember to buy milk::

    $ gkeep items edit --uncheck 150ad84b557.97eb8e3bffcb03e1 "Milk"


Thanks
======
This module is a command-line interface of the module `gkeepapi <https://github.com/kiwiz/gkeepapi/>`_.
Thanks to Kiwiz for maintaining the module.

This module does not use an official Google API to work with Google Keep. As this module does not use an official
API, its operation is not guaranteed for a production environment.

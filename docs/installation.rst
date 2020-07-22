.. highlight:: console

============
Installation
============


Stable release
--------------

To install gkeep, run these commands in your terminal:

.. code-block:: console

    $ sudo pip3 install -U gkeep

This is the preferred method to install gkeep, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Other releases
--------------
You can install other versions from Pypi using::

    $ pip install gkeep==<version>

For versions that are not in Pypi (it is a development version)::

    $ pip install git+https://github.com/Nekmo/gkeep.git@<branch>#egg=gkeep


If you do not have git installed::

    $ pip install https://github.com/Nekmo/gkeep/archive/<branch>.zip


Troubleshooting
---------------
Gkeep is unstable because **it doesn't use an official Google api**. Before opening a new incident update gkeep and its
dependencies to the latest version::

    $ pip install -U gkeep --upgrade-strategy eager

In case of problems with **authentication** check the credentials file in ``~/.config/gkeep/auth.json``. It is
recommended to protect this file for security. Accounts with two-step authentication must use an application password.
For more info: https://support.google.com/mail/answer/185833

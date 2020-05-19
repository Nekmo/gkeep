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

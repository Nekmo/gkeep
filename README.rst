.. image:: https://raw.githubusercontent.com/Nekmo/gkeep/master/logo.png
    :width: 100%

|


Google Keep Cli
###############
Work with Google Keep on your terminal. To install this module::

    pip install gkeep

Create a file with your Google credentials called ``auth.txt`` in the current directory::

    <username> <password>

For example::

    nekmo mypassword1234

You can also use the ``--auth`` parameter to set the path to the file with the credentials::

    gkeep --auth /path/to/auth.txt


Items
=====
Notes can have multiple items with checkboxes. The common parameters for the items are:

* ``<note id>``: note identificator. For example, ``75e4202b0c1.9fc0b868a7b34952``. You can obtain the identifier
  using the web version of Google Keep. Click on the note and look at the url. Example: ``https://keep.google
  .com/#NOTE/75e4202b0c1.9fc0b868a7b34952.``
* ``<item name>``: value of the element. For exemple, ``Milk``.
* ``--check/--uncheck``: Item is checked or not.


Add item on note
----------------
This command allows you to add items to an existing note. By default if the element already exists,
it is not duplicated. If you want duplicate the element, use the ``--duplicate`` parameter. If the element
does not exist, by default it is unchecked.

.. code-block:: bash

    gkeep add-item <note id> "<item name>"[ --check/--uncheck][ --duplicate/no-duplicate]

For example:

.. code-block:: bash

    gkeep add-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies" --check


Edit item on note
-----------------
Modify an existing entry. It allows to change if it is checked and the text.

.. code-block:: bash

    gkeep edit-item <note id> "<item name>"[ --check/--uncheck][ --new-text <new text>]

Examples:

.. code-block:: bash

    gkeep edit-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies" --uncheck

.. code-block:: bash

    gkeep edit-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"
                      --new-text "Chocolate orange cookies"


Delete item on note
-------------------
Delete an existing entry.

.. code-block:: bash

    gkeep delete-item <note id> "<item name>"

Examples:

.. code-block:: bash

    gkeep delete-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"


Is checked item on note
-----------------------
Returns ``True`` if the element is checked. If it is unchecked, it returns ``False``.


.. code-block:: bash

    gkeep delete-item <note id> "<item name>"

Examples:

.. code-block:: bash

    gkeep delete-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"


Thanks
======
This module is a command-line interface of the module ` gkeepapi <https://github.com/kiwiz/gkeepapi/>`_.
Many thanks to Kiwiz for maintaining the module.

This module does not use an official Google API to work with Google Keep. As this module does not use an official
API, its operation is not guaranteed for a production environment.

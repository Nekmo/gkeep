Google Keep Tasks
#################


Items
=====
The common parameters for the items are:

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

    google-keep-tasks add-item <note id> "<item name>"[ --check/--uncheck][ --duplicate/no-duplicate]

For example:

.. code-block:: bash

    google-keep-tasks add-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies" --check


Edit item on note
-----------------
Modify an existing entry. It allows to change if it is checked and the text.

.. code-block:: bash

    google-keep-tasks edit-item <note id> "<item name>"[ --check/--uncheck][ --new-text <new text>]

Examples:

.. code-block:: bash

    google-keep-tasks edit-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies" --uncheck

.. code-block:: bash

    google-keep-tasks edit-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"
                      --new-text "Chocolate orange cookies"


Delete item on note
-------------------
Delete an existing entry.

.. code-block:: bash

    google-keep-tasks delete-item <note id> "<item name>"

Examples:

.. code-block:: bash

    google-keep-tasks delete-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"


Is checked item on note
-----------------------
Returns ``True`` if the element is checked. If it is unchecked, it returns ``False``.


.. code-block:: bash

    google-keep-tasks delete-item <note id> "<item name>"

Examples:

.. code-block:: bash

    google-keep-tasks delete-item 75e4202b0c1.9fc0b868a7b34952 "Chip cookies"

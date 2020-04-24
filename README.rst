.. image:: https://raw.githubusercontent.com/Nekmo/gkeep/master/logo.jpg
    :width: 100%

|

**DEVELOPMENT BRANCH**: The current branch is a development version. Go to the stable release by clicking
on `the master branch <https://github.com/Nekmo/gkeep/tree/master>`_.


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


Notes
=====
It is possible to create, delete, update and view the notes in Google keep. The common parameters are:

* ``title``: Title to add to the note.
* ``text``: Note message body.
* ``color``: color used in the note.
* ``labels``: tags added to notes.


Add note
--------
It is possible to add a new note to Google Keep:

.. code-block:: bash

    gkeep add-note[ --color <color>][--labels <labels>] <title> <text>

For example:

.. code-block:: bash

    gkeep add-note "Today's tasks" "Install gkeep cli and configure it"


Update note
-----------
It is possible to edit an existing note. The following parameters are available to choose the note to edit
(in this command all filters have the prefix ``filter-``):

* ``--filter-id``: id of the note. This is the preferred way to ensure editing the correct note.
* ``--filter-title``: note title. Warning: The titles of the notes are not unique.
* ``--filter-query``: search in titles and body of the notes. This is the least accurate filter.

The syntax is:

.. code-block:: bash

    gkeep update-note <filter>[ --color <color>][--labels <labels>][ --title <title>][ --text <text>]

For example:

.. code-block:: bash

    gkeep update-note --filter-title "Today's tasks" --text "GKeep installed, continue reading the docs"


Search notes
------------
The ``search-notes`` command allows you to search for notes and add filters. In addition to the ``--color``,
``--labels``, ``--title`` and ``--text`` filters the following filters are available:


  * ``--deleted`` / ``--not-deleted``: the note is deleted or not.
  * ``--trashed`` / ``--not-trashed``: the note is trashed or not.
  * ``--pinned`` / ``--not-pinned``: the note is pinned or not.
  * ``--archived`` / ``--not-archived``: the note is archived or not.

The syntax is:

.. code-block:: bash

    gkeep search-notes[ <filters>][ <query>]

For example (the text "GKeep installed" is a search term):

.. code-block:: bash

    gkeep search-notes --not-deleted "GKeep installed"


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
This module is a command-line interface of the module `gkeepapi <https://github.com/kiwiz/gkeepapi/>`_.
Thanks to Kiwiz for maintaining the module.

This module does not use an official Google API to work with Google Keep. As this module does not use an official
API, its operation is not guaranteed for a production environment.

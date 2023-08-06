ewoksweb |release|
==================

*ewoksweb* is a frontend to create, visualize and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows in the web.

ewoksweb has been developed by the `Software group <http://www.esrf.eu/Instrumentation/software>`_ of the `European Synchrotron <https://www.esrf.eu/>`_.


Getting started
---------------

Install requirements

.. code:: bash

    python3 -m pip install ewoksserver[frontend]

Start the server that serves the frontend

.. code:: bash

    ewoks-server

or for an installation with the system python

.. code:: bash

    python3 -m ewoksserver.server

Documentation
-------------

.. toctree::
    :maxdepth: 2

    editor_basics
    create_graph
    node_editing
    link_editing
    execution
    manage_graphs_tasks_icons

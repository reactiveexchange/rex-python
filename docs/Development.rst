.. _development:

=================
Development Guide
=================

Start by creating a virtual environment and installing required packages:

.. code:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Enable development mode when developing new python subpackage or module:

.. code:: bash

    $ python setup.py develop


Deactivate the virtual environment when you are done:

.. code:: bash

    $ deactivate


Upgrade Dependencies
--------------------

Dependencies can be upgraded as follows:

.. code:: bash

    $ pip install pip-tools
    $ pip-compile requirements.in >requirements.txt
    $ pip install -r requirements.txt


The `requirements.txt` file with pip-tools commands helps developer to solve the package dependency
and quick install required packages. Add or change dependency in both `requreiments.txt` and
`setup.cfg` files.

Testing
-------

Run the tests:

.. code:: bash

    $ python setup.py test


Run nosestests:

.. code:: bash

    $ pip install coverage flake8 nose pylint
    $ python setup.py nosetests


Generate coverage report:

.. code:: bash

    $ python setup.py nosetests --cover-html --cover-html-dir=DIR

Run tox:

.. code:: bash

    $ pip install tox
    $ tox

Installation
------------

Install locally:

.. code:: bash

    $ pip install .

Build Python Package
--------------------

Build Python package:

.. code:: bash

    $ python setup.py sdist

Build wheel:

.. code:: bash

    $ python setup.py bdist_wheel


Installing
==========


Supported Python Version 
------------------------

Pincer supports Python 3.8 and higher

Virtual Environment
-------------------

Before installing Pincer, it is recommended to use a virtual environment.
More information can be found in the `venv documentation <https://docs.python.org/3/library/venv.html#module-venv>`_.

.. tab-set::

   .. tab-item:: Linux or MacOS

      .. code-block:: sh

         $ python3 -m venv venv
         $ source venv/bin/activate

   .. tab-item:: Windows

      .. code-block:: sh

         $ python3 -m venv venv
         $ venv\Scripts\activate.bat # Windows


Installing the package
----------------------

As pincer is on PyPi, it can be installed using pip. 
Note: The command to install may vary system to system. Try another if one fails.

.. tab-set::

   .. tab-item:: pip

      .. code-block:: sh

         $ pip install pincer  # should work on most systems

   .. tab-item:: Windows

      .. code-block:: sh

          $ py -m pip install pincer # should work on windows

   .. tab-item:: Linux or MacOS

      .. code-block:: sh

          $ python3 -m pip install pincer # try replacing `3` with the version you have


   .. tab-item:: Install From Github

      .. code-block:: sh

          $ pip install "git+https://github.com/pincer-org/pincer"


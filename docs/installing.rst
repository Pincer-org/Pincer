
Installing
==========


Supported Python Version 
------------------------

Pincer supports Python 3.8 and higher

Virtual Environment
-------------------

Before installing Pincer, it is recommened to use a virtual environment. 
More infomation can be found in the `venv documentation <https://docs.python.org/3/library/venv.html#module-venv>`_.

.. code-block:: sh

	$ python3 -m venv venv
	$ source venv/bin/activate # Unix-like systems
	$ venv\Scripts\activate.bat # Windows

Installing the package
----------------------

As pincer is on PyPi, it can be installed using pip. 
Note: The command to install may vary system to system. Try another if one fails.

.. code-block:: sh

	$ pip install pincer # should work on most systems
	$ python -m pip install pincer
	$ python3 -m pip install pincer # try replacing `3` with the version you have
	$ py -m pip install pincer # should work on windows
	$ path/to/python/binary -m pip install pincer # if Python in not in PATH



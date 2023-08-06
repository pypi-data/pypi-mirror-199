*****
Preprocessor
*****


Preprocessor is a preprocessing library for tweet data written in
Python. When building Machine Learning systems based on tweet and text data, a
preprocessing is required. This is required because of quality of the data as well as dimensionality reduction purposes. 

This library makes it easy to clean the tweets so you don't have to write the same helper functions over and over again ever time.

Features
========

Currently supports cleaning :

-  URLs
-  Hashtags
-  Mentions
-  Emojis
-  Smileys
-  ``.csv`` and ``.xlsx`` file support

Preprocessor ``v0.1.0`` supports
``Python 3.9+ on Windows``. 

Usage
=====

Basic cleaning:
---------------

.. code:: python

    >>> import preprocessor as p
    >>> p.clean('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')
    'Preprocessor is'


Processing files:
-----------------

Preprocessor currently supports processing ``.csv`` and ``.xlsx``
formats. 

Installation
============

Using pip:

.. code:: bash

    $ pip install tweets-preprocess


Using manual installation:

.. code:: bash

    $ python setup.py build
    $ python setup.py install


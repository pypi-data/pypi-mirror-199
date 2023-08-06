Introduction
------------

via-hub-logistic is a library with testing utilities for robotframework that uses a set of python frameworks internally. The project is hosted on GitHub and downloads can be found on PyPI.


Keyword Documentation
---------------------
See `keyword documentation`_ for available keywords and more information
about the library in general.


Installation
------------

The recommended installation method is using pip_::

    pip install --upgrade via-hub-logistc


To install the last legacy via-hub-logistc version, use this command instead::

    pip install via-hub-logistc==1.8.0


Usage
-----

To use via-hub-logistc in Robot Framework tests, the library needs to
first be imported using the ``Library`` setting as any other library.
The library accepts some import time arguments, which are documented
in the `keyword documentation`_ along with all the keywords provided
by the library.


.. code:: robotframework

    *** Settings ***
    Documentation     Simple example using via-hub-logistc.
    Library           via-hub-logistc.Blob

    *** Variables ***
    ${URL}      http://localhost:7272
    ${USER}     user
    ${PWD}      password

    *** Test Cases ***
    Conect azure blob service
        Connect azure blob   ${URL}   ${USER}    ${PWD}

    *** Keywords ***
    Connect azure blob
        [Arguments]    ${url}    ${user}   ${pwd}
        ${conn}=        connect     ${url}    ${user}   ${pwd}



Community
---------

Versions
--------

History
-------
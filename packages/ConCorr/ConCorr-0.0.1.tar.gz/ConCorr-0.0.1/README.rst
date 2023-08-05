ConCorr
===========

The ``ConCorr`` project is a toolbox to analyze functional connectivity
of fMRI data written in Python. 

Installation
------------
Install ``ConCorr`` and its core dependencies via pip::

    pip install ConCorr

Install ``ConCorr`` by cloning GitHub, then move to where the toolbox is
housed in terminal ::

	cd path/to/ConCorr

Then run ``setup.py`` to install dependencies ::

	Python3 setup.py install
	

Dependencies
------------
All of the core dependencies of ``ConCorr`` are listed in the
`requirements.txt <requirements.txt>`_ file and will be installed by ``pip``.

To install ``ConCorr``, along with all the tools you need to develop
and run tests run the following in your virtualenv ::

	pip install -e .[dev] 

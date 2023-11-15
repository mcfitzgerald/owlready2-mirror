Development
===========

Development installation
------------------------

Due due legacy compatibility, the development installation needs to be done

* either manually, by following these steps:

  1. Create a directory (e.g. ``src/``).
     
  2. Add this directory to the $PYTHONPATH shell variable (= traditional way).
     
  3. Put Owlready sources in that directory (in a subdirectory named ``src/owlready2/``).

* or with pip by following these steps:

  1. Create a virtual environment for development and activate it. 

  2. Create an directory with an arbitrary name, e.g. ``mkdir owlready_dev``.

  3. Move or cloning the Owlready2 repository into this directory and change into it.

  4. Run ``pip install -e .[test]`` inside of this Owlready directory.

  5. In case *Python.h* is missing, install python3-dev (e.g. ``sudo apt-get install python3-dev``).

  6. Run the *setup_develop_mode.py* script :
     ``python setup_develop_mode.py`` 
     inside of this Owlready directory (there are explainations in the script, why this is necessary).
     

Finally, To test everything, cd into the **'test'** directory and run ``python regtest.py``.

# ceotr_config

Reusable python application code

# This repo will auto update the PyPI package when there is a push to master
## for trouble shooting look at steps below
- Check `~/resources/dinkum/.pypirc` on the ceotr dev server, ensure it's present and contains the correct token

## To update the dinkum package on PyPI **manually** you will need to do the following:
- ensure the python package "twine" is installed using `pip install twine`
- change the version number in [version/__init__.py](version/__init__.py)
- run the following commands:
    - `python setup.py sdist`
    - `twine upload dist/*`
- enter the CEOTR PyPI username and password, or use token authentication
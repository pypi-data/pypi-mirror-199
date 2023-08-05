# getfast-python

clean out previous dist/\* before uploading

- python3 -m pip install --upgrade build
  python3 -m build
- python3 -m pip install --upgrade twine
  python3 -m twine upload --repository testpypi dist/\*

# for prod upload

- python3 -m twine upload --repository pypi dist/\*

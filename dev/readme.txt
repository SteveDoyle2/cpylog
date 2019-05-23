pip install twine
python setup.py bdist_wheel
python -m twine upload .\dist\cpylog-1.0.4-py3-none-any.whl

pip install twine
python setup.py bdist_wheel --universal
python -m twine upload .\dist\cpylog-1.0.2-py2.py3-none-any.whl

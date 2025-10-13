pip install twine

# python setup.py bdist_wheel  # old
pip wheel --wheel-dir=./wheelhouse cpylog

python -m twine upload .\dist\cpylog-1.0.4-py3-none-any.whl

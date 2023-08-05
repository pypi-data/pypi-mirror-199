# hasaki

~~~shell
python -m pip install --user --upgrade setuptools wheel twine

python setup.py sdist bdist_wheel

# https://test.pypi.org/
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# pip install -i https://test.pypi.org/simple/ hasaki

# https://pypi.org
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# pip install hasaki
~~~
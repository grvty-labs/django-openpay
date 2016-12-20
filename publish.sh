rm -rf dist
rm -rf build
find . -name \*.pyc -delete
find . -maxdepth 1 -name "*.egg-info" -exec rm -rf {} \;
mv django_openpay/migrations tmpMigrations
mkdir django_openpay/migrations
touch django_openpay/migrations/__init__.py
python setup.py sdist bdist_wheel
twine upload dist/* -r pypi
rm -rf django_openpay/migrations
mv tmpMigrations django_openpay/migrations

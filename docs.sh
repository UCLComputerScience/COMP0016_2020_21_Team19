pip install sphinx sphinx_book_theme
cd docs
sphinx-apidoc -o . .. ../*/migrations ../*/tests ../init_db.py
make html
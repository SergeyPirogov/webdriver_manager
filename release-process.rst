Release process
===============

Run tests on target brunch
--------------------------

Steps::

    tox -epep8
    tox -esphinx-docs


Release new version
-------------------

In repo root and master branch run::

    bump2version <release_kind {major|minor|patch}>
    git push --follow-tags

Cut off stable branch
---------------------

Steps::

    git checkout -b vX.X.X-stable
    git push origin vX.X.X-stable


Create GitHub tag
-----------------

Steps::

    Releases ---> Draft New Release
    Name: python-testrelease version X.X.X stable release


Collect changes from previous version
-------------------------------------

Steps::

    git log --oneline --decorate


Build distribution package
--------------------------

Steps::

    python setup.py bdist_wheel


Check install capability for the wheel
--------------------------------------

Steps::

    virtualenv .test_venv
    source .test_venv/bin/activate
    pip install dist/testcontainer-X.X.X-py2.py3-none-any.whl


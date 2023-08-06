@echo off

REM Activate virtual environment
call venv/Scripts/activate

@REM REM Ensure git working directory is clean
@REM git diff-index --quiet HEAD --
@REM if %errorlevel% neq 0 (
@REM     echo Error: git working directory is not clean.
@REM     exit /b 1
@REM )

REM Bump version using bumpversion
@REM bumpversion patch
@REM set /p commit_message="Enter commit message: "
@REM git add .
@REM git commit -m "%commit_message%"
@REM git tag -a v$(python -c "import configparser; config = configparser.ConfigParser(); config.read('.bumpversion.cfg'); print(config.get('bumpversion', 'current_version'))") -m "%commit_message%"


REM Delete contents of dist folder
del /q dist\*

REM Upload package to PyPI
python setup.py sdist
twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGQwMjJkOTRmLTIyYzUtNGQ2YS1hNDk2LTI3NGZmZWNlNmM3ZAACG1sxLFsiYWktaGVhZGVyLWdlbmVyYXRvciJdXQACLFsyLFsiZGI3Y2EwYzktNzZlNi00YjI2LWJkYmEtMTgxZTExMjUzYmM2Il1dAAAGIO5vBwop4nBhpty9ZG6mX3jcZurOWm8PUs8TMqKzyh2y

REM Deactivate virtual environment
deactivate

echo Done.

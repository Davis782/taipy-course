@echo off
echo Running batch file to resolve Taipy and NumPy/numexpr issues...

echo 1. Downgrading NumPy to a version less than 2.0...
pip install "numpy<2.0"

echo 2. Attempting to upgrade numexpr...
pip install --upgrade numexpr

echo 3. Attempting to reinstall numexpr...
pip uninstall -y numexpr
pip install --no-cache-dir numexpr

echo 4. Check if numexpr is installed and the version of numpy.
pip show numexpr
pip show numpy

echo 5. If issues persist, consider creating a new virtual environment.
echo. If you are using venv, run the commands below.

echo. Creating a new virtual environment.
echo. python -m venv taipy_env
echo. taipy_env\Scripts\activate
echo. pip install taipy pandas numexpr numpy
echo. Run the python script again.

echo. Done. Please run your Taipy application again.
pause
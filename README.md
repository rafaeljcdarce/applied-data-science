# Applied Data Science

## Install

Assumes you are on Linux/Mac and have Python 3.6+

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage

See `example.ipynb`

## Extending functionality

To create a new sub-package:
- Create a new folder with the same layout as `applied_data_science/sentiment_pipeline` (e.g. `applied_data_science/YOUR_PACKAGE` with files `YOUR_PACKAGE.py` and `__init__.py`)
- For each bit of code you wish to make available, add `from .YOUR_PACKAGE import YOUR_CODE` to `applied_data_science/YOUR_PACKAGE/__init__.py` 

You should now be able to import your code anywhere using `from applied_data_science.YOUR_PACKAGE import YOUR_CODE`. If this doesn't work, try running `pip install -e .` again. If you are working in a notebook, make sure that it is using the virtual environment and restart your notebook kernel.
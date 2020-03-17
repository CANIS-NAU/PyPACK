# PyPACK

| OS    | Status |
|-------|--------|
| OSX   | [![Build Status](https://travis-ci.com/CANIS-NAU/PyPACK.svg?branch=master)](https://travis-ci.com/CANIS-NAU/PyPACK) |
|Linux  | [![Build Status](https://travis-ci.com/CANIS-NAU/PyPACK.svg?branch=master)](https://travis-ci.com/CANIS-NAU/PyPACK)|

PyPACK (Python Analysis of Community Knowledge) is a Python library that supports social media analysis.

## Installation


### 1. Install Anaconda (Skip to step 2 if you have Anaconda/Miniconda)

Install <a href="https://www.anaconda.com/download/">Anaconda</a>. Be sure to choose the Python 3.x version!


### 2. Open a terminal (on Windows, use the Anaconda prompt that gets installed with Anaconda) and type:

```bash
conda config --add channels conda-forge
conda create -n pypack
conda activate pypack
conda install -c canis-lab pypack
pip install shapely docker pyqtgraph mordecai
```

### 3. Done! How to use pypack GUI
From the terminal type:

```bash
conda activate pypack

```

### 4. Update an existing installation

If you already have an earlier version of the PyHAT Point Spectra GUI installed as described above and you want to wipe it and update to the latest version, just do:

```bash
conda env remove -n pypack
conda clean -a
```
And then follow the instructions above to install a fresh version.

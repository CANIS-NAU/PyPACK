travis-sphinx -v deploy -b master
source deactivate
conda install conda-build anaconda-client
conda config --set anaconda_upload yes;
conda build --token $CONDA_UPLOAD_TOKEN --python $1 -c CANIS-LAB recipe;

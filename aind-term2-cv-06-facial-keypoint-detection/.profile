source activate cv
KERAS_BACKEND=tensorflow python -c "from keras import backend"
echo "jupyter notebook CV_project.ipynb --ip=0.0.0.0 --no-browser >> jupyter.log 2>&1 &"

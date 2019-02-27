source activate dog-project
KERAS_BACKEND=tensorflow python -c "from keras import backend"
echo "jupyter notebook dog_app.ipynb >> jupyter.log 2>&1 &"

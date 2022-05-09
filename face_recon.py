# load all images in a directory into memory
from numpy import asarray
import tensorflow as tf
from tensorflow.keras.models import load_model
from numpy import savez_compressed
from keras.preprocessing.image import img_to_array, load_img
import matplotlib.pyplot as plt
from numpy import load

def load_images(path, size=(256,256)):
    d_list = list()
    # load the image
    pixels = load_img(path, target_size=size)
    # convert to numpy array
    pixels = img_to_array(pixels)
    d_list.append(pixels)
    return asarray(d_list)

# load and prepare training images
def load_real_samples(filename):
	# load compressed arrays
	data = load(filename)
	# unpack arrays
	X1 = data['arr_0']
	# scale from [0,255] to [-1,1]
	X1 = (X1 - 127.5) / 127.5
	return [X1]

def load_face(filename):
    # load dataset
    src_images = load_images("static/uploads/"+filename)
    savez_compressed("cmpz.npz", src_images)

    sz = load_real_samples("cmpz.npz")
    g_model = load_model('my_model.h5')
    X = g_model.predict(sz)
    X = (X+1)/2.0
    plt.imsave("static/uploads/"+filename, X[0])
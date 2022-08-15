
import numpy as np
import pandas as pd

# import io
import os
import tensorflow as tf

from PIL import Image
from glob import glob
import itertools

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
import seaborn as sns


import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras.layers import Conv2D, Flatten, BatchNormalization, Dropout, Dense, MaxPool2D
# from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix

from IPython.display import display
# To see the value of multiple statements at once.
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

basedir = os.path.abspath(os.path.dirname(__file__))
current_file = "Skin_Cancer.h5"


class Model:

    def __init__(self, file) -> None:
        self.path = os.path.join(basedir, file or current_file)

    def load_pre_trained_model(self):
        # check if the path exists before trying to load the model
        if os.path.exists(self.path):
            model = load_model(self.path)
            return model  # return the model
        else:
            print("Model not found")

        '''Prediction for batches of images '''

    def predict_single_image(self, model, file_name, lab_map=None, img_path=None, url=None, img_height=28, img_width=28):
        score = 0

        if not lab_map:
            lab_map = {
                0: 'nv',
                1: 'mel',
                2: 'bkl',
                3: 'bcc',
                4: 'akiec',
                5: 'vasc',
                6: 'df'}
        else:
            # check if the lab_map is a dict
            assert isinstance(
                lab_map, dict), f"expected a dict of key:int and value:str"

        if not img_path and url:
            path = tf.keras.utils.get_file(
                file_name, origin=url)  # download the image
            img = tf.keras.utils.load_img(path, target_size=(
                img_height, img_width))  # load the image
        elif not url and img_path:
            img = tf.keras.utils.load_img(img_path, target_size=(
                img_height, img_width))  # load the image

            # show the image
            # plt.imshow(img)
            # plt.show()

            # convert the image to a numpy array
            # img = tf.keras.preprocessing.image.img_to_array(img)

        else:
            print("Error enter either path or url")
            return
        img_array = tf.keras.utils.img_to_array(
            img)  # convert the image to a numpy array
        # Create a batch images to predict
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array)  # make the prediction
        # use softmax to make the classfication
        score = tf.nn.softmax(predictions[0])

        print("=======================")
        print("score", score.numpy())
        print("========================")

        # predict_imgs_dict = {}
        # predict_imgs_dict['image_pixel'] = np.asarray(Image.open(imgPath).resize((28,28)))
        # print(predict_imgs_dict['image_pixel'].shape)

        # one_picture_predict_data.image_pixel.shape
        # new_one = predict_imgs_dict['image_pixel'].reshape((1,28,28,3))
        # print(new_one.shape)

        # prediction = model.predict(new_one)
        print(
            "This is most likely to be {} with a {:.2f} percent confidence."
            .format(lab_map[np.argmax(score)], 100 * np.max(score))
        )
        label = lab_map[np.argmax(score)]
        conf = 100 * np.max(score)
        return label, conf, score.numpy()

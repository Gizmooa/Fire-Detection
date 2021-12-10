import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


fire_path = "C:/Users/barth/Documents/studie/datalogi/9 semester/Drone/code exercise/network/test/Fire/resized_frame0 copy.jpg"



img = tf.keras.utils.load_img(
    fire_path, target_size=(254, 254)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

model = tf.keras.models.load_model("C:/Users/barth/Documents/studie/datalogi/9 semester/Drone/code exercise/network/saved_model/mymodel")
model.summary()

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to with a ", 100 * np.max(score), " percent confidence.")


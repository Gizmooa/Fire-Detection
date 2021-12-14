import numpy as np
import os
import PIL
import pathlib
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

class FireClassification:
  trainedModel = False
  trainingSetLocation = None
  testSetLocation = None
  modelLocation = None
  batch_size = None
  img_height = None
  img_width = None
  num_classes = None

  def __init__(self, modelLocation = None, testSetLocation = None, trainingSetLocation = None, batch_size = 32,
               img_height = 254, img_width = 254, num_classes = 2):
    self.modelLocation = modelLocation
    self.testSetLocation = testSetLocation
    self.trainingSetLocation = trainingSetLocation
    self.batch_size = batch_size
    self.img_height = img_height
    self.img_width = img_width
    self.num_classes = num_classes

    if (self.modelLocation != None): trainedModel = True

  def createDataset(self):
    train_ds = tf.keras.utils.image_dataset_from_directory(
      self.trainingSetLocation,
      validation_split=0.2,
      subset="training",
      seed=123,
      image_size=(self.img_height, self.img_width),
      batch_size=self.batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
      self.trainingSetLocation,
      validation_split=0.2,
      subset="validation",
      seed=123,
      image_size=(self.img_height, self.img_width),
      batch_size=self.batch_size)
    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    self.standardizeData(train_ds, val_ds)

  def standardizeData(self, train_ds, val_ds):
    normalization_layer = layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    # De 2 variabler bliver ikke brugt?
    image_batch, labels_batch = next(iter(normalized_ds))
    self.createModel(train_ds, val_ds)

  def createModel(self, train_ds, val_ds):
    num_classes = 2

    model = Sequential([
      layers.Rescaling(1./255, input_shape=(self.img_height, self.img_width, 3)),
      layers.Conv2D(16, 3, padding='same', activation='relu'),
      layers.MaxPooling2D(),
      layers.Conv2D(32, 3, padding='same', activation='relu'),
      layers.MaxPooling2D(),
      layers.Conv2D(64, 3, padding='same', activation='relu'),
      layers.MaxPooling2D(),
      layers.Flatten(),
      layers.Dense(128, activation='relu'),
      layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    epochs=1
    history = model.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs
    )
    model.save("saved_model/mymodel")
    self.trainedModel = True
    self.modelLocation = "saved_model/mymodel"

if __name__ == "__main__":
  location = ""
  classifier = FireClassification(testSetLocation=location)
#!mkdir -p saved_model
#model.save("saved_model/mymodel")


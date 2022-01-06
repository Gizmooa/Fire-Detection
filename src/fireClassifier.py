import random
import shutil
from imp import new_module
import numpy as np
import os
import PIL
import pathlib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import os
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Remove warnings from tensorflow.
tf.get_logger().setLevel('ERROR')


class FireClassification:
    """
  [summary]

  Attributes
  ----------
  modelLocation : (str, optional 
      The location where the model is saved as an absolute path. If it is 
      unset, it will be saved in the current folder as saved_model/mymodel.
          
  testSetLocation : str, optional 
      The absolute path to the folder, that holds the testset data. If it is 
      not set, the location is in the current folder, in a folder called 
      test_data.
      
  trainingSetLocation : str, optional 
      [description]. The location of the training data set. If it is not set, 
      the default location is in the current folder in a folder called 
      training_data.
      
  batch_size : int, optional 
      The size of the batches. Defaults to 32.
      
  img_height : int, optional 
      Number of horizontal pixel. Defaults to 254.
      
  img_width : int, optional 
      Number of vertical pixel. Defaults to 254.
      
  num_classes : int, optional 
      The number of classes the nerual network should recognize. Defaults to 2 
      for fire and no fire.
  
  seed : int, optional 
      A seed for the random generator used, to shuffle the given data and trans-
      formation. Default value is 42. 
  
  Methods
  -------
  createDataset
  
  standardizeData
  
  createModel

  predict_image
  
  test_model
    """

    trainingSetLocation = None
    testSetLocation = None
    modelLocation = None
    batch_size = None
    img_height = None
    img_width = None
    num_classes = None
    train_ds = None
    val_ds = None

    def __init__(self, modelLocation=None, testSetLocation=None,
                 trainingSetLocation=None, batch_size=32,
                 img_height=254, img_width=254, num_classes=2, seed=42):

        self.modelLocation = modelLocation
        self.testSetLocation = testSetLocation
        self.trainingSetLocation = trainingSetLocation
        self.batch_size = batch_size
        self.img_height = img_height
        self.img_width = img_width
        self.num_classes = num_classes
        self.seed = seed

    def createDataset(self):
        """Creates the data from the given trainingset location, creates a valida-
    tion split at 0.2. The seed given to the FireClassification object is used
    here for shuffeling and transformations. Sets the attributes val_ds and 
    train_ds to the correct vaules. 
    """
        self.train_ds = tf.keras.utils.image_dataset_from_directory(
            self.trainingSetLocation,
            validation_split=0.2,
            subset="training",
            seed=self.seed,
            shuffle=True,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

        self.val_ds = tf.keras.utils.image_dataset_from_directory(
            self.trainingSetLocation,
            validation_split=0.2,
            subset="validation",
            seed=self.seed,
            shuffle=True,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

    def predict_image(self, image, show_image=False):
        """Takes an image and classifies that picture with the model.
     
    Parameters
    ----------
    image : str
        Absolute path to the picture. 
    
    show_image : bool
        If set to true, the image, will be shown in a window. 
    
    Returns
    -------
        None
    """

        x = np.expand_dims(image, axis=0)

        model = tf.keras.models.load_model(self.modelLocation)

        val = model.predict(x)
        return val

    def test_model(self, model, testSetLocation=None, see_architecture=False, see_confusion_matrix=True):
        """Takes an existing fire classifier, and test it on the given test data.
  
    Parameters
    ----------
    model : str
        Absolute path to the model location.
     
    testSetLocation : str, optional
        Absolute path to the test datas location. It has to be set when the 
        FireClassification object is created, or when the function is called for
        the function to operate.
         
    see_architecture : bool, optional
        Prints the architecture of the model, if it is set to true. It is false 
        by default.

    see_confusion_matrix : bool, optional
        Prints the confusion matrix for the models predictions on the test data set.
        It is true by default.
    
    Returns
    -------
    predictions : numpy array
        A numpy array where each entry is how sure the classifier is, that the
        given picture fire or nonfire. If the entry is (0-0.5], the class-
        ifier predicts that there is a fire. If its (0,5-1], it predicts there
        is no fire. 
    """

        if (testSetLocation == None):
            testSetLocation = self.testSetLocation

        model = tf.keras.models.load_model(model)

        testing_data = tf.keras.utils.image_dataset_from_directory(testSetLocation,
                                                                   image_size=(self.img_height, self.img_width),
                                                                   labels='inferred')

        if (see_architecture):
            model.summary()


        predictions = model.evaluate(testing_data)

        if (see_confusion_matrix == True):
            labels_list = np.array([])
            prediction_list = np.array([])

            for images, labels in testing_data:
                labels_list = np.concatenate((labels_list, labels))
                prediction_list = np.concatenate((prediction_list, model.predict_on_batch(images).flatten()))

            print(confusion_matrix(labels_list, prediction_list > 0.2))


        return predictions



    def create_and_train_model(self, epochs=10):
        """Creates the model from the training data set. It can then validate the
    the models performance with the given validation data set.

    Parameters
    ----------
    epochs : (int,optional) 
        The number of epochs used to create the model. Is set to 1 by default.  
    """
        model = Sequential([
            layers.Rescaling(1. / 255, input_shape=(self.img_height, self.img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])

        callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        model.fit(
            self.train_ds,
            validation_data=self.val_ds,
            epochs=epochs,
            callbacks=[callback]
        )

        abs_path = str(pathlib.Path(__file__).parent.resolve())

        model_location = abs_path.replace("/src", "/saved_model/mymodelny")

        model.save(model_location)

        self.modelLocation = model_location
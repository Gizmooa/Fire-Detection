import numpy as np
import os
import PIL
import pathlib
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

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
  
  Methods
  -------
  createDataset
  
  standardizeData
  
  createModel
  
  test_existing_classifier
    """
    
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

#TODO: Make seed a variable that the user can set. 
  def createDataset(self):
    """Creates the data from the given trainingset location, creates a valida-
    tion split at 0.2. The given validation 
    """
    train_ds = tf.keras.utils.image_dataset_from_directory(
      self.trainingSetLocation,
      validation_split=0.2,
      subset="training",
      seed=123,
      image_size=(self.img_height, self.img_width),
      batch_size=self.batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
      self.trainingSetLocation, #Should this not be testsetlocation. 
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
    """[summary]

    Parameters
    ----------
    train_ds : tf.data.Dataset 
        [description]
        
    val_ds : tf.data.Dataset 
        [description]
    """
    normalization_layer = layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    # De 2 variabler bliver ikke brugt?
    image_batch, labels_batch = next(iter(normalized_ds))
    self.createModel(train_ds, val_ds)
  
  
  def test_existing_classifier(self,model,testSetLocation=None,see_architecture=False):
    """
    Takes an existing fire classifier, and test it on the 
    Parameters
    ----------
    testSetLocation : str, optional
        Absolute path to the test datas location. It has to be set when the 
        FireClassification object is created, or when the function is called for
        the function to operate
         
    see_architecture : bool, optional
        Prints the architecture of the model, if it is set to true. It is false by
        default. 
    """
    
    #if (testSetLocation == None):
    #  testSetLocation = self.testSetLocation
      

    new_model = tf.keras.models.load_model(model)

    new_model.summary()
    #loss, acc = new_model.evaluate(self.testSetLocation, test_labels, verbose=2)
    #print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))
    #print(new_model.predict(test_images).shape)
    
    
    #model.predict(test_data)


  def createModel(self, train_ds, val_ds,epochs=1):
    """Creates the model from the training data set. It can then validate the
    the models performance with the given validation data set.

    Parameters
    ----------
    train_ds : (tf.data.Dataset object): 
        [description]
        
    val_ds : (tf.data.Dataset object): 
        [description]
        
    epochs : (int,optional) 
        The number of epochs used to create the model. Is set to 1 by default.  
    """
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
      layers.Dense(self.num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    
    history = model.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs
    )
    
    model.save("saved_model/mymodel")
    self.trainedModel = True
    self.modelLocation = "saved_model/mymodel"

  
  

if __name__ == "__main__":
  training_location = "C:/Users/barth/Documents/studie/Fire-Detection/classification/test_data"
  test_location     = "C:/Users/barth/Documents/studie/Fire-Detection/classification/test_data"
  model = "C:/Users/barth/Documents/studie/Fire-Detection/saved_model/mymodel"
  classifier = FireClassification(trainingSetLocation=training_location)
  
  #classifier.createDataset()
  classifier.test_existing_classifier(testSetLocation=test_location,model=model,
                                      see_architecture=True)
  
#!mkdir -p saved_model
#model.save("saved_model/mymodel")


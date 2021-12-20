from imp import new_module
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
  
  seed : int, optional 
      A seed for the random generator used, to shuffle the given data and trans-
      formation. Default value is 42. 
  
  Methods
  -------
  createDataset
  
  standardizeData
  
  createModel
  
  predict_folder
    """
    
  trainingSetLocation = None
  testSetLocation = None
  modelLocation = None
  batch_size = None
  img_height = None
  img_width = None
  num_classes = None

  def __init__(self, modelLocation = None, testSetLocation = None, 
               trainingSetLocation = None, batch_size = 32,
               img_height = 254, img_width = 254, num_classes = 2, seed=42):

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
    here for shuffeling and transformations. 
    """
    train_ds = tf.keras.utils.image_dataset_from_directory(
      self.trainingSetLocation,
      validation_split=0.2,
      subset="training",
      seed=self.seed,
      image_size=(self.img_height, self.img_width),
      batch_size=self.batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
      self.trainingSetLocation, #Should this not be testsetlocation. 
      validation_split=0.2,
      subset="validation",
      seed=self.seed,
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
  
  
  #TODO: Fix so that it works. 
  def predict_image(self,model,image,show_image=False):
    """Takes an image and a model, and classifies that picture with the model.
     
    Parameters
    ----------
    model : str
        Absolute path to the trained model. 
        
    image : str
        Absolute path to the picture. 
    
    show_image : bool
        If set to true, the image, will be shown in a window. 
    
    Returns
    -------
        None
    """
    
    img = tf.keras.utils.load_img(image)
 
    y = img.img_to_array(img)
    
    x = np.expand_dims(y,axis=0)
    
    model = tf.keras.models.load_model(model)

    val = model.predict(x)
    print(val)
    
    
  
  def predict_folder(self,model,testSetLocation=None,see_architecture=False):
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
                              image_size=(self.img_height,self.img_width),
                              labels='inferred')

    if(see_architecture):
      model.summary()
    
    predictions = new_model.predict(testing_data)
    return predictions

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
      layers.Dense(128, activation='sigmoid'),
      layers.Dense(1,activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    
    history = model.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs
    )
    
    model.save("saved_model/mymodel")
    self.modelLocation = "saved_model/mymodel"
  

if __name__ == "__main__":
  training_location = "C:/Users/barth/Documents/Studie/Fire-Detection/classification"
  test_location     = "C:/Users/barth/Documents/Studie/Fire-Detection/classification/test_data"
  test_image        = "C:/Users/barth/Documents/studie/Fire-Detection/classification/test_data/Fire/resized_test_fire_frame1.jpg"
  model = "C:/Users/barth/Documents/Studie/Fire-Detection/saved_model/mymodel"
  classifier = FireClassification(trainingSetLocation=training_location)
  
#  classifier.createDataset()
#  test1 = classifier.predict_folder(model=model,testSetLocation=test_location)
#  test2 = classifier.predict_image(model,test_image)
  
#!mkdir -p saved_model
#model.save("saved_model/mymodel")

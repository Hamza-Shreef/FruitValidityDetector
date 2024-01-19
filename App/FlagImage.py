from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from keras.applications.vgg16 import preprocess_input
import sys
import os



def SeeImage(img_path,classification_model):
    labels={
    0:'Fresh apple',
    1:'Fresh banana',
    2:'Fresh orange',
    3:'Rotten apple',
    4:'Rotten banana',
    5:'Rotten orange'
    }
    predicted_class,confidence = predict_class(classification_model, img_path)
    predicted_class_label = labels[predicted_class]
    print(f'The predicted class for the image is: {predicted_class_label}')
    print("Model has seen the image")

    ouptut=OuputModel()
    ouptut.Confidence=confidence
    ouptut.classification_label=predicted_class_label
    if(predicted_class==3 or predicted_class==4 or predicted_class==5):
        ouptut.Flag=False

    return ouptut
    
    





def predict_class(model, img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    confidence=int(predictions.max()*100)
    print(str(confidence)+"% confidence")
    predicted_class = np.argmax(predictions)

    return predicted_class,confidence

class OuputModel():
    Flag=True
    Confidence=100
    classification_label=""


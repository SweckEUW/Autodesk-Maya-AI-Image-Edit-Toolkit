import tensorflow as tf
import numpy as np
from tensorflow import keras
from PIL import Image

model = keras.models.load_model('C:/Users/Simon/Desktop/Projektarbeit/project/mnist_detection/keras_mnist.h5')

img = Image.open("C:/Users/Simon/Desktop/Projektarbeit/project/mnist_detection/1.png")
img = np.array(img)
img = tf.image.rgb_to_grayscale(img)
img = np.reshape(img, (1,28,28))
prediction = model.predict(img)

print(prediction.argmax())
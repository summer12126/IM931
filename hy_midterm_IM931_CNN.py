# -*- coding: utf-8 -*-
"""u2209238_Hayoung_models1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X3_e28S2nbMIkRD4Kda2PEtX02qTzgtb

### SLP

SLP
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from tensorflow.keras import models, layers, optimizers, losses, metrics

import json
from time import time

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True' # legacy hack for those running locally with older versions of Anaconda

# mount your Google Drive (https://drive.google.com)
from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# # change to the main "/My Drive" directory at https://drive.google.com
# %cd /content/drive/My Drive

# data loading and preprocessing
with open("/content/drive/MyDrive/Colab Notebooks/mnist2.json") as f:
    mnist2 = json.load(f)

train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)

# df where our results will be stored
results = pd.DataFrame(
    columns = [
        "test_acc",
        "val_acc",
        "train_acc",
        "test_loss",
        "val_loss",
        "train_loss",
        'dense_units1', 
        'dropout1', 
        'dense_units2', 
        'dropout2', 
        'epochs', 
        'batch_size', 
        'learning_rate',
    ]
)

# Print data dimensions
print("train_images.shape:", train_images.shape)
print("train_labels.shape:", train_labels.shape)
print("test_images.shape:", test_images.shape)
print("test_labels.shape:", test_labels.shape)

train_images_28x28 = train_images.reshape(50000, 28,28)
test_images_28x28 = test_images.reshape(10000, 28,28)
print(train_images_28x28.shape)
print(test_images_28x28.shape)

# Display number of labels
len(train_labels)

# Show output class for the selected training samples
train_labels[0:20]

# Let’s display the 10th digit in this rank-3 tensor
# experiment by changing the digit number

digit = train_images[10]
#print(digit.shape)

# plot the digit
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()

# NOTE: you can change the selection by slicing the dataset as desired
num = 15
images = train_images[:num]     #select 15 samples with their labels
labels = train_labels[:num]

num_row = 3
num_col = 5

# plot images
fig, axes = plt.subplots(num_row, num_col, figsize=(1.5*num_col,2*num_row))
for i in range(num):
    ax = axes[i//num_col, i%num_col]
    ax.imshow(train_images[i], cmap='gray')
    ax.set_title('Label: {}'.format(labels[i]))
plt.tight_layout()
plt.show()

"""Build the network architecture for a single-layer perceptron (SLP) model"""

# The network architecture for a SLP model
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    #layers.Dense(784, activation="relu"),    
    layers.Dense(10, activation="softmax")
    ])

type(model)

# Compile the model
model.compile(optimizer="rmsprop",              
              loss="sparse_categorical_crossentropy",              
              metrics=["accuracy"])

"""Preparing the image data"""

# Preprocess  the  data
train_images = train_images.reshape((50000, 28 * 28))
train_images = train_images.astype("float32") / 255
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype("float32") / 255

print(train_images.dtype)
print(test_images.dtype)
print(train_images.shape)
print(test_images.shape)





"""Training the model 1

"""

history = model.fit(train_images, train_labels, epochs=5, batch_size=128)

model.summary()

"""Use model to make predictions 1 """

# Make predictions
test_digits = test_images[0:10]
predictions = model.predict(test_digits)
predictions[0]

np.set_printoptions(suppress=True)
predictions[0]

predictions[0].argmax()

# Check that the test label agrees:
test_labels[0]

"""Evaluating the model on new data"""

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")



# Plot training loss and training accuracy

import matplotlib.pyplot as plt
accuracy = history.history['accuracy']
loss = history.history['loss']
epochs = range(len(accuracy))
plt.plot(epochs, loss, '-go', label='Training loss')
plt.title('Training loss')
plt.legend()
plt.show()
plt.plot(epochs, accuracy, '-bo', label='Training acc')
plt.title('Training accuracy')
plt.legend()
plt.figure()

# let's try to take a deeper look at what's going on here
model.summary()
# We can see the shapes of the tensors that hold the weights.
# Run the next two lines and write a couple of sentences explaining the output.
ws = model.get_weights()
for i in range(len(ws)):
    print(ws[i].shape)
# write your sentence here

# Now let's look at some of the actual weights. Note that on their own they're pretty meaningless...
print (ws[0][1:8,1:8])

# Now let's take a look at some images and see how they're being classified.
# Choose an image from the 10,000 test images.
input_image_index = 0
model.evaluate(test_images, test_labels)
predicted_network_output = model.predict(test_images[input_image_index:input_image_index+1, :])
#predict_x=model.predict(X_test)
#classes_x=np.argmax(predict_x,axis=1)
# take a look at what gets output from the network
predicted_network_output

"""training the model 2 epochs = 10"""

history = model.fit(train_images, train_labels, epochs=10, batch_size=128)

"""Use model to make predictions"""

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=10, batch_size=256)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=10, batch_size=256)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=10, batch_size=512)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=20, batch_size=50)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=5, batch_size=256)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")



history = model.fit(train_images, train_labels, epochs=10, batch_size=256)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=10, batch_size=512)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")

history = model.fit(train_images, train_labels, epochs=5, batch_size=256)

# Evaluate model accuracy on the test set
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("test_acc: {test_acc}")



"""### MLP"""

train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)

# This code provides functions that help train a 3-layer multilayer perceptron, 
# with a set of specified default parameters.
# 
# default_params() returns a dictionary of the values for the number of units 
# (i.e. columns in the layer's weight matrix).
#
# get_model(dense_units1, dropout1, dense_units2, dropout2) returns a 3-layer model with 
# the specified # fof units and dropout rates.
#
# To work with a different architecture (e.g. CNNs), rewrite the code in get_model() to return
# a different model.

def default_params():
    params = {
        "dense_units1": 128,
        "dropout1": 0.4,
        "dense_units2": 128,
        "dropout2": 0.3,
        
        "epochs": 10,
        "batch_size": 128,
        "learning_rate": 0.001,
        "validation_split": 0.2,
    }    
    return params    

def get_model(
    dense_units1 = 128,
    dropout1 = 0.4,
    dense_units2 = 128,
    dropout2 = 0.3,
):
    model = models.Sequential()
    model.add(layers.Dense(units = dense_units1, activation='relu', input_shape=(28 * 28,)))
    model.add(layers.Dropout(rate = dropout1))
    model.add(layers.Dense(units = dense_units2, activation='relu'))
    model.add(layers.Dropout(rate = dropout2))
    model.add(layers.Dense(units = 10, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )
    
    return model

# Support code to train, test, and plot the loss and accuracy of a given model.

def train_model(
    model,
    train_images,
    train_labels,
    epochs = 10,
    batch_size = 128,
    learning_rate = 0.001,
    validation_split = 0.2,
):
    start_time = time()

    history = model.fit(
        train_images, 
        train_labels, 
        epochs = epochs, 
        batch_size = batch_size,
        validation_split = validation_split,
    )

    end_time = time()
    print("Running time for training: {:.2f} seconds".format(end_time - start_time))
    
    return model, history

def test_model(
    model,
    test_images,
    test_labels,
):
    
    test_loss, test_acc = model.evaluate(
        test_images_new, 
        test_labels_new,
    )
    
    return test_loss, test_acc

def plot_history(histories, run_index):
    history = histories[run_index]
    
    acc = history.history['accuracy']
    loss = history.history['loss']
    val_acc = history.history['val_accuracy']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.plot(epochs, loss, '-bo', label='Training loss')
    plt.plot(epochs, val_loss, '-ro', label = "Validation loss")
    plt.title('Training loss')
    plt.legend()
    plt.show()

    plt.plot(epochs, acc, '-bo', label='Training acc')
    plt.plot(epochs, val_acc, '-ro', label = "validation acc")
    plt.title('Training accuracy')
    plt.legend()
    plt.figure()

    # The below function is a tuning loop for one parameter; 
# we have chosen the number of epochs as an example.
# It will loop over a list of number of epochs to train for; 
# you can modify this function or create your own to iterate 
# over another parameter (e.g. batch size).

def tuning_epochs(list_of_epochs):
    rows = []
    histories = []
    for num_epochs in list_of_epochs:
        print("====== {} epochs ======".format(num_epochs))
        model = get_model()
        current_params = default_params()

        model, history = train_model(
            model = model, 
            train_images = train_images_new, 
            train_labels = train_labels_new,
            epochs = num_epochs,
        )
            
        test_loss, test_acc = test_model(model, test_images_new, test_labels_new)

        # update the parameter we're tuning 
        current_params["epochs"] = num_epochs
        # input results to save to df
        current_params["test_acc"] = test_acc
        current_params["val_acc"] = history.history["val_accuracy"][-1]
        current_params["train_acc"] = history.history["accuracy"][-1]
        current_params["test_loss"] = test_loss
        current_params["val_loss"] = history.history["val_loss"][-1]
        current_params["train_loss"] = history.history["loss"][-1]
        
        rows.append(current_params)
        histories.append(history)
        
        print("Test loss: {:.4f}".format(test_loss))
        print("Test accuracy: {:.4f}".format(test_acc))
        print("\n")
        
    return rows, histories

# Sample usage for the above tuning function.

# results_epochs, histories_epochs = tuning_epochs([1, 2, 4, 8])

# The below is an example tuning loop for 2 parameters at the same time -- in this case learning rate and 
# the number of units in the first layer.

def tuning_LR_and_DU1(list_LR, list_DU1):
    rows = []
    histories = []
    for lr in list_LR:
        for du1 in list_DU1:
            print("====== LR {}, DU1 {} ======".format(lr, du1))
            model = get_model(dense_units1 = du1)
            current_params = default_params()

            model, history = train_model(
                model = model, 
                train_images = train_images_new, 
                train_labels = train_labels_new,
                learning_rate = lr,
            )

            test_loss, test_acc = test_model(model, test_images_new, test_labels_new)

            # update the parameter we're tuning 
            current_params["learning_rate"] = lr
            current_params["dense_units1"] = du1
            # input results to save to df
            current_params["test_acc"] = test_acc
            current_params["val_acc"] = history.history["val_accuracy"][-1]
            current_params["train_acc"] = history.history["accuracy"][-1]
            current_params["test_loss"] = test_loss
            current_params["val_loss"] = history.history["val_loss"][-1]
            current_params["train_loss"] = history.history["loss"][-1]

            rows.append(current_params)
            histories.append(history)

            print("Test loss: {:.4f}".format(test_loss))
            print("Test accuracy: {:.4f}".format(test_acc))
            print("\n")

    return rows, histories

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
tf.config.experimental_run_functions_eagerly(True)
from tensorflow.keras import models, layers, optimizers, losses, metrics
from tensorflow.keras.utils import to_categorical

import pandas as pd
import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

import json
from time import time

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True' # legacy hack for those running locally with older versions of Anaconda

print(f"tensorflow version: {tf.__version__}\n",
      f"keras version: {tf.keras.__version__}\n",
      f"matplotlib version: {matplotlib.__version__}\n",
      f"numpy version: {np.__version__}")



"""MLP1_net3"""

from keras.utils import to_categorical

train_labels_MLP = to_categorical(train_labels)

# Build the second model
network3 = get_model(
    dense_units1 = 128,
    dropout1 = 0.4,
    dense_units2 = 128,
    dropout2 = 0.3,
)
network3.summary()

# train and test the model
network3, history3 = train_model(network3, train_images, train_labels_MLP, epochs=10, batch_size=128, learning_rate=0.001, validation_split = 0.2)
test_model(network3, test_images,test_labels)

"""MLP2_net4"""

# Build the second model
network4 = get_model(
    dense_units1 = 128,
    dropout1 = 0.5,
    dense_units2 = 128,
    dropout2 = 0.4,
)
network4.summary()

# train and test the model
network4, history4 = train_model(network4, train_images, train_labels_MLP, epochs=10, batch_size=256, learning_rate=0.001, validation_split = 0.2)
test_model(network4, test_images,test_labels)

"""Plot training loss and training accuracy"""

plot_history([history3], 0)

import matplotlib.pyplot as plt
accuracy = history3.history['accuracy']
loss = history3.history['loss']

epochs = range(len(accuracy))

plt.plot(epochs, loss, '-go', label='Training loss')
plt.title('Training loss')
plt.legend()
plt.show()

plt.plot(epochs, accuracy, '-bo', label='Training acc')
plt.title('Training accuracy')
plt.legend()
plt.figure()

"""MLP 3"""

# The below is an example tuning loop for 2 parameters at the same time -- in this case learning rate and 
# the number of units in the first layer.

def tuning_LR_and_DU1(list_LR, list_DU1):
    rows = []
    histories = []
    for lr in list_LR:
        for du1 in list_DU1:
            print("====== LR {}, DU1 {} ======".format(lr, du1))
            model = get_model(dense_units1 = du1)
            current_params = default_params()

            model, history = train_model(
                model = model, 
                train_images = train_images_new, 
                train_labels = train_labels_new,
                learning_rate = lr,
            )

            test_loss, test_acc = test_model(model, test_images_new, test_labels_new)

            # update the parameter we're tuning 
            current_params["learning_rate"] = lr
            current_params["dense_units1"] = du1
            # input results to save to df
            current_params["test_acc"] = test_acc
            current_params["val_acc"] = history.history["val_accuracy"][-1]
            current_params["train_acc"] = history.history["accuracy"][-1]
            current_params["test_loss"] = test_loss
            current_params["val_loss"] = history.history["val_loss"][-1]
            current_params["train_loss"] = history.history["loss"][-1]

            rows.append(current_params)
            histories.append(history)

            print("Test loss: {:.4f}".format(test_loss))
            print("Test accuracy: {:.4f}".format(test_acc))
            print("\n")

    return rows, histories

# Sample usage for the above tuning function.
#
# In this case both hyperparameters are explored together, 
# e.g. learning rate=0.0001, units=128; 
# then learning rate=0.0001, units=256; 
# then learning rate=0.0001, units=512; 
# then learning rate=0.001, units=128; etc.

results_LR_DU1, histories_LR_DU1 = tuning_LR_and_DU1([0.0001, 0.001, 0.01], [512, 256, 128])

"""###CNN

build the CNN
"""

from keras.utils import to_categorical

# train_labels_MLP = to_categorical(train_labels)

# Instantiating a small convnet 
from keras.utils import to_categorical
from tensorflow import keras
from tensorflow.keras import layers


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf
tf.config.experimental_run_functions_eagerly(True)
from tensorflow.keras import models, layers, optimizers, losses, metrics
from tensorflow.keras.utils import to_categorical


from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from keras.activations import relu

# This code provides functions that help train a 3-layer multilayer perceptron, 
# with a set of specified default parameters.
# 
# default_params() returns a dictionary of the values for the number of units 
# (i.e. columns in the layer's weight matrix).
#
# get_model(dense_units1, dropout1, dense_units2, dropout2) returns a 3-layer model with 
# the specified # fof units and dropout rates.
#
# To work with a different architecture (e.g. CNNs), rewrite the code in get_model() to return
# a different model.

def default_params():
    params = {
        "dense_units1": 128,
        "dropout1": 0.4,
        "dense_units2": 128,
        "dropout2": 0.3,
        
        "epochs": 10,
        "batch_size": 128,
        "learning_rate": 0.001,
        "validation_split": 0.2,
    }    
    return params    

def get_model(
    dense_units1 = 128,
    dropout1 = 0.4,
    dense_units2 = 128,
    dropout2 = 0.3,
):
    model = models.Sequential()
    model.add(layers.Dense(units = dense_units1, activation='relu', input_shape=(28 * 28,)))
    model.add(layers.Dropout(rate = dropout1))
    model.add(layers.Dense(units = dense_units2, activation='relu'))
    model.add(layers.Dropout(rate = dropout2))
    model.add(layers.Dense(units = 10, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )
    
    return model

# Support code to train, test, and plot the loss and accuracy of a given model.

def train_model(
    model,
    train_images,
    train_labels,
    epochs = 10,
    batch_size = 128,
    learning_rate = 0.001,
    validation_split = 0.2,
):
    start_time = time()

    history = model.fit(
        train_images, 
        train_labels, 
        epochs = epochs, 
        batch_size = batch_size,
        validation_split = validation_split,
    )

    end_time = time()
    print("Running time for training: {:.2f} seconds".format(end_time - start_time))
    
    return model, history

def test_model(
    model,
    test_images,
    test_labels,
):
    
    test_loss, test_acc = model.evaluate(
        test_images_new, 
        test_labels_new,
    )
    
    return test_loss, test_acc

def plot_history(histories, run_index):
    history = histories[run_index]
    
    acc = history.history['accuracy']
    loss = history.history['loss']
    val_acc = history.history['val_accuracy']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.plot(epochs, loss, '-bo', label='Training loss')
    plt.plot(epochs, val_loss, '-ro', label = "Validation loss")
    plt.title('Training loss')
    plt.legend()
    plt.show()

    plt.plot(epochs, acc, '-bo', label='Training acc')
    plt.plot(epochs, val_acc, '-ro', label = "validation acc")
    plt.title('Training accuracy')
    plt.legend()
    plt.figure()

    # The below function is a tuning loop for one parameter; 
# we have chosen the number of epochs as an example.
# It will loop over a list of number of epochs to train for; 
# you can modify this function or create your own to iterate 
# over another parameter (e.g. batch size).

def tuning_epochs(list_of_epochs):
    rows = []
    histories = []
    for num_epochs in list_of_epochs:
        print("====== {} epochs ======".format(num_epochs))
        model = get_model()
        current_params = default_params()

        model, history = train_model(
            model = model, 
            train_images = train_images_new, 
            train_labels = train_labels_new,
            epochs = num_epochs,
        )
            
        test_loss, test_acc = test_model(model, test_images_new, test_labels_new)

        # update the parameter we're tuning 
        current_params["epochs"] = num_epochs
        # input results to save to df
        current_params["test_acc"] = test_acc
        current_params["val_acc"] = history.history["val_accuracy"][-1]
        current_params["train_acc"] = history.history["accuracy"][-1]
        current_params["test_loss"] = test_loss
        current_params["val_loss"] = history.history["val_loss"][-1]
        current_params["train_loss"] = history.history["loss"][-1]
        
        rows.append(current_params)
        histories.append(history)
        
        print("Test loss: {:.4f}".format(test_loss))
        print("Test accuracy: {:.4f}".format(test_acc))
        print("\n")
        
    return rows, histories

"""train CNN"""

def get_model_cnn(

):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.4))

    model.add(layers.Dense(10, activation='softmax'))



    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )
    
    return model

    # Build the second model
network5 = get_model_cnn(
    # dense_units1 = 128,
    # dropout1 = 0.4,
    # dense_units2 = 128,
    # dropout2 = 0.3,
)
network5.summary()


train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)

network5, history5 = train_model(network5, train_images, train_labels, epochs=10, batch_size=128, learning_rate=0.001, validation_split = 0.2)

"""test"""

def test_model(
    model,
    test_images,
    test_labels,
):

    test_loss, test_acc = model.evaluate(
        test_images, 
        test_labels,
    )
    
    return test_loss, test_acc

train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)


test_model(network5, test_images, test_labels)

plot_history([history5], 0)

import matplotlib.pyplot as plt
accuracy = history5.history['accuracy']
loss = history5.history['loss']

epochs = range(len(accuracy))

plt.plot(epochs, loss, '-go', label='Training loss')
plt.title('Training loss')
plt.legend()
plt.show()

plt.plot(epochs, accuracy, '-bo', label='Training acc')
plt.title('Training accuracy')
plt.legend()
plt.figure()

"""different lr """



# build and test 

def get_model_cnn(

):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.4))

    model.add(layers.Dense(10, activation='softmax'))



    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )
    
    return model

    # Build the second model
network6 = get_model_cnn(
    # dense_units1 = 128,
    # dropout1 = 0.4,
    # dense_units2 = 128,
    # dropout2 = 0.3,
)
network6.summary()


train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)

network6, history6 = train_model(network6, train_images, train_labels, epochs=3, batch_size=128, learning_rate=0.001, validation_split = 0.2)


def test_model(
    model,
    test_images,
    test_labels,
):

    test_loss, test_acc = model.evaluate(
        test_images, 
        test_labels,
    )
    
    return test_loss, test_acc

train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)


test_model(network6, test_images, test_labels)

"""lr 0.001 _ dropout 0.25"""

#@title 기본 제목 텍스트

# build and test 

def get_model_cnn(

):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dropout(0.25))

    model.add(layers.Dense(10, activation='softmax'))



    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy']
    )
    
    return model

    # Build the second model
network10 = get_model_cnn(
    # dense_units1 = 128,
    # dropout1 = 0.4,
    # dense_units2 = 128,
    # dropout2 = 0.3,
)
network10.summary()


train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)

network10, history10 = train_model(network10, train_images, train_labels, epochs=10, batch_size=128, learning_rate=0.001, validation_split = 0.2)


def test_model(
    model,
    test_images,
    test_labels,
):

    test_loss, test_acc = model.evaluate(
        test_images, 
        test_labels,
    )
    
    return test_loss, test_acc

train_images = np.array(mnist2["train"]["x"])
test_images = np.array(mnist2["test"]["x"])
train_labels = np.array(mnist2["train"]["y"])
test_labels = np.array(mnist2["test"]["y"])

train_images_new = train_images.reshape((50000, 28 * 28))
train_images_new = train_images_new.astype('float32') / 255

test_images_new = test_images.reshape((10000, 28 * 28))
test_images_new = test_images_new.astype('float32') / 255

train_labels_new = to_categorical(train_labels)
test_labels_new = to_categorical(test_labels)


test_model(network10, test_images, test_labels)
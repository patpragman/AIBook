# copy paste kaggle code

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D

from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras import callbacks

training_datagen = ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2
)
test_datagen = ImageDataGenerator(
    rescale=1. / 255
)

# We prepare the datasets. all codes are similar, let's see the training data to understand the general structure
train_ds = training_datagen.flow_from_directory(
    # first we get the folder where the images are stored in an organized way
    "../data/smiles/train",
    # we provide the list of classes to have a consistent ordering of classes between train and test set apple->0 banana->1 etc
    classes=["smile", "non_smile"],
    # how we want to load images, we want them as rgb images so with 3 channels
    color_mode="rgb",
    # size of batches to group images
    batch_size=16,
    # resize images to match this fixed dimension
    target_size=(64, 64),
    # have classes one hot encoded
    class_mode="categorical",
    # get the training subset
    subset="training"
)

valid_ds = training_datagen.flow_from_directory(
    "../data/smiles/train",
    classes=["smile", "non_smile"],
    color_mode="rgb",
    batch_size=16,
    target_size=(64, 64),
    class_mode="categorical",
    subset="validation"
)

model = Sequential()
model.add(Conv2D(128, (3, 3), input_shape=(64, 64, 3), padding="same", activation="gelu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(64, activation="relu"))
model.add(Dropout(rate=0.2))
model.add(Dense(2, activation="sigmoid"))
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',  # tries to check smile with not smile distro - check for high entropy or not
    metrics=['accuracy']
)
callback_list = [
    callbacks.EarlyStopping(monitor="val_accuracy", patience=10, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(factor=0.8, monitor="val_accuracy", patience=3)
]

history = model.fit(train_ds, validation_data=valid_ds, epochs=50, verbose=1, callbacks=callback_list)

model.save("smile_model",
           overwrite=True)

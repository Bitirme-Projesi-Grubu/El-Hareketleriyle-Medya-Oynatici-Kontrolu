import numpy as np
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense,Dropout,BatchNormalization,Activation
from sklearn.model_selection import train_test_split


dataset = 'Data.csv'
x_data = np.loadtxt(dataset, delimiter=',', dtype='float32', usecols=list(range(1, (21*3)+1)))
y_data = np.loadtxt(dataset, delimiter=',', dtype='int32', usecols=(0))

classes = ["oynat", "durdur", "geriSar", "ileriSar", "sustur", "sesAc"]

X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.7, random_state=45)

model = Sequential()
model.add(Dense(16, input_shape=(21*3,), activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(9, activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(6, activation="relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax'))

model.summary()

cp_callback = tf.keras.callbacks.ModelCheckpoint("model.hdf5", verbose=1, save_weights_only=False)
es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=500, batch_size=128, validation_data=(X_test, y_test), callbacks=[cp_callback, es_callback])
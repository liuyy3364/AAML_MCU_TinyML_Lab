import tensorflow as tf

keras_model = tf.keras.models.load_model('utils/pretrainedResnet.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
tflite_model = converter.convert()
open('pretrainedResnet.tflite', 'wb').write(tflite_model)

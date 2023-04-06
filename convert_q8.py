import tensorflow as tf
import numpy as np
from utils import train

cifar_10_dir = 'utils/cifar-10-batches-py'
def representative_dataset_generator():
    train_data, train_filenames, train_labels, test_data, test_filenames, test_labels, label_names = \
        train.load_cifar_10_data(cifar_10_dir)
    _idx = np.load('utils/calibration_samples_idxs.npy')
    for i in _idx:
        sample_img = np.expand_dims(np.array(test_data[i], dtype=np.float32), axis=0)
        yield [sample_img]

keras_model = tf.keras.models.load_model('utils/pretrainedResnet.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.representative_dataset = representative_dataset_generator
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
tflite_model = converter.convert()
open('pretrainedResnet_quant.tflite', 'wb').write(tflite_model)

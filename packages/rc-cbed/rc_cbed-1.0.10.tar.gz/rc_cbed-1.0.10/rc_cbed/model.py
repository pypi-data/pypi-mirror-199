"""
rc_cbed network design to restore and center CBED images

Author: Ivan Lobato
Email: Ivanlh20@gmail.com
"""
import os
import pathlib
from typing import Tuple

import h5py
import numpy as np
import tensorflow as tf

def fcn_set_gpu_id(gpu_visible_devices: str = "0") -> None:
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_visible_devices

def load_rc_cbed_net(model_path: str = None, gpu_id: str = "0") -> tf.keras.Model:
    fcn_set_gpu_id(gpu_id)
    
    if model_path is None:
        model_path = pathlib.Path(__file__).resolve().parent / 'model'
    else:
        model_path = pathlib.Path(model_path).resolve()
        
    model = tf.keras.models.load_model(model_path, compile=False)
    model.compile()
    return model

def load_test_data(path: str = None) -> Tuple[np.ndarray, np.ndarray]:
    if path is None:
        path = pathlib.Path(__file__).resolve().parent / 'test_data.h5'
    else:
        path = pathlib.Path(path).resolve()

    with h5py.File(path, 'r') as h5file:
        x = np.asarray(h5file['x'][:], dtype=np.float32).transpose(0, 3, 2, 1)
        y = np.asarray(h5file['y'][:], dtype=np.float32).transpose(0, 3, 2, 1)
    
    return x, y
import numpy as np
import math

class BinaryFeatureExtractor:

    @staticmethod
    def entropy(arr):
        freq = np.bincount(arr, minlength=256)
        prob = freq / len(arr)
        return -np.sum([p*np.log2(p) for p in prob if p>0])

    @staticmethod
    def rolling_entropy(arr, size=64):
        out = []
        for i in range(0, len(arr), size):
            chunk = arr[i:i+size]
            if len(chunk)>0:
                out.append(BinaryFeatureExtractor.entropy(chunk))
        return out

    @staticmethod
    def extract_features(byte_arr):
        ent = BinaryFeatureExtractor.entropy(byte_arr)
        roll = np.mean(BinaryFeatureExtractor.rolling_entropy(byte_arr))
        high_entropy = 1.0 if ent > 6.8 else 0.0
        return np.array([ent, roll, high_entropy], dtype=np.float32)

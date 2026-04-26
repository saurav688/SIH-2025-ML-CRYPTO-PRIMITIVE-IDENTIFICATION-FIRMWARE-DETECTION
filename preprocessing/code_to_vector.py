import re
import numpy as np
import hashlib

class CodeToVector:
    """
    Transformer + Keywords + regex features for AES/SHA detection.
    """

    KEYWORDS = {
        "AES": ["aes", "mixcolumns", "sbox", "addroundkey", "subbytes", "rijndael"],
        "SHA": ["sha", "sha256", "rotateright", "ch", "maj", "sigma0", "sigma1"],
    }

    def clean(self, code):
        code = re.sub(r"//.*|#.*", "", code)
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
        return code.lower()

    def keyword_vector(self, code):
        vec = []
        for group in self.KEYWORDS.values():
            vec.append(1.0 if any(k in code for k in group) else 0.0)
        return np.array(vec, dtype=np.float32)  # [AES, SHA]

    def char_ngram_hash(self, code, n=3):
        h = hashlib.sha256(code[:2000].encode()).digest()
        return np.array(list(h[:16]), dtype=np.float32) / 255.0

    def get_vector(self, code):
        code = self.clean(code)
        kw = self.keyword_vector(code)
        ng = self.char_ngram_hash(code)
        return np.concatenate([kw, ng])   # [18-d vector]

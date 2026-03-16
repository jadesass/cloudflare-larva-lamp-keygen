import hashlib
import secrets
from PIL import Image
import numpy as np
from datetime import datetime

class ImageEntropyGenerator:
    def __init__(self):
        self.entropy_pool = bytearray()
    
    def add_image_entropy(self, define_image_path):
        with Image.open(define_image_path) as img:
            img = img.convert('RGB')
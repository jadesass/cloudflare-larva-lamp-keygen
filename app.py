import hashlib
import secrets
from PIL import Image
import numpy as np
from datetime import datetime

class ImageEntropyGenerator:
    def __init__(self):
        self.entropy_pool = bytearray()
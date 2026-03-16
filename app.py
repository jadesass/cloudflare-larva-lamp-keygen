import hashlib
import secrets
from PIL import Image
import numpy as np
from datetime import datetime
from scipy import ndimage
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Define entropy class

class ImageEntropyGenerator:

    def __init__(self):

        self.entropy_pool = bytearray()
    
    def add_image_entropy(self, define_image_path):

        with Image.open(define_image_path) as img:

            img = img.convert('RGB')

            # Get pixel array since numpy returns it as tensor, we need to convert it to bytes

            pixels = np.array(img)
            
            pixel_bytes = pixels.tobytes()
            
            mean = np.mean(pixels).tobytes()

            std = np.std(pixels).tobytes()

            edges = ndimage.sobel(pixels.mean(axis=2))

            edge_bytes = edges.tobytes()
            
            timestamp = str(datetime.now().timestamp()).encode()
            
            # Create system entropy
            system_random = secrets.token_bytes(32)
            
            # Combine all sources
            combined = (pixel_bytes + mean + std + edge_bytes + timestamp + system_random)
            
            # Hash and add to pool
            hashed = hashlib.sha3_512(combined).digest()

            self.entropy_pool.extend(hashed)
    
    def generate_key(self, key_length=32):

        if len(self.entropy_pool) < key_length:

            raise ValueError("Insufficient entropy in pool")
        
        # Use HKDF (HMAC-based Key Derivation Function)
        
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=secrets.token_bytes(16),
            info=b'image-entropy-key'
        )
        
        key = hkdf.derive(bytes(self.entropy_pool))
        
        # Clear used entropy

        self.entropy_pool = self.entropy_pool[key_length:]
        
        return key.hex()


generator = ImageEntropyGenerator()

# Use multiple images to increase entropy add more images as needed for better randomness. Use your own image below
generator.add_image_entropy('image-entropy/ent-1.png')
generator.add_image_entropy('image-entropy/ent-2.png')
generator.add_image_entropy('image-entropy/ent-3.png')

# Generate keys
key1 = generator.generate_key(32)  # 256-bit key
key2 = generator.generate_key(64)  # 512-bit key

print(f"Key 1: {key1}")
print(f"Key 2: {key2}")
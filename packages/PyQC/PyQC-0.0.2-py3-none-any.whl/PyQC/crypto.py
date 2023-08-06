import base64
import uuid

from .ccakem import kem_keygen1024, kem_encaps1024, kem_decaps1024
from .cpake import generate_kyber_keys
from Crypto.Random import get_random_bytes
from .params import KYBER_SYM_BYTES
from Crypto.Cipher import AES
from typing import List, TypeAlias, Tuple, Optional, TypedDict
from .data import KyberKeyPair

# Change in professional version
def get_uuid_4() -> str:
    return str(uuid.uuid4())

int_array: TypeAlias = List[int]
seed_array: TypeAlias = bytearray
keypair: TypeAlias = Tuple[int_array, int_array]
key_exchange: TypeAlias = Tuple[int_array, int_array]

class Kyber:
    def __init__(self, keypair: KyberKeyPair = None):
        if keypair:
            if isinstance(keypair, KyberKeyPair):
                self.kyber_obj = keypair
            else:
                raise Exception(f'The keypair provided is of type {type(keypair)} not of type KyberKeyPair')
        else:
            # * needed to decouple args being passed
            self.kyber_obj = KyberKeyPair(*self.keypair_generation(), uuid = get_uuid_4())
            
    def keypair_generation(self) -> keypair:
        return kem_keygen1024()
        
    def get_seed(self) -> seed_array:
        return bytearray([x & 0xFF for x in get_random_bytes(KYBER_SYM_BYTES)])
        
    # Returns secret, cipher
    def key_exchange(self, others_public_key: int_array) -> key_exchange:
        return kem_encaps1024(others_public_key, self.get_seed())
        
    def session_key_extraction(self, cipher: int_array) -> int_array:
        return kem_decaps1024(self.kyber_obj.private_key, cipher)
        
    def get_public_key(self) -> int_array:
        return self.kyber_obj.public_key
        
    def export_kyber(self) -> KyberKeyPair:
        return self.kyber_obj

# Meant for Kyber
class SessionKey:
    # Dont change the pad_characters right now...
    def __init__(self, secret: int_array, pad_characters: list = ['`']):
        self.key = self.convert_int_array_to_bytes(secret)
        self.pad_chars = pad_characters
        self.pad_length = len(self.pad_chars)
        
    def convert_int_array_to_bytes(self, secret: int_array) -> bytes:
        return bytes([abs(number) for number in secret])
        
    # Base64 won't work right now
    def encrypt(self, message: str, base64_codec: bool = False) -> Tuple[bytes, bytes]:
        aes_cbc_cipher_obj = AES.new(self.key, AES.MODE_CBC)
        counter = 0
        
        while len(message) % 16 != 0:
            message += self.pad_chars[counter % self.pad_length]
            counter += 1
            
        b = message.encode("UTF-8")
        
        ciphertext = aes_cbc_cipher_obj.iv, aes_cbc_cipher_obj.encrypt(b)
        
        if base64_codec:
            return base64.b64encode(ciphertext)
        return ciphertext
        
    # Base64 won't work right now
    def decrypt(self, iv: bytes, cipher_text: bytes, base64_codec: bool = False) -> str:
        aes_cbc_cipher_obj = AES.new(self.key, AES.MODE_CBC, iv=iv)
        
        if base64_codec:
            cipher_text = base64.b64decode(cipher_text)
            
        cleartext = aes_cbc_cipher_obj.decrypt(cipher_text).decode("UTF-8")
        
        # Fix later
        return cleartext.replace('`','')
            
if __name__ == "__main__":
    client = Kyber()
    server = Kyber()
    
    # Exchange Session Key
    secret1, cipher = server.key_exchange(client.get_public_key())
    secret2 = client.session_key_extraction(cipher)
    
    print(secret1 == secret2)
    
    session_client = SessionKey(secret2)
    session_server = SessionKey(secret1)
    
    iv, cipher_text = session_client.encrypt('The force is on our side')
    print(session_server.decrypt(iv, cipher_text))

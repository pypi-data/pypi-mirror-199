import json
import uuid

from .data import JWT_Token, int_array, Uuid, BaseCertificate, DeadOnArrival, Unencrypted_JWT_Token, Entity
from .date_utils import datetime_object, add_time
from datetime import datetime
from .crypto import Kyber, SessionKey

# Change in professional version
def get_uuid_4() -> str:
    return str(uuid.uuid4())

# Auth Server (Oauth) -> others_public_key, others_uuid, auth_server_code, time_of_use (in seconds)
class KyberToken:
    def __init__(self, kyber_obj: Kyber):
        # Definitely change later!!!
        if not kyber_obj.kyber_obj.uuid:
            raise Exception("Need session traceability")
            
        self.kyber_obj = kyber_obj
        self.sessions = {}
        
        
    def start_session(self, peer_info: Entity, auth_server_code: int, time_of_use: int):
        starter_data = self.generate_base_data(auth_server_code, time_of_use)
        
        # Add to C hash table here!
        session_key = self.establish_session_key(peer_info, self.starter_data)
        self.sessions[hash(session_key)] = session_key
        
    def generate_base_data(self, auth_server_code: int, time_of_use: int) -> BaseCertificate:
        # Get new uuid from server
        start_time = datetime_object()
        return BaseCertificate(start_time, get_uuid_4(), auth_server_code, add_time(start_time, time_of_use))
    
    def establish_session_key(self, peer_info: Entity, data: BaseCertificate) -> SessionKey | None:
        # Implement in commercial version
        return None
        
    """
        - Could use this instead of SessionChannelAsync if expected for low resource usage
        - Create during a different programming sprint
    def token_api(self, token: JWT_Token) -> Optional[JWT_Token]:
        pass
    """
        
    # Store in hash bins later!!!
    # Option to pass inheritance for TypedDict regulation of data instances
    
    ### IMPORTANT!!!
    #### Commercial version pass the IV through the gRPC channel/ip flow
    def create_token(self, data: dict, session_key: SessionKey) -> JWT_Token:
        iv, ciphertext = session_key.encrypt(json.dumps(data))
        return JWT_Token(datetime_object(), iv, ciphertext)
        
    # Option to pass inheritance for TypedDict regulation of data instances to subclass data
    ### , iv: bytes in function signature
    def decrypt_token(self, token: JWT_Token, session_key: SessionKey) -> Unencrypted_JWT_Token:
        unencrypted_data = json.loads(session_key.decrypt(token.iv, token.data))
        return Unencrypted_JWT_Token(token.timestamp, unencrypted_data)
        
if __name__ == "__main__":
    client = Kyber()
    server = Kyber()
    
    client_to_server_token_handler = KyberToken(client)
    server_to_client_token_handler = KyberToken(server)
    """
        Different programming sprint!!!
        
    client_entity = Entity(get_uuid_4(), client.get_public_key(), datetime_object())
    
    # Obtained from Oauth server -> commercial
    server_entity = Entity(get_uuid_4(), server.get_public_key(), datetime_object())
    authorization_code = 123456789
    time_of_use = 14400 # 4 hours
    
    # Store sessions/session keys in C hash table
    client_to_server_token_handler.start_session(server, authorization_code, time_of_use)
    """
    
    ################################################
    ## Generate fake session keys here
    secret1, cipher1 = server.key_exchange(client.get_public_key())
    secret2 = client.session_key_extraction(cipher1)
    
    server_session = SessionKey(secret1)
    client_session = SessionKey(secret2)
    ################################################
    
    data = {"resource_id": 12345, "endpoint": "/submission", "results": {"passed": True, "cpu": 12345, "memory": 10000}}
    encrypted_client_token = client_to_server_token_handler.create_token(data, client_session)
    
    print(server_to_client_token_handler.decrypt_token(encrypted_client_token, server_session))
        
        

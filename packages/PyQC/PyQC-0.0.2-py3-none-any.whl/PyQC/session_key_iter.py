import asyncio

from .date_utils import datetime_object, check_delta_timestamp
from datetime import timedelta
from .data import PeerAwarenessKyber
from .requests_utils import RequestApi

"""
@dataclass
class PeerAwarenessKyber:
    channel_id: int
    started_communication: datetime.date
    ip_address: IpAddr
    endpoint: str
    public_key: int_array
    event_watcher: Optional[asyncio.locks.Event] = None
    end_communication: Optional[datetime.date] = None
"""

"""
    Need to test event trigger!
"""

# Manually set through anext so as to wait for the channel -> more control
# Need to verify bounds check first!
# Fix the requests_utils for this!!!
# Need to create JWT_Token for Kyber -> done for RSA
class SessionChannelAsync(RequestApi):
    #######################################
    ####  Cutting The Channel: 4 Ways  ####
    #######################################
    #################################################################
    ####  End communication -> passed by oauth server; graceful  ####
    ####                             ################################
    ####  Timeout by self; graceful  ####
    ####                             #############
    ####  Signal monitored triggered; abrupt  ####
    ####                                      #################################
    ####  Peer ends -> either signal or sends timeout; graceful or abrupt  ####
    ###########################################################################
    def __init__(self, owner_crypto: KyberKeyPair, session_key: SessionKey, peer_awareness: PeerAwarenessKyber, timeout: int = 86400):
        ###########################
        ####  Message Channel  ####
        ###########################
        ############################################################
        ####  Permits UDP multiplexing with tcp seqack numbers  ####
        ####                        ################################
        ####  ConnectID:ciphertext  ####
        ################################
        self.kyber_keypair_obj = owner_crypto
        self.session_key_obj = session_key
        
        self.outgoing_message_channel = asyncio.Queue()
        self.incoming_message_channel = asyncio.Queue()
        
        self.peer_awareness = peer_awareness
        
        self.foreign_channel_api = f"{self.peer_awareness.ip_address}/{self.peer_awareness.endpoint}"
        
        self.event_watcher = self.peer_awareness.event_watcher
        
        self.started_communication = self.peer_awareness.started_communication
        self.end_communication = self.peer_awareness.end_communication
        self.timeout = self.started_communication + timedelta(seconds=timeout)
        self.end_time = self.end_communication if self.end_communication < self.timeout else self.timeout
        
        self.sigkill = False
        
    def valid_timestamp(self) -> bool:
        return check_delta_timestamp(self.started_communication, self.end_time)
        
    def __aiter__(self):
        return self
        
    def create_token(self, message: str) -> JWT_Token:
        pass
        
    # External watcher/controller sets the event boolean
    def check_event_watcher(self) -> bool:
        if self.event_watcher and self.event_watcher.is_set():
            return True
        return False
        
    async def __anext__(self):
        if self.sigkill or self.check_event_watcher():
            raise StopAsyncIteration
            
        if valid_timestamp:
            responses = []
            
            while self.incoming_message_channel.qsize():
                message = await self.incoming_message_channel.get()
                
                if message == "Cutting connection!"):
                    self.sigkill = True
                    # Weird but have to return and mark sigkill... assuming continuous client using anext()
                    return responses
                    
                responses.append(message)
                
            while self.outgoing_message_channel.qsize():
                token = self.create_token(await self.outgoing_message_channel.get())
                await self.post(self.foreign_channel_api, token, _return = False)
                
            return responses
                
        else:
            token = self.create_token("Cutting connection!")
            # Don't have to wait!!!
            await self.post(self.foreign_channel_api, token, _return = False)
            
            raise StopAsyncIteration
            
class SessionChannelUser:
    pass

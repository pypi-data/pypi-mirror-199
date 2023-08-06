import datetime
import asyncio

from dataclasses import dataclass
from typing import List, TypeAlias, Optional, TypedDict

int_array: TypeAlias = List[int]
# Fix later
ip_addr: TypeAlias = str

# Fix later
# Add regex methods here!
@dataclass
class IpAddr:
    ip_address: ip_addr

@dataclass
class Uuid:
    uuid_component: str
    
@dataclass
class Entity:
    uuid: Uuid
    public_key: int_array
    date_created: datetime.date
    
@dataclass
class ValidKeyPair:
    date_created: datetime.date
    last_verified: datetime.date
    valid: bool
    verified_by: Entity

@dataclass
class KyberKeyPair:
    private_key: int_array
    public_key: int_array
    uuid: Optional[Uuid] = None
    valid: Optional[ValidKeyPair] = None
    algorithm: int = 1024
    
@dataclass
class SessionKey:
    times_used_key: int # Both ends count
    sender_uuid: Uuid
    receiver_uuid: Uuid
    key: int_array
    data: bytes
    
"""
@dataclass
class Unencrypted_Data:
    others_uuid: Uuid
    others_public_key: int_array
    session_key: SessionKey
    timestamp: datetime.date
"""

@dataclass
class BaseCertificate:
    session_started: datetime.date
    session_key_uuid: Uuid
    authorization_code: int
    max_time_of_use: datetime.date
    users_invovled: Optional[List[Uuid]] = None # Free version doesnt need this
    
@dataclass
class DeadOnArrival:
    pass
    
@dataclass
class Unencrypted_JWT_Token:
    timestamp: datetime.date
    data: dict # Unencrypted_Data
    cipher: str = "Kyber1024"
    
@dataclass
class JWT_Token:
    timestamp: datetime.date
    iv: bytes
    data: bytes
    cipher: str = "Kyber1024"
    
@dataclass
class PeerAwarenessKyber:
    channel_id: int
    started_communication: datetime.date
    ip_address: IpAddr
    endpoint: str
    public_key: int_array
    event_watcher: Optional[asyncio.locks.Event] = None
    end_communication: Optional[datetime.date] = None

from pydantic import BaseModel, Field, ValidationError

class NetworkLog(BaseModel):
    srcip: str
    dstip: str
    sport: int 
    dsport: int
    proto: str
    service: str 
    state: str
    dur: int
    sbytes: int 
    dbytes: int 
    spkts: int 
    dpkts: int
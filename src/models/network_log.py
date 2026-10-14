from pydantic import BaseModel, Field, AliasPath, field_validator
from typing import Optional

class NetworkLog(BaseModel):
    srcip: str = Field(validation_alias="src_ip")
    dstip: str = Field(validation_alias="dest_ip")
    sport: int = Field(validation_alias="src_port")
    dsport: int = Field(validation_alias="dest_port")
    proto: str
    service: str = Field(default="-", validation_alias="app_proto")
    state: str = Field(default="CON")
    
    # Use AliasPath to dive into the nested "flow" dictionary
    dur: float = Field(default=0.0, validation_alias=AliasPath("flow", "age"))
    sbytes: int = Field(default=0, validation_alias=AliasPath("flow", "bytes_toserver"))
    dbytes: int = Field(default=0, validation_alias=AliasPath("flow", "bytes_toclient"))
    spkts: int = Field(default=0, validation_alias=AliasPath("flow", "pkts_toserver"))
    dpkts: int = Field(default=0, validation_alias=AliasPath("flow", "pkts_toclient"))

    @field_validator("proto", mode="before")
    @classmethod
    def upper_proto(cls, v: str) -> str:
        return v.upper() if v else "TCP"
from pydantic import BaseModel, Field, AliasPath, field_validator
from typing import Optional

class AlertLog(BaseModel):
    srcip: str = Field(validation_alias="src_ip")
    dstip: str = Field(validation_alias="dest_ip")
    sport: int = Field(validation_alias="src_port")
    dsport: int = Field(validation_alias="dest_port")
    proto: str
    
    # Extracting nested fields from the 'alert' dictionary using AliasPath
    signature: str = Field(validation_alias=AliasPath("alert", "signature"))
    sid: int = Field(validation_alias=AliasPath("alert", "signature_id"))
    category: str = Field(default="Unknown", validation_alias=AliasPath("alert", "category"))
    severity: int = Field(default=3, validation_alias=AliasPath("alert", "severity"))
    action: str = Field(default="allowed", validation_alias=AliasPath("alert", "action"))

    @field_validator("proto", mode="before")
    @classmethod
    def upper_proto(cls, v: str) -> str:
        return v.upper() if v else "TCP"
    
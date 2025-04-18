from pydantic import BaseModel, Field
from typing import Optional

class ScrapperBotSchema(BaseModel):
    make: Optional[str] = Field(default="")
    model: Optional[str] = Field(default="")
    version: Optional[str] = Field(default="")
    year_from: Optional[str] = Field(default="")
    year_to: Optional[str] = Field(default="")
    power_from: Optional[str] = Field(default="")
    power_to: Optional[str] = Field(default="")
    powertype: Optional[str] = Field(default="kw")
    num_pages: Optional[int] = Field(default=1)
    zipr: Optional[int] = Field(default=250)

from numpy import delete
from pydantic import BaseModel, Field
from typing import Optional


class AnalyzeSchema(BaseModel):
    target_price: int
    delete_analysis: Optional[bool] = Field(default=False, description="Borra el análisis anterior antes de ejecutar uno nuevo")
    
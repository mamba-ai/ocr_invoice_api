from pydantic import BaseModel


class OCRRequest(BaseModel):
    type: str # "invoice" or "receipt"
    image_base64: str
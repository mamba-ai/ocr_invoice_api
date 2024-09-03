from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

from ocr_agent import load_client, ocr_invoice
from util import convert_base64_to_image, resize_image_if_needed, pil_image_to_base64, detect_image_type
from schema import OCRRequest
from json_examples import invoice_example
from PIL import Image, UnidentifiedImageError


# 设置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

client = load_client()
logger.info("OCR client sucessfully loaded.")

    
app = FastAPI(
    title="MAMBA-AI OCR API",
    description="This API provides OCR services for invoices and receipts, and also other structured documents.",
    version="0.1.0",
    # lifespan=lifespan
)

@app.get("/health")
def health_check():
    return "Running"

@app.get("/")
def read_root():
    return {"Hello": "Welcome to MAMBA-AI OCR API!"}

@app.get("/ping")
def read_root():
    return {"Hello": "Welcome to MAMBA-AI OCR API!"}

@app.post("/predict")
def prediction(request: OCRRequest):
    if request.type == "invoice":
        try:
            # Convert the base64 image to a PIL image
            pil_image = convert_base64_to_image(request.image_base64)
            logging.info("Image converted from base64 to PIL format")
            # Resize the image if needed
            pil_image = resize_image_if_needed(pil_image)
            logging.info("Image resized if needed")
            # Convert the PIL image to a base64 string
            base64_image_string = pil_image_to_base64(pil_image)
            logging.info("PIL image converted back to base64 format")
            # Perform OCR on the invoice image
            invoice_data = ocr_invoice(client, base64_image_string, detect_image_type(base64_image_string), invoice_example)
            logging.info("OCR performed on invoice image")
            logging.info(f"Predicted invoice data: {invoice_data}")
            return JSONResponse(status_code=200, content=invoice_data)   
        except UnidentifiedImageError:
            logging.error("UnidentifiedImageError: The provided image could not be identified.")
            return JSONResponse(status_code=400, content={"error": "The provided image could not be identified."})
        except Exception as e:
            logging.error(f"Error during prediction: \n{str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        logging.warning("Unsupported document type accessed")
        return JSONResponse(status_code=400, content={"error": "Unsupported document type."}) 
import os 
from openai import OpenAI
from dotenv import load_dotenv
import logging
import json

# 设置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def load_client():
    """
    Load the OpenAI client with the API key from the environment variables.

    Returns:
        OpenAI: The OpenAI client object.
    """
    # Load the API key from the environment variables
    load_dotenv()
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", None)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    return client 


def ocr_invoice(client, base64_image_string, image_type, invoice_example):
    """
    Perform OCR on an invoice image and convert the result to a JSON object.

    :param image_path: Path to the invoice image file.
    :return: JSON object containing the parsed invoice data.
    """
    # Convert the image to a base64 string
    # base64_image_string = base64_to_webp_and_back(base64_image_string)
    # image_type = detect_image_type(base64_image_string)
    media_type = f"image/{image_type}"
    
    completion = client.chat.completions.create(
        extra_headers={
            "X-Title": "MAMBA-AI", # Optional. Shows in rankings on openrouter.ai.
        },
        model="anthropic/claude-3.5-sonnet",
        max_tokens=3000,
        temperature=0,
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": "You are a helpful OCR assistant designed to recognize content from image and output JSON.",
            },
            {
                "role": "user",
                "content":[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{base64_image_string}",
                        }
                    },
                    {
                        "type": "text",
                        "text": f'''You are OCR expert, parse, detect, recognize and convert following receipt/invoice image result into structure receipt data object.
Don't make up value not in the Input. Don't lose any information.
Only response json object is needed. No need to response any other information.
Output must be a well-formed JSON format. Following is an example of the JSON object: 
{invoice_example}
If you can't find the value, please leave it null.
'''
                    }
                ]
            }
        ],
    )
    logging.info(completion)
    result = completion.choices[0].message.content
    return result
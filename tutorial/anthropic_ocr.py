import anthropic
from dotenv import load_dotenv
import os 
import base64
import imghdr
import json 
from PIL import Image
import io 


load_dotenv()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def image_to_base64(image_path):
    """
    Load an image file and convert it to a base64 string.

    :param image_path: Path to the image file.
    :return: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        # Read the image file in binary mode
        image_data = image_file.read()
        
        # Encode the binary data to base64
        base64_encoded = base64.b64encode(image_data)
        
        # Convert the base64 bytes to a string
        base64_string = base64_encoded.decode('utf-8')
        
    return base64_string

def pil_image_to_base64(pil_image):
    """
    Convert a PIL image to a base64 string.

    :param pil_image: PIL image object.
    :return: Base64 encoded string of the image.
    """
    # Create a BytesIO object to store the image data
    image_data = io.BytesIO()
    
    # Save the image to the BytesIO object in PNG format
    pil_image.save(image_data, format="PNG")
    
    # Convert the image data to a base64 string
    base64_encoded = base64.b64encode(image_data.getvalue())
    
    # Convert the base64 bytes to a string
    base64_string = base64_encoded.decode('utf-8')
    
    return base64_string

def detect_image_type(base64_str):
    # Decode the base64 string to binary data
    image_data = base64.b64decode(base64_str)
    
    # Detect the image type
    image_type = imghdr.what(None, h=image_data)
    
    return image_type

def save_dict_to_json(data, file_path):
    """
    Save a dictionary to a JSON file.

    :param data: Dictionary to save.
    :param file_path: Path to the JSON file.
    """
    json_data = json.loads(data)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        
def ocr_invoice(base64_image_string):
    """
    Perform OCR on an invoice image and convert the result to a JSON object.

    :param image_path: Path to the invoice image file.
    :return: JSON object containing the parsed invoice data.
    """
    # Convert the image to a base64 string
    image_data = base64_image_string
    image_type = detect_image_type(image_data)
    media_type = f"image/{image_type}"
    
    # Perform OCR on the image
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=3000,
        temperature=0,
        system="You are a helpful OCR assistant designed to recognize content from image and output JSON.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": '''You are OCR expert, parse, detect, recognize and convert following receipt/invoice image result into structure receipt data object. 
    Don't make up value not in the Input. Don't lose any information. 
    Only response json object is needed. No need to response any other information.
    Output must be a well-formed JSON format. Following is an example of the JSON object: 
    {
     "title": "領収書/請求書",
     "recipient": "OOXX株式会社",
     "issue_date": "OO年OO月OO日",
     "description": "飲食代",
     "issuer": "XXOO株式会社",
     "post_code": "123-4567",
     "address": "東京都千代田区駿河台2-2",
     "tel": "987-6543-210",
     "registration_number": "T9010901044466", # optonal
     "before_tax_10_percentage": 60000, # optonal
     "tax_10_percentage": 6000, # optonal
     "before_tax_8_percentage": 10000, # optonal
     "tax_8_percentage": 800, # optonal
     "amount_before_tax": 70000, # optonal
     "total_amount": 76800,
     "items": [],
    }
    If you can't find the value, please leave it null.
    '''
                    }
                ]
            }
        ]
    )
    
    # Return the content of the message
    print(message)
    return message.content[0].text


if __name__ == "__main__":
    # image_path = "/Users/jxl/Documents/LLM/demos/ocr_ivoice/examples/WechatIMG341.jpg"
    # image_path = '/Users/jxl/Documents/LLM/demos/ocr_ivoice/examples/super-market-invoice.webp'
    # image_path = "/Users/jxl/Documents/LLM/demos/ocr_ivoice/examples/invoice-2.jpg"
    image_path = "/Users/jxl/Documents/LLM/demos/ocr_ivoice/examples/demo-examples/invoice-3.jpg"
    pil_image = Image.open(image_path).convert("RGB")
    
    # base64_image_string = image_to_base64(image_path)
    base64_image_string = pil_image_to_base64(pil_image)
    result = ocr_invoice(base64_image_string)
    print(result)
    
    json_file_path = image_path.split("/")[-1].split(".")[0] + ".json"
    save_dict_to_json(result, json_file_path)

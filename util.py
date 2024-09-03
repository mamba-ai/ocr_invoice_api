import base64
import imghdr
from PIL import Image
import io 
import logging

# 设置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def resize_image_if_needed(pil_image, max_size_mb=0.8, max_edge_length=768):
    """
    Detect the size of a PIL image, and if it exceeds 1MB or its long edge is larger than 1024 pixels,
    reduce its size to a smaller size.
    
    Args:
        pil_image (PIL.Image.Image): The input PIL image.
        max_size_mb (int): The maximum allowed size in megabytes.
        max_edge_length (int): The maximum allowed length of the long edge in pixels.
    
    Returns:
        PIL.Image.Image: The resized PIL image.
    """
    # Convert image to bytes and check its size
    img_byte_arr = io.BytesIO()
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")
    pil_image.save(img_byte_arr, format='JPEG')
    img_size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
    logging.info(f"Image size: {img_size_mb} MB")
    
    # Check if the image size exceeds the maximum allowed size
    if img_size_mb > max_size_mb or max(pil_image.size) > max_edge_length:
        # Calculate the new size while maintaining the aspect ratio
        aspect_ratio = pil_image.width / pil_image.height
        if pil_image.width > pil_image.height:
            new_width = min(max_edge_length, pil_image.width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(max_edge_length, pil_image.height)
            new_width = int(new_height * aspect_ratio)
        
        # Resize the image
        pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert the resized image to bytes and check its size again
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='JPEG')
        img_size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
        
        # If the resized image still exceeds the maximum allowed size, reduce the quality
        if img_size_mb > max_size_mb:
            quality = 95
            while img_size_mb > max_size_mb and quality > 10:
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='JPEG', quality=quality)
                img_size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
                quality -= 10
                
    return pil_image


def convert_base64_to_image(base64_str):
    """
    Convert a base64 string to a PIL image.
    Args:
        base64_str (str): The input base64 string.
    Returns:
        PIL.Image.Image: The decoded PIL image.
    """
    # Decode the base64 string into bytes
    image_data = base64.b64decode(base64_str)
    # Open the image from the byte data
    image = Image.open(io.BytesIO(image_data))
    return image


def pil_image_to_base64(pil_image):
    """
    Convert a PIL image to a base64 string.
    :param pil_image: PIL image object.
    :return: Base64 encoded string of the image.
    """
    # Create a BytesIO object to store the image data
    image_data = io.BytesIO()
    # Save the image to the BytesIO object in JPEG format
    pil_image.save(image_data, format="JPEG")
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



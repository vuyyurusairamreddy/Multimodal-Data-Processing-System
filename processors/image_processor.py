# image_processor placeholder
from PIL import Image
import pytesseract

def process_image(file_path):
    try:
        image = Image.open(file_path)
        
        text = pytesseract.image_to_string(image)
        
        metadata = {
            'format': image.format,
            'size': image.size,
            'mode': image.mode
        }
        
        return text.strip(), metadata
    
    except Exception as e:
        return f"Error processing image: {str(e)}", {}

from PIL import Image
import os

def preprocess_image(image_path):

    image = Image.open(image_path)

    # Convert to RGB
    image = image.convert("RGB")

    # Resize for model input
    image = image.resize((224, 224))

    processed_path = image_path.replace(".", "_processed.")

    image.save(processed_path)

    return processed_path
from PIL import Image, ImageEnhance
import os

def generate_explainability_overlay(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))

    # Create simple red heatmap-style overlay for prototype explainability
    heatmap = Image.new("RGB", image.size, (255, 0, 0))

    # Blend original image with red overlay
    overlay = Image.blend(image, heatmap, alpha=0.25)

    # Slightly enhance contrast
    overlay = ImageEnhance.Contrast(overlay).enhance(1.2)

    overlay_path = image_path.replace(".", "_overlay.")

    overlay.save(overlay_path)

    return overlay_path
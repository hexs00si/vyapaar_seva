import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
import uuid

def calculate_brightness(image):
    return np.mean(image)

def calculate_contrast(image):
    return np.max(image) - np.min(image)

def calculate_sharpness(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpness = np.mean(np.abs(laplacian))
    return sharpness

def calculate_brightness_multiplier(brightness):
    if brightness < 100:
        return 1.5  
    elif brightness > 200:
        return 0.8  
    else:
        return 1.0

def calculate_contrast_multiplier(contrast):
    if contrast < 50:
        return 1.5  
    elif contrast > 150:
        return 0.8  
    else:
        return 1.0

def calculate_sharpness_multiplier(sharpness):
    if sharpness < 10:
        return 1.5  
    elif sharpness > 50:
        return 0.8  
    else:
        return 1.0

def enhance_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    brightness = calculate_brightness(img_rgb)
    contrast = calculate_contrast(img_rgb)
    sharpness = calculate_sharpness(img_rgb)

    brightness_multiplier = calculate_brightness_multiplier(brightness)
    contrast_multiplier = calculate_contrast_multiplier(contrast)
    sharpness_multiplier = calculate_sharpness_multiplier(sharpness)

    img_pil = Image.fromarray(img_rgb)
    enhancer = ImageEnhance.Brightness(img_pil)
    img_enhanced = enhancer.enhance(brightness_multiplier)
    enhancer = ImageEnhance.Contrast(img_enhanced)
    img_enhanced = enhancer.enhance(contrast_multiplier)
    enhancer = ImageEnhance.Sharpness(img_enhanced)
    img_enhanced = enhancer.enhance(sharpness_multiplier)

    # Save the enhanced image with a unique filename
    enhanced_image_dir = "enhanced_image"
    if not os.path.exists(enhanced_image_dir):
        os.makedirs(enhanced_image_dir)
    enhanced_image_path = os.path.join(enhanced_image_dir, str(uuid.uuid4()) + ".jpg")
    img_enhanced.save(enhanced_image_path)

    return enhanced_image_path

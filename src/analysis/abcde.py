import cv2
import numpy as np
from sklearn.cluster import KMeans

def analyze_abcde(image: np.ndarray) -> dict:
    """
    Perform classical computer vision ABCDE analysis on a skin lesion image.
    
    Args:
        image: A numpy array representing an RGB image.
        
    Returns:
        A dictionary containing the ABCDE metrics.
    """
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Invalid image provided for ABCDE analysis.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Otsu's thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        # Fallback if no contours found
        return {
            "asymmetry": 0,
            "border_irregularity": 0,
            "color_variation": 0,
            "diameter": 0,
            "evolution": None
        }
        
    # Get the largest contour (assuming it's the lesion)
    cnt = max(contours, key=cv2.contourArea)
    
    # Create a mask for the largest contour
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [cnt], -1, 255, -1)
    
    # --- A: Asymmetry ---
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Crop mask to bounding box for better symmetry calculation
    cropped_mask = mask[y:y+h, x:x+w]
    
    # We pad the cropped mask to make its width even if it's odd
    if cropped_mask.shape[1] % 2 != 0:
        cropped_mask = np.pad(cropped_mask, ((0,0), (0,1)), mode='constant')
        w += 1
        
    half_w = w // 2
    if half_w > 0:
        left_half = cropped_mask[:, :half_w]
        right_half = cv2.flip(cropped_mask[:, half_w:], 1)
        
        intersection = np.logical_and(left_half, right_half).sum()
        union = np.logical_or(left_half, right_half).sum()
        
        asymmetry_score = int(100 * (1 - intersection / union)) if union > 0 else 0
    else:
        asymmetry_score = 0
        
    asymmetry_score = max(0, min(100, asymmetry_score))

    # --- B: Border Irregularity ---
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    
    if perimeter > 0:
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        border_score = int(100 * (1 - circularity))
    else:
        border_score = 0
        
    border_score = max(0, min(100, border_score))
        
    # --- C: Color Variation ---
    # Get pixels within the lesion mask
    lesion_pixels = image[mask == 255]
    
    if len(lesion_pixels) > 5:
        # Downsample for faster KMeans if there are many pixels
        if len(lesion_pixels) > 5000:
            indices = np.random.choice(len(lesion_pixels), 5000, replace=False)
            lesion_pixels = lesion_pixels[indices]
            
        pixels = lesion_pixels.reshape(-1, 3)
        
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        unique_colors = len(np.unique(kmeans.labels_))
        color_score = int(unique_colors / 5 * 100)
    else:
        color_score = 0
        
    # --- D: Diameter ---
    diameter_pixels = max(w, h)
    diameter_score = int(min(diameter_pixels / 200 * 100, 100))
    
    # --- E: Evolution ---
    evolution_score = None

    return {
        "asymmetry": asymmetry_score,
        "border_irregularity": border_score,
        "color_variation": color_score,
        "diameter": diameter_score,
        "evolution": evolution_score
    }

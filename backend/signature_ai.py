import cv2
import numpy as np


def preprocess_signature(image_bytes):

    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Invalid image")

    # Remove noise
    image = cv2.GaussianBlur(image, (3, 3), 0)

    # Convert signature to black/white
    _, binary = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Find signature area
    coords = cv2.findNonZero(binary)

    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        binary = binary[y:y+h, x:x+w]

    # Resize
    binary = cv2.resize(binary, (300, 150))

    return binary


def extract_features(image):

    # Contours
    contours, _ = cv2.findContours(
        image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contour_count = len(contours)

    # Ink pixels
    ink_pixels = np.sum(image > 0)

    # Bounding box
    points = cv2.findNonZero(image)

    if points is not None:
        x, y, w, h = cv2.boundingRect(points)
        aspect_ratio = w / h if h != 0 else 0
    else:
        aspect_ratio = 0

    # Normalized image vector
    vector = image.astype(np.float32).flatten() / 255.0

    return {
        "vector": vector,
        "contours": contour_count,
        "ink_pixels": ink_pixels,
        "aspect_ratio": aspect_ratio
    }


def compare_signatures(real_bytes, doubt_bytes):

    real_image = preprocess_signature(real_bytes)
    doubt_image = preprocess_signature(doubt_bytes)

    real_features = extract_features(real_image)
    doubt_features = extract_features(doubt_image)

    # Pixel similarity
    difference = cv2.absdiff(
        real_image,
        doubt_image
    )

    mean_difference = np.mean(difference)

    pixel_similarity = max(
        0,
        100 - (mean_difference / 255 * 100)
    )

    # Aspect ratio similarity
    ratio_difference = abs(
        real_features["aspect_ratio"]
        - doubt_features["aspect_ratio"]
    )

    ratio_similarity = max(
        0,
        100 - ratio_difference * 50
    )

    # Contour similarity
    contour_difference = abs(
        real_features["contours"]
        - doubt_features["contours"]
    )

    contour_similarity = max(
        0,
        100 - contour_difference * 10
    )

    # Final score
    similarity = (
        pixel_similarity * 0.70 +
        ratio_similarity * 0.20 +
        contour_similarity * 0.10
    )

    similarity = round(
        max(0, min(100, similarity)),
        2
    )

    forgery_risk = round(100 - similarity, 2)

    if similarity >= 80:
        result = "GENUINE"
    elif similarity >= 60:
        result = "SUSPICIOUS"
    else:
        result = "POSSIBLE FORGERY"

    return {
        "similarity": similarity,
        "forgery_risk": forgery_risk,
        "result": result,
        "pixel_similarity": round(pixel_similarity, 2),
        "shape_similarity": round(ratio_similarity, 2),
        "stroke_similarity": round(contour_similarity, 2)
    }
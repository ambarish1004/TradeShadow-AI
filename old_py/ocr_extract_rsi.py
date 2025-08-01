import cv2
import pytesseract
import re
import os

# Setup Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image
image_path = "captures/capture_0.png"
if not os.path.exists(image_path):
    print(f"❌ Image not found: {image_path}")
    exit()

image = cv2.imread(image_path)

# === Step 1: Try both Top and Bottom RSI zones ===
# These coords are common defaults. Adjust later if needed.
regions = {
    "top_rsi": (910, 605, 1005, 640),
    "bottom_rsi": (910, 695, 1005, 735)
}

# === Step 2: Use Tesseract config optimized for RSI values ===
custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.'

# === Step 3: Loop through each region, extract text ===
found = False
for name, (x1, y1, x2, y2) in regions.items():
    crop = image[y1:y2, x1:x2]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)  # Invert for black text on white
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save cropped debug image
    cv2.imwrite(f"{name}_debug.png", thresh)
    print(f"📸 Saved: {name}_debug.png")

    # OCR
    text = pytesseract.image_to_string(thresh, config=custom_config)
    cleaned = text.strip()
    print(f"🔍 OCR Result from {name}:", repr(cleaned))

    # Extract RSI
    match = re.search(r"(\d+\.\d+)", cleaned)
    if match:
        rsi_value = float(match.group(1))
        print(f"✅ RSI Extracted from {name}: {rsi_value}")
        found = True
        break

if not found:
    print("❌ Could not extract RSI value from any region.")

# import cv2
# import pytesseract
# from PIL import Image
# import numpy as np

# # Tesseract path (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# # Load an image from your captures folder
# image_path = "captures/capture_0.png"  # Replace with your actual image
# image = cv2.imread(image_path)

# # Optional: Crop ROI where RSI appears (modify based on your chart layout)
# # For now, full image
# roi = image[0:image.shape[0], 0:image.shape[1]]

# # Convert to grayscale
# gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# # Apply threshold to clean up
# gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# # OCR Config
# custom_config = r'--oem 3 --psm 6'

# # Run OCR
# text = pytesseract.image_to_string(gray, config=custom_config)
# print("🧾 Extracted Text:\n", text)


# import cv2
# import pytesseract
# import re

# # Tesseract path (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# # Load image
# image_path = "captures/capture_0.png"
# image = cv2.imread(image_path)

# # Convert to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Thresholding to improve OCR
# gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# # OCR config
# custom_config = r'--oem 3 --psm 6'

# # Run OCR
# text = pytesseract.image_to_string(gray, config=custom_config)
# print("🧾 Extracted Text:\n", text)

# # Search for RSI value using regex
# rsi_match = re.search(r'RSI(?:\s*\w*)*[:\s\-]*?(\d{2}\.\d{2})', text, re.IGNORECASE)

# if rsi_match:
#     rsi_value = float(rsi_match.group(1))
#     print(f"✅ Extracted RSI Value: {rsi_value}")
# else:
#     print("❌ Could not find RSI value in OCR text.")








import cv2
import pytesseract
import re

# Path to Tesseract OCR (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Load the chart image
image_path = "captures/capture_0.png"
image = cv2.imread(image_path)

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Improve contrast with thresholding
gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

# Tesseract config
custom_config = r'--oem 3 --psm 6'

# Extract text from image
text = pytesseract.image_to_string(gray, config=custom_config)
print("🧾 Extracted Text:\n", text)

# Extract RSI value from text
rsi_match = re.search(r'RSI(?:\s*\w*)*[:\s\-]*?(\d{2}\.\d{2})', text, re.IGNORECASE)

if rsi_match:
    rsi_value = float(rsi_match.group(1))
    print(f"✅ Extracted RSI Value: {rsi_value}")

    # 🚨 Alert logic
    if rsi_value < 30:
        print("📉 ALERT: RSI is LOW (Oversold Zone) → Possible BUY Opportunity")
    elif rsi_value > 70:
        print("📈 ALERT: RSI is HIGH (Overbought Zone) → Possible SELL Opportunity")
    else:
        print("ℹ️ RSI is in normal range (No immediate action)")
else:
    print("❌ Could not find RSI value in OCR text.")

# import os
# import time
# import json
# import threading
# import ctypes
# import tkinter as tk
# from tkinter import messagebox
# import win32gui
# import win32ui
# from PIL import Image
# import cv2
# import pytesseract
# import re

# # OCR config
# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# output_dir = "captures"
# json_path = os.path.join(output_dir, "ocr_data.json")
# os.makedirs(output_dir, exist_ok=True)

# recording = False
# recording_thread = None

# # Load existing JSON or initialize
# if os.path.exists(json_path):
#     with open(json_path, "r", encoding="utf-8") as f:
#         ocr_results = json.load(f)
# else:
#     ocr_results = []

# def get_hwnd_by_title(title_contains):
#     def enum_handler(hwnd, result):
#         if win32gui.IsWindowVisible(hwnd):
#             window_text = win32gui.GetWindowText(hwnd)
#             if title_contains.lower() in window_text.lower():
#                 result.append(hwnd)

#     matches = []
#     win32gui.EnumWindows(enum_handler, matches)
#     return matches[0] if matches else None

# def extract_text_and_rsi(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
#     text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')

#     rsi_match = re.search(r'RSI(?:\s*\w*)*[:\s\-]*?(\d{2}\.\d{2})', text, re.IGNORECASE)
#     rsi_value = float(rsi_match.group(1)) if rsi_match else None
#     return text, rsi_value

# def capture_and_extract(hwnd, counter):
#     left, top, right, bottom = win32gui.GetWindowRect(hwnd)
#     width, height = right - left, bottom - top

#     hwnd_dc = win32gui.GetWindowDC(hwnd)
#     mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
#     save_dc = mfc_dc.CreateCompatibleDC()
#     save_bitmap = win32ui.CreateBitmap()
#     save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
#     save_dc.SelectObject(save_bitmap)

#     result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

#     if result == 1:
#         temp_path = os.path.join(output_dir, f"temp_{counter}.bmp")
#         png_path = os.path.join(output_dir, f"temp_{counter}.png")
#         save_bitmap.SaveBitmapFile(save_dc, temp_path)

#         with Image.open(temp_path) as img:
#             img.save(png_path)
#         os.remove(temp_path)

#         text, rsi = extract_text_and_rsi(png_path)
#         os.remove(png_path)

#         ocr_results.append({
#             "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
#             "rsi": rsi,
#             "text": text.strip()
#         })

#         with open(json_path, "w", encoding="utf-8") as f:
#             json.dump(ocr_results, f, indent=2)

#         print(f"[+] Captured & saved (RSI: {rsi}) ✅")
#     else:
#         print("❌ Failed to capture window.")

#     win32gui.DeleteObject(save_bitmap.GetHandle())
#     save_dc.DeleteDC()
#     mfc_dc.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwnd_dc)

# def record_screen(title):
#     global recording
#     hwnd = get_hwnd_by_title(title)
#     if not hwnd:
#         print("❌ Window not found.")
#         return

#     counter = 0
#     while recording:
#         if not win32gui.IsIconic(hwnd):
#             capture_and_extract(hwnd, counter)
#             counter += 1
#         else:
#             print("⚠ Window is minimized. Skipping...")
#         time.sleep(1)  # Adjust interval if needed

# def start_recording():
#     global recording, recording_thread
#     title = title_entry.get().strip()
#     if not title:
#         messagebox.showerror("Error", "Enter window title.")
#         return
#     if recording:
#         return

#     recording = True
#     recording_thread = threading.Thread(target=record_screen, args=(title,), daemon=True)
#     recording_thread.start()
#     status_label.config(text="⏺ Recording...", fg="red")
#     print(f"✅ Started recording: {title}")

# def stop_recording():
#     global recording
#     recording = False
#     status_label.config(text="⏹ Stopped", fg="green")
#     print("🛑 Stopped.")

# def gui_main():
#     global title_entry, status_label
#     root = tk.Tk()
#     root.title("TradeShadow – Smart Capture")
#     root.geometry("350x300")

#     tk.Label(root, text="🔍 Enter Window Title:").pack(pady=10)
#     title_entry = tk.Entry(root, width=40)
#     title_entry.pack(pady=5)

#     tk.Button(root, text="▶ Start Capturing", command=start_recording, width=30).pack(pady=10)
#     tk.Button(root, text="⏹ Stop Capturing", command=stop_recording, width=30).pack(pady=5)

#     status_label = tk.Label(root, text="Idle", fg="blue", font=("Arial", 12))
#     status_label.pack(pady=20)

#     root.mainloop()

# if __name__ == "__main__":
#     gui_main()





















# import os
# import time
# import json
# import threading
# import ctypes
# import tkinter as tk
# from tkinter import messagebox
# import win32gui
# import win32ui
# from PIL import Image
# import cv2
# import pytesseract
# import re
# from datetime import datetime, timedelta
# from tkinter import messagebox

# # OCR config
# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# output_dir = "captures"
# json_path = os.path.join(output_dir, "ocr_data.json")
# os.makedirs(output_dir, exist_ok=True)

# recording = False
# recording_thread = None

# # Load existing data
# def load_ocr_data():
#     if os.path.exists(json_path):
#         with open(json_path, "r", encoding="utf-8") as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return []
#     return []

# # Remove entries older than 24 hours
# def clean_old_entries(data):
#     now = datetime.now()
#     cleaned_data = []
#     for entry in data:
#         try:
#             entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
#             if now - entry_time <= timedelta(hours=24):
#                 cleaned_data.append(entry)
#         except:
#             continue  # Ignore bad timestamps
#     return cleaned_data

# def get_hwnd_by_title(title_contains):
#     def enum_handler(hwnd, result):
#         if win32gui.IsWindowVisible(hwnd):
#             window_text = win32gui.GetWindowText(hwnd)
#             if title_contains.lower() in window_text.lower():
#                 result.append(hwnd)

#     matches = []
#     win32gui.EnumWindows(enum_handler, matches)
#     return matches[0] if matches else None

# def extract_text_and_rsi(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
#     text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')

#     rsi_match = re.search(r'RSI(?:\s*\w*)*[:\s\-]*?(\d{2}\.\d{2})', text, re.IGNORECASE)
#     rsi_value = float(rsi_match.group(1)) if rsi_match else None
#     return text, rsi_value

# def capture_and_extract(hwnd, counter):
#     left, top, right, bottom = win32gui.GetWindowRect(hwnd)
#     width, height = right - left, bottom - top

#     hwnd_dc = win32gui.GetWindowDC(hwnd)
#     mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
#     save_dc = mfc_dc.CreateCompatibleDC()
#     save_bitmap = win32ui.CreateBitmap()
#     save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
#     save_dc.SelectObject(save_bitmap)

#     result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

#     if result == 1:
#         temp_path = os.path.join(output_dir, f"temp_{counter}.bmp")
#         png_path = os.path.join(output_dir, f"temp_{counter}.png")
#         save_bitmap.SaveBitmapFile(save_dc, temp_path)

#         with Image.open(temp_path) as img:
#             img.save(png_path)
#         os.remove(temp_path)

#         text, rsi = extract_text_and_rsi(png_path)
#         os.remove(png_path)

#         now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         data = load_ocr_data()
#         data = clean_old_entries(data)  # remove old entries

#         data.append({
#             "timestamp": now_str,
#             "rsi": rsi,
#             "text": text.strip()
#         })

#         with open(json_path, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2)

#         print(f"[+] Captured & saved (RSI: {rsi}) ✅")
#     else:
#         print("❌ Failed to capture window.")

#     win32gui.DeleteObject(save_bitmap.GetHandle())
#     save_dc.DeleteDC()
#     mfc_dc.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwnd_dc)

# def record_screen(title):
#     global recording
#     hwnd = get_hwnd_by_title(title)
#     if not hwnd:
#         print("❌ Window not found.")
#         return

#     counter = 0
#     while recording:
#         if not win32gui.IsIconic(hwnd):
#             capture_and_extract(hwnd, counter)
#             counter += 1
#         else:
#             print("⚠ Window is minimized. Skipping...")
#         time.sleep(1)

# def start_recording():
#     global recording, recording_thread
#     title = title_entry.get().strip()
#     if not title:
#         messagebox.showerror("Error", "Enter window title.")
#         return
#     if recording:
#         return

#     recording = True
#     recording_thread = threading.Thread(target=record_screen, args=(title,), daemon=True)
#     recording_thread.start()
#     status_label.config(text="⏺ Recording...", fg="red")
#     print(f"✅ Started recording: {title}")

# def stop_recording():
#     global recording
#     recording = False
#     status_label.config(text="⏹ Stopped", fg="green")
#     print("🛑 Stopped.")

# def gui_main():
#     global title_entry, status_label
#     root = tk.Tk()
#     root.title("TradeShadow – Smart Capture")
#     root.geometry("350x300")

#     tk.Label(root, text="🔍 Enter Window Title:").pack(pady=10)
#     title_entry = tk.Entry(root, width=40)
#     title_entry.pack(pady=5)

#     tk.Button(root, text="▶ Start Capturing", command=start_recording, width=30).pack(pady=10)
#     tk.Button(root, text="⏹ Stop Capturing", command=stop_recording, width=30).pack(pady=5)

#     status_label = tk.Label(root, text="Idle", fg="blue", font=("Arial", 12))
#     status_label.pack(pady=20)

#     root.mainloop()

# if __name__ == "__main__":
#     gui_main()























import os
import time
import json
import threading
import ctypes
import tkinter as tk
from tkinter import messagebox
import win32gui
import win32ui
from PIL import Image
import cv2
import pytesseract
import re
from datetime import datetime, timedelta
from tkinter import messagebox
from screen_capture.telegram_bot import send_telegram_alert

# OCR config
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

output_dir = "captures"
json_path = os.path.join(output_dir, "ocr_data.json")
os.makedirs(output_dir, exist_ok=True)

recording = False
recording_thread = None

def load_ocr_data():
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def clean_old_entries(data):
    now = datetime.now()
    cleaned_data = []
    for entry in data:
        try:
            entry_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            if now - entry_time <= timedelta(hours=24):
                cleaned_data.append(entry)
        except:
            continue
    return cleaned_data

def get_hwnd_by_title(title_contains):
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if title_contains.lower() in window_text.lower():
                result.append(hwnd)
    matches = []
    win32gui.EnumWindows(enum_handler, matches)
    return matches[0] if matches else None

def extract_text_and_rsi(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')
    rsi_match = re.search(r'RSI(?:\s*\w*)*[:\s\-]*?(\d{2}\.\d{2})', text, re.IGNORECASE)
    rsi_value = float(rsi_match.group(1)) if rsi_match else None
    return text, rsi_value

def capture_and_extract(hwnd, counter):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

    if result == 1:
        temp_path = os.path.join(output_dir, f"temp_{counter}.bmp")
        png_path = os.path.join(output_dir, f"temp_{counter}.png")
        save_bitmap.SaveBitmapFile(save_dc, temp_path)

        with Image.open(temp_path) as img:
            img.save(png_path)
        os.remove(temp_path)

        text, rsi = extract_text_and_rsi(png_path)
        os.remove(png_path)

        # 🚨 RSI Alert Popup
        if rsi is not None:
            log_dir = "alerts"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "alerts.log")
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if rsi < 30:
                msg = f"{now_str} 📉 RSI = {rsi} → Possible BUY"
                print(msg)
                send_telegram_alert(msg)
                messagebox.showwarning("📉 RSI Alert", msg)
            elif rsi > 70:
                msg = f"{now_str} 📈 RSI = {rsi} → Possible SELL"
                print(msg)
                send_telegram_alert(msg)
                messagebox.showwarning("📈 RSI Alert", msg)
            else:
                msg = f"{now_str} ℹ️ RSI = {rsi} (Normal)"
                print(msg)

            # Always log RSI status
            with open(log_file, "a", encoding="utf-8") as log:
                log.write(msg + "\n")

        else:
            print("❌ RSI not detected in this capture.")

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = load_ocr_data()
        data = clean_old_entries(data)
        data.append({
            "timestamp": now_str,
            "rsi": rsi,
            "text": text.strip()
        })

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[+] Captured & saved (RSI: {rsi}) ✅")
    else:
        print("❌ Failed to capture window.")

    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

def record_screen(title):
    global recording
    hwnd = get_hwnd_by_title(title)
    if not hwnd:
        print("❌ Window not found.")
        return

    counter = 0
    while recording:
        if not win32gui.IsIconic(hwnd):
            capture_and_extract(hwnd, counter)
            counter += 1
        else:
            print("⚠ Window is minimized. Skipping...")
        time.sleep(1)

def start_recording():
    global recording, recording_thread
    title = title_entry.get().strip()
    if not title:
        messagebox.showerror("Error", "Enter window title.")
        return
    if recording:
        return
    recording = True
    recording_thread = threading.Thread(target=record_screen, args=(title,), daemon=True)
    recording_thread.start()
    status_label.config(text="⏺ Recording...", fg="red")
    print(f"✅ Started recording: {title}")

def stop_recording():
    global recording
    recording = False
    status_label.config(text="⏹ Stopped", fg="green")
    print("🛑 Stopped.")

def gui_main():
    global title_entry, status_label
    root = tk.Tk()
    root.title("TradeShadow – Smart Capture")
    root.geometry("350x300")

    tk.Label(root, text="🔍 Enter Window Title:").pack(pady=10)
    title_entry = tk.Entry(root, width=40)
    title_entry.pack(pady=5)

    tk.Button(root, text="▶ Start Capturing", command=start_recording, width=30).pack(pady=10)
    tk.Button(root, text="⏹ Stop Capturing", command=stop_recording, width=30).pack(pady=5)

    status_label = tk.Label(root, text="Idle", fg="blue", font=("Arial", 12))
    status_label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    gui_main()

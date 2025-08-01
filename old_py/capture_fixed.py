# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image
# import mss
# import os
# import time
# import threading

# output_dir = "captures"
# os.makedirs(output_dir, exist_ok=True)

# recording = False
# capture_region = None
# recording_thread = None
# gui_root = None

# def select_region():
#     global capture_region

#     region_selector = tk.Tk()
#     region_selector.attributes('-fullscreen', True)
#     region_selector.attributes('-alpha', 0.3)
#     region_selector.config(bg='black')
#     region_selector.title("Select Region")

#     start_x = start_y = 0
#     rect_id = None

#     canvas = tk.Canvas(region_selector, cursor="cross", bg="gray")
#     canvas.pack(fill=tk.BOTH, expand=True)

#     def on_mouse_down(event):
#         nonlocal start_x, start_y, rect_id
#         start_x, start_y = event.x, event.y
#         rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

#     def on_mouse_drag(event):
#         nonlocal rect_id
#         canvas.coords(rect_id, start_x, start_y, event.x, event.y)

#     def on_mouse_up(event):
#         end_x, end_y = event.x, event.y
#         region_selector.destroy()

#         left = min(start_x, end_x)
#         top = min(start_y, end_y)
#         width = abs(end_x - start_x)
#         height = abs(end_y - start_y)

#         if width > 0 and height > 0:
#             global capture_region
#             capture_region = {"top": top, "left": left, "width": width, "height": height}
#         else:
#             messagebox.showerror("Error", "Invalid region selected.")

#     canvas.bind("<Button-1>", on_mouse_down)
#     canvas.bind("<B1-Motion>", on_mouse_drag)
#     canvas.bind("<ButtonRelease-1>", on_mouse_up)

#     region_selector.mainloop()

# def record_screen():
#     global recording, capture_region, gui_root
#     counter = 0

#     with mss.mss() as sct:
#         while recording and capture_region:
#             # Don't show the GUI on top of captured area
#             gui_root.withdraw()

#             # Take screenshot of selected region only (regardless of active window)
#             img = sct.grab(capture_region)
#             output = Image.frombytes("RGB", img.size, img.rgb)

#             filepath = os.path.join(output_dir, f"capture_{counter}.png")
#             output.save(filepath)
#             print(f"[+] Saved: {filepath}")
#             counter += 1

#             time.sleep(1)

#         gui_root.deiconify()

# def start_recording():
#     global recording, recording_thread, capture_region
#     if not capture_region:
#         messagebox.showerror("Error", "No region selected!")
#         return

#     recording = True
#     recording_thread = threading.Thread(target=record_screen, daemon=True)
#     recording_thread.start()
#     print("✅ Recording started...")

# def stop_recording():
#     global recording
#     recording = False
#     print("🛑 Recording stopped.")

# def main_gui():
#     global gui_root
#     gui_root = tk.Tk()
#     gui_root.title("TradeShadow - Region Recorder")
#     gui_root.geometry("300x200")
#     gui_root.resizable(False, False)

#     select_btn = tk.Button(gui_root, text="🎯 Select Region", command=select_region, width=25, height=2)
#     select_btn.pack(pady=10)

#     start_btn = tk.Button(gui_root, text="▶ Start Recording", command=start_recording, width=25, height=2)
#     start_btn.pack(pady=10)

#     stop_btn = tk.Button(gui_root, text="⏹ Stop Recording", command=stop_recording, width=25, height=2)
#     stop_btn.pack(pady=10)

#     gui_root.mainloop()

# if __name__ == "__main__":
#     main_gui()




import tkinter as tk
from tkinter import messagebox
import time
import os
import threading
import ctypes
import win32gui
import win32ui
import win32con
from PIL import Image

output_dir = "captures"
os.makedirs(output_dir, exist_ok=True)

recording = False
recording_thread = None

# 🔍 Find window by title
def get_hwnd_by_title(title_contains):
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if title_contains.lower() in window_text.lower():
                result.append(hwnd)

    matches = []
    win32gui.EnumWindows(enum_handler, matches)
    return matches[0] if matches else None

# 📸 Capture the background window using PrintWindow
def capture_window(hwnd, counter):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    # Use ctypes to call PrintWindow
    PW_RENDERFULLCONTENT = 0x00000002  # or 0x00000001 if needed
    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)

    if result == 1:
        bmp_path = os.path.join(output_dir, f"capture_{counter}.bmp")
        png_path = os.path.join(output_dir, f"capture_{counter}.png")
        save_bitmap.SaveBitmapFile(save_dc, bmp_path)

        # Convert BMP to PNG using Pillow
        with Image.open(bmp_path) as img:
            img.save(png_path)
        os.remove(bmp_path)  # remove BMP after conversion

        print(f"[+] Saved: {png_path}")
    else:
        print("❌ Failed to capture window.")

    # Clean up
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

# 🔁 Recording loop
def record_screen(window_title):
    global recording
    counter = 0
    hwnd = get_hwnd_by_title(window_title)

    if not hwnd:
        print("❌ Target window not found.")
        return

    while recording:
        if win32gui.IsIconic(hwnd):
            print("⚠ Window is minimized. Skipping frame.")
        else:
            capture_window(hwnd, counter)
            counter += 1
        time.sleep(0.5)

# ▶ Start button handler
def start_recording():
    global recording, recording_thread
    window_title = title_entry.get().strip()

    if not window_title:
        messagebox.showerror("Error", "❗ Enter a window title.")
        return

    hwnd = get_hwnd_by_title(window_title)
    if not hwnd:
        messagebox.showerror("Error", "❌ Window not found.")
        return

    if recording:
        messagebox.showinfo("Info", "Recording already in progress.")
        return

    recording = True
    recording_thread = threading.Thread(target=record_screen, args=(window_title,), daemon=True)
    recording_thread.start()
    status_label.config(text="⏺ Recording...", fg="red")
    print(f"✅ Recording started for window: '{window_title}'")

# ⏹ Stop button handler
def stop_recording():
    global recording
    if not recording:
        messagebox.showinfo("Info", "Recording is not running.")
        return

    recording = False
    status_label.config(text="⏹ Stopped", fg="green")
    print("🛑 Recording stopped.")

# 🖼 GUI setup
def main_gui():
    global status_label, title_entry

    root = tk.Tk()
    root.title("📸 Background Window Recorder")
    root.geometry("340x300")

    tk.Label(root, text="🔍 Window Title:").pack(pady=(20, 0))

    title_entry = tk.Entry(root, width=40)
    title_entry.pack(pady=5)

    tk.Button(root, text="▶ Start Capturing", command=start_recording, width=30, height=2).pack(pady=10)
    tk.Button(root, text="⏹ Stop Capturing", command=stop_recording, width=30, height=2).pack(pady=10)

    status_label = tk.Label(root, text="Idle", fg="blue", font=("Helvetica", 12))
    status_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
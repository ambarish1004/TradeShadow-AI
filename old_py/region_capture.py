# import pyautogui
# import time
# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import messagebox
# from PIL import ImageGrab
# import os

# region = []

# # Select screen region function
# def select_region():
#     def on_mouse_down(event):
#         canvas.start_x = canvas.canvasx(event.x)
#         canvas.start_y = canvas.canvasy(event.y)
#         canvas.rect = canvas.create_rectangle(canvas.start_x, canvas.start_y, canvas.start_x, canvas.start_y, outline='red', width=2)

#     def on_mouse_drag(event):
#         curX = canvas.canvasx(event.x)
#         curY = canvas.canvasy(event.y)
#         canvas.coords(canvas.rect, canvas.start_x, canvas.start_y, curX, curY)

#     def on_mouse_up(event):
#         end_x = canvas.canvasx(event.x)
#         end_y = canvas.canvasy(event.y)

#         x1 = min(canvas.start_x, end_x)
#         y1 = min(canvas.start_y, end_y)
#         x2 = max(canvas.start_x, end_x)
#         y2 = max(canvas.start_y, end_y)

#         region.append((int(x1), int(y1), int(x2 - x1), int(y2 - y1)))
#         root.quit()

#     root = tk.Tk()
#     root.attributes('-fullscreen', True)
#     root.attributes('-alpha', 0.3)
#     root.configure(background='black')
#     root.title("Select Region")

#     canvas = tk.Canvas(root, cursor="cross", bg='black')
#     canvas.pack(fill=tk.BOTH, expand=True)

#     canvas.bind("<ButtonPress-1>", on_mouse_down)
#     canvas.bind("<B1-Motion>", on_mouse_drag)
#     canvas.bind("<ButtonRelease-1>", on_mouse_up)

#     root.mainloop()
#     root.destroy()

# # Show option popup (navigate or record)
# def show_start_options():
#     def start_recording_now():
#         app.destroy()
#         start_capture()

#     def navigate_then_record():
#         app.destroy()
#         notify_navigation_then_capture()

#     app = tk.Tk()
#     app.title("Choose Action")
#     app.geometry("300x150")
#     app.attributes("-topmost", True)

#     tk.Label(app, text="What do you want to do?", font=("Arial", 12)).pack(pady=10)
#     tk.Button(app, text="🧭 Navigate First", command=navigate_then_record, width=20, height=2).pack(pady=5)
#     tk.Button(app, text="🎬 Start Recording", command=start_recording_now, width=20, height=2).pack(pady=5)

#     app.mainloop()

# # Wait until user presses a button to start capture
# def notify_navigation_then_capture():
#     notify = tk.Tk()
#     notify.title("Navigate and Start")
#     notify.geometry("300x100")
#     notify.attributes("-topmost", True)

#     tk.Label(notify, text="Navigate to desired screen,\nthen click below to start recording", font=("Arial", 10)).pack(pady=10)
#     tk.Button(notify, text="✅ Start Recording", command=notify.destroy).pack(pady=5)

#     notify.mainloop()
#     start_capture()

# # Capture screen every 5s
# def start_capture():
#     if not region or region[0][2] == 0 or region[0][3] == 0:
#         print("❌ Invalid region selected. Please select a proper area.")
#         return

#     print(f"✅ Region selected: {region[0]}")
#     print("📸 Starting capture every 5 seconds. Press Ctrl+C to stop.")

#     if not os.path.exists("screen_capture"):
#         os.makedirs("screen_capture")

#     i = 0
#     try:
#         while True:
#             x, y, w, h = region[0]
#             img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
#             img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#             filename = f'screen_capture/capture_{i}.png'
#             cv2.imwrite(filename, img_np)
#             print(f"🖼️ Captured: {filename}")
#             i += 1
#             time.sleep(5)
#     except KeyboardInterrupt:
#         print("⛔ Stopped capturing.")

# # --- Run Script ---
# select_region()
# show_start_options()





























# import cv2
# import numpy as np
# import time
# import os
# import tkinter as tk
# from tkinter import messagebox
# import win32gui
# import win32ui
# import win32con
# import win32api

# region = []
# target_hwnd = None

# def select_region():
#     def on_mouse_down(event):
#         canvas.start_x = canvas.canvasx(event.x)
#         canvas.start_y = canvas.canvasy(event.y)
#         canvas.rect = canvas.create_rectangle(canvas.start_x, canvas.start_y, canvas.start_x, canvas.start_y, outline='red', width=2)

#     def on_mouse_drag(event):
#         curX = canvas.canvasx(event.x)
#         curY = canvas.canvasy(event.y)
#         canvas.coords(canvas.rect, canvas.start_x, canvas.start_y, curX, curY)

#     def on_mouse_up(event):
#         end_x = canvas.canvasx(event.x)
#         end_y = canvas.canvasy(event.y)

#         x1 = min(canvas.start_x, end_x)
#         y1 = min(canvas.start_y, end_y)
#         x2 = max(canvas.start_x, end_x)
#         y2 = max(canvas.start_y, end_y)

#         region.append((int(x1), int(y1), int(x2 - x1), int(y2 - y1)))
#         root.quit()

#     root = tk.Tk()
#     root.attributes('-fullscreen', True)
#     root.attributes('-alpha', 0.3)
#     root.configure(background='black')
#     root.title("Select Region")

#     canvas = tk.Canvas(root, cursor="cross", bg='black')
#     canvas.pack(fill=tk.BOTH, expand=True)

#     canvas.bind("<ButtonPress-1>", on_mouse_down)
#     canvas.bind("<B1-Motion>", on_mouse_drag)
#     canvas.bind("<ButtonRelease-1>", on_mouse_up)

#     root.mainloop()
#     root.destroy()

# def get_window_at_click():
#     print("🖱️ Click on the window you want to monitor...")
#     time.sleep(1)
#     messagebox.showinfo("Select Window", "Click OK, then click on the target window")
#     time.sleep(0.5)
#     x, y = win32api.GetCursorPos()
#     hwnd = win32gui.WindowFromPoint((x, y))
#     win_name = win32gui.GetWindowText(hwnd)
#     print(f"✅ Window selected: {win_name} ({hwnd})")
#     return hwnd

# def show_start_options():
#     def start_recording_now():
#         app.destroy()
#         start_capture()

#     def navigate_then_record():
#         app.destroy()
#         notify_navigation_then_capture()

#     app = tk.Tk()
#     app.title("Choose Action")
#     app.geometry("300x150")
#     app.attributes("-topmost", True)

#     tk.Label(app, text="What do you want to do?", font=("Arial", 12)).pack(pady=10)
#     tk.Button(app, text="🧭 Navigate First", command=navigate_then_record, width=20, height=2).pack(pady=5)
#     tk.Button(app, text="🎬 Start Recording", command=start_recording_now, width=20, height=2).pack(pady=5)

#     app.mainloop()

# def notify_navigation_then_capture():
#     notify = tk.Tk()
#     notify.title("Navigate and Start")
#     notify.geometry("300x100")
#     notify.attributes("-topmost", True)

#     tk.Label(notify, text="Navigate to desired screen,\nthen click below to start recording", font=("Arial", 10)).pack(pady=10)
#     tk.Button(notify, text="✅ Start Recording", command=notify.destroy).pack(pady=5)

#     notify.mainloop()
#     start_capture()

# def start_capture():
#     if not region or region[0][2] == 0 or region[0][3] == 0 or target_hwnd is None:
#         print("❌ Invalid setup. Region or window not selected.")
#         return

#     print(f"🎯 Target HWND: {target_hwnd}, Region: {region[0]}")
#     print("📸 Capturing every 5 seconds. Press Ctrl+C to stop.")

#     if not os.path.exists("screen_capture"):
#         os.makedirs("screen_capture")

#     i = 0
#     try:
#         while True:
#             window_dc = win32gui.GetWindowDC(target_hwnd)
#             dc_obj = win32ui.CreateDCFromHandle(window_dc)
#             mem_dc = dc_obj.CreateCompatibleDC()

#             x, y, w, h = region[0]

#             bmp = win32ui.CreateBitmap()
#             bmp.CreateCompatibleBitmap(dc_obj, w, h)
#             mem_dc.SelectObject(bmp)
#             mem_dc.BitBlt((0, 0), (w, h), dc_obj, (x, y), win32con.SRCCOPY)

#             bmp_info = bmp.GetInfo()
#             bmp_str = bmp.GetBitmapBits(True)
#             img = np.frombuffer(bmp_str, dtype='uint8')
#             img.shape = (h, w, 4)

#             img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
#             filename = f"screen_capture/capture_{i}.png"
#             cv2.imwrite(filename, img)
#             print(f"🖼️ Captured: {filename}")

#             dc_obj.DeleteDC()
#             mem_dc.DeleteDC()
#             win32gui.ReleaseDC(target_hwnd, window_dc)
#             win32gui.DeleteObject(bmp.GetHandle())

#             i += 1
#             time.sleep(5)

#     except KeyboardInterrupt:
#         print("⛔ Stopped capturing.")

# # --- Run the Program ---
# select_region()
# target_hwnd = get_window_at_click()
# show_start_options()





















# import pyautogui
# import time
# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import messagebox
# from PIL import ImageGrab
# import os

# region = []

# # Select screen region function (fullscreen overlay)
# def select_region():
#     def on_mouse_down(event):
#         canvas.start_x = canvas.canvasx(event.x)
#         canvas.start_y = canvas.canvasy(event.y)
#         canvas.rect = canvas.create_rectangle(canvas.start_x, canvas.start_y, canvas.start_x, canvas.start_y, outline='red', width=2)

#     def on_mouse_drag(event):
#         curX = canvas.canvasx(event.x)
#         curY = canvas.canvasy(event.y)
#         canvas.coords(canvas.rect, canvas.start_x, canvas.start_y, curX, curY)

#     def on_mouse_up(event):
#         end_x = canvas.canvasx(event.x)
#         end_y = canvas.canvasy(event.y)

#         x1 = min(canvas.start_x, end_x)
#         y1 = min(canvas.start_y, end_y)
#         x2 = max(canvas.start_x, end_x)
#         y2 = max(canvas.start_y, end_y)

#         region.append((int(x1), int(y1), int(x2 - x1), int(y2 - y1)))
#         root.quit()

#     root = tk.Tk()
#     root.attributes('-fullscreen', True)
#     root.attributes('-alpha', 0.3)
#     root.configure(background='black')
#     root.title("Select Region")

#     canvas = tk.Canvas(root, cursor="cross", bg='black')
#     canvas.pack(fill=tk.BOTH, expand=True)

#     canvas.bind("<ButtonPress-1>", on_mouse_down)
#     canvas.bind("<B1-Motion>", on_mouse_drag)
#     canvas.bind("<ButtonRelease-1>", on_mouse_up)

#     root.mainloop()
#     root.destroy()

# # Show option popup (navigate or record)
# def show_start_options():
#     def start_recording_now():
#         app.destroy()
#         start_capture()

#     def navigate_then_record():
#         app.destroy()
#         notify_navigation_then_capture()

#     app = tk.Tk()
#     app.title("Choose Action")
#     app.geometry("300x150")
#     app.attributes("-topmost", True)

#     tk.Label(app, text="What do you want to do?", font=("Arial", 12)).pack(pady=10)
#     tk.Button(app, text="🧭 Navigate First", command=navigate_then_record, width=20, height=2).pack(pady=5)
#     tk.Button(app, text="🎬 Start Recording", command=start_recording_now, width=20, height=2).pack(pady=5)

#     app.mainloop()

# # Wait until user presses a button to start capture (after navigation)
# def notify_navigation_then_capture():
#     notify = tk.Tk()
#     notify.title("Navigate and Start")
#     notify.geometry("300x100")
#     notify.attributes("-topmost", True)

#     tk.Label(notify, text="Navigate to desired screen,\nthen click below to start recording", font=("Arial", 10)).pack(pady=10)
#     tk.Button(notify, text="✅ Start Recording", command=notify.destroy).pack(pady=5)

#     notify.mainloop()
#     start_capture()

# # Start the screen capturing (after region is selected)
# def start_capture():
#     region.clear()  # clear previous region if any
#     select_region()  # ask for region only now

#     if not region or region[0][2] == 0 or region[0][3] == 0:
#         print("❌ Invalid region selected. Please select a proper area.")
#         return

#     print(f"✅ Region selected: {region[0]}")
#     print("📸 Starting capture every 5 seconds. Press Ctrl+C to stop.")

#     if not os.path.exists("screen_capture"):
#         os.makedirs("screen_capture")

#     i = 0
#     try:
#         while True:
#             x, y, w, h = region[0]
#             img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
#             img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#             filename = f'screen_capture/capture_{i}.png'
#             cv2.imwrite(filename, img_np)
#             print(f"🖼️ Captured: {filename}")
#             i += 1
#             time.sleep(5)
#     except KeyboardInterrupt:
#         print("⛔ Stopped capturing.")

# # --- Entry Point ---
# show_start_options()




# import tkinter as tk
# from tkinter import simpledialog, messagebox
# import win32gui
# import win32ui
# import win32con
# import ctypes
# import os
# from PIL import Image
# import time

# output_dir = "screen_capture"
# os.makedirs(output_dir, exist_ok=True)

# capture_region = None
# target_hwnd = None

# def list_windows():
#     windows = []

#     def enum_window_callback(hwnd, _):
#         if win32gui.IsWindowVisible(hwnd):
#             title = win32gui.GetWindowText(hwnd)
#             if title:
#                 windows.append((title, hwnd))

#     win32gui.EnumWindows(enum_window_callback, None)
#     return windows

# def select_region_overlay():
#     root = tk.Tk()
#     root.attributes("-fullscreen", True)
#     root.attributes("-alpha", 0.3)
#     root.configure(bg='black')
#     root.title("Drag to select region")

#     selection = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
#     canvas = tk.Canvas(root, cursor="cross", bg='black')
#     canvas.pack(fill=tk.BOTH, expand=True)

#     rect = None

#     def on_mouse_down(event):
#         selection['x1'] = root.winfo_pointerx()
#         selection['y1'] = root.winfo_pointery()

#     def on_mouse_drag(event):
#         nonlocal rect
#         x2 = root.winfo_pointerx()
#         y2 = root.winfo_pointery()
#         canvas.delete("selection")
#         rect = canvas.create_rectangle(
#             selection['x1'], selection['y1'], x2, y2, outline='red', width=2, tags="selection")

#     def on_mouse_up(event):
#         selection['x2'] = root.winfo_pointerx()
#         selection['y2'] = root.winfo_pointery()
#         root.destroy()

#     canvas.bind("<Button-1>", on_mouse_down)
#     canvas.bind("<B1-Motion>", on_mouse_drag)
#     canvas.bind("<ButtonRelease-1>", on_mouse_up)

#     root.mainloop()

#     x1, y1 = selection['x1'], selection['y1']
#     x2, y2 = selection['x2'], selection['y2']
#     x, y = min(x1, x2), min(y1, y2)
#     w, h = abs(x2 - x1), abs(y2 - y1)
#     return (x, y, w, h)

# def focus_window(hwnd):
#     ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_RESTORE)
#     ctypes.windll.user32.SetForegroundWindow(hwnd)

# def capture_visible_window_region(hwnd, region, count):
#     left, top, width, height = region

#     # Get the window DC (only works if part of window is visible on screen)
#     hwndDC = win32gui.GetWindowDC(hwnd)
#     mfcDC = win32ui.CreateDCFromHandle(hwndDC)
#     saveDC = mfcDC.CreateCompatibleDC()
#     saveBitMap = win32ui.CreateBitmap()
#     saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
#     saveDC.SelectObject(saveBitMap)

#     # Copy from screen buffer using BitBlt
#     saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)

#     bmpinfo = saveBitMap.GetInfo()
#     bmpstr = saveBitMap.GetBitmapBits(True)

#     img = Image.frombuffer(
#         'RGB',
#         (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
#         bmpstr, 'raw', 'BGRX', 0, 1)

#     # Save as PNG
#     save_path = os.path.join(output_dir, f"capture_{count}.png")
#     img.save(save_path)

#     # Clean up
#     win32gui.DeleteObject(saveBitMap.GetHandle())
#     saveDC.DeleteDC()
#     mfcDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwndDC)

#     print(f"✅ Captured: {save_path}")

# def main():
#     global target_hwnd, capture_region

#     windows = list_windows()
#     if not windows:
#         messagebox.showerror("Error", "No windows found.")
#         return

#     titles = [title for title, _ in windows]
#     selected = simpledialog.askstring("Select Window", "Enter window name:\n\n" + "\n".join(titles))

#     match = next(((title, hwnd) for title, hwnd in windows if title == selected), None)
#     if not match:
#         messagebox.showerror("Error", "Window not found.")
#         return

#     target_title, target_hwnd = match
#     print(f"✅ Selected: {target_title}")

#     focus_window(target_hwnd)
#     time.sleep(1.5)

#     print("🖱️  Please select region to capture...")
#     capture_region = select_region_overlay()
#     print(f"✅ Region selected: {capture_region}")

#     count = 0
#     print("📸 Starting capture every 5 seconds. Press Ctrl+C to stop.")
#     try:
#         while True:
#             capture_visible_window_region(target_hwnd, capture_region, count)
#             count += 1
#             time.sleep(5)
#     except KeyboardInterrupt:
#         print("🛑 Stopped.")

# if __name__ == "__main__":
#     main()
# # tujhe yaaron mein kya bhai mile - YouTube - Brave













import tkinter as tk
from tkinter import messagebox
from PIL import Image
import mss
import os
import time
import threading

output_dir = "captures"
os.makedirs(output_dir, exist_ok=True)

recording = False
capture_region = None
recording_thread = None
gui_root = None

def select_region():
    global capture_region

    region_selector = tk.Tk()
    region_selector.attributes('-fullscreen', True)
    region_selector.attributes('-alpha', 0.3)
    region_selector.config(bg='black')
    region_selector.title("Select Region")

    start_x = start_y = 0
    rect_id = None

    canvas = tk.Canvas(region_selector, cursor="cross", bg="gray")
    canvas.pack(fill=tk.BOTH, expand=True)

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

    def on_mouse_drag(event):
        nonlocal rect_id
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        end_x, end_y = event.x, event.y
        region_selector.destroy()

        left = min(start_x, end_x)
        top = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)

        # mss expects (left, top, width, height)
        if width > 0 and height > 0:
            global capture_region
            capture_region = {"top": top, "left": left, "width": width, "height": height}
        else:
            messagebox.showerror("Error", "Invalid region selected.")

    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    region_selector.mainloop()

def record_screen():
    global recording, capture_region, gui_root
    counter = 0

    with mss.mss() as sct:
        while recording and capture_region:
            gui_root.withdraw()
            time.sleep(0.2)

            img = sct.grab(capture_region)
            output = Image.frombytes("RGB", img.size, img.rgb)

            filepath = os.path.join(output_dir, f"capture_{counter}.png")
            output.save(filepath)
            print(f"[+] Saved: {filepath}")
            counter += 1

            gui_root.deiconify()
            time.sleep(1)

def start_recording():
    global recording, recording_thread, capture_region
    if not capture_region:
        messagebox.showerror("Error", "No region selected!")
        return

    recording = True
    recording_thread = threading.Thread(target=record_screen)
    recording_thread.start()
    print("✅ Recording started...")

def stop_recording():
    global recording, recording_thread
    recording = False
    if recording_thread:
        recording_thread.join()
    print("🛑 Recording stopped.")

def main_gui():
    global gui_root
    gui_root = tk.Tk()
    gui_root.title("Region Screen Recorder")

    select_btn = tk.Button(gui_root, text="🎯 Select Region", command=select_region, width=30, height=2)
    select_btn.pack(pady=10)

    start_btn = tk.Button(gui_root, text="▶ Start Recording", command=start_recording, width=30, height=2)
    start_btn.pack(pady=10)

    stop_btn = tk.Button(gui_root, text="⏹ Stop Recording", command=stop_recording, width=30, height=2)
    stop_btn.pack(pady=10)

    gui_root.mainloop()

if __name__ == "__main__":
    main_gui()

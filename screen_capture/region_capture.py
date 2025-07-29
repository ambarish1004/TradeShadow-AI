import pyautogui
import time
import cv2
import numpy as np
import tkinter as tk
from PIL import ImageGrab

region = []

def select_region():
    def on_mouse_down(event):
        canvas.start_x = canvas.canvasx(event.x)
        canvas.start_y = canvas.canvasy(event.y)
        canvas.rect = canvas.create_rectangle(canvas.start_x, canvas.start_y, canvas.start_x, canvas.start_y, outline='red', width=2)

    def on_mouse_drag(event):
        curX = canvas.canvasx(event.x)
        curY = canvas.canvasy(event.y)
        canvas.coords(canvas.rect, canvas.start_x, canvas.start_y, curX, curY)

    def on_mouse_up(event):
        end_x = canvas.canvasx(event.x)
        end_y = canvas.canvasy(event.y)

        x1 = min(canvas.start_x, end_x)
        y1 = min(canvas.start_y, end_y)
        x2 = max(canvas.start_x, end_x)
        y2 = max(canvas.start_y, end_y)

        region.append((int(x1), int(y1), int(x2 - x1), int(y2 - y1)))
        root.quit()

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.configure(background='black')
    root.title("Select Region")

    canvas = tk.Canvas(root, cursor="cross", bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    root.destroy()

select_region()

if not region or region[0][2] == 0 or region[0][3] == 0:
    print("❌ Invalid region selected. Please select a proper area.")
    exit()

print(f"✅ Region selected: {region[0]}")
print("📸 Starting capture every 5 seconds. Press Ctrl+C to stop.")

i = 0
try:
    while True:
        x, y, w, h = region[0]
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))  # Uses PIL directly
        img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        filename = f'screen_capture/capture_{i}.png'
        cv2.imwrite(filename, img_np)
        print(f"🖼️ Captured: {filename}")
        i += 1
        time.sleep(5)
except KeyboardInterrupt:
    print("⛔ Stopped capturing.")

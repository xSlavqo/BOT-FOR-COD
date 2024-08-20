import pyautogui
import pytesseract
from PIL import Image, ImageTk  # Dodaj import ImageTk
import tkinter as tk

def on_click(event):
    x, y = event.x, event.y
    root.destroy()
    left = x - 100
    top = y - 100
    right = x + 100
    bottom = y + 100
    cropped_image = screenshot.crop((left, top, right, bottom))
    text = pytesseract.image_to_string(cropped_image)
    print(text)

screenshot = pyautogui.screenshot()

root = tk.Tk()
root.title("Kliknij na punkt")
root.geometry(f"{screenshot.width}x{screenshot.height}")

screenshot_tk = ImageTk.PhotoImage(screenshot)  # Poprawiona linia

canvas = tk.Canvas(root, width=screenshot.width, height=screenshot.height)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=screenshot_tk)

canvas.bind("<Button-1>", on_click)

root.mainloop()

import cv2
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

regions = []
drawing = False
ix, iy = -1, -1

def on_mouse_press(event):
    global ix, iy, drawing
    if event.inaxes:
        drawing = True
        ix, iy = int(event.xdata), int(event.ydata)

def on_mouse_release(event):
    global ix, iy, drawing, regions, ax, img
    if event.inaxes and drawing:
        x, y = int(event.xdata), int(event.ydata)
        width, height = x - ix, y - iy
        regions.append((ix, iy, width, height))
        rect = Rectangle((ix, iy), width, height, linewidth=2, edgecolor='g', facecolor='none')
        ax.add_patch(rect)
        fig.canvas.draw()
        drawing = False

def capture_screenshot_and_define_regions():
    global img, ax, fig
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    img = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots()
    ax.imshow(img)
    fig.canvas.mpl_connect('button_press_event', on_mouse_press)
    fig.canvas.mpl_connect('button_release_event', on_mouse_release)
    plt.show()

    return regions

if __name__ == "__main__":
    import time
    time.sleep(2)
    selected_regions = capture_screenshot_and_define_regions()
    print(f'Zaznaczone regiony: {selected_regions}')

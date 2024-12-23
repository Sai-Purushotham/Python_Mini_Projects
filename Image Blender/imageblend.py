import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


def image1():  
    photo1 = askopenfilename()
    if photo1: 
        global img1
        img1 = cv2.imread(photo1)
        img1 = cv2.resize(img1, (500, 500))


def image2():  
    photo2 = askopenfilename()
    if photo2:  #
        global img2
        img2 = cv2.imread(photo2)
        img2 = cv2.resize(img2, (500, 500))


def proceed():  
    try:
        global img1, img2
        alpha = t.get(1.0, "end-1c")
        alpha = float(alpha)
        if 0 <= alpha <= 1:
            beta = 1 - alpha
            if 'img1' in globals() and 'img2' in globals():
                res = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
                cv2.imshow('Result', res)
                cv2.imwrite("Output.jpg", res)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                messagebox.showerror("Error", "Please select both images first.")
        else:  # when alpha is invalid
            messagebox.showerror("Error", "Invalid alpha value. It must be between 0 and 1.")
    except ValueError:
        messagebox.showerror("Error", "Alpha must be a valid number.")



window = tk.Tk()
window.title("Image Blending")
window.geometry('300x140')

label = tk.Label(window, text="Enter alpha (0 to 1)").grid(row=0, column=0)
label = tk.Label(window, text="Image 1").grid(row=1, column=0)
label = tk.Label(window, text="Image 2").grid(row=2, column=0)

t = tk.Text(window, height=1, width=5)
b1 = tk.Button(window, text='Choose Image 1', command=image1)
b2 = tk.Button(window, text='Choose Image 2', command=image2)
proceed_btn = tk.Button(window, text='Proceed', command=proceed)

t.grid(row=0, column=1)
b1.grid(row=1, column=1)
b2.grid(row=2, column=1)
proceed_btn.grid(row=3, column=1)

window.mainloop()

cv2.destroyAllWindows()

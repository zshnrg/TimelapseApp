# Screenshot timelapse app

import os
import customtkinter
import tkinter as tk
from tkinter import filedialog

def open_file():
    # open file dialog and get file path
    file_path = filedialog.askopenfilename()

    # do something with the file path
    print("Selected file:", file_path)

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady = 20, padx = 60, fill = "both", expand=True)

button = customtkinter.CTkButton(master=frame, text="Open File", command=open_file)
button.pack(pady = 10, padx = 20)

button = customtkinter.CTkButton(master=frame, text="Start")
button.pack(pady = 10, padx = 20)

root.mainloop()

import pyautogui
from time import sleep

# ss = pyautogui.screenshot()
# for i in range(10):
#     ss.save(f"C:\\Users\\ghosa\\Downloads\\test\\ss{i}.png")
#     sleep(3)
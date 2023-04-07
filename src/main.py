# Screenshot timelapse app

import customtkinter
import tkinter as tk
from tkinter import filedialog
import pyautogui
import time
import threading

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("700x350")
app.title("Screenshot Timelapse App")

targetdir = ""
startState = False
pauseButton = False

class Stopwatch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stopwatch_elapsed_time = 0
        self._stopwatch_running = False
        self._stopwatch_paused = False

    def run(self):
        self._stopwatch_running = True
        while self._stopwatch_running:
            if not self._stopwatch_paused:
                time.sleep(0.1)
                self._stopwatch_elapsed_time += 0.1
                print(self._stopwatch_elapsed_time)

    def stop(self):
        self._stopwatch_running = False

    def pause(self):
        self._stopwatch_paused = True

    def resume(self):
        self._stopwatch_paused = False

    def get_elapsed_time(self):
        return round(self._stopwatch_elapsed_time, 1)

def open_file_button():
    global targetdir
    # open file dialog and get file path
    targetdir = filedialog.askdirectory()

    targetdir_entry.delete(0, tk.END)
    targetdir_entry.insert(0, targetdir)

    # do something with the file path
    print("Selected file:", targetdir)

def open_file_entry():
    global targetdir
    targetdir = targetdir_entry.get()

def get_valid_interval():
    interval = interval_entry.get().split(" ")[0]
    try:
        int(interval)
    except ValueError:
        interval_entry.delete(0, tk.END)
        interval_entry.insert(0, str(1) + " sec")
        return 1

def increase_interval_entry():
    get_valid_interval()
    interval = interval_entry.get().split(" ")[0]
    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, str(int(interval) + 1) + " sec")

def decrease_interval_entry():
    get_valid_interval()
    interval = interval_entry.get().split(" ")[0]
    if int(interval) <= 1:
        return
    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, str(int(interval) - 1) + " sec")

stopwatch_thread = Stopwatch()

def start_button():
    global targetdir, startState, pauseButton, stopwatch_thread

    if not startState:
        stopwatch_thread = Stopwatch()
        stopwatch_thread.start()

    startState = True
    stop_button.configure(state=tk.NORMAL)
    if not pauseButton:
        print("Start button pressed")
        stopwatch_thread.resume()
        start_button.configure(text="Pause", fg_color="red", hover_color="#802000")
        pauseButton = True

    else:
        print("Pause button pressed")
        stopwatch_thread.pause()
        start_button.configure(text="Continue", fg_color="#3a7ebf", hover_color="#325882")
        pauseButton = False

def stop_button():
    global startState, pauseButton
    startState = False
    pauseButton = False
    stopwatch_thread.stop()
    stop_button.configure(state=tk.DISABLED)
    start_button.configure(text="Start", fg_color="#3a7ebf", hover_color="#325882")


def on_close():
    stopwatch_thread.stop()
    app.quit()

############################### Master frame ###############################

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady = 20, padx = 60, expand=True, fill="x")

########### Target directory frame ###########

dir_frame = customtkinter.CTkFrame(master=frame)
dir_frame.pack(fill="both", expand=True)

targetdir_entry = customtkinter.CTkEntry(master=dir_frame, placeholder_text="Target Directory")
targetdir_entry.pack(side="left", padx = 10, pady = 10, fill="x", expand=True)

fileexplorer_button = customtkinter.CTkButton(master=dir_frame, text="Open Folder", command=open_file_button)
fileexplorer_button.pack(side="right", padx = 10)

########## Time frame ##########

sec_frame = customtkinter.CTkFrame(master=frame)
sec_frame.pack(fill="x", expand=True)

# Time interval frame

interval_frame = customtkinter.CTkFrame(master=sec_frame, fg_color="transparent")
interval_frame.pack(side="left", padx = 5, pady = 5, fill="x")

interval_entry = customtkinter.CTkEntry(master=interval_frame, placeholder_text="Time Interval (seccond)", width=20)
interval_entry.pack(fill="x", padx = 5, pady = 5, expand=True)
interval_entry.insert(0, "5 sec")

decrease_button = customtkinter.CTkButton(master=interval_frame, text="-", command=decrease_interval_entry)
decrease_button.pack(side="left", padx = 5, fill="x", expand=True)

increase_button = customtkinter.CTkButton(master=interval_frame, text="+", command=increase_interval_entry)
increase_button.pack(side="right", padx = 5, fill="x", expand=True)

# Elapsed time frame

time_frame = customtkinter.CTkFrame(master=sec_frame)
time_frame.pack(side="left", padx = 10, pady = 10, fill="x", expand=True)

elapsed_time_label = customtkinter.CTkLabel(master=time_frame, text=f"Elapsed Time\t: {stopwatch_thread.get_elapsed_time()}")
elapsed_time_label.pack(padx = 10, anchor="w")

frame_label = customtkinter.CTkLabel(master=time_frame, text="Frame\t\t: 0")
frame_label.pack(padx = 10, anchor="w")

##################### Action frame #####################

action_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent")
action_frame.pack(fill="x", expand=True)

# Start button

start_button = customtkinter.CTkButton(master=action_frame, text="Start", command=start_button)
start_button.pack(side="left", pady = 10, padx = 5, fill="x", expand=True)

# Stop button

stop_button = customtkinter.CTkButton(master=action_frame, text="Stop", state=tk.DISABLED, command=stop_button)
stop_button.pack(side="right", pady = 10, padx = 5, fill="x", expand=True)

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()
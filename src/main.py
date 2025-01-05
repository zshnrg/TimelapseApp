# Screenshot timelapse app

import customtkinter
import tkinter as tk
from tkinter import filedialog
import pyautogui
import time
import threading
from videoProcessor import process_video

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("../data/theme.json")

app = customtkinter.CTk()
app.geometry("700x350")
app.title("Screenshot Timelapse App")

targetdir = ""
startState = False
pauseButton = False
interval = 1

############################### Fonts ###############################
font_regular = customtkinter.CTkFont(family="Roboto", size=12, weight="normal")
font_bold = customtkinter.CTkFont(family="Roboto", size=14, weight="bold")

class Stopwatch(threading.Thread):
    def __init__(self):
        global interval, app, targetdir
        threading.Thread.__init__(self)
        self._stopwatch_elapsed_time = 0
        self._stopwatch_running = False
        self._stopwatch_paused = False
        self._count = 0

    def run(self):
        self._stopwatch_running = True
        while self._stopwatch_running:
            if not self._stopwatch_paused:
                try:
                    time.sleep(1)
                    self._stopwatch_elapsed_time += 1
                    hour = int(self._stopwatch_elapsed_time / 3600)
                    minute = int((self._stopwatch_elapsed_time - hour * 3600) / 60)
                    second = int(self._stopwatch_elapsed_time - hour * 3600 - minute * 60)
                    elapsed_time_label.configure(text=f"Elapsed Time\t: {hour}:{minute:02d}:{second:02d}")
                    print(self._stopwatch_elapsed_time)

                    if self._stopwatch_elapsed_time % interval == 0:
                        pyautogui.screenshot(f"{targetdir}/screenshot-{self._count:08d}.png")
                        print(f"Screenshot taken at {self._stopwatch_elapsed_time} seconds")
                        self._count += 1
                        frame_label.configure(text=f"Frame\t\t: {self._count}")

                except Exception as e:
                    print(e)
                    self._stopwatch_running = False
        print("Stopwatch stopped")

    def stop(self, app):
        elapsed_time_label.configure(text=f"Elapsed Time\t: 0:00:00")
        frame_label.configure(text=f"Frame\t\t: 0")
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
        return int(interval)
    except ValueError:
        interval_entry.delete(0, tk.END)
        interval_entry.insert(0, str(5) + " sec")
        return 5

def increase_interval_entry():
    interval = get_valid_interval()
    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, str(int(interval) + 1) + " sec")

def decrease_interval_entry():
    interval = get_valid_interval()
    if int(interval) <= 1:
        return
    interval_entry.delete(0, tk.END)
    interval_entry.insert(0, str(int(interval) - 1) + " sec")

stopwatch_thread = Stopwatch()

def start_button():
    global targetdir, startState, pauseButton, stopwatch_thread, interval

    if targetdir == "":
        set_warning("Please select a target directory", "red")
        return

    set_warning("Program is running ...", "#459e5f")

    if not startState:
        stopwatch_thread = Stopwatch()
        stopwatch_thread.start()

    interval = get_valid_interval()

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
    stopwatch_thread.stop(app)
    stop_button.configure(state=tk.DISABLED)
    start_button.configure(text="Start", fg_color="#3a7ebf", hover_color="#325882", state=tk.DISABLED)

    set_warning("Processing timelapse frames into video ...", "#e69138")
    process_video(targetdir)
    set_warning("Video exported! Check your target directory", "#6aa84f")
    start_button.configure(state=tk.NORMAL)
    

def set_warning(str, color="transparent"):
    warning_label.configure(text=str)
    warning_frame.configure(fg_color=color)


############################### Master frame ###############################

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady = 20, padx = 60, expand=True, fill="x", side="top")

########### Target directory frame ###########

dir_frame = customtkinter.CTkFrame(master=frame)
dir_frame.pack(fill="both", expand=True)

targetdir_entry = customtkinter.CTkEntry(master=dir_frame, placeholder_text="Target Directory", font=font_regular)
targetdir_entry.pack(side="left", padx = 10, pady = 10, fill="x", expand=True)

fileexplorer_button = customtkinter.CTkButton(master=dir_frame, text="Open Folder", command=open_file_button, font=font_bold)
fileexplorer_button.pack(side="right", padx = 10)

########## Time frame ##########

sec_frame = customtkinter.CTkFrame(master=frame)
sec_frame.pack(fill="x", expand=True)

# Time interval frame

interval_frame = customtkinter.CTkFrame(master=sec_frame, fg_color="transparent")
interval_frame.pack(side="left", padx = 5, pady = 5, fill="x")

interval_entry = customtkinter.CTkEntry(master=interval_frame, placeholder_text="Time Interval (seccond)", width=20, font=font_regular)
interval_entry.pack(fill="x", padx = 5, pady = 5, expand=True)
interval_entry.insert(0, "5 sec")

decrease_button = customtkinter.CTkButton(master=interval_frame, text="-", command=decrease_interval_entry, font=font_bold)
decrease_button.pack(side="left", padx = 5, fill="x", expand=True)

increase_button = customtkinter.CTkButton(master=interval_frame, text="+", command=increase_interval_entry, font=font_bold)
increase_button.pack(side="right", padx = 5, fill="x", expand=True)

# Elapsed time frame

time_frame = customtkinter.CTkFrame(master=sec_frame)
time_frame.pack(side="left", padx = 10, pady = 10, fill="x", expand=True)

elapsed_time_label = customtkinter.CTkLabel(master=time_frame, text="Elapsed Time\t: 0:00:00", font=font_regular)
elapsed_time_label.pack(padx = 10, anchor="w")

frame_label = customtkinter.CTkLabel(master=time_frame, text="Frame\t\t: 0", font=font_regular)
frame_label.pack(padx = 10, anchor="w")

##################### Action frame #####################

action_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent")
action_frame.pack(fill="x", expand=True)

# Start button

start_button = customtkinter.CTkButton(master=action_frame, text="Start", command=start_button, font=font_bold)
start_button.pack(side="left", pady = 10, padx = 5, fill="x", expand=True)

# Stop button

stop_button = customtkinter.CTkButton(master=action_frame, text="Stop", state=tk.DISABLED, command=stop_button, font=font_bold)
stop_button.pack(side="right", pady = 10, padx = 5, fill="x", expand=True)

# WARNING
warning_frame = customtkinter.CTkFrame(master=app, fg_color="#07789b")
warning_frame.pack(fill="x", side="top", expand=True)
warning_label = customtkinter.CTkLabel(master=warning_frame, text="Don't forget to choose your destination folder", font=font_bold)
warning_label.pack(padx = 10, pady = 10, anchor="w")

app.mainloop()
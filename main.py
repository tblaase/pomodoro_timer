import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL

import sv_ttk
import darkdetect
import pywinstyles, sys
import platform
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
OS = platform.system().lower()
THEME = darkdetect.theme().lower()

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    reset_button.config(state=DISABLED)
    start_button.config(state=NORMAL)
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    start_button.config(state=DISABLED)
    reset_button.config(state=NORMAL)
    global reps
    reps +=1

    work_secs = WORK_MIN * 60
    short_break_secs = SHORT_BREAK_MIN * 60
    long_break_secs = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_secs)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_secs)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_secs)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps, timer
    # hours is not really needed here, but could easily be implemented
    #hours, remainder = divmod(int(count), 3600)
    minutes,seconds = divmod(int(count), 60)

    #display_time = ('0' + str(hours) + ':' if 10 > hours > 0 else (str(hours) + ':' if hours > 9 else ''))
    display_time = (f"0{minutes}:" if 10 > minutes >= 0 else f"{minutes}:")
    display_time += (f"0{seconds}" if 10 > seconds >= 0 else str(seconds))

    canvas.itemconfig(timer_text, text=display_time)
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
        print(timer)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✓"
        check_marks.config(text=marks)

# ---------------------------- SET THEME ------------------------------- #
def apply_theme_to_titlebar(root):
    if OS == 'windows':
        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            # Set the title bar color to the background color on Windows 11 for better appearance
            pywinstyles.change_header_color(root, "#1c1c1c" if THEME == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark" if THEME == "dark" else "normal")

            # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)
    elif OS =='linux':
        print("theme not implemented for Linux")
    else:
        print("theme not implemented for MacOS")

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = tk.Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
title_label.grid(column=1,row=0)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1,row=1)

start_button = ttk.Button(window, text="Start", command=start_timer)
start_button.grid(column=0, row=2)
reset_button = ttk.Button(window, text="Reset", command=reset_timer, state=DISABLED)
reset_button.grid(column=2, row=2)

check_marks = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME,20))
check_marks.grid(column=1, row=3)

apply_theme_to_titlebar(window)
sv_ttk.set_theme("light")

# global variables
reps = 0
timer = ""

window.mainloop()

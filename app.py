import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from tkcalendar import Calendar
import time
import datetime
import pytz


# Window Setup
window = tk.Tk()
window.title("Clock - Calendar App")
window.geometry("1000x600")
window.iconbitmap("icon.ico")
window.resizable(False, False)

# Frames
calendar_frame = ttk.Frame(window)
world_clock_frame = ttk.Frame(window)
clock_frame = ttk.Frame(window)
stopwatch_frame = ttk.Frame(window)
countdown_frame = ttk.Frame(window)
buttons_frame = ttk.Frame(window)
bottom_frame = ttk.Frame(window)

calendar_frame.place(x = 0, y = 0, relwidth = 0.5, relheight = 0.9)
world_clock_frame.place(relx = 0.5, y = 0, relwidth = 0.25, relheight = 0.9)
buttons_frame.place(relx = 0.75, y = 0, relwidth = 0.25, relheight = 0.225)
clock_frame.place(relx = 0.75, rely = 0.225, relwidth = 0.25, relheight = 0.225)
stopwatch_frame.place(relx = 0.75, rely = 0.45, relwidth = 0.25, relheight = 0.225)
countdown_frame.place(relx = 0.75, rely = 0.675, relwidth = 0.25, relheight = 0.225)
bottom_frame.place(x = 0, rely = 0.9, relwidth = 1, relheight = 0.1)

# calendar_frame
calendar = Calendar(calendar_frame, selectmode = 'day', year=datetime.datetime.now().year,
                    month = datetime.datetime.now().month, day = datetime.datetime.now().day)
calendar.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# world_clock_frame
cities = [
    ("Tokyo", "Asia/Tokyo"),
    ("Delhi", "Asia/Kolkata"),
    ("Shanghai", "Asia/Shanghai"),
    ("São Paulo", "America/Sao_Paulo"),
    ("Mexico City", "America/Mexico_City"),
    ("Cairo", "Africa/Cairo"),
    ("New York City", "America/New_York"),
    ("Buenos Aires", "America/Argentina/Buenos_Aires"),
    ("Istanbul", "Europe/Istanbul"),
    ("Los Angeles", "America/Los_Angeles"),
    ("Moscow", "Europe/Moscow"),
    ("Paris", "Europe/Paris"),
    ("Seoul", "Asia/Seoul"),
    ("London", "Europe/London"),
    ("Chicago", "America/Chicago"),
    ("Madrid", "Europe/Madrid"),
    ("Berlin", "Europe/Berlin"),
    ("Hong Kong", "Asia/Hong_Kong"),
]

city_labels = {}

# Function to update the time for each city
def update_world_clocks():
    for city, timezone in cities:
        tz = pytz.timezone(timezone)
        city_time = datetime.datetime.now(tz).strftime("%H:%M:%S")
        city_labels[city].config(text = f"{city}: {city_time}")
    
    world_clock_frame.after(1000, update_world_clocks)

for i, (city, timezone) in enumerate(cities):
    city_label = ttk.Label(world_clock_frame, text = f"{city}: ", font = ("Arial", 10))
    city_label.grid(row = i, column = 0, padx = 10, pady = 5, sticky = "w")
    city_labels[city] = city_label

update_world_clocks()

# buttons_frame
def show_help():
    showinfo("Help", "This is a clock and calendar application.\n\n"
                     "Features include:\n"
                     "- Calendar\n"
                     "- World Clock\n"
                     "- Your Local Clock\n"
                     "- Stopwatch\n"
                     "- Countdown Timer")

help_button = ttk.Button(buttons_frame, text = "Help", command = show_help)
exit_button = ttk.Button(buttons_frame, text = "Exit", command = window.destroy)

help_button.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.35)
exit_button.place(relx = 0.1, rely = 0.55, relwidth = 0.8, relheight = 0.35)

# clock_frame
def update_local_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_frame.after(1000, update_local_clock)

clock_label = ttk.Label(clock_frame, text = "", font = ("Arial", 40), anchor = "center")
clock_label.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.7)

local_time_label = ttk.Label(clock_frame, text = "Current Local Time", font = ("Arial", 12), anchor = "center")
local_time_label.place(relx = 0, rely = 0.7, relwidth = 1, relheight = 0.3)

update_local_clock()

# stopwatch_frame
is_running = False
start_time = 0.0
elapsed_time = 0.0

def update_stopwatch():
    if is_running:
        global elapsed_time
        current_time = time.time()
        elapsed_time = current_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        seconds, milliseconds = divmod(seconds, 1)
        milliseconds = int(milliseconds * 1000)
        
        stopwatch_label.config(text = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}")
        stopwatch_frame.after(10, update_stopwatch)

def start_stopwatch():
    global is_running, start_time
    if not is_running:
        is_running = True
        start_time = time.time() - elapsed_time
        update_stopwatch()

def stop_stopwatch():
    global is_running
    is_running = False

def reset_stopwatch():
    global is_running, elapsed_time
    is_running = False
    elapsed_time = 0.0
    stopwatch_label.config(text = "00:00:00.000")

stopwatch_label = ttk.Label(stopwatch_frame, text = "00:00:00.000", font = ("Arial", 30), anchor = "center")
stopwatch_label.place(x = 0, y = 0, relwidth = 1, relheight = 0.5)

start_button = ttk.Button(stopwatch_frame, text = "Start", command = start_stopwatch)
stop_button = ttk.Button(stopwatch_frame, text = "Stop", command = stop_stopwatch)
reset_button = ttk.Button(stopwatch_frame, text = "Reset", command = reset_stopwatch)

start_button.place(relx = 0.1, rely = 0.55, relwidth = 0.25, relheight = 0.3)
stop_button.place(relx = 0.4, rely = 0.55, relwidth = 0.25, relheight = 0.3)
reset_button.place(relx = 0.7, rely = 0.55, relwidth = 0.25, relheight = 0.3)

# countdown_frame
countdown_running = False
countdown_time_left = 0
update_interval = 1000

def update_countdown():
    global countdown_time_left
    if countdown_running and countdown_time_left > 0:
        countdown_time_left -= 1
        minutes, seconds = divmod(countdown_time_left, 60)
        hours, minutes = divmod(minutes, 60)
        
        countdown_label.config(text = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
        countdown_label.after(update_interval, update_countdown)
    elif countdown_time_left <= 0 and countdown_running:
        countdown_label.config(text = "Time's up!")
        stop_countdown()

def start_countdown():
    global countdown_running, countdown_time_left
    if not countdown_running:
        try:
            input_time = int(hours_var.get()) * 3600 + int(minutes_var.get()) * 60 + int(seconds_var.get())
            if input_time > 0:
                countdown_time_left = input_time
                countdown_running = True
                update_countdown()
            else:
                showerror("Invalid Input", "Please enter a positive time value.")
        except ValueError:
            showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")

def stop_countdown():
    global countdown_running
    countdown_running = False

def reset_countdown():
    global countdown_running, countdown_time_left
    countdown_running = False
    countdown_time_left = 0
    countdown_label.config(text = "00:00:00")
    hours_var.set("0")
    minutes_var.set("0")
    seconds_var.set("0")

countdown_label = ttk.Label(countdown_frame, text = "00:00:00", font = ("Arial", 30), anchor = "center")
countdown_label.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.4)

hours_var = tk.StringVar(value = "0")
minutes_var = tk.StringVar(value = "0")
seconds_var = tk.StringVar(value = "0")

hours_entry = ttk.Entry(countdown_frame, textvariable = hours_var, justify = "center", font = ("Arial", 12))
minutes_entry = ttk.Entry(countdown_frame, textvariable = minutes_var, justify = "center", font = ("Arial", 12))
seconds_entry = ttk.Entry(countdown_frame, textvariable = seconds_var, justify = "center", font = ("Arial", 12))

hours_entry.place(relx = 0.1, rely = 0.4, relwidth = 0.25, relheight = 0.15)
minutes_entry.place(relx = 0.35, rely = 0.4, relwidth = 0.25, relheight = 0.15)
seconds_entry.place(relx = 0.6, rely = 0.4, relwidth = 0.25, relheight = 0.15)

start_countdown_button = ttk.Button(countdown_frame, text = "Start", command = start_countdown)
stop_countdown_button = ttk.Button(countdown_frame, text = "Stop", command = stop_countdown)
reset_countdown_button = ttk.Button(countdown_frame, text = "Reset", command = reset_countdown)

start_countdown_button.place(relx = 0.1, rely = 0.6, relwidth = 0.25, relheight = 0.15)
stop_countdown_button.place(relx = 0.35, rely = 0.6, relwidth = 0.25, relheight = 0.15)
reset_countdown_button.place(relx = 0.6, rely = 0.6, relwidth = 0.25, relheight = 0.15)

# Bottom Frame
bottom_label = ttk.Label(bottom_frame, text = "A Paul Jimon Production\nArad, Romania\n2024", anchor = "center", justify = "center")
bottom_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)


# Run
if __name__ == "__main__":
    window.mainloop()
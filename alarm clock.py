import tkinter as tk
import datetime
import threading
import winsound

# Global variables
alarm_set = False
stop_alarm_flag = False

def set_alarm():
    global alarm_set
    alarm_time = alarm_entry.get()

    try:
        alarm_datetime = datetime.datetime.strptime(alarm_time, "%I:%M:%S %p")
        current_datetime = datetime.datetime.now().strftime("%I:%M:%S %p")
        current_datetime = datetime.datetime.strptime(current_datetime, "%I:%M:%S %p")

        time_diff = (alarm_datetime - current_datetime).total_seconds()

        if time_diff <= 0:
            time_diff += 86400

        root.after(int(time_diff * 1000), trigger_alarm)
        alarm_set = True
        message_label.config(text="Alarm set for {} and it is {} seconds from now".format(alarm_time,time_diff))
        
    except ValueError:
        message_label.config(text="Invalid time format!")

def trigger_alarm():
    global alarm_set
    if alarm_set:
        alarm_set = False
        stop_alarm_flag = False

        threading.Thread(target=play_beep_sound).start()

        alarm_win = tk.Toplevel(root)
        alarm_win.title("Wake Up!")
        alarm_win.geometry("400x300")

        wake_up_label = tk.Label(alarm_win, text="Time to Wake up!", font=("Arial", 24))
        wake_up_label.pack(pady=50)

        root.bind("<KeyPress>", lambda event: stop_alarm(event, alarm_win))

def play_beep_sound():
    while not stop_alarm_flag:
        winsound.Beep(1000, 500)

def stop_alarm(event, window):
    global stop_alarm_flag
    stop_alarm_flag = True
    window.destroy()

# Create the main GUI window
root = tk.Tk()
root.title("Alarm Clock")
root.geometry('400x250')
root.configure(bg='skyblue')

# Create GUI elements
alarm_label = tk.Label(root, text="Enter alarm time (HH:MM:SS AM/PM):")
alarm_label.pack(pady=10)

alarm_entry = tk.Entry(root)
alarm_entry.pack(pady=8)

set_alarm_button = tk.Button(root, text="Set Alarm", command=set_alarm)
set_alarm_button.pack(pady=8)

message_label = tk.Label(root, text="")
message_label.pack()

# Run the GUI event loop
root.mainloop()

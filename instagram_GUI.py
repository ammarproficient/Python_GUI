import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread, Event
import time
from bs4 import BeautifulSoup

def parse_html(html_file_path, stop_event):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        following_links = soup.find_all('a')
        following_names = [link.text for link in following_links]

        for index, name in enumerate(following_names, start=1):
            print(f"{index}. {name}")
            if stop_event.is_set():
                break
            time.sleep(0.1)  # Simulate work and make the loop responsive to stops

    except Exception as e:
        print(f"Error: {e}")

def start_parsing():
    global stop_event
    stop_event.clear()
    thread = Thread(target=parse_html, args=(file_path, stop_event,))
    thread.start()

def stop_parsing():
    global stop_event
    stop_event.set()

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html;*.htm")])
    if file_path:
        print(f"Selected file: {file_path}")

# Setup Tkinter window
root = tk.Tk()
root.title("HTML Parser")
root.geometry("300x150")

stop_event = Event()
file_path = ""  # Initialize file_path variable

# Open file button
open_button = ttk.Button(root, text="Open HTML File", command=open_file)
open_button.pack(pady=5)

# Start button
start_button = ttk.Button(root, text="Start", command=start_parsing)
start_button.pack(pady=5)

# Stop button
stop_button = ttk.Button(root, text="Stop", command=stop_parsing)
stop_button.pack(pady=5)

def on_closing():
    stop_parsing()  # Ensure parsing stops
    root.destroy()  # Destroy the window

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

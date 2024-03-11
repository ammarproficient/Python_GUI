import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from threading import Thread, Event
import time
from bs4 import BeautifulSoup


def parse_html(html_file_path, output_file_path, stop_event):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        following_links = soup.find_all('a')

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for index, link in enumerate(following_links, start=1):
                name = link.text.strip()
                url = link.get('href', '')
                output_file.write(f"{index}. Name: {name} | URL: {url}\n")

                print(f"{index}. Name: {name} | URL: {url}")
                if stop_event.is_set():
                    break
                time.sleep(0.1)  # Simulate work and make the loop responsive to stops

    except Exception as e:
        print(f"Error: {e}")


def start_parsing():
    global stop_event, file_path, output_file_path
    stop_event.clear()
    if not file_path or not output_file_path:
        messagebox.showinfo("Info", "Please select an HTML file and specify an output file.")
        return
    thread = Thread(target=parse_html, args=(file_path, output_file_path, stop_event,))
    thread.start()


def stop_parsing():
    global stop_event
    stop_event.set()


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html;*.htm")])
    if file_path:
        print(f"Selected file: {file_path}")


def save_file():
    global output_file_path
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if output_file_path:
        print(f"Output will be saved to: {output_file_path}")


# Setup Tkinter window
root = tk.Tk()
root.title("HTML Parser")
root.geometry("400x200")

stop_event = Event()
file_path = "D:/Python Projects/Python_GUI"  # Initialize file_path variable
output_file_path = "D:/Python Projects/Python_GUI"  # Initialize output_file_path variable

# Open file button
open_button = ttk.Button(root, text="Open HTML File", command=open_file)
open_button.pack(pady=5)

# Save file button
save_button = ttk.Button(root, text="Save Output As", command=save_file)
save_button.pack(pady=5)

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

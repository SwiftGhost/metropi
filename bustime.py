import tkinter as tk
from datetime import datetime, timedelta
import requests
import csv
import os

# Load route colors from CSV file
def load_route_colors(file_path="route_colors.csv"):
    route_colors = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                route_colors[row['Route']] = {
                    'circle_color': f"#{row['Circle Color']}",
                    'text_color': f"#{row['Text Color']}",
                }
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Ensure the file exists.")
    return route_colors

# Function to fetch bus data from the API
def get_bus_data():
    api_key = 'YOUR_API_KEY'
    stop_ids = 'YOUR_STOP_IDS
    url = f'http://metromap.cityofmadison.com/bustime/api/v3/getpredictions?key={api_key}&stpid={stop_ids}&format=json'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('bustime-response', {}).get('prd', [])
    except requests.RequestException as e:
        print(f"Error fetching bus data: {e}")
        return []

# Function to parse and format bus data
def parse_bus_data(data):
    now = datetime.now()
    buses = []
    cutoff_time = now + timedelta(minutes=45)  # Only consider buses arriving in the next 45 minutes
    for entry in data:
        prdtm = datetime.strptime(entry['prdtm'], "%Y%m%d %H:%M")
        if prdtm > cutoff_time:
            continue

        minutes_until = (prdtm - now).total_seconds() // 60
        minutes_until = int(minutes_until)
        if minutes_until <= 0:
            time_display = "DUE"
        else:
            time_display = f"{minutes_until} min"

        buses.append({
            'route': entry['rt'],
            'destination': entry['des'],
            'direction': entry['rtdir'],
            'time': time_display,
            'arrival_time': prdtm
        })

    # Sort buses by arrival time
    buses.sort(key=lambda x: x['arrival_time'])
    return buses

# Function to update the display
def update_display():
    global current_index
    bus_data = get_bus_data()
    parsed_data = parse_bus_data(bus_data)

    if not parsed_data:
        for widget in frame.winfo_children():
            widget.destroy()
        no_buses_label = tk.Label(frame, text="No buses available in the next 45 minutes.", font=('Helvetica', 32))
        no_buses_label.pack()
        time_display.config(text=f"Current Time: {datetime.now().strftime('%I:%M %p')}")
        return

    buses_to_display = parsed_data[current_index:current_index + 3]

    for widget in frame.winfo_children():
        widget.destroy()

    for i, bus in enumerate(buses_to_display):
        route = bus['route']
        colors = route_colors.get(route, {'circle_color': '#000000', 'text_color': '#FFFFFF'})
        
        # Create a canvas to draw the circle
        canvas = tk.Canvas(frame, width=100, height=100)
        canvas.grid(row=i, column=0, padx=10, pady=10)
        canvas.create_oval(10, 10, 90, 90, fill=colors['circle_color'])  # Draw a circle
        canvas.create_text(50, 50, text=route, font=('Helvetica', 36), fill=colors['text_color'])  # Add route letter

        destination_label = tk.Label(frame, text=f"{bus['destination']}\n({bus['direction']})", font=('Helvetica', 32))
        destination_label.grid(row=i, column=1, padx=10, pady=10)

        time_label = tk.Label(frame, text=bus['time'], font=('Helvetica', 48))
        time_label.grid(row=i, column=2, padx=10, pady=10, sticky='e')

    current_time = datetime.now().strftime("%I:%M %p")
    time_display.config(text=f"Current Time: {current_time}")

    # Cycle through buses in groups of 3
    if current_index + 3 < len(parsed_data):
        current_index += 3
    else:
        current_index = 0

    root.after(10000, update_display)  # Update every 10 seconds

# Load route colors
route_colors = load_route_colors("route_colors.csv")

# GUI setup
root = tk.Tk()
root.title("Bus Arrivals")
root.geometry("800x480")

frame = tk.Frame(root)
frame.pack()

time_display = tk.Label(root, font=('Helvetica', 24))
time_display.pack()

current_index = 0  # To track the current starting index for displayed buses
update_display()
root.mainloop()

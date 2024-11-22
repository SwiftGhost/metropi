import tkinter as tk
from datetime import datetime, timedelta
import requests
import csv
import json
import os

# Load settings
def load_settings(file_path="settings.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Please create it using the template.")
        exit(1)

# Load route colors from CSV
def load_route_colors(file_path="route_colors.csv"):
    route_colors = {}
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                route_colors[row["Route"]] = {
                    "circle_color": f"#{row['Circle Color']}",
                    "text_color": f"#{row['Text Color']}",
                }
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Ensure the file exists.")
    return route_colors

# Fetch bus data
def get_bus_data(api_key, stop_ids):
    url = f"http://metromap.cityofmadison.com/bustime/api/v3/getpredictions?key={api_key}&stpid={','.join(stop_ids)}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("bustime-response", {}).get("prd", [])
    except requests.RequestException as e:
        print(f"Error fetching bus data: {e}")
        return []

# Parse bus data
def parse_bus_data(data, timeframe_minutes, preferred_routes):
    now = datetime.now()
    buses = []
    cutoff_time = now + timedelta(minutes=timeframe_minutes)
    for entry in data:
        prdtm = datetime.strptime(entry["prdtm"], "%Y%m%d %H:%M")
        if prdtm > cutoff_time or (preferred_routes and entry["rt"] not in preferred_routes):
            continue

        minutes_until = int((prdtm - now).total_seconds() // 60)
        time_display = "DUE" if minutes_until <= 0 else f"{minutes_until} min"
        buses.append({
            "route": entry["rt"],
            "destination": entry["des"],
            "direction": entry["rtdir"],
            "time": time_display,
            "arrival_time": prdtm,
            "imminent": minutes_until <= settings["alerts"]["alert_threshold_minutes"]
        })

    buses.sort(key=lambda x: x["arrival_time"])
    return buses

# Save bus data to file
def export_bus_data(data, file_path):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["route", "destination", "direction", "time", "arrival_time"])
        writer.writeheader()
        writer.writerows(data)

# Update display
def update_display():
    global current_index
    bus_data = get_bus_data(settings["api_key"], settings["stop_ids"])
    parsed_data = parse_bus_data(bus_data, settings["timeframe_minutes"], settings["preferred_routes"])

    # Export data if enabled
    if settings["export_data"]["enabled"]:
        export_bus_data(parsed_data, settings["export_data"]["file_path"])

    if not parsed_data:
        for widget in frame.winfo_children():
            widget.destroy()
        tk.Label(frame, text="No buses available.", font=("Helvetica", settings["font_sizes"]["destination"])).pack()
        time_display.config(text=f"Current Time: {datetime.now().strftime('%I:%M %p')}")
        return

    buses_to_display = parsed_data[current_index:current_index + 3]

    for widget in frame.winfo_children():
        widget.destroy()

    for i, bus in enumerate(buses_to_display):
        route = bus["route"]
        colors = route_colors.get(route, {"circle_color": "#000000", "text_color": "#FFFFFF"})

        highlight_color = settings["alerts"]["alert_color"] if bus["imminent"] else colors["circle_color"]

        canvas = tk.Canvas(frame, width=100, height=100, bg=settings["theme"]["background_color"])
        canvas.grid(row=i, column=0, padx=10, pady=10)
        canvas.create_oval(10, 10, 90, 90, fill=highlight_color)
        canvas.create_text(50, 50, text=route, font=("Helvetica", settings["font_sizes"]["route"]), fill=colors["text_color"])

        tk.Label(frame, text=f"{bus['destination']} ({bus['direction']})", font=("Helvetica", settings["font_sizes"]["destination"])).grid(row=i, column=1, padx=10, pady=10)
        tk.Label(frame, text=bus["time"], font=("Helvetica", settings["font_sizes"]["time"])).grid(row=i, column=2, padx=10, pady=10, sticky="e")

    current_time = datetime.now().strftime("%I:%M %p")
    time_display.config(text=f"Current Time: {current_time}")

    if current_index + 3 < len(parsed_data):
        current_index += 3
    else:
        current_index = 0

    root.after(settings["refresh_interval_seconds"] * 1000, update_display)

# Load settings and colors
settings = load_settings("settings.json")
route_colors = load_route_colors("route_colors.csv")

# GUI setup
root = tk.Tk()
root.title("Bus Arrivals")
root.geometry("800x480")
root.configure(bg=settings["theme"]["background_color"])

frame = tk.Frame(root, bg=settings["theme"]["background_color"])
frame.pack()

time_display = tk.Label(root, font=("Helvetica", settings["font_sizes"]["current_time"]), bg=settings["theme"]["background_color"], fg=settings["theme"]["text_color"])
time_display.pack()

current_index = 0
update_display()
root.mainloop()

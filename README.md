# Bus Arrivals Display

This project is a Python-based GUI application that displays upcoming bus arrival times for specified bus stops using the Madison Metro Transit API. The program uses the `tkinter` library for the interface, cycles through buses arriving within the next 45 minutes, and includes customizable route colors.

---

## Features

- Displays the next bus arrival times for selected stops.
- Cycles through buses in groups of three every 10 seconds.
- Customizable route and text colors via a `route_colors.csv` file.
- Works with any stop IDs supported by the Madison Metro Transit API.

---

## Requirements

- Python 3.8 or later
- Internet connection (to fetch bus data from the API)
- Libraries: `requests`, `tkinter` (built-in), `csv` (built-in)

---

## Setup Instructions

### 1. Download the Repository
1. Click the **Code** button at the top of the repository page.
2. Select **Download ZIP**.
3. Extract the ZIP file to a folder of your choice.

### 2. Install Dependencies
Install the required library by running:
```python
pip install requests
```

### 3. Get an API Key
- Sign up for a Madison Metro Transit API key [here](https://metromap.cityofmadison.com/dev-account).
- Copy the key and replace `YOUR_API_KEY` in the script with your API key.

### 4. Find Your Stop IDs
To get your stop IDs:
1. Visit [Metro Bus Tracker](https://metromap.cityofmadison.com/predictions).
2. Either:
   - Click **Find Stops Near Me** to locate nearby stops, or
   - Select your route and direction, then find your stop.
3. The stop number will be displayed to the left of the stop name.

Replace `YOUR_STOP_IDS` in the script with a comma-separated list of your stop IDs (e.g., `0847,3572,8866`).

### 5. Configure Route Colors
The route colors are stored in a CSV file named `route_colors.csv`. You can modify this file to reflect the color scheme for your routes. Each row should have:

- `Route`: The route name or number.
- `Circle Color`: The color of the circle displayed for the route in hexadecimal format (e.g., `333366`).
- `Text Color`: The color of the text displayed on the circle in hexadecimal format (e.g., `FEFEFE`).

Ensure this file is in the same directory as the script.

---

## Running the Program

To run the application:
1. Open a terminal or command prompt.
2. Navigate to the folder containing the extracted files.
3. Run the script:
   ```python
   python bus_arrivals_display.py
   ```

The application will open a window displaying bus arrival times, cycling through buses arriving within the next 45 minutes.

---

## Files

1. **`bus_arrivals_display.py`**: The main Python script.
2. **`route_colors.csv`**: Customizable route colors for bus routes.
3. **`requirements.txt`**: Lists the required Python dependencies (only `requests`).

---

## Customization

- **Update Route Colors**: Modify `route_colors.csv` to adjust the circle and text colors for routes.
- **Adjust API Parameters**: Change the `stop_ids` or API URL in the script to use different stops or endpoints.
- **Change Refresh Rate**: Modify the `root.after(10000, update_display)` line to adjust the update interval (in milliseconds).

---

## Troubleshooting

- **Route Colors Not Showing Correctly**: Ensure `route_colors.csv` is properly formatted and located in the same directory as the script.
- **API Errors**: Check your API key and ensure it's valid.
- **No Data Displayed**: Confirm that the stop IDs are correct and buses are scheduled within the next 45 minutes.

---

## License

This project is open source and available under the MIT License. See the `LICENSE` file for details.

---

Feel free to fork the repository, report issues, or contribute! 😊

import io
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pyperclip
import requests
from PIL import Image, ImageTk

import creds

api_key = creds.key

Lightyellow = "#FFB754"
Feldgrau = "#586F6B"
Green = "#35CFF9"
Yellow = "#B2A0C4"

try:
    key = creds.key
except KeyError:
    messagebox.showerror("Key Error", " Error in the API Key ")

def save_city_list():
    with open('cities.txt', 'w') as file:
        for city in city_list:
            file.write(city + '\n')

def load_city_list():
    try:
        with open('cities.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

global city_list
city_list = load_city_list()

class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Forecast App")
        self.root.geometry('1000x800')
        self.root.config(bg=Lightyellow)

        self.weather_data = tk.StringVar()
        self.city_name = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.tooltip_window = None
        self.name_label = tk.Label(self.root, text="WEATHER FORECASTER", font=('8514oem', 48, 'bold'), bg=Lightyellow)
        self.name_label.place(x=150, y=50, height=50, width=600)

        self.city_label = tk.Label(self.root, text="Enter city:", font=('Terminal', 20, 'bold'), bg=Lightyellow, fg=Green)
        self.city_label.place(x=15, y=150, height=30, width=200)

        self.city_entry = tk.Entry(self.root, font=('Terminal', 20, 'bold'), bg=Feldgrau)

        self.city_entry.place(x=290, y=150, height=30, width=400)

        
        
        self.weather_button = tk.Button(self.root, text="Forecast", font=('Small Fonts', 20), bg=Green, fg=Lightyellow,
                                        command=self.get_weather_data)
        self.weather_button.place(x=350, y=200, height=40, width=200)
        self.weather_button.bind("<Enter>", lambda event, msg="Get the weather forecast for the entered city.": self.show_tooltip(event, msg))
        self.weather_button.bind("<Leave>", self.hide_tooltip)

        

       


        self.forecast_label = tk.Label(self.root, text='', font=('Fixedsys', 20), bg=Feldgrau, fg=Yellow)
        self.forecast_label.place(x=15, y=250, height=400, width=915)

        self.icon_label = None

        self.celsius_button = tk.Button(self.root, text="Celsius", font=('Small Fonts', 20), bg=Green,
                                        fg=Lightyellow, command=self.displayInCel)
        self.celsius_button.place(x=15, y=700, height=40, width=160)
        self.celsius_button.bind("<Enter>",
                                 lambda event, msg="Switch temperature display to Celsius (°C).": self.show_tooltip(
                                     event, msg))
        self.celsius_button.bind("<Leave>", self.hide_tooltip)

        self.fahrenheit_button = tk.Button(self.root, text="Fahrenheit", font=('Small Fonts', 20), bg=Green,
                                           fg=Lightyellow, command=self.displayInF)
        self.fahrenheit_button.place(x=390, y=700, height=40, width=160)
        self.fahrenheit_button.bind("<Enter>",
                                 lambda event, msg="Switch temperature display to Fahrenheit (°F).": self.show_tooltip(
                                     event, msg))
        self.fahrenheit_button.bind("<Leave>", self.hide_tooltip)


        



        self.clear_button = tk.Button(self.root, text="Clear", font=('Small Fonts', 20), bg=Green,
                                      fg=Lightyellow, command=self.clearAll)
        self.clear_button.place(x=740, y=700, height=40, width=160)
        self.clear_button.bind("<Enter>", lambda event, msg="Clear previous data": self.show_tooltip(event, msg))
        self.clear_button.bind("<Leave>", self.hide_tooltip)

    def display_weather_info(self, forecast_text, temperature, weather_description, wind_speed, humidity, icon_url):
        forecast_text += f"Temperature: {temperature}\n"
        forecast_text += f"Conditions: {weather_description}\n"
        forecast_text += f"Wind Speed: {wind_speed} m/s\n"
        forecast_text += f"Humidity: {humidity}%"

        icon_response = requests.get(icon_url)
        if icon_response.status_code == 200:
            icon_image = Image.open(io.BytesIO(icon_response.content))
            icon_image = ImageTk.PhotoImage(icon_image)
            if self.icon_label:
                self.icon_label.destroy()

            self.icon_label = tk.Label(self.root, image=icon_image, bg=Feldgrau)
            self.icon_label.image = icon_image
            self.icon_label.place(x=300, y=530)

        self.forecast_label.config(text=forecast_text)

    def get_weather_data(self):
        cityname = self.city_entry.get()

        try:
            weather_data = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + key).json()

            if 'message' in weather_data:
                error_message = weather_data['message']
                self.forecast_label.config(text=f"Error: {error_message}", fg='red')
            else:
                forecast_text = f"Weather for {self.city_entry.get()} in Kelvin :\n"
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                wind_speed = weather_data['wind']['speed']
                humidity = weather_data['main']['humidity']
                icon = weather_data['weather'][0]['icon']
                icon_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'

                self.display_weather_info(forecast_text, temperature, weather_description, wind_speed, humidity,
                                          icon_url)
                self.weather_data.set('')
                self.weather_data.set(self.weather_data.get() + forecast_text + f'Temperature - {temperature} Condition {weather_description} Wind Speed - {wind_speed} m/s Humidity - {humidity}%')




        except requests.exceptions.RequestException:
            messagebox.showerror("Network Error", "There was an issue connecting to the weather service. Please check your internet connection.")

    def displayInCel(self):
        cityname = self.city_entry.get()

        weather_data = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + key  + "&units=metric").json()

        if 'message' in weather_data:
            error_message = weather_data['message']
            self.forecast_label.config(text=f"Error: {error_message}", fg='red')
        else:
            forecast_text = f"Weather for {self.city_entry.get()} in °C :\n"
            temperature = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            humidity = weather_data['main']['humidity']
            icon = weather_data['weather'][0]['icon']
            icon_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'

            self.display_weather_info(forecast_text, temperature, weather_description, wind_speed, humidity,
                                      icon_url)

    def displayInF(self):
        cityname = self.city_entry.get()

        weather_data = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + key + "&units=imperial").json()

        if 'message' in weather_data:
            error_message = weather_data['message']
            self.forecast_label.config(text=f"Error: {error_message}", fg='red')
        else:
            forecast_text = f"Weather for {self.city_entry.get()} in °F :\n"
            temperature = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            humidity = weather_data['main']['humidity']
            icon = weather_data['weather'][0]['icon']
            icon_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'

            self.display_weather_info(forecast_text, temperature, weather_description, wind_speed, humidity,
                                      icon_url)
    def refreshData(self):
        self.get_weather_data()

    def clearAll(self):
        self.forecast_label.config(text='')
        self.city_entry.delete(0,tk.END)
        if self.icon_label:
            self.icon_label.destroy()

    def show_tooltip(self, event,msg):
        self.tooltip_window = tk.Toplevel(self.root)
        tooltip_label = tk.Label(self.tooltip_window,
                                 text=msg)
        tooltip_label.pack()
        self.tooltip_window.overrideredirect(True)
        x = self.root.winfo_pointerx() + 20
        y = self.root.winfo_pointery() + 20
        self.tooltip_window.geometry("+{}+{}".format(x, y))

    def hide_tooltip(self, event):
        # Destroy the tooltip window
        self.tooltip_window.destroy()
        self.tooltip_window = None

    def saveCity(self):

        city = self.city_entry.get()
        city_list.append(city)

        self.city_combo['values'] = city_list
        save_city_list()

    def loadCity(self):
        city = self.city_name.get()
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.get_weather_data()

    def clearSavedCities(self):
        global city_list  # Add this line to access the global city_list variable
        city_list = []  # Clear the list
        self.city_combo['values'] = city_list  # Update the Combobox values
        save_city_list()  # Save the updated city list to the file

    def copyData(self):
        # Get the forecast text from the forecast_text StringVar
        text = self.weather_data.get()
        pyperclip.copy(text)

    def detectCity(self):
        location_url='https://ipinfo.io/json'
        location_response = requests.get(location_url)
        data=location_response.json()
        cityname = data['city']
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, cityname)
        self.get_weather_data()




    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = WeatherApp()    
    app.run()

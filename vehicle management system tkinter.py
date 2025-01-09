import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class Vehicle:
    def __init__(self, vehicle_id, make, model, year, color):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    def __str__(self):
        return f"ID: {self.vehicle_id}, Make: {self.make}, Model: {self.model}, Year: {self.year}, Color: {self.color}"


class VehicleManagementSystem:
    def __init__(self):
        self.vehicles = {}
        self.load_data()

    def add_vehicle(self, vehicle_id, make, model, year, color):
        if vehicle_id in self.vehicles:
            return "Vehicle with this ID already exists."
        else:
            vehicle = Vehicle(vehicle_id, make, model, year, color)
            self.vehicles[vehicle_id] = vehicle
            self.save_data()
            return "Vehicle added successfully."

    def get_vehicle(self, vehicle_id):
        return self.vehicles.get(vehicle_id, None)

    def update_vehicle(self, vehicle_id, make=None, model=None, year=None, color=None):
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle:
            if make: vehicle.make = make
            if model: vehicle.model = model
            if year: vehicle.year = year
            if color: vehicle.color = color
            self.save_data()
            return "Vehicle updated successfully."
        else:
            return "Vehicle not found."

    def delete_vehicle(self, vehicle_id):
        if vehicle_id in self.vehicles:
            del self.vehicles[vehicle_id]
            self.save_data()
            return "Vehicle deleted successfully."
        else:
            return "Vehicle not found."

    def list_vehicles(self):
        if not self.vehicles:
            return "No vehicles in the system."
        else:
            vehicle_list = "\n".join(str(vehicle) for vehicle in self.vehicles.values())
            return vehicle_list

    def load_data(self):
        """Load vehicle data from a JSON file"""
        if os.path.exists("vehicles.json"):
            with open("vehicles.json", "r") as file:
                try:
                    data = json.load(file)
                    self.vehicles = {key: Vehicle(**value) for key, value in data.items()}
                except json.JSONDecodeError:
                    pass  # No data or invalid data; continue with empty vehicles

    def save_data(self):
        """Save vehicle data to a JSON file"""
        data = {vehicle_id: vars(vehicle) for vehicle_id, vehicle in self.vehicles.items()}
        with open("vehicles.json", "w") as file:
            json.dump(data, file)


class Application(tk.Tk):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.title("Vehicle Management System")
        self.geometry("600x500")
        self.create_widgets()

    def create_widgets(self):
        # Create Frames
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        list_frame = tk.Frame(self)
        list_frame.pack(pady=10)

        # Vehicle ID
        self.lbl_vehicle_id = tk.Label(input_frame, text="Vehicle ID:")
        self.lbl_vehicle_id.grid(row=0, column=0, padx=10, pady=5)
        self.entry_vehicle_id = tk.Entry(input_frame)
        self.entry_vehicle_id.grid(row=0, column=1, padx=10, pady=5)

        # Make
        self.lbl_make = tk.Label(input_frame, text="Make:")
        self.lbl_make.grid(row=1, column=0, padx=10, pady=5)
        self.entry_make = tk.Entry(input_frame)
        self.entry_make.grid(row=1, column=1, padx=10, pady=5)

        # Model
        self.lbl_model = tk.Label(input_frame, text="Model:")
        self.lbl_model.grid(row=2, column=0, padx=10, pady=5)
        self.entry_model = tk.Entry(input_frame)
        self.entry_model.grid(row=2, column=1, padx=10, pady=5)

        # Year
        self.lbl_year = tk.Label(input_frame, text="Year:")
        self.lbl_year.grid(row=3, column=0, padx=10, pady=5)
        self.entry_year = tk.Entry(input_frame)
        self.entry_year.grid(row=3, column=1, padx=10, pady=5)

        # Color
        self.lbl_color = tk.Label(input_frame, text="Color:")
        self.lbl_color.grid(row=4, column=0, padx=10, pady=5)
        self.entry_color = tk.Entry(input_frame)
        self.entry_color.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        self.btn_add = tk.Button(input_frame, text="Add Vehicle", command=self.add_vehicle)
        self.btn_add.grid(row=5, column=0, padx=10, pady=5)

        self.btn_view = tk.Button(input_frame, text="View Vehicle", command=self.view_vehicle)
        self.btn_view.grid(row=5, column=1, padx=10, pady=5)

        self.btn_update = tk.Button(input_frame, text="Update Vehicle", command=self.update_vehicle)
        self.btn_update.grid(row=6, column=0, padx=10, pady=5)

        self.btn_delete = tk.Button(input_frame, text="Delete Vehicle", command=self.delete_vehicle)
        self.btn_delete.grid(row=6, column=1, padx=10, pady=5)

        self.btn_list = tk.Button(input_frame, text="List All Vehicles", command=self.list_vehicles)
        self.btn_list.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # List Box to show vehicles
        self.list_box = tk.Listbox(list_frame, width=80, height=15)
        self.list_box.pack()

    def clear_entries(self):
        self.entry_vehicle_id.delete(0, tk.END)
        self.entry_make.delete(0, tk.END)
        self.entry_model.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_color.delete(0, tk.END)

    def add_vehicle(self):
        vehicle_id = self.entry_vehicle_id.get()
        make = self.entry_make.get()
        model = self.entry_model.get()
        year = self.entry_year.get()
        color = self.entry_color.get()

        if not vehicle_id or not make or not model or not year or not color:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if not year.isdigit() or len(year) != 4:
            messagebox.showwarning("Input Error", "Please enter a valid year.")
            return

        result = self.system.add_vehicle(vehicle_id, make, model, year, color)
        messagebox.showinfo("Add Vehicle", result)
        self.clear_entries()

    def view_vehicle(self):
        vehicle_id = self.entry_vehicle_id.get()
        vehicle = self.system.get_vehicle(vehicle_id)
        if vehicle:
            messagebox.showinfo("Vehicle Details", str(vehicle))
        else:
            messagebox.showwarning("View Vehicle", "Vehicle not found.")
        self.clear_entries()

    def update_vehicle(self):
        vehicle_id = self.entry_vehicle_id.get()
        make = self.entry_make.get()
        model = self.entry_model.get()
        year = self.entry_year.get()
        color = self.entry_color.get()

        result = self.system.update_vehicle(vehicle_id, make, model, year, color)
        messagebox.showinfo("Update Vehicle", result)
        self.clear_entries()

    def delete_vehicle(self):
        vehicle_id = self.entry_vehicle_id.get()
        result = self.system.delete_vehicle(vehicle_id)
        messagebox.showinfo("Delete Vehicle", result)
        self.clear_entries()

    def list_vehicles(self):
        vehicles = self.system.list_vehicles()
        self.list_box.delete(0, tk.END)  # Clear the listbox
        if vehicles == "No vehicles in the system.":
            self.list_box.insert(tk.END, vehicles)
        else:
            for vehicle in vehicles.split("\n"):
                self.list_box.insert(tk.END, vehicle)


if __name__ == "__main__":
    system = VehicleManagementSystem()
    app = Application(system)
    app.mainloop()

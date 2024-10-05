from monitoring_system import PowerConsumptionMonitor, CostCalculator, DataAnalyzer
import random
import pandas as pd

def initialize_default_data(monitor):
    device_types = ['Heater', 'Air Conditioner', 'Light', 'Fan', 'Refrigerator', 'Washing Machine', 'Microwave', 'TV', 'Computer', 'Oven']
    locations = ['Living Room', 'Bedroom', 'Kitchen', 'Bathroom', 'Garage', 'Office', 'Dining Room', 'Hallway', 'Basement', 'Attic']
    number_of_randoms = 10
    default_data = []
    for i in range(number_of_randoms):
        device_id = f'Device{i+1}'
        voltage = random.choice([random.randint(50,1000) for _ in range(number_of_randoms)])
        current = round(random.uniform(0.5, 2.0), 2)
        device_type = random.choice(device_types)
        location = random.choice(locations)
        
        default_data.append({
            'device_id': device_id,
            'voltage': voltage,
            'current': current,
            'device_type': device_type,
            'location': location
        })

    for device in default_data:
        monitor.add_device_data(device['device_id'], device['voltage'], device['current'], device['device_type'], device['location'])
    monitor.save_to_csv("data.csv")
    monitor.load_from_csv("data.csv")

def main():
    monitor = PowerConsumptionMonitor()
    initialize_default_data(monitor)

    cost_calculator = CostCalculator()
    cost_calculator.data = monitor.data

    data_analyzer = DataAnalyzer()
    data_analyzer.data = monitor.data

    while True:
        print("\nPower Consumption Monitoring System")
        print("1. Add Device Data")
        print("2. Sort Data")
        print("3. Filter Data by Threshold")
        print("4. Search for a Device")
        print("5. Calculate Energy Cost")
        print("6. Analyze and Plot Data")
        print("7. Save Data to CSV")
        print("8. Load Data from CSV")
        print("9. Exit")
        choice = input("\nEnter your choice: \n")

        if choice == '1':
            device_id = input("Enter Device ID: \n")
            try:
                voltage = float(input("Enter Voltage: \n"))
                current = float(input("Enter Current: \n"))
                device_type = input("Enter Device Type: \n")
                location = input("Enter Location: \n")
                monitor.add_device_data(device_id, voltage, current, device_type, location)
                monitor.save_to_csv("data.csv")
                monitor.load_from_csv("data.csv")
                print("\nData added successfully.\n")
            except ValueError:
                print("\nInvalid input for voltage or current. Please enter numeric values.\n")
        
        elif choice == '2':
            criterion = input("choose to sort by:\n 1-current, \n 2-voltage, \n 3-power\n")
            monitor.sort_by_consumption(criterion)
            print(f"\nData sorted by {criterion}:\n")

            devices_dict = {
                "Device IDs": [],
                "Voltages": [],
                "Currents": [],
                "Power Consumptions": [],
                "Devices Types": [],
                "Locations": []
            }
            for device in monitor.data:
                devices_dict["Device IDs"].append(device['device_id'])
                devices_dict["Voltages"].append(device['voltage'])
                devices_dict["Currents"].append(device['current'])
                devices_dict["Power Consumptions"].append(device['power_consumption'])
                devices_dict["Devices Types"].append(device['device_type'])
                devices_dict["Locations"].append(device['location'])
            print(pd.DataFrame(devices_dict))
    
        elif choice == '3':
            try:
                threshold = float(input("\nEnter power consumption threshold: \n"))
                filtered_data = monitor.filter_by_threshold(threshold)
                print("\nDevices exceeding the threshold:\n")
                for device in filtered_data:
                    print(f"Device ID: {device['device_id']}, Voltage: {device['voltage']}, Current: {device['current']}, Power Consumption: {device['power_consumption']}, Device Type: {device['device_type']}, Location: {device['location']}")
            except ValueError:
                print("\nInvalid input for threshold. Please enter a numeric value.\n")
        
        elif choice == '4':
            device_id = input("\nEnter Device ID to search: \n")
            device = monitor.search_device(device_id)
            if device:
                print(f"\nDevice found: Device ID: {device['device_id']}, Voltage: {device['voltage']}, Current: {device['current']}, Power Consumption: {device['power_consumption']}, Device Type: {device['device_type']}, Location: {device['location']}")
            else:
                print("\nDevice not found.\n")
        
        elif choice == '5':
            device_id = input("Enter Device ID to calculate energy cost: ")
            device = monitor.search_device(device_id)
            if device:
                try:
                    hours = float(input("Enter number of hours: "))
                    rate_per_kwh = float(input("Enter rate per kWh: "))
                    cost = cost_calculator.calculate_energy_cost(device_id, hours, rate_per_kwh)
                    if cost is not None:
                        print(f"Energy cost for {device['device_id']}: ${cost:.2f}")
                    else:
                        print("Device not found.")
                except ValueError:
                    print("Invalid input for hours or rate. Please enter numeric values.")
            else:
                print("Device not found.")
        
        elif choice == '6':
            data_analyzer.analyze_data()
            data_analyzer.plot_data()

        elif choice == '7':
            filename = input("\nEnter filename to save data (e.g., data.csv): \n")
            try:
                monitor.save_to_csv(filename)
                print(f"\nData saved to {filename}.\n")
            except Exception as e:
                print(f"\nAn error occurred while saving to CSV: {e}\n")
        
        elif choice == '8':
            filename = input("\nEnter filename to load data (e.g., data.csv): \n")
            try:
                monitor.load_from_csv(filename)
                print(f"Data loaded from {filename}.")
            except FileNotFoundError:
                print("\nFile not found. Please check the filename and try again.\n")
            except Exception as e:
                print(f"\nAn error occurred while loading from CSV: {e}\n")
        
        elif choice == '9':
            print("\nExiting the system.\n")
            break
        
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()

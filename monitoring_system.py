import csv
import matplotlib.pyplot as plt
import pandas as pd

class PowerConsumptionMonitor():
    def __init__(self):
        self.data = []

    def add_device_data(self, device_id, voltage, current, device_type, location):
        self.data.append({
            'device_id': device_id,
            'voltage': voltage,
            'current': current,
            'power_consumption': round(voltage * current),
            'device_type': device_type,
            'location': location
        })
        
    def sort_by_consumption(self, criterion):
        if criterion == 'power':
            self.data.sort(key=lambda x: float(x['power_consumption']), reverse=True)
        elif criterion == 'voltage':
            self.data.sort(key=lambda x: float(x['voltage']), reverse=True)
        elif criterion == 'current':
            self.data.sort(key=lambda x: float(x['current']), reverse=True)
        else:
            print("Invalid criterion. Please choose 'power', 'voltage', or 'current'.")

    def filter_by_threshold(self, threshold):
        return [device for device in self.data if float(device['power_consumption']) > threshold]

    def search_device(self, device_id):
        for device in self.data:
            if device['device_id'] == device_id:
                return device
        return None
    
    def save_to_csv(self, filename):
        keys = self.data[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.data)
    
    def load_from_csv(self, filename):
        with open(filename, 'r') as input_file:
            dict_reader = csv.DictReader(input_file)
            self.data = list(dict_reader)
    
class CostCalculator(PowerConsumptionMonitor):
    def calculate_energy_cost(self, device_id, hours, rate_per_kwh):
        device = self.search_device(device_id)
        if device:
            power = float(device['voltage']) * float(device['current'])  # Power in watts
            energy = power * hours / 1000  # Energy in kWh
            return energy * rate_per_kwh
        else:
            return None
        
class DataAnalyzer(PowerConsumptionMonitor):
    def analyze_data(self):
        self.df = pd.DataFrame(self.data)
        return self.df

    def plot_data(self):
        df = self.df.sort_values(by='device_id')  # Sort by device_id
        plt.figure(figsize=(10, 6))

        # Create a bar graph for power
        bar_width = 0.25
        device_ids = df['device_id']
        indices = range(len(device_ids))

        plt.bar(indices, df['power_consumption'].astype(float), bar_width, label='Power')

        plt.title('Bar Graph of Power per device')
        plt.xlabel('Device ID')
        plt.ylabel('power consumption (W)')
        plt.xticks([i for i in indices], device_ids)
        plt.legend()

        plt.show()



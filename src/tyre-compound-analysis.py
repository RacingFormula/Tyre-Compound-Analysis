import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class TyreCompoundAnalysis:
    def __init__(self, compounds, config):
        self.compounds = compounds  # List of compounds to analyse
        self.track_temperature = config.get("track_temperature", 30)  # degrees Celsius
        self.race_distance = config.get("race_distance", 50)  # laps
        self.load_per_lap = config.get("load_per_lap", 1500)  # Load in Newtons

    def simulate_compound(self, compound):
        grip = compound["base_grip"]
        degradation_rate = compound["degradation_rate"]
        thermal_sensitivity = compound["thermal_sensitivity"]

        remaining_grip = []
        temperatures = []

        current_grip = grip
        current_temp = self.track_temperature

        for lap in range(1, self.race_distance + 1):
            # Degrade grip based on degradation rate
            current_grip -= degradation_rate
            current_grip = max(0, current_grip)
            
            # Calculate thermal increase
            temp_increase = (self.load_per_lap / 1000) * thermal_sensitivity
            current_temp += temp_increase - ((current_temp - self.track_temperature) * 0.1)  # Heat dissipation

            # Append lap results
            remaining_grip.append(current_grip)
            temperatures.append(current_temp)

        return {
            "remaining_grip": remaining_grip,
            "temperatures": temperatures
        }

    def analyse_compounds(self):
        results = {}

        for compound in self.compounds:
            name = compound["name"]
            print(f"Simulating for {name} compound...")
            results[name] = self.simulate_compound(compound)

        return results

    def plot_results(self, results):
        laps = range(1, self.race_distance + 1)

        plt.figure(figsize=(14, 8))

        # Plot remaining grip
        plt.subplot(2, 1, 1)
        for compound, data in results.items():
            plt.plot(laps, data["remaining_grip"], label=f"{compound} Grip")
        plt.title("Tyre Grip Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Grip Level")
        plt.legend()
        plt.grid(True)

        # Plot temperatures
        plt.subplot(2, 1, 2)
        for compound, data in results.items():
            plt.plot(laps, data["temperatures"], label=f"{compound} Temperature")
        plt.title("Tyre Temperature Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    compounds = [
        {
            "name": "Soft",
            "base_grip": 1.0,
            "degradation_rate": 0.02,
            "thermal_sensitivity": 0.1
        },
        {
            "name": "Medium",
            "base_grip": 0.9,
            "degradation_rate": 0.015,
            "thermal_sensitivity": 0.08
        },
        {
            "name": "Hard",
            "base_grip": 0.8,
            "degradation_rate": 0.01,
            "thermal_sensitivity": 0.05
        }
    ]

    config = {
        "track_temperature": 30,
        "race_distance": 50,
        "load_per_lap": 1500
    }

    analysis = TyreCompoundAnalysis(compounds, config)
    results = analysis.analyse_compounds()
    analysis.plot_results(results)
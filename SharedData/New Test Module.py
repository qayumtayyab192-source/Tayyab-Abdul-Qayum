from math import exp, log
import tkinter as tk
import csv
import os

class GraphDrawing:
    def __init__(self):
        self.screenwidth = screen.winfo_screenwidth()
        self.screenheight = screen.winfo_screenheight()
        self.canvas = tk.Canvas(screen, width=self.screenwidth, height=self.screenheight, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.x_adjustment_ratio = (self.screenwidth+75) // 100
        self.TemperatureValues = []
        self.y_adjustment_ratio = (self.screenheight+56) // 60

        self.entry = tk.Entry(screen, width=10, font=("Arial", 15), fg="black")
        self.canvas.create_window(650, 25, window=self.entry)

        self.entry.bind("<Return>", self.IsItSoluble)

        self.prompt_label = tk.Label(screen, text="Enter a chemical's index and temperature, separated by a comma:", font=("Arial", 15))
        self.canvas.create_window(300, 25, window=self.prompt_label)

        self.result_label = tk.Label(self.canvas, text="", font=("Arial", 15), anchor="e")
        self.result_label.place(x=self.screenwidth - 400, y=10)

        self.entry.focus_set()

    def clear_screen(self):
        if self.result_label:
            self.result_label.config(text="")

        self.canvas.delete("all")

        self.canvas.create_window(650, 25, window=self.entry)
        self.canvas.create_window(300, 25, window=self.prompt_label)

    def IsItSoluble(self, event):
        self.raw_input = self.entry.get().strip()

        if "," not in self.raw_input:
            self.prompt_label.config(text="Error: Please enter comma separated values:")
            self.entry.delete(0, tk.END)
            return

        try:
            self.chemical_index = int(self.raw_input.split(",")[0])
            self.temperature = int(self.raw_input.split(",")[1])
        except ValueError:
            self.prompt_label.config(text="Error: Please enter comma separated integers:")
            self.entry.delete(0, tk.END)
            return

        self.entry.delete(0, tk.END)

        if self.temperature < 0 or self.temperature > 100:
            self.prompt_label.config(text="Error: Please enter comma separated values:")
            screen.after(1000, self.ResetPromptText)
            return

        self.solubility_solver()

        if self.temperature > 0 and self.temperature <= 100:
            current_value = self.TemperatureValues[(self.temperature*2)-1]
        elif self.temperature == 0:
            current_value = self.TemperatureValues[self.temperature * 2]

        if current_value > 0:
            message = f"Highly soluble at {self.temperature}*C"
        elif current_value > -2:
            message = f"Soluble at {self.temperature}*C"
        elif current_value > -4:
            message = f"Moderately Soluble at {self.temperature}*C"
        elif current_value > -6:
            message = f"Low solubility at {self.temperature}*C"
        else:
            message = f"Highly insoluble at {self.temperature}*C"

        self.result_label.config(text=message)

    def ResetPromptText(self):
        self.prompt_label.config(text="Enter a chemical's index and temperature, separated by a comma:")

    def solubility_solver(self):
        self.TemperatureValues = []
        with open(Expected_Solubility, "r") as f:
            content = f.readlines()

        with open(Delta_H_URL, "r") as f:
            enthalpy = f.readlines()
        try:
            item = float(content[self.chemical_index])
        except IndexError:
            return "Solubility not found"

        enthalpy_change = enthalpy[self.chemical_index]
        current_enthalpy = float(enthalpy_change.replace("\n", ""))

        safe_item = max(item, -12.0)

        S25 = 10**safe_item

        for i in range(0, 1005, 5):
            temp_k = (i/10) + 273.15
            ST = S25 * exp(-1 * ((1 / (temp_k) - (1 / 298.15)) * current_enthalpy / 8.314))
            actual_value = log(ST, 10)

            self.TemperatureValues.append(actual_value)

        self.min_val = min(self.TemperatureValues)
        self.max_val = max(self.TemperatureValues)
        self.data_range = self.max_val - self.min_val
        if self.data_range == 0:
            self.data_range = 1
        self.top_margin = 50
        self.bottom_margin = 70
        self.drawable_height = self.screenheight - self.top_margin - self.bottom_margin

        self.canvas.delete("all")
        self.canvas.create_window(650, 25, window=self.entry)
        self.canvas.create_window(300, 25, window=self.prompt_label)

        self.Curve_Drawer()

    def Curve_Drawer(self):
        for i in range(1, len(self.TemperatureValues)):
            normalised_fraction_1 = (self.TemperatureValues[i-1] - self.min_val) / self.data_range
            normalised_fraction_2 = (self.TemperatureValues[i] - self.min_val) / self.data_range

            line_x1 = 10 + self.x_adjustment_ratio * i/2
            line_y1 = self.screenheight - self.bottom_margin - (normalised_fraction_1 * self.drawable_height)
            line_x2 = 10 + self.x_adjustment_ratio * (i+1)/2
            line_y2 = self.screenheight - self.bottom_margin - (normalised_fraction_2 * self.drawable_height)

            self.canvas.create_line([(line_x1, line_y1), (line_x2, line_y2)], width=2, fill="red")

        self.mesh_drawer()

    def mesh_drawer(self):
        vertical_y1 = self.screenheight - 50
        vertical_y2 = 50
        horizontal_x1 = self.screenwidth - 19
        horizontal_x2 = 18

        for i in range(1, 101):
            vertical_x = self.x_adjustment_ratio * i
            self.canvas.create_line([(vertical_x, vertical_y1), (vertical_x, vertical_y2)], width=2)
            if i % 10 == 0:
                label = tk.Label(self.canvas, text=str(i-1), font=("Arial", 10))
                label.place(x=vertical_x-5, y=vertical_y1)

        for i in range(0, 51):
            fraction = i / 50
            horizontal_y = self.screenheight - self.bottom_margin - (fraction * self.drawable_height)
            self.canvas.create_line([(horizontal_x1, horizontal_y), (horizontal_x2, horizontal_y)], width=2)
            if i % 5 == 0:
                multiplier = round(i * self.max_val / 50)
                self.canvas.create_text(horizontal_x2 - 1, horizontal_y, text=f"{multiplier:.1f}", font=("Arial", 7), anchor="e")

        X_Axis_Label = tk.Label(self.canvas, text="Temperature (*C)", font=("Arial", 15), anchor="e")
        X_Axis_Label.place(x=(self.screenwidth//2)-50, y=self.screenheight-30)

        Y_Axis_Label = tk.Label(self.canvas, text="Solubility (log base 10)", font=("Arial", 15), anchor="e")
        Y_Axis_Label.place(x=(self.screenwidth//2)-70, y=10)

if __name__ == "__main__":
    features_to_keep = [
        'MolLogP', 'TPSA', 'MolWt', 'NumHAcceptors', 'NumHDonors',
        'NumRotatableBonds', 'NumAromaticRings', 'NumSaturatedRings',
        'NumAliphaticRings', 'RingCount', 'BalabanJ', 'BertzCT'
    ]

    soluble = []
    delta_H = []
    indexes_to_ignore = []
    soluble_index = []
    delta_h_index = ""
    individual_rows = []
    names = []

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    file = os.path.join(BASE_DIR, "Chemical_Properties", "curated-solubility-dataset.csv")
    edited_file = os.path.join(BASE_DIR, "Chemical_Properties", "Chemical_Matrices.txt")
    True_Values = os.path.join(BASE_DIR, "Chemical_Properties", "Actual_Solubility.txt")
    Delta_H_URL = os.path.join(BASE_DIR, "Chemical_Properties", "DeltaH.txt")
    NamesLink = os.path.join(BASE_DIR, "Chemical_Properties", "Names.txt")
    screen = tk.Tk()
    screen.configure(background="white")
    screen.attributes("-fullscreen", True)
    Expected_Solubility = os.path.join(BASE_DIR, "Chemical_Properties", "Predicted_Solubility.txt")

    with open(Expected_Solubility, "r") as f:
        content = f.readlines()

    NumberOfElements = len(content)

    with open(file, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        for i, row in enumerate(reader):
            current_row = []

            if i > NumberOfElements:
                break

            if i == 0:
                for col_idx, word in enumerate(row):
                    if word not in features_to_keep:
                        if word == "Solubility":
                            soluble_index.append(col_idx)
                        else:
                            indexes_to_ignore.append(col_idx)
                    elif word == "MolWt":
                        delta_h_index = col_idx
            else:
                try:
                    for col_idx, word in enumerate(row):
                        if col_idx not in indexes_to_ignore:
                            if col_idx in soluble_index:
                                soluble.append(word)
                            elif col_idx == delta_h_index:
                                if float(word) >= 150:
                                    delta_H.append("25000.0")
                                elif 80 <= float(word) < 150:
                                    delta_H.append("18000.0")
                                else:
                                    delta_H.append("-15000.0")
                            else:
                                current_row.append(float(word))
                    individual_rows.append(current_row)
                except ValueError:
                    pass

    app = GraphDrawing()
    screen.mainloop()
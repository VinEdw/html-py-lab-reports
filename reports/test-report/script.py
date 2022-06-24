import sys
sys.path.append("..\\..")

from lab_report_tools import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Read the data from the csv and turn it into a DataTable
density_table = DataTable.from_csv("raw-data/mass-volume-data.csv") 
# Rename the column keys to something easier to work with
density_table.rename_column("mass (g)", "mass")
density_table.rename_column("volume (mL)", "volume")
# Change the column labels to something that should be shown when the table is printed
density_table.labels["mass"] = "MASS (g)"
density_table.labels["volume"] = "VOLUME (mL)"

# Turn the number strings in the table into PrecisionNumbers
density_table["mass"] = [PrecisionNumber(num) for num in density_table["mass"]]
density_table["volume"] = [PrecisionNumber(num) for num in density_table["volume"]]

# Calculate the density (mass/volume) for each row and put that into a new column
density_table.create_column(lambda row: row["mass"] / row["volume"], "density", label="DENSITY (g/mL)")


# Create a copy of the density table
density_table_w_error = density_table.copy()
# For each column in the new table, copy the PrecisionNumbers that are there and change their default_style to "absolute_error"
for col in density_table_w_error:
    copied_data = []
    for cell in density_table_w_error[col]:
        copied_cell: PrecisionNumber = cell.copy()
        copied_cell.default_style = "absolute_error"
        copied_data.append(copied_cell)
    density_table_w_error[col] = copied_data

print(density_table)
print()
print(density_table_w_error)
print()

# Write the data tables to the report.md document
file_editor.write_between_tags(str(density_table), "density-table-1", "div", "report.md")
file_editor.write_between_tags(str(density_table_w_error), "density-table-2", "div", "report.md")

# ================================================== #

# Open the concentration & absorbance data
c_a_tb = DataTable.from_csv("raw-data/concentration-absorbance-data.csv")
# Convert the numbers from str to float
for col in c_a_tb:
    c_a_tb[col] = [float(val) for val in c_a_tb[col]]
print(c_a_tb)
# Plot the Absorbance vs. Concentration in a scatter plot
c_a_fig, c_a_ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))
c_a_ax.plot(c_a_tb["Concentration (M)"], c_a_tb["Absorbance (A)"], "bo")
c_a_ax.set_title("Absorbance vs. Concentration")
c_a_ax.grid(True, which="minor") # default linewidth is 0.8 (I think)
c_a_ax.grid(True, which="major", linewidth=1.5)
# Find and plot the line of best fit
y_int, slope = np.polynomial.polynomial.polyfit(c_a_tb["Concentration (M)"], c_a_tb["Absorbance (A)"], 1)
y_avg = sum(c_a_tb["Absorbance (A)"])/len(c_a_tb["Absorbance (A)"])
R_squared = 1 - sum(((slope * x + y_int) - y)**2 for x, y in zip(c_a_tb["Concentration (M)"], c_a_tb["Absorbance (A)"])) / sum((y - y_avg)**2 for y in c_a_tb["Absorbance (A)"])
line_x_vals = np.array([0, 0.5])
line_y_vals = slope * line_x_vals + y_int
c_a_ax.plot(line_x_vals, line_y_vals, "r")
c_a_ax.text(0.03, 1.2, f"$y={slope:.4f}\\ x + {y_int:.3f}$\n$R^2={R_squared:.4f}$", backgroundcolor="lightgray", color="blue")
# Customize the x-axis
c_a_ax.set_xlabel("Concentration (M)")
c_a_ax.set_xlim(0, 0.5)
x_ticks = np.arange(0, 0.51, 0.1)
c_a_ax.set_xticks(x_ticks, [f"{val:.3f}" for val in x_ticks])
c_a_ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(5))
# Customize the y-axis
c_a_ax.set_ylabel("Absorbance (A)")
c_a_ax.set_ylim(0, 1.5)
y_ticks = np.arange(0, 1.51, 0.5)
c_a_ax.set_yticks(y_ticks, [f"{val:.3f}" for val in y_ticks])
c_a_ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator(5))
# Save the figure as a png
c_a_fig.savefig("media/absorbance-concentration-graph.png")
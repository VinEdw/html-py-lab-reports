import sys
sys.path.append("..\\..")

from lab_report_tools import *
import matplotlib.pyplot as plt
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

concentration_absorbance_table = DataTable.from_csv("raw-data/concentration-absorbance-data.csv")
print(concentration_absorbance_table)
c_a_fig, c_a_ax = plt.subplots(1, 1)
c_a_ax.scatter(concentration_absorbance_table["Concentration (M)"], concentration_absorbance_table["Absorbance (A)"])
c_a_ax.set_title("Absorbance vs. Concentration")
c_a_ax.set_xlabel("Concentration (M)")
c_a_ax.set_ylabel("Absorbance (A)")
c_a_fig.show()
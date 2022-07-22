from lab_report_tools import *
import matplotlib.pyplot as plt

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

# Write the data tables to the report.html document
file_editor.write_between_markers(density_table.get_html(caption="Density Table (regular)"), "density-table-1", "report.html")
file_editor.write_between_markers(density_table_w_error.get_html(caption="Density Table (absolute error)"), "density-table-2", "report.html")

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
# Customize the x-axis and y-axis
graphing.style_axis(c_a_ax, "x", 0, 0.5, label="Concentration (M)", major_tick_spacing=0.1, minor_tick_count=5, major_tick_formatter="{x:.3f}")
graphing.style_axis(c_a_ax, "y", 0, 1.5, label="Absorbance (A)", major_tick_spacing=0.5, minor_tick_count=5, major_tick_formatter="{x:.3f}")
# Find and plot the line of best fit
y_int, slope, R_squared = graphing.plot_best_fit_line(c_a_ax, c_a_tb["Concentration (M)"], c_a_tb["Absorbance (A)"], "r")
# Add a label for the line
c_a_ax.text(0.03, 1.2, f"$y={slope:.4f}\\ x + {y_int:.3f}$\n$R^2={R_squared:.4f}$", backgroundcolor="lightgray", color="blue")
# Save the figure as a png
c_a_fig.tight_layout()
c_a_fig.savefig("media/absorbance-concentration-graph.png")
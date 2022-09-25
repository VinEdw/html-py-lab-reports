from lab_report_tools import *
import matplotlib.pyplot as plt

file_name = "newtons-second-law-lab-report.html"

# Set up hanging-mass-acceleration-table

m_a_tb = DataTable.from_csv("raw-data/hanging-mass-acceleration-data.csv")
m_a_tb.rename_column("m_h (g)", "m_h")
m_a_tb.labels["m_h"] = "$m_h$ (g)"
m_a_tb.rename_column("a_up (m/s^2)", "a_up")
m_a_tb.labels["a_up"] = "$a_{up}$ (m/s^2)"
m_a_tb.rename_column("a_down (m/s^2)", "a_down")
m_a_tb.labels["a_down"] = "$a_{down}$ (m/s^2)"

for col in m_a_tb:
    data = m_a_tb[col]
    if col == "m_h":
        data = [int(val) for val in data]
    else:
        data = [PrecisionNumber(val, decimal_place=-4) for val in data]
    m_a_tb[col] = data

m_a_tb.create_column(lambda r: (r["a_up"] + r["a_down"])/2, "a_avg", label="$a_{avg}$ (m/s^2)")
n_a_avg = []
for val in m_a_tb["a_avg"]:
    n_val: PrecisionNumber = val.copy()
    n_val.decimal_place = -4
    n_a_avg.append(n_val)
m_a_tb["a_avg"] = n_a_avg

file_editor.write_between_markers(m_a_tb.get_html(
    caption="Hanging Mass & Acceleration Data"), "hanging-mass-acceleration-table", file_name)

print(m_a_tb)

# Plot average acceleration versus hanging mass

m_a_fig, m_a_ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))
m_a_ax.plot(m_a_tb["m_h"], m_a_tb["a_avg"], "bo")
m_a_ax.set_title("Average Acceleration vs Hanging Mass")
m_a_ax.grid(True, which="minor") # default linewidth is 0.8 (I think)
m_a_ax.grid(True, which="major", linewidth=1.5)
# Customize the x-axis and y-axis
graphing.style_axis(m_a_ax, "x", 0, 30, label=m_a_tb.labels["m_h"], major_tick_spacing=5)
graphing.style_axis(m_a_ax, "y", 0, 0.8, label=m_a_tb.labels["a_avg"], major_tick_spacing=0.2, major_tick_formatter="{x:.4f}")
# Find and plot the line of best fit
y_int, slope, R_squared = graphing.plot_best_fit_line(m_a_ax, m_a_tb["m_h"], m_a_tb["a_avg"], "r")
# Save the figure as a png
m_a_fig.tight_layout()
m_a_fig.savefig("media/hanging-mass-acceleration-graph.png")

# double check slope uncertainy
n = m_a_tb.row_count
m_h_avg = sum(m_a_tb["m_h"]) / n
y_dists = sum((row["a_avg"] - (row["m_h"]*slope + y_int))**2 for row in m_a_tb.rows())
x_dists = sum((val - m_h_avg)**2 for val in m_a_tb["m_h"])
error = (y_dists / x_dists / (n - 2))**0.5
print(error)
print(repr(error))
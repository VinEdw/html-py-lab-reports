from lab_report_tools import *

# Get the logger pro tables into the report

slow_ball_table = DataTable.from_csv("raw-data/slow-ball-data.csv")
fast_ball_table = DataTable.from_csv("raw-data/fast-ball-data.csv")

desired_columns = ["Time (s)", "X (m)", "Y (m)", "X Velocity (m/s)", "Y Velocity (m/s)"]

for table in (slow_ball_table, fast_ball_table):
    col_list = list(table.keys())
    for col in col_list:
        if col not in desired_columns:
            del table[col]
        else:
            desired_index = desired_columns.index(col)
            table.move_column(col, desired_index)
    for i, col in enumerate(table):
        if i < 3:
            table[col] = [PrecisionNumber(val, sig_figs=4) if float(
                val) != 0.0 else 0 for val in table[col]]
        else:
            table[col] = [PrecisionNumber(
                val, decimal_place=-3) if float(val) != 0.0 else 0 for val in table[col]]
    table.create_column([i for i in range(1, table.row_count + 1)], "Row", index=0, label="", use_dict=False)
    print(table)

file_editor.write_between_markers(slow_ball_table.get_html(
    caption="Run 1 Logger Pro Video Data"), "slow-ball-table", "projectile-motion-lab-report.html")
file_editor.write_between_markers(fast_ball_table.get_html(
    caption="Run 2 Logger Pro Video Data"), "fast-ball-table", "projectile-motion-lab-report.html")

# Get logger pro graphs into the report

run_list = ["slow", "fast"]
graph_order = ["x-t", "y-t", "vx-t", "vy-t", "y-x"]
figure_template = '<figure>\n  <img src="{src}">\n  <figcaption>{caption}</figcaption>\n</figure>'
symbol_name_map = {
    "t": "Time",
    "x": "Horizontal Position",
    "y": "Vertical Position",
    "vx": "Horizontal Velocity",
    "vy": "Vertical Velocity",
}

for i, run in enumerate(run_list):
    text = ""
    for graph in graph_order:
        file_name = f"media/{run}-{graph}.png"
        y_ax, x_ax = graph.split("-")
        graph_caption = f"Run {i + 1}—{symbol_name_map[y_ax]} vs {symbol_name_map[x_ax]}"
        text += figure_template.format(caption=graph_caption, src=file_name) + "\n"
    file_editor.write_between_markers(text, f"{run}-ball-graphs", "projectile-motion-lab-report.html")

# Get distance along angled board data into the report

angled_distance_data = DataTable.from_csv("raw-data/distance-along-angled-board.csv")
angled_distance_data.create_column([i for i in range(1, angled_distance_data.row_count + 1)], "Trial", index=0, label="Trial", use_dict=False)
angled_distance_data["d (cm)"] = [PrecisionNumber(val, decimal_place=-2) for val in angled_distance_data["d (cm)"]]
print(angled_distance_data)
angled_distance_avg = sum(angled_distance_data["d (cm)"]) / len(angled_distance_data["d (cm)"])
print(angled_distance_avg)
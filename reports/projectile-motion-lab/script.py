from lab_report_tools import *

# Get the tables into the report

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
    print(table)

file_editor.write_between_markers(slow_ball_table.get_html(
    caption="Run 1 Logger Pro Video Data"), "slow-ball-table", "projectile-motion-lab-report.html")
file_editor.write_between_markers(fast_ball_table.get_html(
    caption="Run 2 Logger Pro Video Data"), "fast-ball-table", "projectile-motion-lab-report.html")

# Get the graphs into the report

run_list = ["slow", "fast"]
graph_order = ["x-t", "y-t", "vx-t", "vy-t", "y-x"]
figure_template = '<figure>\n  <figcaption>{caption}</figcaption>\n  <img src="{src}">\n</figure>'
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
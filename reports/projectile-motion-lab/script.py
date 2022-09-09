from lab_report_tools import *

slow_ball_table = DataTable.from_csv("raw-data/slow-ball-data.csv")
fast_ball_table = DataTable.from_csv("raw-data/fast-ball-data.csv")

desired_columns = ["Time (s)","X (m)","Y (m)","X Velocity (m/s)","Y Velocity (m/s)"]

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
            table[col] = [PrecisionNumber(val, sig_figs=4) if float(val) != 0.0 else 0 for val in table[col]]
        else:
            table[col] = [PrecisionNumber(val, decimal_place=-3) if float(val) != 0.0 else 0 for val in table[col]]
    print(table)

file_editor.write_between_markers(slow_ball_table.get_html(caption="Run 1 Logger Pro Video Data"), "slow-ball-table", "projectile-motion-lab-report.html")
file_editor.write_between_markers(fast_ball_table.get_html(caption="Run 1 Logger Pro Video Data"), "fast-ball-table", "projectile-motion-lab-report.html")

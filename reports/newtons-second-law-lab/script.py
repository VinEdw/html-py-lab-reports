from lab_report_tools import *

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
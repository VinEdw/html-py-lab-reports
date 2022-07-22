import matplotlib as mpl
import numpy as np

def style_axis(ax, x_or_y: str, low: float, high: float, *, label: str = None, major_tick_spacing: float = None, minor_tick_count: int = None, major_tick_formatter: str = None):
    """
    Style the x or y axis of a plot with reasonable settings. Namely
    - Low
    - High
    - Label
    - Major tick spacing
    - Minor tick count
    - Major tick formatter (x for tick value, and pos for tick position; can use string or lambda function)
    """
    if x_or_y == "x":
        axis = ax.xaxis
        ax.set_xlim(low, high)
        if label != None:
            ax.set_xlabel(label)
    elif x_or_y == "y":
        axis = ax.yaxis
        ax.set_ylim(low, high)
        if label != None:
            ax.set_ylabel(label)
    else:
        return
    if major_tick_spacing != None:
        axis.set_major_locator(mpl.ticker.MultipleLocator(float(major_tick_spacing)))
    if major_tick_formatter != None:
        axis.set_major_formatter(major_tick_formatter)
    if minor_tick_count != None:
        axis.set_minor_locator(mpl.ticker.AutoMinorLocator(int(minor_tick_count)))

def plot_best_fit_line(ax, x_vals, y_vals, style="r"):
    """
    Plot line of best fit on the ax.
    Return the a tuple containing the slope, y-intercept, and R^2.
    """
    x_vals = [float(val) for val in x_vals]
    y_vals = [float(val) for val in y_vals]
    y_int, slope = np.polynomial.polynomial.polyfit(x_vals, y_vals, 1)
    y_avg = sum(y_vals)/len(y_vals)
    R_squared = 1 - sum(((slope * x + y_int) - y)**2 for x, y in zip(x_vals, y_vals)) / sum((y - y_avg)**2 for y in y_vals)
    line_x_vals = np.array(ax.get_xlim())
    line_y_vals = slope * line_x_vals + y_int
    ax.plot(line_x_vals, line_y_vals, style)
    return (float(y_int), float(slope), float(R_squared))
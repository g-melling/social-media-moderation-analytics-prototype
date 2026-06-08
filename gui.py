import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from backend import Backend


backend = Backend()

REQUIRED_FILES = {
    "users": "USERS.csv",
    "posts": "POSTS.csv",
    "interactions": "INTERACTIONS.csv",
    "topics": "TOPICS.csv",
}

selected_files = {}
chart_canvas = None
chart_toolbar = None


# Helper functions

def add_button(parent, text, command, pady=4):
    button = ttk.Button(parent, text=text, width=30, command=command)
    button.pack(fill="x", pady=pady)
    return button


def add_heading(parent, text):
    ttk.Label(parent, text=text, style="Card.TLabel", font=("Arial", 12, "bold")).pack(anchor="w")


def run_action(action, status_message=None, success_popup=True):
    """Run a backend/GUI action safely and show any errors in one place."""
    try:
        result = action()
        if status_message:
            status_var.set(status_message)
        if success_popup and isinstance(result, str):
            messagebox.showinfo("Success", result)
        return result
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None


def pick_file(key):
    filename = filedialog.askopenfilename(
        title=f"Select {key.upper()} CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
    )
    if filename:
        selected_files[key].set(filename)


def get_selected_paths():
    return {key: var.get() for key, var in selected_files.items()}


def clear_table():
    tree.delete(*tree.get_children())
    tree["columns"] = []


def show_table(dataframe):
    clear_table()

    if dataframe is None:
        return

    columns = [str(col) for col in dataframe.columns]
    tree["columns"] = columns

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=130, anchor="center")

    for _, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))


def show_chart(fig=None):
    global chart_canvas, chart_toolbar

    for widget in chart_frame.winfo_children():
        widget.destroy()

    if fig is None:
        ttk.Label(
            chart_frame,
            text="Run analysis with visualisation to display embedded chart here.",
        ).pack(expand=True)
        return

    chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    chart_toolbar = NavigationToolbar2Tk(chart_canvas, chart_frame)
    chart_toolbar.update()


def show_results(table=None, chart=None, status_message=None):
    if table is not None:
        show_table(table)
    show_chart(chart)
    if status_message:
        status_var.set(status_message)


def run_table_chart_analysis(analysis_function, status_message, reset_index=False):
    def action():
        table, chart = analysis_function()
        if reset_index:
            table = table.reset_index()
        show_results(table, chart, status_message)
    run_action(action, success_popup=False)


def add_file_picker(parent, key, default_name):
    selected_files[key] = tk.StringVar(value=str(Path(default_name)) if Path(default_name).exists() else "")

    row = ttk.Frame(parent, style="Card.TFrame")
    row.pack(fill="x", pady=(8, 0))

    ttk.Label(row, text=key.capitalize(), style="Card.TLabel", width=12).pack(side="left")
    ttk.Entry(row, textvariable=selected_files[key], width=28).pack(side="left", fill="x", expand=True, padx=(4, 6))
    ttk.Button(row, text="Browse", command=lambda: pick_file(key)).pack(side="left")


# Button Commands

def load_data():
    run_action(
        lambda: backend.load_data(get_selected_paths()),
        "Data loaded. You can now clean, analyse, or save backup.",
    )


def restore_backup():
    run_action(backend.restore_backup, "Backup restored successfully.")


def clean_data():
    run_action(
        backend.clean_data,
        "Data cleaned. Bot accounts excluded from human behaviour analysis.",
    )


def save_backup():
    run_action(backend.save_backup, "Backup saved.")


def merge_analysis():
    run_table_chart_analysis(
        backend.merge_analysis,
        "Report pattern analysis complete.",
    )


def pivot_analysis():
    run_table_chart_analysis(
        backend.pivot_analysis,
        "Pivot analysis complete.",
        reset_index=True,
    )


def categorical_analysis():
    def action():
        table = backend.categorical_analysis().reset_index()
        show_results(table, None, "Categorical analysis complete.")
    run_action(action, success_popup=False)


def calculate_stats():
    def action():
        metric = metric_var.get()
        result = backend.calculate_stats(metric)
        messagebox.showinfo(
            "Statistics",
            f"Metric: {metric}\n"
            f"Mean: {result['mean']:.2f}\n"
            f"Median: {result['median']:.2f}\n"
            f"Mode: {result['mode']}",
        )
    run_action(action, success_popup=False)


def correlation_analysis():
    run_table_chart_analysis(
        backend.correlation_analysis,
        "Correlation visualisation complete.",
        reset_index=True,
    )


def view_audit_log():
    def action():
        window = tk.Toplevel(root)
        window.title("Audit Log")

        text = tk.Text(window, width=100, height=30)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, backend.get_audit_log())
        text.config(state="disabled")
    run_action(action, success_popup=False)


# Main window

root = tk.Tk()
root.title("Social Media Moderation Analytics")
root.geometry("1250x900")
root.minsize(980, 640)

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f4f6f8")
style.configure("Card.TFrame", background="white")
style.configure("TLabel", background="#f4f6f8", font=("Arial", 10))
style.configure("Card.TLabel", background="white", font=("Arial", 10))
style.configure("Title.TLabel", background="#f4f6f8", font=("Arial", 18, "bold"))
style.configure("Status.TLabel", background="white", foreground="darkgreen", font=("Arial", 10, "bold"))
style.configure("Ethics.TLabel", background="white", foreground="darkred", font=("Arial", 9))
style.configure("TButton", font=("Arial", 10), padding=7)
style.configure("Treeview", rowheight=25)

header = ttk.Frame(root, padding=(18, 14, 18, 8))
header.pack(fill="x")
ttk.Label(header, text="Social Media Moderation Analytics", style="Title.TLabel").pack(anchor="w")
ttk.Label(header, text="Load datasets, clean records, and view embedded analytics charts.").pack(anchor="w", pady=(4, 0))

main_frame = ttk.Frame(root, padding=(18, 8, 18, 18))
main_frame.pack(fill="both", expand=True)
main_frame.columnconfigure(0, weight=0, minsize=360)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

# Scrollable container for left panel
left_container = ttk.Frame(main_frame)
left_container.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

canvas = tk.Canvas(left_container, width=460, background="#f4f6f8", highlightthickness=0)
scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=canvas.yview)

scrollable_frame = ttk.Frame(canvas, style="Card.TFrame", padding=14)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

left_frame = scrollable_frame

right_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=14)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.rowconfigure(1, weight=1)
right_frame.columnconfigure(0, weight=1)

# Left Panel

add_heading(left_frame, "Data Management")
for key, default_name in REQUIRED_FILES.items():
    add_file_picker(left_frame, key, default_name)

add_button(left_frame, "Load Data", load_data, pady=(14, 4))
add_button(left_frame, "Clean Data", clean_data)
add_button(left_frame, "Save Backup", save_backup)
add_button(left_frame, "Restore Backup", restore_backup)

status_var = tk.StringVar(value="Select CSV files, then load data or restore a saved backup.")
ttk.Label(left_frame, textvariable=status_var, style="Status.TLabel", wraplength=320).pack(anchor="w", pady=(14, 8))
ttk.Label(
    left_frame,
    text="Ethics note: bot accounts are excluded from human behaviour analysis, and outputs should support human review.",
    style="Ethics.TLabel",
    wraplength=320,
).pack(anchor="w", pady=(0, 10))

ttk.Separator(left_frame).pack(fill="x", pady=12)
add_heading(left_frame, "Analytics")

add_button(left_frame, "Report Pattern Analysis", merge_analysis, pady=(8, 4))
add_button(left_frame, "Pivot Analysis", pivot_analysis)
add_button(left_frame, "Categorical Analysis", categorical_analysis)

ttk.Label(left_frame, text="Engagement Metric:", style="Card.TLabel").pack(anchor="w", pady=(10, 0))
metric_var = tk.StringVar(value=backend.get_available_metrics()[0])
metric_menu = ttk.OptionMenu(
    left_frame, 
    metric_var, 
    metric_var.get(), 
    *backend.get_available_metrics()
    )
metric_menu.pack(fill="x", pady=4)

add_button(left_frame, "Calculate Statistics", calculate_stats)
add_button(left_frame, "Correlation Visualisation", correlation_analysis)
add_button(left_frame, "View Audit Log", view_audit_log, pady=(14, 4))

# Right panel 

ttk.Label(right_frame, text="Results", style="Card.TLabel", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")

notebook = ttk.Notebook(right_frame)
notebook.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

table_frame = ttk.Frame(notebook, padding=8)
chart_frame = ttk.Frame(notebook, padding=8)
notebook.add(table_frame, text="Table")
notebook.add(chart_frame, text="Chart")

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)
chart_frame.rowconfigure(0, weight=1)
chart_frame.columnconfigure(0, weight=1)

tree = ttk.Treeview(table_frame, show="headings")
y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
tree.grid(row=0, column=0, sticky="nsew")
y_scroll.grid(row=0, column=1, sticky="ns")
x_scroll.grid(row=1, column=0, sticky="ew")

show_chart()
root.mainloop()

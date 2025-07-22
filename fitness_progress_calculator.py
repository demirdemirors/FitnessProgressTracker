import customtkinter as ctk
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import io
from tkinter import filedialog

# Set appearance mode and color theme for modern look
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

class FitnessProgressApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Set custom app icon if available
        if os.path.exists("app_icon.ico"):
            self.iconbitmap("app_icon.ico")
        self.title("Fitness Progress Calculator")
        self.geometry("900x650")
        self.minsize(700, 500)
        self.configure(padx=24, pady=24)

        # In-memory workout data
        self.data_columns = ["Exercise", "Date", "Weight", "Reps"]
        self.workout_df = self.load_data()

        # Title label
        self.title_label = ctk.CTkLabel(self, text="Fitness Progress Calculator", font=("Montserrat", 30, "bold"))
        self.title_label.pack(pady=(0, 28))

        # Theme toggle button (top right)
        self.theme_var = ctk.StringVar(value="System")
        self.theme_toggle = ctk.CTkSegmentedButton(self, values=["Light", "Dark", "System"], variable=self.theme_var, command=self.toggle_theme)
        self.theme_toggle.configure(fg_color="#95a5a6", selected_color="#34495e", unselected_color="#bdc3c7")
        self.theme_toggle.place(relx=1.0, y=10, anchor="ne")

        # Placeholder for main content
        self.content_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=("#f0f0f0", "#222222"))
        self.content_frame.pack(expand=True, fill="both")

        # --- Entry Form ---
        self.form_frame = ctk.CTkFrame(self.content_frame, corner_radius=12)
        self.form_frame.pack(pady=16, padx=32, fill="x")

        # Exercise Name
        self.exercise_label = ctk.CTkLabel(self.form_frame, text="Exercise Name:", font=("Montserrat", 15))
        self.exercise_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="e")
        self.exercise_var = ctk.StringVar()
        self.exercise_entry = ctk.CTkComboBox(self.form_frame, variable=self.exercise_var, values=["Squat", "Bench Press", "Deadlift", "Overhead Press", "Other"], width=180)
        self.exercise_entry.grid(row=0, column=1, padx=(5, 15), pady=10, sticky="w")

        # Date
        self.date_label = ctk.CTkLabel(self.form_frame, text="Date (YYYY-MM-DD):", font=("Montserrat", 15))
        self.date_label.grid(row=0, column=2, padx=(10, 5), pady=10, sticky="e")
        self.date_var = ctk.StringVar()
        self.date_entry = ctk.CTkEntry(self.form_frame, textvariable=self.date_var, width=120)
        self.date_entry.grid(row=0, column=3, padx=(5, 15), pady=10, sticky="w")

        # Weight (kg)
        self.weight_label = ctk.CTkLabel(self.form_frame, text="Weight (kg):", font=("Montserrat", 15))
        self.weight_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="e")
        self.weight_var = ctk.StringVar()
        self.weight_entry = ctk.CTkEntry(self.form_frame, textvariable=self.weight_var, width=100)
        self.weight_entry.grid(row=1, column=1, padx=(5, 15), pady=10, sticky="w")

        # Reps
        self.reps_label = ctk.CTkLabel(self.form_frame, text="Reps:", font=("Montserrat", 15))
        self.reps_label.grid(row=1, column=2, padx=(10, 5), pady=10, sticky="e")
        self.reps_var = ctk.StringVar()
        self.reps_entry = ctk.CTkEntry(self.form_frame, textvariable=self.reps_var, width=100)
        self.reps_entry.grid(row=1, column=3, padx=(5, 15), pady=10, sticky="w")

        # Submit Button
        self.submit_button = ctk.CTkButton(self.form_frame, text="Add Entry", font=("Roboto", 16, "bold"), width=120, command=self.handle_submit, fg_color="#3498db", hover_color="#217dbb")
        self.submit_button.grid(row=0, column=4, rowspan=2, padx=(20, 10), pady=10, sticky="ns")

        # Status bar/message label for feedback
        self.message_label = ctk.CTkLabel(self, text="", font=("Montserrat", 14), text_color="#e74c3c", anchor="w")
        self.message_label.pack(side="bottom", fill="x", padx=0, pady=0)

        # --- Table View ---
        # Filter Controls
        self.filter_frame = ctk.CTkFrame(self.content_frame, corner_radius=12)
        self.filter_frame.pack(padx=20, pady=(0, 8), fill="x")

        # Exercise filter
        self.filter_exercise_var = ctk.StringVar(value="All")
        self.filter_exercise_combo = ctk.CTkComboBox(self.filter_frame, variable=self.filter_exercise_var, values=["All", "Squat", "Bench Press", "Deadlift", "Overhead Press", "Other"], width=160)
        self.filter_exercise_combo.grid(row=0, column=0, padx=(10, 5), pady=8)

        # Date range filter
        self.filter_start_var = ctk.StringVar()
        self.filter_end_var = ctk.StringVar()
        self.filter_start_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.filter_start_var, width=110, placeholder_text="Start Date")
        self.filter_start_entry.grid(row=0, column=1, padx=(5, 5), pady=8)
        self.filter_end_entry = ctk.CTkEntry(self.filter_frame, textvariable=self.filter_end_var, width=110, placeholder_text="End Date")
        self.filter_end_entry.grid(row=0, column=2, padx=(5, 5), pady=8)

        # Filter button
        self.filter_button = ctk.CTkButton(self.filter_frame, text="Filter", command=self.apply_filters, width=90, fg_color="#2ecc71", hover_color="#27ae60")
        self.filter_button.grid(row=0, column=3, padx=(10, 10), pady=8)

        # --- Stats Display ---
        self.stats_frame = ctk.CTkFrame(self.content_frame, corner_radius=12)
        self.stats_frame.pack(padx=32, pady=(0, 12), fill="x")
        self.max_label = ctk.CTkLabel(self.stats_frame, text="Max: -- kg", font=("Montserrat", 15, "bold"))
        self.max_label.grid(row=0, column=0, padx=10, pady=8)
        self.avg_label = ctk.CTkLabel(self.stats_frame, text="Avg: -- kg", font=("Montserrat", 15, "bold"))
        self.avg_label.grid(row=0, column=1, padx=10, pady=8)
        self.rm_label = ctk.CTkLabel(self.stats_frame, text="1RM Est: -- kg", font=("Montserrat", 15, "bold"))
        self.rm_label.grid(row=0, column=2, padx=10, pady=8)

        self.export_button = ctk.CTkButton(self.stats_frame, text="Export", command=self.export_data, width=100, fg_color="#f39c12", hover_color="#b9770e")
        self.export_button.grid(row=0, column=3, padx=10, pady=8)
        self.import_button = ctk.CTkButton(self.stats_frame, text="Import", command=self.import_data, width=100, fg_color="#8e44ad", hover_color="#5e3370")
        self.import_button.grid(row=0, column=4, padx=10, pady=8)

        # --- Plot Area ---
        self.plot_control_frame = ctk.CTkFrame(self.content_frame, corner_radius=12)
        self.plot_control_frame.pack(padx=32, pady=(0, 0), fill="x")
        self.plot_type_var = ctk.StringVar(value="Weight Over Time")
        self.plot_type_combo = ctk.CTkComboBox(self.plot_control_frame, variable=self.plot_type_var, values=["Weight Over Time", "1RM Estimate Over Time"], width=220, command=self.on_plot_type_change)
        self.plot_type_combo.pack(side="left", padx=10, pady=6)

        self.plot_frame = ctk.CTkFrame(self.content_frame, corner_radius=12)
        self.plot_frame.pack(padx=32, pady=(0, 20), fill="both", expand=False)
        self.plot_canvas = None
        self.plot_update()

        self.table_frame = ctk.CTkFrame(self.content_frame, corner_radius=12)
        self.table_frame.pack(padx=32, pady=(0, 20), fill="both", expand=True)

        self.table = ttk.Treeview(self.table_frame, columns=self.data_columns, show="headings", height=8)
        for col in self.data_columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=120)
        self.table.pack(fill="both", expand=True)

        self.refresh_table()

        # Footer
        self.footer_label = ctk.CTkLabel(self, text="Ⓒ Demir Demirörs 2025", font=("Montserrat", 12), anchor="e")
        self.footer_label.pack(side="bottom", pady=(10, 0), anchor="e")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_data(self):
        if os.path.exists("workout_data.csv"):
            try:
                df = pd.read_csv("workout_data.csv")
                # Ensure all columns exist
                for col in self.data_columns:
                    if col not in df.columns:
                        df[col] = ""
                return df[self.data_columns]
            except Exception:
                pass
        return pd.DataFrame(columns=self.data_columns)

    def validate_form(self):
        exercise = self.exercise_var.get().strip()
        date_str = self.date_var.get().strip()
        weight = self.weight_var.get().strip()
        reps = self.reps_var.get().strip()
        # Check required fields
        if not exercise or not date_str or not weight or not reps:
            return False, "All fields are required."
        # Validate date
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False, "Date must be in YYYY-MM-DD format."
        # Validate weight
        try:
            w = float(weight)
            if w <= 0:
                return False, "Weight must be positive."
        except ValueError:
            return False, "Weight must be a number."
        # Validate reps
        try:
            r = int(reps)
            if r <= 0:
                return False, "Reps must be positive."
        except ValueError:
            return False, "Reps must be an integer."
        return True, ""

    def handle_submit(self):
        valid, msg = self.validate_form()
        if not valid:
            self.message_label.configure(text=msg, text_color="#e74c3c")
            return
        self.message_label.configure(text="", text_color="#2ecc71")
        # Add entry to DataFrame
        entry = {
            "Exercise": self.exercise_var.get().strip(),
            "Date": self.date_var.get().strip(),
            "Weight": float(self.weight_var.get().strip()),
            "Reps": int(self.reps_var.get().strip()),
        }
        self.workout_df = pd.concat([
            self.workout_df,
            pd.DataFrame([entry], columns=self.data_columns)
        ], ignore_index=True)
        # Clear form
        self.exercise_var.set("")
        self.date_var.set("")
        self.weight_var.set("")
        self.reps_var.set("")
        self.message_label.configure(text="Entry added!", text_color="#2ecc71")
        self.refresh_table()

    def on_plot_type_change(self, *args):
        self.plot_update()

    def plot_update(self, df=None):
        if df is None:
            df = self.workout_df
        plot_type = self.plot_type_var.get()
        if plot_type == "Weight Over Time":
            self.plot_weight_over_time(df)
        else:
            self.plot_1rm_over_time(df)

    def apply_filters(self):
        df = self.workout_df.copy()
        # Filter by exercise
        exercise = self.filter_exercise_var.get()
        if exercise and exercise != "All":
            df = df[df["Exercise"] == exercise]
        # Filter by date range
        start = self.filter_start_var.get().strip()
        end = self.filter_end_var.get().strip()
        if start:
            try:
                df = df[df["Date"] >= start]
            except Exception:
                pass
        if end:
            try:
                df = df[df["Date"] <= end]
            except Exception:
                pass
        self.refresh_table(df)
        self.update_stats(df)
        self.plot_update(df)

    def refresh_table(self, df=None):
        if df is None:
            df = self.workout_df
        # Clear table
        for row in self.table.get_children():
            self.table.delete(row)
        # Insert all rows from DataFrame
        for _, row in df.iterrows():
            self.table.insert("", "end", values=(row["Exercise"], row["Date"], row["Weight"], row["Reps"]))
        self.update_stats(df)
        self.plot_update(df)

    def update_stats(self, df):
        if df.empty:
            self.max_label.configure(text="Max: -- kg")
            self.avg_label.configure(text="Avg: -- kg")
            self.rm_label.configure(text="1RM Est: -- kg")
            return
        max_weight = df["Weight"].max()
        avg_weight = df["Weight"].mean()
        # Epley 1RM: 1RM = weight * (1 + reps/30)
        df["1RM"] = df.apply(lambda row: row["Weight"] * (1 + row["Reps"] / 30), axis=1)
        max_rm = df["1RM"].max()
        self.max_label.configure(text=f"Max: {max_weight:.1f} kg")
        self.avg_label.configure(text=f"Avg: {avg_weight:.1f} kg")
        self.rm_label.configure(text=f"1RM Est: {max_rm:.1f} kg")

    def plot_weight_over_time(self, df=None):
        if df is None:
            df = self.workout_df
        # Remove previous plot if exists
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        if df.empty:
            label = ctk.CTkLabel(self.plot_frame, text="No data to plot.", font=("Roboto", 14))
            label.pack()
            return
        # Sort by date
        try:
            plot_df = df.copy()
            plot_df = plot_df.sort_values("Date")
            dates = plot_df["Date"].tolist()
            weights = plot_df["Weight"].tolist()
            fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
            ax.plot(dates, weights, marker="o", color="#3498db")
            ax.set_title("Weight Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Weight (kg)")
            ax.grid(True, linestyle=":", alpha=0.5)
            fig.tight_layout()
            self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.plot_canvas.draw()
            self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)
        except Exception:
            label = ctk.CTkLabel(self.plot_frame, text="Error plotting data.", font=("Roboto", 14))
            label.pack()

    def plot_1rm_over_time(self, df=None):
        if df is None:
            df = self.workout_df
        # Remove previous plot if exists
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        if df.empty:
            label = ctk.CTkLabel(self.plot_frame, text="No data to plot.", font=("Roboto", 14))
            label.pack()
            return
        # Sort by date
        try:
            plot_df = df.copy()
            plot_df = plot_df.sort_values("Date")
            plot_df["1RM"] = plot_df.apply(lambda row: row["Weight"] * (1 + row["Reps"] / 30), axis=1)
            dates = plot_df["Date"].tolist()
            rms = plot_df["1RM"].tolist()
            fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
            ax.plot(dates, rms, marker="o", color="#e67e22")
            ax.set_title("1RM Estimate Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("1RM (kg)")
            ax.grid(True, linestyle=":", alpha=0.5)
            fig.tight_layout()
            self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.plot_canvas.draw()
            self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)
        except Exception:
            label = ctk.CTkLabel(self.plot_frame, text="Error plotting data.", font=("Roboto", 14))
            label.pack()

    def export_data(self):
        try:
            # Export to Excel
            self.workout_df.to_excel("workout_data.xlsx", index=False)
            # Export to Markdown
            md = self.workout_df.to_markdown(index=False)
            with open("workout_data.md", "w") as f:
                f.write(md)
            self.message_label.configure(text="Exported to Excel and Markdown!", text_color="#2ecc71")
        except Exception as e:
            self.message_label.configure(text=f"Export failed: {e}", text_color="#e74c3c")

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")])
        if not file_path:
            return
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            # Ensure all columns exist
            for col in self.data_columns:
                if col not in df.columns:
                    df[col] = ""
            self.workout_df = df[self.data_columns]
            self.refresh_table()
            self.message_label.configure(text="Import successful!", text_color="#2ecc71")
        except Exception as e:
            self.message_label.configure(text=f"Import failed: {e}", text_color="#e74c3c")

    def on_close(self):
        # Auto-save to CSV
        try:
            self.workout_df.to_csv("workout_data.csv", index=False)
        except Exception:
            pass
        self.destroy()

    def toggle_theme(self, mode):
        ctk.set_appearance_mode(mode)

if __name__ == "__main__":
    app = FitnessProgressApp()
    app.mainloop() 
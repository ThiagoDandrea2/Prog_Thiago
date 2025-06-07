import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# matplotlib imports for chart embedding
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = "members_data.json"

class HRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Company Members and Dependents - HR Tool")
        self.geometry("1200x760")
        self.configure(bg="#ffffff")
        self.resizable(True, True)

        self.members = []
        self.selected_member_index = None

        self.load_data()
        self.create_header()
        self.create_main_content()
        self.refresh_member_table()
        self.update_summary()
        self.draw_chart()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.members = json.load(f)
                    if not isinstance(self.members, list):
                        self.members = []
            except Exception:
                messagebox.showwarning("Data Load Error", "Failed to load saved data file. Starting with empty data.")
                self.members = []
        else:
            self.members = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.members, f, indent=4)
        except Exception as e:
            messagebox.showerror("Data Save Error", f"Failed to save data: {e}")

    def create_header(self):
        header_frame = tk.Frame(self, bg="#ffffff", height=60)
        header_frame.pack(fill="x", side="top")

        logo_label = tk.Label(header_frame, text="HR Company Tool",
                              font=("Inter", 24, "bold"), fg="#111827", bg="#ffffff")
        logo_label.pack(side="left", padx=24, pady=10)

        nav_frame = tk.Frame(header_frame, bg="#ffffff")
        nav_frame.pack(side="right", padx=24, pady=10)

        home_btn = ttk.Button(nav_frame, text="Home", command=self.nav_home)
        home_btn.pack(side="left", padx=8)
        about_btn = ttk.Button(nav_frame, text="About", command=self.nav_about)
        about_btn.pack(side="left", padx=8)

    def nav_home(self):
        messagebox.showinfo("Navigation", "You are already on Home.")

    def nav_about(self):
        messagebox.showinfo("About", "HR Company Members App v1.0\nDeveloped with Tkinter and Matplotlib.")

    def create_main_content(self):
        main_frame = tk.Frame(self, bg="#ffffff")
        main_frame.pack(expand=True, fill="both", padx=32, pady=24)

        # Left panel: Form card
        form_card = tk.Frame(main_frame, bg="#f9fafb", bd=1, relief="solid", highlightthickness=0)
        form_card.pack(side="left", fill="y", padx=(0, 24), pady=5, ipadx=20, ipady=20)
        form_card.configure(highlightbackground="#e5e7eb", highlightcolor="#e5e7eb")
        form_card.grid_propagate(False)
        form_card.config(width=450, height=720)

        title_label = tk.Label(form_card, text="Member & Dependents Form",
                               font=("Inter", 20, "bold"), bg="#f9fafb", fg="#111827")
        title_label.pack(anchor="w", pady=(0,20))

        self.member_vars = {}
        self.create_label_entry(form_card, "Member ID", "member_id")
        self.create_label_entry(form_card, "Name", "name")
        self.create_label_entry(form_card, "Department", "department")
        self.create_label_entry(form_card, "Position", "position")
        self.create_label_entry(form_card, "Phone", "phone")
        self.create_label_entry(form_card, "Email", "email")

        dep_section_label = tk.Label(form_card, text="Dependents",
                                     font=("Inter", 16, "bold"), bg="#f9fafb", fg="#374151")
        dep_section_label.pack(anchor="w", pady=(20,5))

        self.dependents_frame = tk.Frame(form_card, bg="#f9fafb")
        self.dependents_frame.pack(fill="both", expand=False)

        dep_btn_frame = tk.Frame(form_card, bg="#f9fafb")
        dep_btn_frame.pack(fill="x", pady=(0,10))

        add_dep_btn = ttk.Button(dep_btn_frame, text="Add Dependent", command=self.add_dependent_row)
        add_dep_btn.pack(side="left")

        clear_dep_btn = ttk.Button(dep_btn_frame, text="Clear Dependents", command=self.clear_dependents)
        clear_dep_btn.pack(side="left", padx=10)

        self.dependent_rows = []

        btn_frame = tk.Frame(form_card, bg="#f9fafb")
        btn_frame.pack(fill="x", pady=(30,0))

        self.create_btn = ttk.Button(btn_frame, text="Create New Member", command=self.create_member)
        self.create_btn.pack(fill="x", pady=5)

        self.update_btn = ttk.Button(btn_frame, text="Update Selected Member", command=self.update_member, state="disabled")
        self.update_btn.pack(fill="x", pady=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete Selected Member", command=self.delete_member, state="disabled")
        self.delete_btn.pack(fill="x", pady=5)

        self.clear_form_btn = ttk.Button(btn_frame, text="Clear Form", command=self.clear_form)
        self.clear_form_btn.pack(fill="x", pady=5)

        # Right panel: Table + summary + chart
        right_frame = tk.Frame(main_frame, bg="#ffffff")
        right_frame.pack(side="left", fill="both", expand=True)

        table_label = tk.Label(right_frame, text="Company Members & Dependents",
                               font=("Inter", 20, "bold"), bg="#ffffff", fg="#111827")
        table_label.pack(anchor="w", pady=(0,15), padx=5)

        columns = ("ID", "Name", "Department", "Position", "Phone", "Email", "Dependents Count")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("Name", width=160, anchor="w")
        self.tree.column("Dependents Count", width=140, anchor="center")
        self.tree.pack(fill="both", expand=False, padx=5, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        summary_frame = tk.Frame(right_frame, bg="#f9fafb", bd=1, relief="solid", padx=24, pady=16)
        summary_frame.pack(fill="x", pady=12, padx=5)

        self.emp_count_var = tk.StringVar(value="0")
        self.dep_count_var = tk.StringVar(value="0")

        emp_count_label = tk.Label(summary_frame, text="Total Employees:", font=("Inter", 16, "bold"), fg="#374151", bg="#f9fafb")
        emp_count_label.grid(row=0, column=0, sticky="w")

        emp_count_val = tk.Label(summary_frame, textvariable=self.emp_count_var, font=("Inter", 16), fg="#6b7280", bg="#f9fafb")
        emp_count_val.grid(row=1, column=0, sticky="w", pady=(0,8))

        dep_count_label = tk.Label(summary_frame, text="Total Dependents:", font=("Inter", 16, "bold"), fg="#374151", bg="#f9fafb")
        dep_count_label.grid(row=0, column=1, sticky="w", padx=50)

        dep_count_val = tk.Label(summary_frame, textvariable=self.dep_count_var, font=("Inter", 16), fg="#6b7280", bg="#f9fafb")
        dep_count_val.grid(row=1, column=1, sticky="w", pady=(0,8), padx=50)

        summary_frame.columnconfigure(0, weight=1)
        summary_frame.columnconfigure(1, weight=1)

        # Chart card frame
        chart_card = tk.Frame(right_frame, bg="#f9fafb", bd=1, relief="solid", padx=16, pady=16)
        chart_card.pack(fill="both", expand=True, padx=5, pady=12)

        chart_title = tk.Label(chart_card, text="Employees & Dependents Overview",
                               font=("Inter", 18, "bold"), fg="#111827", bg="#f9fafb")
        chart_title.pack(anchor="w", pady=(0,10))

        # Matplotlib figure for chart
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor("#f9fafb")
        self.ax.set_facecolor("#f9fafb")

        # Remove spines for minimal look
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color("#6b7280")
        self.ax.spines['bottom'].set_color("#6b7280")

        # Set y axis color to gray
        self.ax.yaxis.label.set_color("#6b7280")
        self.ax.xaxis.label.set_color("#6b7280")
        self.ax.tick_params(colors="#6b7280")

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_card)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_label_entry(self, parent, label_text, var_name):
        label = tk.Label(parent, text=label_text, bg="#f9fafb", fg="#374151", font=("Inter", 14, "bold"))
        label.pack(anchor="w", pady=(0,4))
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var, font=("Inter", 12))
        entry.pack(fill="x", pady=(0,12))
        self.member_vars[var_name] = var

    def add_dependent_row(self):
        row_frame = tk.Frame(self.dependents_frame, bg="#f9fafb")
        row_frame.pack(fill="x", pady=4)

        name_var = tk.StringVar()
        rel_var = tk.StringVar()
        age_var = tk.StringVar()

        name_entry = ttk.Entry(row_frame, textvariable=name_var, width=20)
        name_entry.pack(side="left", padx=(0,12))
        name_entry.insert(0, "Name")

        rel_entry = ttk.Entry(row_frame, textvariable=rel_var, width=20)
        rel_entry.pack(side="left", padx=(0,12))
        rel_entry.insert(0, "Relationship")

        age_entry = ttk.Entry(row_frame, textvariable=age_var, width=8)
        age_entry.pack(side="left", padx=(0,12))
        age_entry.insert(0, "Age")

        remove_btn = ttk.Button(row_frame, text="Remove", command=lambda: self.remove_dependent_row(row_frame))
        remove_btn.pack(side="left")

        self.dependent_rows.append({
            "frame": row_frame,
            "name": name_var,
            "relationship": rel_var,
            "age": age_var,
        })

    def remove_dependent_row(self, frame):
        for dep in self.dependent_rows:
            if dep["frame"] == frame:
                dep["frame"].destroy()
                self.dependent_rows.remove(dep)
                break

    def clear_dependents(self):
        for dep in self.dependent_rows:
            dep["frame"].destroy()
        self.dependent_rows.clear()

    def clear_form(self):
        for var in self.member_vars.values():
            var.set("")
        self.clear_dependents()
        self.selected_member_index = None
        self.update_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        self.create_btn.config(state="normal")

    def create_member(self):
        member_data = self.collect_form_data()
        if not member_data:
            return

        for mem in self.members:
            if mem["member_id"] == member_data["member_id"]:
                messagebox.showwarning("Duplicate ID", "Member ID already exists. Use update instead.")
                return

        self.members.append(member_data)
        self.save_data()
        self.refresh_member_table()
        self.clear_form()
        messagebox.showinfo("Success", "Member added successfully.")

    def update_member(self):
        if self.selected_member_index is None:
            messagebox.showwarning("No Selection", "Select a member to update.")
            return

        member_data = self.collect_form_data()
        if not member_data:
            return

        for i, mem in enumerate(self.members):
            if i != self.selected_member_index and mem["member_id"] == member_data["member_id"]:
                messagebox.showwarning("Duplicate ID", "Another member already has this ID.")
                return

        self.members[self.selected_member_index] = member_data
        self.save_data()
        self.refresh_member_table()
        self.clear_form()
        messagebox.showinfo("Success", "Member updated successfully.")

    def delete_member(self):
        if self.selected_member_index is None:
            messagebox.showwarning("No Selection", "Select a member to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?")
        if confirm:
            self.members.pop(self.selected_member_index)
            self.save_data()
            self.refresh_member_table()
            self.clear_form()
            messagebox.showinfo("Deleted", "Member deleted successfully.")

    def collect_form_data(self):
        member_id = self.member_vars["member_id"].get().strip()
        name = self.member_vars["name"].get().strip()
        department = self.member_vars["department"].get().strip()
        position = self.member_vars["position"].get().strip()
        phone = self.member_vars["phone"].get().strip()
        email = self.member_vars["email"].get().strip()

        if not member_id:
            messagebox.showwarning("Input Error", "Member ID is required.")
            return None
        if not name:
            messagebox.showwarning("Input Error", "Member name is required.")
            return None

        dependents = []
        for dep in self.dependent_rows:
            dep_name = dep["name"].get().strip()
            dep_rel = dep["relationship"].get().strip()
            dep_age = dep["age"].get().strip()
            if dep_name or dep_rel or dep_age:
                if dep_age:
                    try:
                        dep_age_int = int(dep_age)
                        if dep_age_int < 0:
                            messagebox.showwarning("Input Error", "Dependent age cannot be negative.")
                            return None
                    except ValueError:
                        messagebox.showwarning("Input Error", f"Dependent age must be a number. Invalid: {dep_age}")
                        return None
                else:
                    dep_age_int = None
                dependents.append({"name": dep_name, "relationship": dep_rel, "age": dep_age_int})

        return {
            "member_id": member_id,
            "name": name,
            "department": department,
            "position": position,
            "phone": phone,
            "email": email,
            "dependents": dependents,
        }

    def refresh_member_table(self):
        self.tree.delete(*self.tree.get_children())
        for idx, member in enumerate(self.members):
            self.tree.insert(
                "",
                "end",
                iid=idx,
                values=(
                    member["member_id"],
                    member["name"],
                    member["department"],
                    member["position"],
                    member["phone"],
                    member["email"],
                    len(member["dependents"])
                )
            )
        self.update_summary()
        self.draw_chart()

    def update_summary(self):
        total_employees = len(self.members)
        total_dependents = sum(len(m["dependents"]) for m in self.members)
        self.emp_count_var.set(str(total_employees))
        self.dep_count_var.set(str(total_dependents))

    def draw_chart(self):
        total_employees = len(self.members)
        total_dependents = sum(len(m["dependents"]) for m in self.members)

        self.ax.clear()
        self.fig.patch.set_facecolor("#f9fafb")
        self.ax.set_facecolor("#f9fafb")

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color("#6b7280")
        self.ax.spines['bottom'].set_color("#6b7280")

        self.ax.yaxis.label.set_color("#6b7280")
        self.ax.xaxis.label.set_color("#6b7280")
        self.ax.tick_params(colors="#6b7280")

        categories = ['Employees', 'Dependents']
        values = [total_employees, total_dependents]
        bar_colors = ['#374151', '#6b7280']  # dark gray and medium gray

        bars = self.ax.bar(categories, values, color=bar_colors, alpha=0.8, width=0.5)

        # Add value labels above bars
        for bar in bars:
            height = bar.get_height()
            self.ax.annotate(f'{height}',
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 6),
                             textcoords="offset points",
                             ha='center', va='bottom',
                             fontsize=12, color="#374151", fontweight='bold')

        self.ax.set_ylim(0, max(values + [1]) * 1.2)  # Add some headroom if zero

        self.ax.set_ylabel('Count', fontsize=14, color="#374151", fontweight='bold')
        self.ax.set_title('Company Size Overview', fontsize=16, fontweight='bold', color="#111827", pad=20)

        self.canvas.draw_idle()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.clear_form()
            return
        idx = int(selected[0])
        self.selected_member_index = idx
        member = self.members[idx]
        self.member_vars["member_id"].set(member["member_id"])
        self.member_vars["name"].set(member["name"])
        self.member_vars["department"].set(member["department"])
        self.member_vars["position"].set(member["position"])
        self.member_vars["phone"].set(member["phone"])
        self.member_vars["email"].set(member["email"])

        self.clear_dependents()
        for d in member["dependents"]:
            self.add_dependent_row()
            last_dep = self.dependent_rows[-1]
            last_dep["name"].set(d.get("name", ""))
            last_dep["relationship"].set(d.get("relationship", ""))
            age_val = d.get("age")
            last_dep["age"].set(str(age_val) if age_val is not None else "")

        self.create_btn.config(state="disabled")
        self.update_btn.config(state="normal")
        self.delete_btn.config(state="normal")


if __name__ == "__main__":
    # Check for matplotlib and required packages
    try:
        import matplotlib
        import matplotlib.backends.backend_tkagg
    except ImportError:
        import sys
        sys.exit("matplotlib is required to run this program. Please install it via 'pip install matplotlib'")

    app = HRApp()
    app.mainloop()


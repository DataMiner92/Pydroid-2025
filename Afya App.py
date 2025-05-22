import sqlite3
from datetime import datetime
import random
import string
import secrets
import re
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import os
import json
import time
import uuid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import csv
try:
    import pandas as pd
except ImportError:
    pd = None  # Excel export will be disabled if pandas is not installed

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        self.root.resizable(TRUE, TRUE)
        self.root.configure(bg="white")

        self.session_token = None
        self.session_expiry = None
        self.session_timeout_minutes = 30  # Session expires after 30 minutes of inactivity
        # ...existing code...

        # Removed invalid usage of 'self' outside of a class or method
        self.apply_theme()
        # Initialize database
        self.initialize_database()
        
        # Create login frame
        self.create_login_frame()
        
        # Initialize main application (will be created after login)
        self.main_frame = None

        # Initialize status variable
        self.status_var = StringVar()
        self.status_var.set("Ready")
    
    def start_session(self, username):
        self.session_token = str(uuid.uuid4())
        self.session_expiry = time.time() + self.session_timeout_minutes * 60
        self.current_user = username

    def is_session_active(self):
        return self.session_token is not None and time.time() < self.session_expiry

    def refresh_session(self):
        if self.session_token:
            self.session_expiry = time.time() + self.session_timeout_minutes * 60

    def end_session(self):
        self.session_token = None
        self.session_expiry = None
        self.current_user = None
    

    def apply_theme(self):
    # Apply a modern theme
        style = ttk.Style()
        style.theme_use("clam")  # Use the 'clam' theme for a modern look

        # Customize button styles
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))
    
    def initialize_database(self):
        try:
            # Initialize database connection and cursor
            self.conn = sqlite3.connect("afya.db")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")

            # Create tables
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER CHECK(age > 0 AND age < 120),
                    gender TEXT CHECK(gender IN ('M', 'F', 'Other')),
                    contact TEXT NOT NULL UNIQUE,
                    department TEXT NOT NULL,
                    doctor_id INTEGER,
                    admission_date TEXT NOT NULL,
                    discharge_date TEXT,
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
                )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_journey (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                stage TEXT NOT NULL, -- e.g., Reception, Triage, Doctor, Pharmacy, Lab
                timestamp TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            )
        """)
        # Add payment_method to patients if not present
        try:
            self.cursor.execute("ALTER TABLE patients ADD COLUMN payment_method TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TEXT NOT NULL
                )
            """)
                # Create users table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('Admin', 'Doctor', 'Receptionist', 'Pharmacist'))
                )
            """)

                # Add a default admin user if no users exist
            self.cursor.execute("SELECT COUNT(*) FROM users")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO users (username, password, role)
                    VALUES ('admin', 'admin123', 'Admin')
                """)
                self.conn.commit()

            # Other table creation logic...
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Database error: {e}")
        
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    contact TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    availability TEXT NOT NULL,
                    department TEXT NOT NULL
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    head_doctor_id INTEGER,
                    description TEXT,
                    FOREIGN KEY (head_doctor_id) REFERENCES doctors(id)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS pharmacy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    medicine_name TEXT NOT NULL UNIQUE,
                    stock INTEGER NOT NULL CHECK(stock >= 0),
                    price REAL NOT NULL CHECK(price > 0),
                    expiry_date TEXT,
                    supplier TEXT
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date TEXT NOT NULL,
                    status TEXT DEFAULT 'Scheduled',
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS issued_medicines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    medicine_id INTEGER NOT NULL,
                    issue_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (medicine_id) REFERENCES pharmacy(id)
                )
            """)

                # Create admissions_log table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS admissions_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    admission_date TEXT NOT NULL,
                    discharge_date TEXT,
                    department TEXT NOT NULL,
                    doctor_id INTEGER,
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                )
            """)
            # Create billing table with the description column
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS billing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    date TEXT NOT NULL,
                    status TEXT DEFAULT 'Pending',
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Database error: {e}")

        def ensure_billing_date_column(self):
            try:
                self.cursor.execute("ALTER TABLE billing ADD COLUMN date TEXT")
                self.conn.commit()
            except sqlite3.OperationalError:
                # Column already exists
                pass

    def create_login_frame(self):
        self.login_frame = Frame(self.root, bg="#f1f1f1")
        self.login_frame.place(relwidth=1, relheight=1)

        header_frame = Frame(self.login_frame, bg="orange")
        header_frame.pack(fill=X)
        Label(header_frame, text="HMS Pro 2025", font=("Arial", 24, "bold"), bg="orange").pack(pady=10)

        # Load background image
        bg_image = PhotoImage(file="C:/Users/user/Desktop/afya.png")
        bg_label = Label(self.login_frame, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection

        login_container = Frame(self.login_frame, bg="#f1f1f1", highlightbackground="orange", highlightthickness=1)
        login_container.config(borderwidth=2, relief="ridge")
        login_container.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(login_container, text="Username:", font=("Arial", 12), bg="#f1f1f1").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        # Fetch usernames from the database
        self.cursor.execute("SELECT username FROM users")
        usernames = [row[0] for row in self.cursor.fetchall()]
        self.username_var = StringVar()
        self.username_dropdown = ttk.Combobox(login_container, textvariable=self.username_var, values=usernames, state="readonly", font=("Arial", 12))
        self.username_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.username_dropdown.set("Select Username")  # Inline text for username dropdown
        if usernames:
            self.username_dropdown.current(0)

        Label(login_container, text="Password:", font=("Arial", 12), bg="#f1f1f1").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.password_entry = Entry(login_container, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.password_entry.insert(0, "Enter Password")  # Inline text for password entry
        self.password_entry.bind("<FocusIn>", lambda event: self.password_entry.delete(0, END))  # Clear inline text on focus

        self.captcha_num1 = random.randint(1, 10)
        self.captcha_num2 = random.randint(1, 10)
        self.captcha_answer = self.captcha_num1 + self.captcha_num2

        Label(login_container, text=f"CAPTCHA: {self.captcha_num1} + {self.captcha_num2} = ?", font=("Arial", 12), bg="#f1f1f1").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.captcha_entry = Entry(login_container, font=("Arial", 12))
        self.captcha_entry.grid(row=2, column=1, padx=10, pady=10)

        # Add "Remember Me" checkbox
        self.remember_me_var = BooleanVar()
        remember_me_checkbox = Checkbutton(login_container, text="Remember Me", variable=self.remember_me_var, bg="#f1f1f1", font=("Arial", 10))
        remember_me_checkbox.grid(row=3, column=0, columnspan=2, pady=5)

        Button(login_container, text="Login", bg="orange", font=("Arial", 12), command=self.login, width=15).grid(row=4, column=0, columnspan=2, pady=20)

        

    def login(self):
        username = self.username_var.get()
        password = self.password_entry.get()
        captcha_input = self.captcha_entry.get()

        # Validate CAPTCHA
        try:
            captcha_input = int(captcha_input)
        except ValueError:
            messagebox.showerror("CAPTCHA Error", "CAPTCHA must be a number")
            return

        if captcha_input != self.captcha_answer:
            if not hasattr(self, 'captcha_attempts'):
                self.captcha_attempts = 0
            self.captcha_attempts += 1

            # Log failed CAPTCHA attempt
            self.log_action("Failed CAPTCHA", f"Username: {username}, Attempt: {self.captcha_attempts}")

            if self.captcha_attempts >= 2:
                self.log_action("Account Lockout", f"Username: {username} locked out after failed CAPTCHA")
                messagebox.showerror("CAPTCHA Error", "Too many failed CAPTCHA attempts. Please try again later.")
                self.notify_admins(f"Account lockout for username: {username} due to repeated failed CAPTCHA.")
                self.login_frame.destroy()
                self.create_login_frame()  # Reset login frame
                return

            messagebox.showerror("CAPTCHA Error", f"Incorrect CAPTCHA. You have {2 - self.captcha_attempts} attempt(s) left.")
            return

        try:
            # Check if the username and password match
            self.cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
            result = self.cursor.fetchone()

            if result:
                self.user_role = result[0]  # Store the user's role
                self.start_session(username)
                self.log_action("Login Success", f"Username: {username}")
                self.login_frame.destroy()
                self.create_main_application()
            else:
                # Log failed login attempt
                if not hasattr(self, 'failed_login_attempts'):
                    self.failed_login_attempts = {}
                self.failed_login_attempts[username] = self.failed_login_attempts.get(username, 0) + 1
                self.log_action("Failed Login", f"Username: {username}, Attempt: {self.failed_login_attempts[username]}")

                # If more than 3 failed attempts, notify admin
                if self.failed_login_attempts[username] >= 3:
                    self.notify_admins(f"Suspicious activity: 3+ failed login attempts for username: {username}")
                    messagebox.showerror("Login Failed", "Too many failed login attempts. Admin has been notified.")
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

        def notify_admins(self, message):
    # Log the notification in audit logs
            self.log_action("Security Alert", message)
            # Optionally, show a popup if an admin is logged in
            if hasattr(self, "user_role") and self.user_role == "Admin":
                messagebox.showwarning("Security Alert", message)

        def bind_enter_key(self):
            self.root.bind('<Return>', lambda event: self.login())

        def sensitive_action(self):
            if not self.is_session_active():
                messagebox.showwarning("Session Expired", "Your session has expired. Please log in again.")
                self.end_session()
                self.create_login_frame()
                return
            self.refresh_session()
            # ...proceed with action...
        
    def create_main_application(self):
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Add background image
        bg_image = PhotoImage(file="C:/Users/user/Desktop/afya.png")
        bg_label = Label(self.main_frame, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection

        # Create menu bar
        self.create_menu_bar()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create tabs based on role
        if self.user_role == "Admin":
            self.create_patient_tab()
            self.create_doctor_tab()
            self.create_department_tab()
            self.create_pharmacy_tab()
            self.create_appointment_tab()
            self.create_report_tab()
            self.create_admissions_tab()
            self.create_billing_tab()
            self.create_user_management_tab()
            self.create_audit_logs_tab()
            self.create_dashboard_tab()
            
        elif self.user_role == "Doctor":
            self.create_patient_tab()
            self.create_appointment_tab()
            self.create_report_tab()
        elif self.user_role == "Receptionist":
            self.create_patient_tab()
            self.create_appointment_tab()
            self.create_billing_tab()
        elif self.user_role == "Pharmacist":
            self.create_pharmacy_tab()
            self.create_billing_tab()

        if self.user_role == "Admin":
            self.cursor.execute("""
                SELECT timestamp, details FROM audit_logs
                WHERE action = 'Security Alert'
                ORDER BY timestamp DESC LIMIT 5
            """)
            alerts = self.cursor.fetchall()
            if alerts:
                alert_text = "\n".join([f"{t}: {d}" for t, d in alerts])
                messagebox.showwarning("Recent Security Alerts", alert_text)

        # Status bar
        self.status_var = StringVar()
        self.status_var.set(f"Logged in as {self.user_role}")
        status_bar = Label(self.main_frame, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor=W)
        status_bar.pack(side=BOTTOM, fill=X)

    def create_user_management_tab(self):
        if self.user_role != "Admin":
            return  # Only admins can access this tab

        self.user_tab = Frame(self.notebook)
        self.notebook.add(self.user_tab, text="User Management")

        # Create user management widgets
        self.user_tree = ttk.Treeview(self.user_tab, columns=("ID", "Username", "Role"), show="headings")
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Role", text="Role")

        self.user_tree.column("ID", width=50)
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Role", width=100)

        self.user_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Buttons frame
        button_frame = Frame(self.user_tab)
        button_frame.pack(fill=X, padx=10, pady=10)

        Button(button_frame, text="Add User", command=self.show_add_user_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edit User", command=self.show_edit_user_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete User", command=self.delete_user).pack(side=LEFT, padx=5)
    
    def delete_user(self):
            selected_item = self.user_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a user to delete")
                return
    
            user_data = self.user_tree.item(selected_item)['values']
            user_id = user_data[0]
    
            confirmation = messagebox.askyesno("Confirm", f"Are you sure you want to delete user {user_data[1]}?")
            if confirmation:
                try:
                    self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    self.conn.commit()
                    messagebox.showinfo("Success", "User deleted successfully")
                    self.refresh_user_list()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Failed to delete user: {e}")
    
    def show_edit_user_dialog(self):
            selected_item = self.user_tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a user to edit")
                return
    
            user_data = self.user_tree.item(selected_item)['values']
    
            dialog = Toplevel(self.root)
            dialog.title("Edit User")
            dialog.geometry("400x300")
            dialog.resizable(False, False)
    
            Label(dialog, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
            username_entry = Entry(dialog)
            username_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
            username_entry.insert(0, user_data[1])
    
            Label(dialog, text="Role:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
            role_var = StringVar(value=user_data[2])
            role_dropdown = ttk.Combobox(dialog, textvariable=role_var, values=["Admin", "Doctor", "Receptionist", "Pharmacist"], state="readonly")
            role_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
    
            Button(dialog, text="Save", command=lambda: self.update_user(
                user_data[0],  # user_id
                username_entry.get(),
                role_var.get(),
                dialog
            )).grid(row=2, column=0, columnspan=2, pady=20)    
    
    def update_user(self, user_id, username, role, dialog):
            if not username or not role:
                messagebox.showerror("Error", "All fields are required")
                return
    
            try:
                self.cursor.execute("UPDATE users SET username = ?, role = ? WHERE id = ?", (username, role, user_id))
                self.conn.commit()
                messagebox.showinfo("Success", "User updated successfully")
                dialog.destroy()
                self.refresh_user_list()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")

        # Load initial user data
            self.refresh_user_list()    

    def refresh_user_list(self):
        # Clear existing data
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        # Fetch users
        self.cursor.execute("SELECT id, username, role FROM users")
        users = self.cursor.fetchall()

        # Populate the table
        for user in users:
            self.user_tree.insert("", END, values=user)

    def show_add_user_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        Label(dialog, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        username_entry = Entry(dialog)
        username_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        Label(dialog, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        password_entry = Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)

        Label(dialog, text="Role:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        role_var = StringVar(value="Receptionist")
        role_dropdown = ttk.Combobox(dialog, textvariable=role_var, values=["Admin", "Doctor", "Receptionist", "Pharmacist"], state="readonly")
        role_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky=EW)

        Button(dialog, text="Save", command=lambda: self.save_user(
            username_entry.get(),
            password_entry.get(),
            role_var.get(),
            dialog
        )).grid(row=3, column=0, columnspan=2, pady=20)

    def save_user(self, username, password, role, dialog):
        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully")
            dialog.destroy()
            self.refresh_user_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def log_action(self, action, details=""):
        username = getattr(self, "username_var", None)
        if isinstance(username, StringVar):
            username = username.get()
        elif hasattr(self, "username_var"):
            username = self.username_var
        else:
            username = "Unknown"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(
                "INSERT INTO audit_logs (username, action, details, timestamp) VALUES (?, ?, ?, ?)",
                (username, action, details, timestamp)
            )
            self.conn.commit()
        except Exception:
            pass  # Avoid recursion if logging fails

    def create_audit_logs_tab(self):
        if self.user_role != "Admin":
            return
        self.audit_tab = Frame(self.notebook)
        self.notebook.add(self.audit_tab, text="Audit Logs")

        tree = ttk.Treeview(self.audit_tab, columns=("ID", "User", "Action", "Details", "Timestamp"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("User", text="User")
        tree.heading("Action", text="Action")
        tree.heading("Details", text="Details")
        tree.heading("Timestamp", text="Timestamp")
        tree.column("ID", width=40)
        tree.column("User", width=100)
        tree.column("Action", width=120)
        tree.column("Details", width=300)
        tree.column("Timestamp", width=140)
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Load logs
        self.cursor.execute("SELECT id, username, action, details, timestamp FROM audit_logs ORDER BY timestamp DESC")
        for row in self.cursor.fetchall():
            tree.insert("", END, values=row)

    def toggle_theme(self):
        current_theme = self.root.cget("bg")
        if current_theme == "white":
            # Switch to dark mode
            self.root.configure(bg="black")
            if self.main_frame:
                self.main_frame.configure(bg="black")
            self.status_var.set("Dark Mode Enabled")
        else:
            # Switch to light mode
            self.root.configure(bg="white")
            if self.main_frame:
                self.main_frame.configure(bg="white")
            self.status_var.set("Light Mode Enabled")

    def ai_chatbot(self):
        dialog = Toplevel(self.root)
        dialog.title("Hospital AI Assistant")
        dialog.geometry("600x400")
        dialog.resizable(False, False)

        # Chat display area
        chat_display = Text(dialog, wrap=WORD, state=DISABLED, height=20, width=70)
        chat_display.pack(pady=10, padx=10)

        # Input area
        input_frame = Frame(dialog)
        input_frame.pack(fill=X, padx=10, pady=10)

        input_label = Label(input_frame, text="You:")
        input_label.pack(side=LEFT, padx=5)

        user_input = Entry(input_frame, width=50)
        user_input.pack(side=LEFT, padx=5, fill=X, expand=True)

        def process_query():
            query = user_input.get().lower().strip()
            user_input.delete(0, END)

            if not query:
                return

            chat_display.config(state=NORMAL)
            chat_display.insert(END, f"You: {query}\n")

            if query in ['exit', 'quit', 'bye']:
                chat_display.insert(END, "AI: Goodbye! Have a nice day.\n")
                chat_display.config(state=DISABLED)
                return

            elif query == 'help':
                response = """
    AI Assistant Commands:
    - help: Show this help message
    - doctors: Information about doctors
    - patients: Information about patients
    - departments: List of departments
    - medicines: Information about available medicines
    - appointments: How to schedule appointments
    - contact: Hospital contact information
    - emergency: Emergency contacts
    - exit: Quit the chatbot
    """
            elif 'doctor' in query:
                self.cursor.execute("SELECT COUNT(*) FROM doctors")
                count = self.cursor.fetchone()[0]
                response = f"We have {count} doctors available. You can:\n- View all doctors in Doctor Management\n- Search for specific doctors by name or specialization\n- Contact the hospital for more information."
            elif 'patient' in query:
                self.cursor.execute("SELECT COUNT(*) FROM patients WHERE discharge_date IS NULL")
                count = self.cursor.fetchone()[0]
                response = f"There are currently {count} patients in our care.\n- Patient records can be accessed by authorized staff\n- Use Patient Management to view or update records."
            elif 'department' in query:
                self.cursor.execute("SELECT name FROM departments")
                depts = [d[0] for d in self.cursor.fetchall()]
                if depts:
                    response = "Our hospital has these departments:\n" + "\n".join(f"- {dept}" for dept in depts) + "\nYou can view more details in Department Management."
                else:
                    response = "Department information is not currently available."
            elif 'medicine' in query or 'pharmacy' in query:
                self.cursor.execute("SELECT COUNT(*) FROM pharmacy WHERE stock > 0")
                count = self.cursor.fetchone()[0]
                response = f"Our pharmacy currently stocks {count} different medicines.\n- View available medicines in Pharmacy Management\n- Contact the pharmacy for prescription information."
            elif 'appointment' in query:
                response = """
    To schedule an appointment:
    1. Visit our reception desk
    2. Call our appointment hotline: +254 (700) 111-1111
    3. Use our online portal (coming soon)

    You'll need:
    - Patient information
    - Preferred doctor (if any)
    - Reason for visit
    """
            elif 'contact' in query:
                response = """
    Hospital Contact Information:
    - Main Phone: +254 (700) 111-1112
    - Emergency: +254 (700) 111-1112
    - Email: info@afyahospital.org
    - Address: 123 Nairobi, Kenya
    - Website: www.afyahospital.org
    """
            elif 'emergency' in query:
                response = """
    Emergency Contacts:
    - Hospital Emergency: +1 (555) 789-9999
    - Ambulance: 911 (or local emergency number)
    - Poison Control: +254 (710) 222-3333
    - Mental Health Crisis: +254 (700) 111-1111

    For immediate life-threatening emergencies, call 911.
    """
            else:
                response = "I'm sorry, I didn't understand that. Type 'help' for available commands."

            chat_display.insert(END, f"AI: {response}\n")
            chat_display.config(state=DISABLED)

        send_button = Button(input_frame, text="Send", command=process_query)
        send_button.pack(side=LEFT, padx=5)

        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

    def backup_database(self):
        backup_file = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Save database backup as"
        )
        
        if not backup_file:
            return
        
        try:
            # Create a backup connection
            backup_conn = sqlite3.connect(backup_file)
            
            # Use the backup API to copy the database
            with backup_conn:
                self.conn.backup(backup_conn)
            
            backup_conn.close()
            messagebox.showinfo("Success", f"Database backup created successfully at:\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")
    
    def restore_database(self):
        backup_file = filedialog.askopenfilename(
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Select database backup to restore"
        )
        
        if not backup_file:
            return
        
        confirmation = messagebox.askyesno(
            "Confirm Restore",
            "WARNING: This will overwrite the current database.\nAre you sure you want to continue?"
        )
        
        if not confirmation:
            return
        
        try:
            # Close the current connection
            self.conn.close()
            
            # Make a temporary copy of the current database (just in case)
            temp_backup = "hospital_backup_before_restore.db"
            if os.path.exists("afya.db"):
                os.replace("afya.db", temp_backup)
            
            # Copy the backup file to the current database file
            import shutil
            shutil.copy(backup_file, "afya.db")
            
            # Reconnect to the database
            self.conn = sqlite3.connect("afya.db")
            self.cursor = self.conn.cursor()
            
            messagebox.showinfo(
                "Success", 
                f"Database restored successfully from:\n{backup_file}\n\n"
                f"Original database was saved as:\n{temp_backup}"
            )
            
            # Refresh all views
            if self.main_frame:
                self.refresh_patient_list()
                self.refresh_doctor_list()
                self.refresh_department_list()
                self.refresh_pharmacy_list()
                self.refresh_appointment_list()
                
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {e}")
            # Try to reconnect to the original database
            try:
                if os.path.exists(temp_backup):
                    os.replace(temp_backup, "afya.db")
                self.conn = sqlite3.connect("afya.db")
                self.cursor = self.conn.cursor()
            except:
                pass
    
    def show_about(self):
        messagebox.showinfo(
            "About Hospital Management System",
            "Hospital Management System\n\n"
            "Version 1.0\n"
            "Developed with Python and Tkinter\n\n"
            "©2025 Hospital Management"
        )
    
    def __del__(self):
        # Close database connection when the application is closed
        if hasattr(self, 'conn'):
            self.conn.close()



    def create_menu_bar(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Backup Database", command=self.backup_database)
        file_menu.add_command(label="Restore Database", command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
         # View menu
        view_menu = Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
        menubar.add_cascade(label="View", menu=view_menu)

        view_menu = Menu(menubar, tearoff=0)
        view_menu.add_command(label="Virtual Assistant", command=self.ai_chatbot)
        menubar.add_cascade(label="Virtual Assistant", menu=view_menu)

        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
    

    def create_patient_tab(self):
        self.patient_tab = Frame(self.notebook)
        self.notebook.add(self.patient_tab, text="Patient Management")
        
        # Create patient management widgets
        self.patient_tree = ttk.Treeview(self.patient_tab, columns=("ID", "Name", "Age", "Gender", "Contact", "Department", "Doctor", "Admission", "Discharge"), show="headings")
        
        # Configure columns
        self.patient_tree.heading("ID", text="ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("Contact", text="Contact")
        self.patient_tree.heading("Department", text="Department")
        self.patient_tree.heading("Doctor", text="Doctor")
        self.patient_tree.heading("Admission", text="Admission Date")
        self.patient_tree.heading("Discharge", text="Discharge Date")
        
        # Set column widths
        self.patient_tree.column("ID", width=50)
        self.patient_tree.column("Name", width=150)
        self.patient_tree.column("Age", width=50)
        self.patient_tree.column("Gender", width=70)
        self.patient_tree.column("Contact", width=120)
        self.patient_tree.column("Department", width=120)
        self.patient_tree.column("Doctor", width=150)
        self.patient_tree.column("Admission", width=150)
        self.patient_tree.column("Discharge", width=150)
        
        self.patient_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        button_frame = Frame(self.patient_tab)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        Button(button_frame, text="Add Patient", command=self.show_add_patient_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edit Patient", command=self.edit_patient).pack(side=LEFT, padx=5)
        Button(button_frame, text="Discharge Patient", command=self.discharge_patient).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.refresh_patient_list).pack(side=LEFT, padx=5)
        Button(button_frame, text="Search", command=self.search_patient_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Reception", command=self.show_reception_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Triage", command=self.show_triage_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Patient Journey", command=lambda: self.show_patient_journey(self.get_selected_patient_id())).pack(side=LEFT, padx=5)
        Button(button_frame, text="Export CSV", command=self.export_patients_csv).pack(side=LEFT, padx=5)
        if pd is not None:
            Button(button_frame, text="Export Excel", command=self.export_patients_excel).pack(side=LEFT, padx=5)

    def export_patients_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Patients Data as CSV"
        )
        if not file_path:
            return

        try:
            self.cursor.execute("""
                SELECT p.id, p.name, p.age, p.gender, p.contact, p.department, 
                       d.name as doctor_name, p.admission_date, p.discharge_date
                FROM patients p
                LEFT JOIN doctors d ON p.doctor_id = d.id
            """)
            patients = self.cursor.fetchall()

            columns = ["ID", "Name", "Age", "Gender", "Contact", "Department", "Doctor", "Admission Date", "Discharge Date"]
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(patients)

            messagebox.showinfo("Success", f"Patients data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

    def export_patients_excel(self):
                if pd is None:
                    messagebox.showerror("Error", "Pandas library is not installed. Please install it to export to Excel.")
                    return
        
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                    title="Save Patients Data as Excel"
                )
                if not file_path:
                    return
        
                try:
                    self.cursor.execute("""
                        SELECT p.id, p.name, p.age, p.gender, p.contact, p.department, 
                            d.name as doctor_name, p.admission_date, p.discharge_date
                        FROM patients p
                        LEFT JOIN doctors d ON p.doctor_id = d.id
                    """)
                    patients = self.cursor.fetchall()
        
                    columns = ["ID", "Name", "Age", "Gender", "Contact", "Department", "Doctor", "Admission Date", "Discharge Date"]
                    df = pd.DataFrame(patients, columns=columns)
                    df.to_excel(file_path, index=False)
                    messagebox.showinfo("Success", f"Patients data exported successfully to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export data: {e}")
        
    

    def show_add_patient_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New Patient")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        
        
        # Form fields
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        age_entry = Entry(dialog)
        age_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Gender:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        gender_var = StringVar(value="M")
        Radiobutton(dialog, text="Male", variable=gender_var, value="M").grid(row=2, column=1, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Female", variable=gender_var, value="F").grid(row=3, column=1, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Other", variable=gender_var, value="Other").grid(row=4, column=1, padx=10, pady=5, sticky=W)
        
        Label(dialog, text="Contact:").grid(row=5, column=0, padx=10, pady=10, sticky=W)
        contact_entry = Entry(dialog)
        contact_entry.grid(row=5, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Department:").grid(row=6, column=0, padx=10, pady=10, sticky=W)
        department_entry = Entry(dialog)
        department_entry.grid(row=6, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Doctor:").grid(row=7, column=0, padx=10, pady=10, sticky=W)
        
        # Get available doctors
        self.cursor.execute("SELECT id, name FROM doctors")
        doctors = self.cursor.fetchall()
        doctor_options = ["None"] + [f"{doc[0]} - {doc[1]}" for doc in doctors]
        doctor_var = StringVar(value="None")
        doctor_dropdown = ttk.Combobox(dialog, textvariable=doctor_var, values=doctor_options, state="readonly")
        doctor_dropdown.grid(row=7, column=1, padx=10, pady=10, sticky=EW)
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Save", command=lambda: self.save_patient(
            name_entry.get(),
            age_entry.get(),
            gender_var.get(),
            contact_entry.get(),
            department_entry.get(),
            doctor_var.get().split(" - ")[0] if doctor_var.get() != "None" else None,
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(dialog, text="Cancel", command=dialog.destroy).grid(row=9, column=0, columnspan=2, pady=20)
    
    def save_patient(self, name, age, gender, contact, department, doctor_id, dialog):
        # Validation
        if not name or not age or not contact or not department:
            messagebox.showerror("Error", "All fields are required except doctor")
            return
        
        try:
            age = int(age)
            if age <= 0 or age >= 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a number between 1 and 119")
            return
        
        if doctor_id == "None":
            doctor_id = None
        
        admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            self.cursor.execute("""
                INSERT INTO patients (name, age, gender, contact, department, doctor_id, admission_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, age, gender, contact, department, doctor_id, admission_date))
            patient_id = self.cursor.lastrowid

            # Log admission
            self.cursor.execute("""
                INSERT INTO admissions_log (patient_id, admission_date, department, doctor_id)
                VALUES (?, ?, ?, ?)
            """, (patient_id, admission_date, department, doctor_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Patient added successfully")
            dialog.destroy()
            self.refresh_patient_list()
            self.refresh_admissions_data()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Contact number already exists in the system")
        
        try:
            self.cursor.execute("ALTER TABLE patients ADD COLUMN payment_method TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # Already exists
    
    def refresh_patient_list(self):
        # Clear existing data
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        # Get patients with doctor names via LEFT JOIN
        self.cursor.execute("""
            SELECT p.id, p.name, p.age, p.gender, p.contact, p.department, 
                   d.name as doctor_name, p.admission_date, p.discharge_date
            FROM patients p
            LEFT JOIN doctors d ON p.doctor_id = d.id
        """)
        
        patients = self.cursor.fetchall()
        
        # Add to treeview
        for patient in patients:
            self.patient_tree.insert("", END, values=patient)
    
    def edit_patient(self):
        selected_item = self.patient_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient to edit")
            return
        
        patient_data = self.patient_tree.item(selected_item)['values']
        
        dialog = Toplevel(self.root)
        dialog.title("Edit Patient")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        
        # Form fields with current data
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        name_entry.insert(0, patient_data[1])
        
        Label(dialog, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        age_entry = Entry(dialog)
        age_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        age_entry.insert(0, patient_data[2])
        
        Label(dialog, text="Gender:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        gender_var = StringVar(value=patient_data[3])
        Radiobutton(dialog, text="Male", variable=gender_var, value="M").grid(row=2, column=1, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Female", variable=gender_var, value="F").grid(row=3, column=1, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Other", variable=gender_var, value="Other").grid(row=4, column=1, padx=10, pady=5, sticky=W)
        
        Label(dialog, text="Contact:").grid(row=5, column=0, padx=10, pady=10, sticky=W)
        contact_entry = Entry(dialog)
        contact_entry.grid(row=5, column=1, padx=10, pady=10, sticky=EW)
        contact_entry.insert(0, patient_data[4])
        
        Label(dialog, text="Department:").grid(row=6, column=0, padx=10, pady=10, sticky=W)
        department_entry = Entry(dialog)
        department_entry.grid(row=6, column=1, padx=10, pady=10, sticky=EW)
        department_entry.insert(0, patient_data[5])
        
        Label(dialog, text="Doctor:").grid(row=7, column=0, padx=10, pady=10, sticky=W)
        
        # Get available doctors
        self.cursor.execute("SELECT id, name FROM doctors")
        doctors = self.cursor.fetchall()
        doctor_options = ["None"] + [f"{doc[0]} - {doc[1]}" for doc in doctors]
        
        # Find current doctor if exists
        current_doctor = "None"
        if patient_data[6]:  # If there's a doctor assigned
            for doc in doctors:
                if doc[1] == patient_data[6]:
                    current_doctor = f"{doc[0]} - {doc[1]}"
                    break
        
        doctor_var = StringVar(value=current_doctor)
        doctor_dropdown = ttk.Combobox(dialog, textvariable=doctor_var, values=doctor_options, state="readonly")
        doctor_dropdown.grid(row=7, column=1, padx=10, pady=10, sticky=EW)
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Update", command=lambda: self.update_patient(
            patient_data[0],  # patient_id
            name_entry.get(),
            age_entry.get(),
            gender_var.get(),
            contact_entry.get(),
            department_entry.get(),
            doctor_var.get().split(" - ")[0] if doctor_var.get() != "None" else None,
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def update_patient(self, patient_id, name, age, gender, contact, department, doctor_id, dialog):
        # Validation
        if not name or not age or not contact or not department:
            messagebox.showerror("Error", "All fields are required except doctor")
            return
        
        try:
            age = int(age)
            if age <= 0 or age >= 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a number between 1 and 119")
            return
        
        if doctor_id == "None":
            doctor_id = None
        
        try:
            self.cursor.execute("""
                UPDATE patients 
                SET name = ?, age = ?, gender = ?, contact = ?, department = ?, doctor_id = ?
                WHERE id = ?
            """, (name, age, gender, contact, department, doctor_id, patient_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Patient updated successfully")
            dialog.destroy()
            self.refresh_patient_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Contact number already exists in the system")
    
    def discharge_patient(self):
        selected_item = self.patient_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient to discharge")
            return
        
        patient_data = self.patient_tree.item(selected_item)['values']
        patient_id = patient_data[0]
        
        # Check if already discharged
        if patient_data[8]:  # discharge_date exists
            messagebox.showinfo("Info", "This patient is already discharged")
            return
        
        confirmation = messagebox.askyesno("Confirm", "Are you sure you want to discharge this patient?")
        if confirmation:
            discharge_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("UPDATE patients SET discharge_date = ? WHERE id = ?", 
                               (discharge_date, patient_id))
            
            # Log discharge
            self.cursor.execute("""
                UPDATE admissions_log 
                SET discharge_date = ? 
                WHERE patient_id = ? AND discharge_date IS NULL
            """, (discharge_date, patient_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Patient discharged successfully")
            self.refresh_patient_list()
            self.refresh_admissions_data()
            
            # Generate discharge report
            self.generate_discharge_report(patient_id)

    def generate_discharge_report(self, patient_id):
        try:
            # Fetch patient details
            self.cursor.execute("""
                SELECT p.name, p.age, p.gender, p.contact, p.department, d.name as doctor_name, p.admission_date, p.discharge_date
                FROM patients p
                LEFT JOIN doctors d ON p.doctor_id = d.id
                WHERE p.id = ?
            """, (patient_id,))
            patient = self.cursor.fetchone()

            # Fetch recommended medicines
            self.cursor.execute("""
                SELECT m.medicine_name, m.price, m.supplier
                FROM issued_medicines im
                JOIN pharmacy m ON im.medicine_id = m.id
                WHERE im.patient_id = ?
            """, (patient_id,))
            medicines = self.cursor.fetchall()

            # Fetch diagnosis (if stored in a separate table or as notes)
            self.cursor.execute("""
                SELECT notes
                FROM appointments
                WHERE patient_id = ? AND status = 'Completed'
                ORDER BY appointment_date DESC LIMIT 1
            """, (patient_id,))
            diagnosis = self.cursor.fetchone()

            # Generate report
            report = f"Discharge Report\n{'='*50}\n"
            report += f"Name: {patient[0]}\n"
            report += f"Age: {patient[1]}\n"
            report += f"Gender: {patient[2]}\n"
            report += f"Contact: {patient[3]}\n"
            report += f"Department: {patient[4]}\n"
            report += f"Doctor in Charge: {patient[5]}\n"
            report += f"Admission Date: {patient[6]}\n"
            report += f"Discharge Date: {patient[7]}\n\n"

            report += "Diagnosis:\n"
            report += f"{diagnosis[0] if diagnosis else 'No diagnosis available'}\n\n"

            report += "Medicines Recommended:\n"
            if medicines:
                for med in medicines:
                    report += f"- {med[0]} (Price: {med[1]}, Supplier: {med[2]})\n"
            else:
                report += "No medicines recommended.\n"

            # Display report in a new window
            dialog = Toplevel(self.root)
            dialog.title("Discharge Report")
            dialog.geometry("600x400")
            dialog.resizable(False, False)

            report_text = Text(dialog, wrap=WORD, height=20, width=70)
            report_text.insert(END, report)
            report_text.config(state=DISABLED)
            report_text.pack(pady=10, padx=10)

            Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to generate discharge report: {e}")
    
    def search_patient_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Search Patients")
        dialog.geometry("400x700")
        dialog.resizable(False, False)
        
        Label(dialog, text="Search by:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        search_var = StringVar(value="name")
        Radiobutton(dialog, text="Name", variable=search_var, value="name").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Contact", variable=search_var, value="contact").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="ID", variable=search_var, value="id").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        Label(dialog, text="Search term:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        term_entry = Entry(dialog)
        term_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        
        button_frame = Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text="Search", command=lambda: self.search_patient(
            search_var.get(),
            term_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def search_patient(self, search_by, term, dialog):
        if not term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Clear existing data
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        if search_by == "name":
            self.cursor.execute("""
                SELECT p.id, p.name, p.age, p.gender, p.contact, p.department, 
                       d.name as doctor_name, p.admission_date, p.discharge_date
                FROM patients p
                LEFT JOIN doctors d ON p.doctor_id = d.id
                WHERE p.name LIKE ?
            """, (f"%{term}%",))
        elif search_by == "contact":
            self.cursor.execute("""
                SELECT p.id, p.name, p.age, p.gender, p.contact, p.department, 
                       d.name as doctor_name, p.admission_date, p.discharge_date
                FROM patients p
                LEFT JOIN doctors d ON p.doctor_id = d.id
                WHERE p.contact LIKE ?
            """, (f"%{term}%",))
        elif search_by == "id":
            self.cursor.execute("""
                SELECT p.id, p.name, p.age, p.gender, p.contact, p.department, 
                       d.name as doctor_name, p.admission_date, p.discharge_date
                FROM patients p
                LEFT JOIN doctors d ON p.doctor_id = d.id
                WHERE p.id = ?
            """, (term,))
        
        patients = self.cursor.fetchall()
        
        if not patients:
            messagebox.showinfo("Info", "No matching patients found")
            return
        
        # Add to treeview
        for patient in patients:
            self.patient_tree.insert("", END, values=patient)
        
        dialog.destroy()
    
    
    def create_doctor_tab(self):
        self.doctor_tab = Frame(self.notebook)
        self.notebook.add(self.doctor_tab, text="Doctor Management")
        
        # Create doctor management widgets
        self.doctor_tree = ttk.Treeview(self.doctor_tab, columns=("ID", "Name", "Specialization", "Department", "Contact", "Email", "Availability"), show="headings")
        
        # Configure columns
        self.doctor_tree.heading("ID", text="ID")
        self.doctor_tree.heading("Name", text="Name")
        self.doctor_tree.heading("Specialization", text="Specialization")
        self.doctor_tree.heading("Department", text="Department")
        self.doctor_tree.heading("Contact", text="Contact")
        self.doctor_tree.heading("Email", text="Email")
        self.doctor_tree.heading("Availability", text="Availability")
        
        # Set column widths
        self.doctor_tree.column("ID", width=50)
        self.doctor_tree.column("Name", width=150)
        self.doctor_tree.column("Specialization", width=150)
        self.doctor_tree.column("Department", width=120)
        self.doctor_tree.column("Contact", width=120)
        self.doctor_tree.column("Email", width=150)
        self.doctor_tree.column("Availability", width=150)
        
        self.doctor_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        button_frame = Frame(self.doctor_tab)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        Button(button_frame, text="Add Doctor", command=self.show_add_doctor_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edit Doctor", command=self.edit_doctor).pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete Doctor", command=self.delete_doctor).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.refresh_doctor_list).pack(side=LEFT, padx=5)
        Button(button_frame, text="Search", command=self.search_doctor_dialog).pack(side=LEFT, padx=5)
        
        # Load initial doctor data
        self.refresh_doctor_list()
    
    def show_add_doctor_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New Doctor")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        
        # Form fields
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Specialization:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        specialization_entry = Entry(dialog)
        specialization_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Department:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        department_entry = Entry(dialog)
        department_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Contact:").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        contact_entry = Entry(dialog)
        contact_entry.grid(row=3, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Email:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        email_entry = Entry(dialog)
        email_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Availability:").grid(row=5, column=0, padx=10, pady=10, sticky=W)
        availability_entry = Entry(dialog)
        availability_entry.grid(row=5, column=1, padx=10, pady=10, sticky=EW)
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Save", command=lambda: self.save_doctor(
            name_entry.get(),
            specialization_entry.get(),
            department_entry.get(),
            contact_entry.get(),
            email_entry.get(),
            availability_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def save_doctor(self, name, specialization, department, contact, email, availability, dialog):
        # Validation
        if not name or not specialization or not department or not contact or not availability:
            messagebox.showerror("Error", "All fields except email are required")
            return
        
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO doctors (name, specialization, department, contact, email, availability)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, specialization, department, contact, email or None, availability))
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor added successfully")
            dialog.destroy()
            self.refresh_doctor_list()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def refresh_doctor_list(self):
        # Clear existing data
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        
        # Get all doctors
        self.cursor.execute("SELECT id, name, specialization, department, contact, email, availability FROM doctors")
        doctors = self.cursor.fetchall()
        
        # Add to treeview
        for doctor in doctors:
            self.doctor_tree.insert("", END, values=doctor)
    
    def edit_doctor(self):
        selected_item = self.doctor_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a doctor to edit")
            return
        
        doctor_data = self.doctor_tree.item(selected_item)['values']
        
        dialog = Toplevel(self.root)
        dialog.title("Edit Doctor")
        dialog.geometry("500x700")
        dialog.resizable(False, False)
        
        # Form fields with current data
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        name_entry.insert(0, doctor_data[1])
        
        Label(dialog, text="Specialization:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        specialization_entry = Entry(dialog)
        specialization_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        specialization_entry.insert(0, doctor_data[2])
        
        Label(dialog, text="Department:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        department_entry = Entry(dialog)
        department_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        department_entry.insert(0, doctor_data[3])
        
        Label(dialog, text="Contact:").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        contact_entry = Entry(dialog)
        contact_entry.grid(row=3, column=1, padx=10, pady=10, sticky=EW)
        contact_entry.insert(0, doctor_data[4])
        
        Label(dialog, text="Email:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        email_entry = Entry(dialog)
        email_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        email_entry.insert(0, doctor_data[5] if doctor_data[5] else "")
        
        Label(dialog, text="Availability:").grid(row=5, column=0, padx=10, pady=10, sticky=W)
        availability_entry = Entry(dialog)
        availability_entry.grid(row=5, column=1, padx=10, pady=10, sticky=EW)
        availability_entry.insert(0, doctor_data[6])
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Update", command=lambda: self.update_doctor(
            doctor_data[0],  # doctor_id
            name_entry.get(),
            specialization_entry.get(),
            department_entry.get(),
            contact_entry.get(),
            email_entry.get(),
            availability_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def update_doctor(self, doctor_id, name, specialization, department, contact, email, availability, dialog):
        # Validation
        if not name or not specialization or not department or not contact or not availability:
            messagebox.showerror("Error", "All fields except email are required")
            return
        
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        try:
            self.cursor.execute("""
                UPDATE doctors 
                SET name = ?, specialization = ?, department = ?, contact = ?, email = ?, availability = ?
                WHERE id = ?
            """, (name, specialization, department, contact, email or None, availability, doctor_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor updated successfully")
            dialog.destroy()
            self.refresh_doctor_list()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def delete_doctor(self):
        selected_item = self.doctor_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        doctor_data = self.doctor_tree.item(selected_item)['values']
        doctor_id = doctor_data[0]
        
        # Check if doctor is assigned to any patients
        self.cursor.execute("SELECT id FROM patients WHERE doctor_id = ?", (doctor_id,))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Cannot delete doctor. They are assigned to patients.")
            return
        
        # Check if doctor is head of any department
        self.cursor.execute("SELECT id FROM departments WHERE head_doctor_id = ?", (doctor_id,))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Cannot delete doctor. They are head of a department.")
            return
        
        confirmation = messagebox.askyesno("Confirm", f"Are you sure you want to delete doctor {doctor_data[1]}?")
        if confirmation:
            self.cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor deleted successfully")
            self.refresh_doctor_list()
    
    def search_doctor_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Search Doctors")
        dialog.geometry("400x700")
        dialog.resizable(False, False)
        
        Label(dialog, text="Search by:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        search_var = StringVar(value="name")
        Radiobutton(dialog, text="Name", variable=search_var, value="name").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Specialization", variable=search_var, value="specialization").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Department", variable=search_var, value="department").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        Label(dialog, text="Search term:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        term_entry = Entry(dialog)
        term_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        
        button_frame = Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text="Search", command=lambda: self.search_doctor(
            search_var.get(),
            term_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def search_doctor(self, search_by, term, dialog):
        if not term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Clear existing data
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        
        if search_by == "name":
            self.cursor.execute("SELECT * FROM doctors WHERE name LIKE ?", (f"%{term}%",))
        elif search_by == "specialization":
            self.cursor.execute("SELECT * FROM doctors WHERE specialization LIKE ?", (f"%{term}%",))
        elif search_by == "department":
            self.cursor.execute("SELECT * FROM doctors WHERE department LIKE ?", (f"%{term}%",))
        
        doctors = self.cursor.fetchall()
        
        if not doctors:
            messagebox.showinfo("Info", "No matching doctors found")
            return
        
        # Add to treeview
        for doctor in doctors:
            self.doctor_tree.insert("", END, values=doctor)
        
        dialog.destroy()
    
    def create_department_tab(self):
        self.department_tab = Frame(self.notebook)
        self.notebook.add(self.department_tab, text="Department Management")
        
        # Create department management widgets
        self.department_tree = ttk.Treeview(self.department_tab, columns=("ID", "Name", "Head Doctor", "Description"), show="headings")
        
        # Configure columns
        self.department_tree.heading("ID", text="ID")
        self.department_tree.heading("Name", text="Name")
        self.department_tree.heading("Head Doctor", text="Head Doctor")
        self.department_tree.heading("Description", text="Description")
        
        # Set column widths
        self.department_tree.column("ID", width=50)
        self.department_tree.column("Name", width=200)
        self.department_tree.column("Head Doctor", width=200)
        self.department_tree.column("Description", width=300)
        
        self.department_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        button_frame = Frame(self.department_tab)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        Button(button_frame, text="Add Department", command=self.show_add_department_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edit Department", command=self.edit_department).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.refresh_department_list).pack(side=LEFT, padx=5)
        
        # Load initial department data
        self.refresh_department_list()
    
    def show_add_department_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New Department")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        # Form fields
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Head Doctor:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        
        # Get available doctors
        self.cursor.execute("SELECT id, name FROM doctors")
        doctors = self.cursor.fetchall()
        doctor_options = ["None"] + [f"{doc[0]} - {doc[1]}" for doc in doctors]
        doctor_var = StringVar(value="None")
        doctor_dropdown = ttk.Combobox(dialog, textvariable=doctor_var, values=doctor_options, state="readonly")
        doctor_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        description_entry = Text(dialog, height=5, width=40)
        description_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Save", command=lambda: self.save_department(
            name_entry.get(),
            doctor_var.get().split(" - ")[0] if doctor_var.get() != "None" else None,
            description_entry.get("1.0", END).strip(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def save_department(self, name, head_doctor_id, description, dialog):
        if not name:
            messagebox.showerror("Error", "Department name is required")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO departments (name, head_doctor_id, description)
                VALUES (?, ?, ?)
            """, (name, head_doctor_id, description or None))
            self.conn.commit()
            messagebox.showinfo("Success", "Department added successfully")
            dialog.destroy()
            self.refresh_department_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Department name already exists")
    
    def refresh_department_list(self):
        # Clear existing data
        for item in self.department_tree.get_children():
            self.department_tree.delete(item)
        
        # Get departments with head doctor names via LEFT JOIN
        self.cursor.execute("""
            SELECT d.id, d.name, doc.name as head_doctor, d.description
            FROM departments d
            LEFT JOIN doctors doc ON d.head_doctor_id = doc.id
        """)
        
        departments = self.cursor.fetchall()
        
        # Add to treeview
        for dept in departments:
            self.department_tree.insert("", END, values=dept)
    
    def edit_department(self):
        selected_item = self.department_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a department to edit")
            return
        
        dept_data = self.department_tree.item(selected_item)['values']
        
        dialog = Toplevel(self.root)
        dialog.title("Edit Department")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        # Form fields with current data
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        name_entry.insert(0, dept_data[1])
        
        Label(dialog, text="Head Doctor:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        
        # Get available doctors
        self.cursor.execute("SELECT id, name FROM doctors")
        doctors = self.cursor.fetchall()
        doctor_options = ["None"] + [f"{doc[0]} - {doc[1]}" for doc in doctors]
        
        # Find current head doctor if exists
        current_doctor = "None"
        if dept_data[2]:  # If there's a head doctor
            for doc in doctors:
                if doc[1] == dept_data[2]:
                    current_doctor = f"{doc[0]} - {doc[1]}"
                    break
        
        doctor_var = StringVar(value=current_doctor)
        doctor_dropdown = ttk.Combobox(dialog, textvariable=doctor_var, values=doctor_options, state="readonly")
        doctor_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        description_entry = Text(dialog, height=5, width=40)
        description_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        description_entry.insert("1.0", dept_data[3] if dept_data[3] else "")
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Update", command=lambda: self.update_department(
            dept_data[0],  # department_id
            name_entry.get(),
            doctor_var.get().split(" - ")[0] if doctor_var.get() != "None" else None,
            description_entry.get("1.0", END).strip(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def update_department(self, department_id, name, head_doctor_id, description, dialog):
        if not name:
            messagebox.showerror("Error", "Department name is required")
            return
        
        try:
            self.cursor.execute("""
                UPDATE departments 
                SET name = ?, head_doctor_id = ?, description = ?
                WHERE id = ?
            """, (name, head_doctor_id, description or None, department_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Department updated successfully")
            dialog.destroy()
            self.refresh_department_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Department name already exists")
    
    def create_pharmacy_tab(self):
        self.pharmacy_tab = Frame(self.notebook)
        self.notebook.add(self.pharmacy_tab, text="Pharmacy Management")
        
        # Create pharmacy management widgets
        self.pharmacy_tree = ttk.Treeview(self.pharmacy_tab, columns=("ID", "Name", "Stock", "Price", "Expiry", "Supplier"), show="headings")
        
        # Configure columns
        self.pharmacy_tree.heading("ID", text="ID")
        self.pharmacy_tree.heading("Name", text="Name")
        self.pharmacy_tree.heading("Stock", text="Stock")
        self.pharmacy_tree.heading("Price", text="Price")
        self.pharmacy_tree.heading("Expiry", text="Expiry Date")
        self.pharmacy_tree.heading("Supplier", text="Supplier")
        
        # Set column widths
        self.pharmacy_tree.column("ID", width=50)
        self.pharmacy_tree.column("Name", width=200)
        self.pharmacy_tree.column("Stock", width=80)
        self.pharmacy_tree.column("Price", width=80)
        self.pharmacy_tree.column("Expiry", width=100)
        self.pharmacy_tree.column("Supplier", width=150)
        
        self.pharmacy_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        button_frame = Frame(self.pharmacy_tab)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        Button(button_frame, text="Add Medicine", command=self.show_add_medicine_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Edit Medicine", command=self.edit_medicine).pack(side=LEFT, padx=5)
        Button(button_frame, text="Restock", command=self.restock_medicine_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.refresh_pharmacy_list).pack(side=LEFT, padx=5)
        Button(button_frame, text="Search", command=self.search_medicine_dialog).pack(side=LEFT, padx=5)
        
        # Load initial pharmacy data
        self.refresh_pharmacy_list()
    
    def show_add_medicine_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add New Medicine")
        dialog.geometry("500x700")
        dialog.resizable(False, False)
        
        # Form fields
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Stock:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        stock_entry = Entry(dialog)
        stock_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Price:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        price_entry = Entry(dialog)
        price_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Expiry Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        expiry_entry = Entry(dialog)
        expiry_entry.grid(row=3, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Supplier:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        supplier_entry = Entry(dialog)
        supplier_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Save", command=lambda: self.save_medicine(
            name_entry.get(),
            stock_entry.get(),
            price_entry.get(),
            expiry_entry.get(),
            supplier_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def save_medicine(self, name, stock, price, expiry, supplier, dialog):
        # Validation
        if not name or not stock or not price:
            messagebox.showerror("Error", "Name, stock and price are required")
            return
        
        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Stock must be a positive integer")
            return
        
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Price must be a positive number")
            return
        
        if expiry and not re.match(r'^\d{4}-\d{2}-\d{2}$', expiry):
            messagebox.showerror("Error", "Expiry date must be in YYYY-MM-DD format")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO pharmacy (medicine_name, stock, price, expiry_date, supplier)
                VALUES (?, ?, ?, ?, ?)
            """, (name, stock, price, expiry or None, supplier or None))
            self.conn.commit()
            messagebox.showinfo("Success", "Medicine added successfully")
            dialog.destroy()
            self.refresh_pharmacy_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Medicine name already exists")
    
    def refresh_pharmacy_list(self):
        # Clear existing data
        for item in self.pharmacy_tree.get_children():
            self.pharmacy_tree.delete(item)
        
        # Get all medicines
        self.cursor.execute("SELECT id, medicine_name, stock, price, expiry_date, supplier FROM pharmacy")
        medicines = self.cursor.fetchall()
        
        # Add to treeview
        for med in medicines:
            self.pharmacy_tree.insert("", END, values=med)
    
    def edit_medicine(self):
        selected_item = self.pharmacy_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a medicine to edit")
            return
        
        med_data = self.pharmacy_tree.item(selected_item)['values']
        
        dialog = Toplevel(self.root)
        dialog.title("Edit Medicine")
        dialog.geometry("500x700")
        dialog.resizable(False, False)
        
        # Form fields with current data
        Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        name_entry = Entry(dialog)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        name_entry.insert(0, med_data[1])
        
        Label(dialog, text="Stock:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        stock_entry = Entry(dialog)
        stock_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        stock_entry.insert(0, med_data[2])
        
        Label(dialog, text="Price:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        price_entry = Entry(dialog)
        price_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        price_entry.insert(0, med_data[3])
        
        Label(dialog, text="Expiry Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        expiry_entry = Entry(dialog)
        expiry_entry.grid(row=3, column=1, padx=10, pady=10, sticky=EW)
        expiry_entry.insert(0, med_data[4] if med_data[4] else "")
        
        Label(dialog, text="Supplier:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        supplier_entry = Entry(dialog)
        supplier_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        supplier_entry.insert(0, med_data[5] if med_data[5] else "")
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Update", command=lambda: self.update_medicine(
            med_data[0],  # medicine_id
            name_entry.get(),
            stock_entry.get(),
            price_entry.get(),
            expiry_entry.get(),
            supplier_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def update_medicine(self, medicine_id, name, stock, price, expiry, supplier, dialog):
        # Validation
        if not name or not stock or not price:
            messagebox.showerror("Error", "Name, stock and price are required")
            return
        
        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Stock must be a positive integer")
            return
        
        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Price must be a positive number")
            return
        
        if expiry and not re.match(r'^\d{4}-\d{2}-\d{2}$', expiry):
            messagebox.showerror("Error", "Expiry date must be in YYYY-MM-DD format")
            return
        
        try:
            self.cursor.execute("""
                UPDATE pharmacy 
                SET medicine_name = ?, stock = ?, price = ?, expiry_date = ?, supplier = ?
                WHERE id = ?
            """, (name, stock, price, expiry or None, supplier or None, medicine_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Medicine updated successfully")
            dialog.destroy()
            self.refresh_pharmacy_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Medicine name already exists")
    
    def restock_medicine_dialog(self):
        selected_item = self.pharmacy_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a medicine to restock")
            return
        
        med_data = self.pharmacy_tree.item(selected_item)['values']
        
        dialog = Toplevel(self.root)
        dialog.title("Restock Medicine")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        Label(dialog, text=f"Medicine: {med_data[1]}").pack(pady=10)
        Label(dialog, text=f"Current Stock: {med_data[2]}").pack(pady=5)
        
        Label(dialog, text="Quantity to add:").pack(pady=10)
        quantity_entry = Entry(dialog)
        quantity_entry.pack(pady=5)
        
        button_frame = Frame(dialog)
        button_frame.pack(pady=20)
        
        Button(button_frame, text="Restock", command=lambda: self.restock_medicine(
            med_data[0],  # medicine_id
            med_data[2],  # current stock
            quantity_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def restock_medicine(self, medicine_id, current_stock, quantity, dialog):
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return
        
        new_stock = int(current_stock) + quantity
        
        self.cursor.execute("UPDATE pharmacy SET stock = ? WHERE id = ?", 
                          (new_stock, medicine_id))
        self.conn.commit()
        messagebox.showinfo("Success", f"Medicine restocked successfully. New stock: {new_stock}")
        dialog.destroy()
        self.refresh_pharmacy_list()
    
    def search_medicine_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Search Medicines")
        dialog.geometry("400x700")
        dialog.resizable(False, False)
        
        Label(dialog, text="Search by:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        search_var = StringVar(value="name")
        Radiobutton(dialog, text="Name", variable=search_var, value="name").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Supplier", variable=search_var, value="supplier").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Low Stock (<10)", variable=search_var, value="low_stock").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        Label(dialog, text="Search term:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        term_entry = Entry(dialog)
        term_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        
        button_frame = Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text="Search", command=lambda: self.search_medicine(
            search_var.get(),
            term_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def search_medicine(self, search_by, term, dialog):
        # Clear existing data
        for item in self.pharmacy_tree.get_children():
            self.pharmacy_tree.delete(item)
        
        if search_by == "name":
            if not term:
                messagebox.showwarning("Warning", "Please enter a search term")
                return
            self.cursor.execute("SELECT * FROM pharmacy WHERE medicine_name LIKE ?", (f"%{term}%",))
        elif search_by == "supplier":
            if not term:
                messagebox.showwarning("Warning", "Please enter a search term")
                return
            self.cursor.execute("SELECT * FROM pharmacy WHERE supplier LIKE ?", (f"%{term}%",))
        elif search_by == "low_stock":
            self.cursor.execute("SELECT * FROM pharmacy WHERE stock < 10")
        
        medicines = self.cursor.fetchall()
        
        if not medicines:
            messagebox.showinfo("Info", "No matching medicines found")
            return
        
        # Add to treeview
        for med in medicines:
            self.pharmacy_tree.insert("", END, values=med)
        
        dialog.destroy()
    
    def issue_medicine(self, patient_id, medicine_id, quantity):
        try:
            # Check stock availability
            self.cursor.execute("SELECT stock FROM pharmacy WHERE id = ?", (medicine_id,))
            stock = self.cursor.fetchone()[0]
            if stock < quantity:
                messagebox.showerror("Error", "Not enough stock available")
                return

            # Update stock
            new_stock = stock - quantity
            self.cursor.execute("UPDATE pharmacy SET stock = ? WHERE id = ?", (new_stock, medicine_id))

            # Record issued medicine
            self.cursor.execute("""
                INSERT INTO issued_medicines (patient_id, medicine_id, issue_date)
                VALUES (?, ?, ?)
            """, (patient_id, medicine_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            # Log the pharmacy stage in the patient journey
            self.cursor.execute(
                "INSERT INTO patient_journey (patient_id, stage, timestamp, details) VALUES (?, ?, ?, ?)",
                (patient_id, "Pharmacy", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Issued {quantity} units of medicine ID {medicine_id}")
            )
            self.conn.commit()

            messagebox.showinfo("Success", "Medicine issued and patient journey updated.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to issue medicine: {e}")
        # ...existing code to check stock, update stock, etc...
        self.cursor.execute("""
            INSERT INTO issued_medicines (patient_id, medicine_id, issue_date)
            VALUES (?, ?, ?)
        """, (patient_id, medicine_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

        # Log the pharmacy stage in the patient journey
        self.cursor.execute(
            "INSERT INTO patient_journey (patient_id, stage, timestamp, details) VALUES (?, ?, ?, ?)",
            (patient_id, "Pharmacy", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Medicine issued")
        )
        self.conn.commit()

        messagebox.showinfo("Success", "Medicine issued and patient journey updated.")

    
    def create_appointment_tab(self):
        self.appointment_tab = Frame(self.notebook)
        self.notebook.add(self.appointment_tab, text="Appointment Management")
        
        # Create appointment management widgets
        self.appointment_tree = ttk.Treeview(self.appointment_tab, columns=("ID", "Patient", "Doctor", "Date", "Status", "Notes"), show="headings")
        
        # Configure columns
        self.appointment_tree.heading("ID", text="ID")
        self.appointment_tree.heading("Patient", text="Patient")
        self.appointment_tree.heading("Doctor", text="Doctor")
        self.appointment_tree.heading("Date", text="Date")
        self.appointment_tree.heading("Status", text="Status")
        self.appointment_tree.heading("Notes", text="Notes")
        
        # Set column widths
        self.appointment_tree.column("ID", width=50)
        self.appointment_tree.column("Patient", width=150)
        self.appointment_tree.column("Doctor", width=150)
        self.appointment_tree.column("Date", width=150)
        self.appointment_tree.column("Status", width=100)
        self.appointment_tree.column("Notes", width=200)
        
        self.appointment_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        button_frame = Frame(self.appointment_tab)
        button_frame.pack(fill=X, padx=10, pady=10)
        
        Button(button_frame, text="Schedule Appointment", command=self.show_schedule_appointment_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Update Status", command=self.update_appointment_status).pack(side=LEFT, padx=5)
        Button(button_frame, text="Cancel Appointment", command=self.cancel_appointment).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.refresh_appointment_list).pack(side=LEFT, padx=5)
        Button(button_frame, text="Search", command=self.search_appointment_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Export CSV", command=self.export_appointments_csv).pack(side=LEFT, padx=5)
            # Load initial appointment data
        self.refresh_appointment_list()
    
    def export_appointments_csv(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return
            self.cursor.execute("""
                SELECT a.id, p.name, d.name, a.appointment_date, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
            """)
            rows = self.cursor.fetchall()
            headers = ["ID", "Patient", "Doctor", "Date", "Status", "Notes"]
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            messagebox.showinfo("Export", f"Appointment data exported to {file_path}")


    def show_schedule_appointment_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Schedule Appointment")
        dialog.geometry("500x700")
        dialog.resizable(False, False)
        
        # Get available patients
        self.cursor.execute("SELECT id, name FROM patients")
        patients = self.cursor.fetchall()
        
        if not patients:
            messagebox.showwarning("Warning", "No patients available. Please add patients first.")
            dialog.destroy()
            return
        
        Label(dialog, text="Patient:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        patient_var = StringVar()
        patient_dropdown = ttk.Combobox(dialog, textvariable=patient_var, 
                                      values=[f"{p[0]} - {p[1]}" for p in patients], 
                                      state="readonly")
        patient_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=EW)
        
        # Get available doctors
        self.cursor.execute("SELECT id, name FROM doctors")
        doctors = self.cursor.fetchall()
        
        if not doctors:
            messagebox.showwarning("Warning", "No doctors available. Please add doctors first.")
            dialog.destroy()
            return
        
        Label(dialog, text="Doctor:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        doctor_var = StringVar()
        doctor_dropdown = ttk.Combobox(dialog, textvariable=doctor_var, 
                                      values=[f"{d[0]} - {d[1]}" for d in doctors], 
                                      state="readonly")
        doctor_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky=EW)
        
        Label(dialog, text="Date and Time:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        date_entry = Entry(dialog)
        date_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        Label(dialog, text="Notes:").grid(row=3, column=0, padx=10, pady=10, sticky=W)
        notes_entry = Text(dialog, height=5, width=40)
        notes_entry.grid(row=3, column=1, padx=10, pady=10, sticky=EW)
        
        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        Button(button_frame, text="Schedule", command=lambda: self.save_appointment(
            patient_var.get().split(" - ")[0],
            doctor_var.get().split(" - ")[0],
            date_entry.get(),
            notes_entry.get("1.0", END).strip(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
        Button(button_frame, text="Export CSV", command=self.export_appointments_csv).pack(side=LEFT, padx=5)


    
    
    def save_appointment(self, patient_id, doctor_id, date_time, notes, dialog):
        if not patient_id or not doctor_id or not date_time:
            messagebox.showerror("Error", "Patient, doctor and date/time are required")
            return
        
        try:
            # Validate date format
            datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD HH:MM")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes)
                VALUES (?, ?, ?, ?)
            """, (patient_id, doctor_id, date_time, notes or None))
            self.conn.commit()
            messagebox.showinfo("Success", "Appointment scheduled successfully")
            dialog.destroy()
            self.refresh_appointment_list()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    
    def refresh_appointment_list(self):
        # Clear existing data
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        # Get appointments with patient and doctor names via JOIN
        self.cursor.execute("""
            SELECT a.id, p.name as patient, d.name as doctor, 
                   a.appointment_date, a.status, a.notes
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date
        """)
        
        appointments = self.cursor.fetchall()
        
        # Add to treeview
        for appt in appointments:
            self.appointment_tree.insert("", END, values=appt)
    
    def update_appointment_status(self):
        selected_item = self.appointment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return
        
        appt_data = self.appointment_tree.item(selected_item)['values']
        appt_id = appt_data[0]
        
        dialog = Toplevel(self.root)
        dialog.title("Update Appointment Status")
        dialog.geometry("300x700")
        dialog.resizable(False, False)
        
        Label(dialog, text="Current Status:").pack(pady=10)
        Label(dialog, text=appt_data[4], font=("Arial", 12, "bold")).pack()
        
        Label(dialog, text="New Status:").pack(pady=10)
        status_var = StringVar(value=appt_data[4])
        status_frame = Frame(dialog)
        status_frame.pack()
        
        Radiobutton(status_frame, text="Scheduled", variable=status_var, value="Scheduled").grid(row=0, column=0, padx=5)
        Radiobutton(status_frame, text="Completed", variable=status_var, value="Completed").grid(row=0, column=1, padx=5)
        Radiobutton(status_frame, text="Cancelled", variable=status_var, value="Cancelled").grid(row=0, column=2, padx=5)
        
        button_frame = Frame(dialog)
        button_frame.pack(pady=20)
        
        Button(button_frame, text="Update", command=lambda: self.save_appointment_status(
            appt_id,
            status_var.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def save_appointment_status(self, appointment_id, status, dialog):
        self.cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", 
                          (status, appointment_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Appointment status updated successfully")
        dialog.destroy()
        self.refresh_appointment_list()
    
    def cancel_appointment(self):
        selected_item = self.appointment_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        appt_data = self.appointment_tree.item(selected_item)['values']
        
        if appt_data[4] == "Cancelled":
            messagebox.showinfo("Info", "This appointment is already cancelled")
            return
        
        confirmation = messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?")
        if confirmation:
            self.cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE id = ?", 
                              (appt_data[0],))
            self.conn.commit()
            messagebox.showinfo("Success", "Appointment cancelled successfully")
            self.refresh_appointment_list()
    
    def search_appointment_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Search Appointments")
        dialog.geometry("400x700")
        dialog.resizable(False, False)
        
        Label(dialog, text="Search by:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        
        search_var = StringVar(value="patient")
        Radiobutton(dialog, text="Patient", variable=search_var, value="patient").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Doctor", variable=search_var, value="doctor").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        Radiobutton(dialog, text="Date", variable=search_var, value="date").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        
        Label(dialog, text="Search term:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
        term_entry = Entry(dialog)
        term_entry.grid(row=4, column=1, padx=10, pady=10, sticky=EW)
        
        button_frame = Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        Button(button_frame, text="Search", command=lambda: self.search_appointment(
            search_var.get(),
            term_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)
    
    def search_appointment(self, search_by, term, dialog):
        if not term and search_by != "date":
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Clear existing data
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        if search_by == "patient":
            self.cursor.execute("""
                SELECT a.id, p.name as patient, d.name as doctor, 
                       a.appointment_date, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE p.name LIKE ?
                ORDER BY a.appointment_date
            """, (f"%{term}%",))
        elif search_by == "doctor":
            self.cursor.execute("""
                SELECT a.id, p.name as patient, d.name as doctor, 
                       a.appointment_date, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE d.name LIKE ?
                ORDER BY a.appointment_date
            """, (f"%{term}%",))
        elif search_by == "date":
            self.cursor.execute("""
                SELECT a.id, p.name as patient, d.name as doctor, 
                       a.appointment_date, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                WHERE date(a.appointment_date) = ?
                ORDER BY a.appointment_date
            """, (term,))
        
        appointments = self.cursor.fetchall()
        
        if not appointments:
            messagebox.showinfo("Info", "No matching appointments found")
            return
        
        # Add to treeview
        for appt in appointments:
            self.appointment_tree.insert("", END, values=appt)
        
        dialog.destroy()
    
        def export_appointments_csv(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return
            self.cursor.execute("""
                SELECT a.id, p.name, d.name, a.appointment_date, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
            """)
            rows = self.cursor.fetchall()
            headers = ["ID", "Patient", "Doctor", "Date", "Status", "Notes"]
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            messagebox.showinfo("Export", f"Appointment data exported to {file_path}")


    def create_report_tab(self):
        self.report_tab = Frame(self.notebook)
        self.notebook.add(self.report_tab, text="Reports")

        # Create report generation widgets
        Label(self.report_tab, text="Generate Patient Report", font=("Arial", 16, "bold")).pack(pady=10)

        Label(self.report_tab, text="Select Patient:", font=("Arial", 12)).pack(pady=5)
        self.cursor.execute("SELECT id, name FROM patients")
        patients = self.cursor.fetchall()
        patient_options = [f"{p[0]} - {p[1]}" for p in patients]
        self.selected_patient_var = StringVar(value=patient_options[0] if patients else "")
        patient_dropdown = ttk.Combobox(self.report_tab, textvariable=self.selected_patient_var, values=patient_options, state="readonly")
        patient_dropdown.pack(pady=5)

        Button(self.report_tab, text="Generate Report", command=self.generate_patient_report).pack(pady=10)

        # Add Print Button
        Button(self.report_tab, text="Print Report", command=self.print_report).pack(pady=10)

        # Text area to display the report
        self.report_text = Text(self.report_tab, wrap=WORD, height=20, width=80)
        self.report_text.pack(pady=10)

    def generate_patient_report(self):
        selected_patient = self.selected_patient_var.get()
        if not selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to generate the report")
            return

        patient_id = selected_patient.split(" - ")[0]

        try:
            # Fetch patient details
            self.cursor.execute("""
                SELECT p.name, p.age, p.gender, p.contact, p.department, d.name as doctor_name, p.admission_date, p.discharge_date
                FROM patients p
                LEFT JOIN doctors d ON p.doctor_id = d.id
                WHERE p.id = ?
            """, (patient_id,))
            patient = self.cursor.fetchone()

            # Fetch recommended medicines
            self.cursor.execute("""
                SELECT m.medicine_name, m.price, m.supplier
                FROM issued_medicines im
                JOIN pharmacy m ON im.medicine_id = m.id
                WHERE im.patient_id = ?
            """, (patient_id,))
            medicines = self.cursor.fetchall()

            # Generate report
            report = f"Patient Report\n{'='*50}\n"
            report += f"Name: {patient[0]}\n"
            report += f"Age: {patient[1]}\n"
            report += f"Gender: {patient[2]}\n"
            report += f"Contact: {patient[3]}\n"
            report += f"Department: {patient[4]}\n"
            report += f"Doctor: {patient[5]}\n"
            report += f"Admission Date: {patient[6]}\n"
            report += f"Discharge Date: {patient[7] if patient[7] else 'N/A'}\n\n"

            report += "Medicines Recommended:\n"
            if medicines:
                for med in medicines:
                    report += f"- {med[0]} (Price: {med[1]}, Supplier: {med[2]})\n"
            else:
                report += "No medicines recommended.\n"

            # Display report in the text area
            self.report_text.delete(1.0, END)
            self.report_text.insert(END, report)

            # Save the report to a temporary file for printing
            with open("patient_report.txt", "w") as file:
                file.write(report)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def print_report(self):
        try:
            # Open the report file in the default text editor for printing
            os.startfile("patient_report.txt", "print")
            # Clear the text area after printing
            self.report_text.delete(1.0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print the report: {e}")

    def create_admissions_tab(self):
        self.admissions_tab = Frame(self.notebook)
        self.notebook.add(self.admissions_tab, text="Admissions")

        # Frame for analytics
        analytics_frame = Frame(self.admissions_tab)
        analytics_frame.pack(fill=X, padx=10, pady=10)

        # Total admissions
        self.total_admissions_var = StringVar(value="0")
        Label(analytics_frame, text="Total Admissions:", font=("Arial", 12)).grid(row=0, column=0, sticky=W, padx=5)
        Label(analytics_frame, textvariable=self.total_admissions_var, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=W, padx=5)

        # Currently admitted patients
        self.current_admissions_var = StringVar(value="0")
        Label(analytics_frame, text="Currently Admitted:", font=("Arial", 12)).grid(row=1, column=0, sticky=W, padx=5)
        Label(analytics_frame, textvariable=self.current_admissions_var, font=("Arial", 12, "bold")).grid(row=1, column=1, sticky=W, padx=5)

        # Total discharges
        self.total_discharges_var = StringVar(value="0")
        Label(analytics_frame, text="Total Discharges:", font=("Arial", 12)).grid(row=2, column=0, sticky=W, padx=5)
        Label(analytics_frame, textvariable=self.total_discharges_var, font=("Arial", 12, "bold")).grid(row=2, column=1, sticky=W, padx=5)

        # Admissions log table
        admissions_frame = Frame(self.admissions_tab)
        admissions_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.admissions_tree = ttk.Treeview(admissions_frame, columns=("ID", "Patient", "Department", "Doctor", "Admission Date", "Discharge Date"), show="headings")
        self.admissions_tree.heading("ID", text="ID")
        self.admissions_tree.heading("Patient", text="Patient")
        self.admissions_tree.heading("Department", text="Department")
        self.admissions_tree.heading("Doctor", text="Doctor")
        self.admissions_tree.heading("Admission Date", text="Admission Date")
        self.admissions_tree.heading("Discharge Date", text="Discharge Date")

        self.admissions_tree.column("ID", width=50)
        self.admissions_tree.column("Patient", width=150)
        self.admissions_tree.column("Department", width=120)
        self.admissions_tree.column("Doctor", width=150)
        self.admissions_tree.column("Admission Date", width=150)
        self.admissions_tree.column("Discharge Date", width=150)

        self.admissions_tree.pack(fill=BOTH, expand=True)

        # Load initial data
        self.refresh_admissions_data()
    
    def refresh_admissions_data(self):
        try:
            # Clear existing data
            for item in self.admissions_tree.get_children():
                self.admissions_tree.delete(item)

            # Fetch admissions log
            self.cursor.execute("""
                SELECT al.id, p.name, al.department, d.name as doctor_name, al.admission_date, al.discharge_date
                FROM admissions_log al
                JOIN patients p ON al.patient_id = p.id
                LEFT JOIN doctors d ON al.doctor_id = d.id
            """)
            admissions = self.cursor.fetchall()

            # Populate the table
            for admission in admissions:
                self.admissions_tree.insert("", END, values=admission)

            # Update analytics
            self.cursor.execute("SELECT COUNT(*) FROM admissions_log")
            self.total_admissions_var.set(self.cursor.fetchone()[0])

            self.cursor.execute("SELECT COUNT(*) FROM admissions_log WHERE discharge_date IS NULL")
            self.current_admissions_var.set(self.cursor.fetchone()[0])

            self.cursor.execute("SELECT COUNT(*) FROM admissions_log WHERE discharge_date IS NOT NULL")
            self.total_discharges_var.set(self.cursor.fetchone()[0])

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to refresh admissions data: {e}")        

    def create_billing_tab(self):
        self.billing_tab = Frame(self.notebook)
        self.notebook.add(self.billing_tab, text="Billing & Collection")

        # Frame for billing table
        billing_frame = Frame(self.billing_tab)
        billing_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.billing_tree = ttk.Treeview(billing_frame, columns=("ID", "Patient", "Description", "Amount", "Date"), show="headings")
        self.billing_tree.heading("ID", text="ID")
        self.billing_tree.heading("Patient", text="Patient")
        self.billing_tree.heading("Description", text="Description")
        self.billing_tree.heading("Amount", text="Amount")
        self.billing_tree.heading("Date", text="Date")

        self.billing_tree.column("ID", width=50)
        self.billing_tree.column("Patient", width=150)
        self.billing_tree.column("Description", width=200)
        self.billing_tree.column("Amount", width=100)
        self.billing_tree.column("Date", width=150)

        self.billing_tree.pack(fill=BOTH, expand=True)

        # Buttons frame
        button_frame = Frame(self.billing_tab)
        button_frame.pack(fill=X, padx=10, pady=10)

        Button(button_frame, text="Add Transaction", command=self.show_add_transaction_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Generate Invoice", command=self.generate_invoice_dialog).pack(side=LEFT, padx=5)
        Button(button_frame, text="Refresh", command=self.refresh_billing_data).pack(side=LEFT, padx=5)
        Button(button_frame, text="Export CSV", command=self.export_billing_csv).pack(side=LEFT, padx=5)

        # Load initial billing data
        # Ensure the billing table has the required columns
        try:
            self.cursor.execute("ALTER TABLE billing ADD COLUMN date TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            # Column already exists
            pass

        self.refresh_billing_data()

    def export_billing_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        self.cursor.execute("""
            SELECT b.id, p.name, b.description, b.amount, b.date
            FROM billing b
            JOIN patients p ON b.patient_id = p.id
        """)
        rows = self.cursor.fetchall()
        headers = ["ID", "Patient", "Description", "Amount", "Date"]
        with open(file_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        messagebox.showinfo("Export", f"Billing data exported to {file_path}")
        

    def show_add_transaction_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add Transaction")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        # Get available patients
        self.cursor.execute("SELECT id, name FROM patients")
        patients = self.cursor.fetchall()

        if not patients:
            messagebox.showwarning("Warning", "No patients available. Please add patients first.")
            dialog.destroy()
            return

        Label(dialog, text="Patient:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        patient_var = StringVar()
        patient_dropdown = ttk.Combobox(dialog, textvariable=patient_var, 
                                        values=[f"{p[0]} - {p[1]}" for p in patients], 
                                        state="readonly")
        patient_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        Label(dialog, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        description_entry = Entry(dialog)
        description_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)

        Label(dialog, text="Amount:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        amount_entry = Entry(dialog)
        amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky=EW)

        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        Button(button_frame, text="Save", command=lambda: self.save_transaction(
            patient_var.get().split(" - ")[0],
            description_entry.get(),
            amount_entry.get(),
            dialog
        )).pack(side=LEFT, padx=10)

        Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)

    def save_transaction(self, patient_id, description, amount, dialog):
        if not patient_id or not description or not amount:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive number")
            return

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Insert transaction into the database
        payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO billing (patient_id, description, amount, date, payment_date)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_id, description, amount, date, payment_date))
        self.conn.commit()
        messagebox.showinfo("Success", "Transaction added successfully")
        dialog.destroy()
        
        try:
            self.cursor.execute("""
                INSERT INTO billing (patient_id, description, amount, date)
                VALUES (?, ?, ?, ?)
            """, (patient_id, description, amount, date))
            self.conn.commit()
            messagebox.showinfo("Success", "Transaction added successfully")
            dialog.destroy()
            self.refresh_billing_data()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def refresh_billing_data(self):
        try:
            # Clear existing data
            for item in self.billing_tree.get_children():
                self.billing_tree.delete(item)

            # Fetch billing data
            self.cursor.execute("""
                SELECT b.id, p.name, b.description, b.amount, b.date
                FROM billing b
                JOIN patients p ON b.patient_id = p.id
            """)
            transactions = self.cursor.fetchall()

            # Populate the table
            for transaction in transactions:
                self.billing_tree.insert("", END, values=transaction)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to refresh billing data: {e}")

        def update_billing_table(self):
            try:
                # Add the 'description' column if it doesn't exist
                self.cursor.execute("ALTER TABLE billing ADD COLUMN description, date TEXT NOT NULL DEFAULT ''")
                self.conn.commit()
            except sqlite3.OperationalError:
                # Column already exists
                pass       

    def generate_invoice_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Generate Invoice")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        # Get available patients
        self.cursor.execute("SELECT id, name FROM patients")
        patients = self.cursor.fetchall()

        if not patients:
            messagebox.showwarning("Warning", "No patients available. Please add patients first.")
            dialog.destroy()
            return

        Label(dialog, text="Select Patient:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        patient_var = StringVar()
        patient_dropdown = ttk.Combobox(dialog, textvariable=patient_var, 
                                        values=[f"{p[0]} - {p[1]}" for p in patients], 
                                        state="readonly")
        patient_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        # Buttons
        button_frame = Frame(dialog)
        button_frame.grid(row=1, column=0, columnspan=2, pady=20)

        Button(button_frame, text="Generate", command=lambda: self.generate_invoice(
                    patient_var.get().split(" - ")[0],
                    dialog
                )).pack(side=LEFT, padx=10)

    def generate_invoice(self, patient_id, dialog):
                button_frame = Frame(dialog)
                button_frame.grid(row=1, column=0, columnspan=2, pady=20)

                Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=LEFT, padx=10)

                
                try:
                    # Fetch patient details
                    self.cursor.execute("SELECT name FROM patients WHERE id = ?", (patient_id,))
                    patient_name = self.cursor.fetchone()[0]
        
                    # Fetch billing transactions for the patient
                    self.cursor.execute("""
                        SELECT description, amount, date
                        FROM billing
                        WHERE patient_id = ?
                    """, (patient_id,))
                    transactions = self.cursor.fetchall()
        
                    if not transactions:
                        messagebox.showinfo("Info", "No transactions found for the selected patient")
                        return
        
                    # Generate invoice content
                    invoice = f"Invoice for {patient_name}\n{'='*50}\n"
                    total_amount = 0
                    for desc, amount, date in transactions:
                        invoice += f"{date}: {desc} - ${amount:.2f}\n"
                        total_amount += amount
                    invoice += f"\nTotal Amount: ${total_amount:.2f}\n"
        
                    # Save invoice to a file
                    invoice_file = filedialog.asksaveasfilename(
                        defaultextension=".txt",
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                        title="Save Invoice As"
                    )
                    if invoice_file:
                        with open(invoice_file, "w") as file:
                            file.write(invoice)
                        messagebox.showinfo("Success", "Invoice generated and saved successfully")
                        dialog.destroy()
        
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Failed to generate invoice: {e}")
      
    def create_dashboard_tab(self):
        self.dashboard_tab = Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Analytics Dashboard")

        # Create a notebook inside the dashboard for multiple charts
        chart_notebook = ttk.Notebook(self.dashboard_tab)
        chart_notebook.pack(fill=BOTH, expand=True)

        # --- Patient Demographics ---
        demo_frame = Frame(chart_notebook)
        chart_notebook.add(demo_frame, text="Patient Demographics")

        fig1, axs1 = plt.subplots(1, 3, figsize=(12, 4))
        fig1.tight_layout(pad=3.0)

        # Age distribution
        self.cursor.execute("SELECT age FROM patients")
        ages = [row[0] for row in self.cursor.fetchall()]
        axs1[0].hist(ages, bins=range(0, 120, 10), color='skyblue', edgecolor='black')
        axs1[0].set_title("Age Distribution")
        axs1[0].set_xlabel("Age")
        axs1[0].set_ylabel("Count")

        # Gender distribution
        self.cursor.execute("SELECT gender FROM patients")
        genders = [row[0] for row in self.cursor.fetchall()]
        gender_counts = {g: genders.count(g) for g in set(genders)}
        axs1[1].pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%', startangle=90)
        axs1[1].set_title("Gender Distribution")

        # Department distribution
        self.cursor.execute("SELECT department FROM patients")
        departments = [row[0] for row in self.cursor.fetchall()]
        dept_counts = {d: departments.count(d) for d in set(departments)}
        axs1[2].bar(dept_counts.keys(), dept_counts.values(), color='orange')
        axs1[2].set_title("Department Distribution")
        axs1[2].set_xticklabels(dept_counts.keys(), rotation=45, ha='right')

        canvas1 = FigureCanvasTkAgg(fig1, master=demo_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

        # --- Revenue Trends ---
        revenue_frame = Frame(chart_notebook)
        chart_notebook.add(revenue_frame, text="Revenue Trends")

        fig2, ax2 = plt.subplots(figsize=(7, 4))
        self.cursor.execute("""
            SELECT strftime('%Y-%m', date), SUM(amount)
            FROM billing
            GROUP BY strftime('%Y-%m', date)
            ORDER BY strftime('%Y-%m', date)
        """)
        data = self.cursor.fetchall()
        months = [row[0] for row in data]
        totals = [row[1] for row in data]
        ax2.plot(months, totals, marker='o', color='green')
        ax2.set_title("Monthly Revenue")
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Total Revenue")
        ax2.tick_params(axis='x', rotation=45)
        canvas2 = FigureCanvasTkAgg(fig2, master=revenue_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

        # --- Appointment Statistics ---
        appt_frame = Frame(chart_notebook)
        chart_notebook.add(appt_frame, text="Appointment Stats")

        fig3, ax3 = plt.subplots(figsize=(5, 4))
        self.cursor.execute("""
            SELECT status, COUNT(*) FROM appointments GROUP BY status
        """)
        appt_data = self.cursor.fetchall()
        statuses = [row[0] for row in appt_data]
        counts = [row[1] for row in appt_data]
        ax3.bar(statuses, counts, color=['blue', 'red', 'gray'])
        ax3.set_title("Appointment Status Counts")
        ax3.set_xlabel("Status")
        ax3.set_ylabel("Count")
        canvas3 = FigureCanvasTkAgg(fig3, master=appt_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=BOTH, expand=True)

    def show_reception_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Reception - Patient Check-in")
        dialog.geometry("400x250")
        dialog.resizable(False, False)

        # Select patient
        self.cursor.execute("SELECT id, name FROM patients WHERE admission_date IS NOT NULL AND discharge_date IS NULL")
        patients = self.cursor.fetchall()
        if not patients:
            messagebox.showwarning("Warning", "No admitted patients found.")
            dialog.destroy()
            return

        Label(dialog, text="Patient:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        patient_var = StringVar()
        patient_dropdown = ttk.Combobox(dialog, textvariable=patient_var, values=[f"{p[0]} - {p[1]}" for p in patients], state="readonly")
        patient_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        Label(dialog, text="Payment Method:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        payment_var = StringVar(value="Cash")
        payment_dropdown = ttk.Combobox(dialog, textvariable=payment_var, values=["Cash", "Insurance", "Mpesa", "Card"], state="readonly")
        payment_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky=EW)

        Button(dialog, text="Check-in", command=lambda: self.reception_checkin(
            patient_var.get().split(" - ")[0],
            payment_var.get(),
            dialog
        )).grid(row=2, column=0, columnspan=2, pady=20)

    def reception_checkin(self, patient_id, payment_method, dialog):
        try:
            self.cursor.execute("UPDATE patients SET payment_method = ? WHERE id = ?", (payment_method, patient_id))
            self.cursor.execute(
                "INSERT INTO patient_journey (patient_id, stage, timestamp, details) VALUES (?, ?, ?, ?)",
                (patient_id, "Reception", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Payment: {payment_method}")
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Patient checked in at Reception.")
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check in: {e}")        

    def show_triage_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Triage - Patient Assessment")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        # Select patient
        self.cursor.execute("SELECT id, name FROM patients WHERE admission_date IS NOT NULL AND discharge_date IS NULL")
        patients = self.cursor.fetchall()
        if not patients:
            messagebox.showwarning("Warning", "No admitted patients found.")
            dialog.destroy()
            return

        Label(dialog, text="Patient:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        patient_var = StringVar()
        patient_dropdown = ttk.Combobox(dialog, textvariable=patient_var, values=[f"{p[0]} - {p[1]}" for p in patients], state="readonly")
        patient_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky=EW)

        Label(dialog, text="Vitals/Notes:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        notes_entry = Text(dialog, height=5, width=30)
        notes_entry.grid(row=1, column=1, padx=10, pady=10, sticky=EW)

        Button(dialog, text="Record Triage", command=lambda: self.triage_record(
            patient_var.get().split(" - ")[0],
            notes_entry.get("1.0", END).strip(),
            dialog
        )).grid(row=2, column=0, columnspan=2, pady=20)

    def triage_record(self, patient_id, notes, dialog):
        try:
            self.cursor.execute(
                "INSERT INTO patient_journey (patient_id, stage, timestamp, details) VALUES (?, ?, ?, ?)",
                (patient_id, "Triage", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), notes)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Triage recorded.")
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record triage: {e}")        

    def show_patient_journey(self, patient_id):
        dialog = Toplevel(self.root)
        dialog.title("Patient Journey")
        dialog.geometry("600x400")
        dialog.resizable(False, False)

        tree = ttk.Treeview(dialog, columns=("Stage", "Timestamp", "Details"), show="headings")
        tree.heading("Stage", text="Stage")
        tree.heading("Timestamp", text="Timestamp")
        tree.heading("Details", text="Details")
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Ensure the patient_journey table exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_journey (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                stage TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        """)
        self.conn.commit()

        # Fetch patient journey data
        self.cursor.execute("SELECT stage, timestamp, details FROM patient_journey WHERE patient_id = ? ORDER BY timestamp", (patient_id,))
        for row in self.cursor.fetchall():
            tree.insert("", END, values=row)
        
    def complete_appointment(self, patient_id, doctor_id, notes):
        # ...existing code to mark appointment as completed...
        self.cursor.execute(
            "INSERT INTO patient_journey (patient_id, stage, timestamp, details) VALUES (?, ?, ?, ?)",
            (patient_id, "Doctor", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"Seen by doctor {doctor_id}: {notes}")
        )
        self.conn.commit()
    def get_selected_patient_id(self):
        selected_item = self.patient_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient")
            return None
        patient_data = self.patient_tree.item(selected_item)['values']
        return patient_data[0]

    from tkinter import filedialog


if __name__ == "__main__":
    root = Tk()
    app = HospitalManagementSystem(root)
    root.configure(bg="cyan")
    root.mainloop()
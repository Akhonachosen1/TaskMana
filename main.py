import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Load tasks from a file
def load_tasks(file_name="tasks_data.txt"):
    tasks = []
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 5:
                    title, description, due_date, status, assigned_to = values
                    tasks.append({
                        "title": title,
                        "description": description,
                        "due_date": due_date,
                        "status": status,
                        "assigned_to": assigned_to
                    })
                else:
                    print(f"Skipping invalid line: {line.strip()}")
    return tasks

# Save tasks to a file
def save_tasks(tasks, file_name="tasks_data.txt"):
    with open(file_name, "w") as file:
        for task in tasks:
            file.write(f"{task['title']},{task['description']},{task['due_date']},{task['status']},{task['assigned_to']}\n")

# Add a new task
def add_task():
    global tasks
    title = title_entry.get().strip()
    description = description_entry.get().strip()
    due_date = due_date_entry.get().strip()
    assigned_to = assigned_to_entry.get().strip()
    
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date (YYYY-MM-DD).")
        return
    
    tasks.append({
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "Incomplete",
        "assigned_to": assigned_to
    })
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    assigned_to_entry.delete(0, tk.END)
    update_task_list()
    messagebox.showinfo("Success", f"Task '{title}' added.")

def mark_task_complete():
    global tasks
def mark_task_complete():
    selected_task = task_listbox.get(tk.ACTIVE)
    title = selected_task.split(" | ")[0]
    for task in tasks:
        if task['title'] == title:
            task['status'] = "Completed"
            update_task_list()
            messagebox.showinfo("Success", f"Task '{title}' marked as complete.")
            return
    messagebox.showerror("Not Found", f"Task '{title}' not found.")
def delete_task():
    global tasks
# Delete a task
def delete_task():
    selected_task = task_listbox.get(tk.ACTIVE)
    title = selected_task.split(" | ")[0]
    for task in tasks:
        if task['title'] == title:
            tasks.remove(task)
            update_task_list()
            messagebox.showinfo("Success", f"Task '{title}' deleted.")
            return
    messagebox.showerror("Not Found", f"Task '{title}' not found.")

# Update task list display
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔️" if task['status'] == "Completed" else "❌"
        task_listbox.insert(tk.END, f"{task['title']} | {task['description']} | {task['due_date']} | {status} | {task['assigned_to']}")

def save_and_exit():
    global tasks

# Save tasks and exit
def save_and_exit():
    save_tasks(tasks)
    root.quit()

# Check for overdue tasks
def check_overdue_tasks():
    overdue_tasks = []
    current_date = datetime.now().date()
    for task in tasks:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
        if due_date < current_date and task['status'] != "Completed":
            overdue_tasks.append(task['title'])
    if overdue_tasks:
        messagebox.showwarning("Overdue Tasks", f"The following tasks are overdue: {', '.join(overdue_tasks)}")

# Load existing tasks
tasks = load_tasks()

# Create main window
root = tk.Tk()
root.title("Task Manager")

# Add Task UI Elements
title_label = tk.Label(root, text="Task Title:")
title_label.grid(row=0, column=0, padx=10, pady=5)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1, padx=10, pady=5)

description_label = tk.Label(root, text="Description:")
description_label.grid(row=1, column=0, padx=10, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=5)

due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):")
due_date_label.grid(row=2, column=0, padx=10, pady=5)
due_date_entry = tk.Entry(root)
due_date_entry.grid(row=2, column=1, padx=10, pady=5)

assigned_to_label = tk.Label(root, text="Assigned To:")
assigned_to_label.grid(row=3, column=0, padx=10, pady=5)
assigned_to_entry = tk.Entry(root)
assigned_to_entry.grid(row=3, column=1, padx=10, pady=5)

add_task_button = tk.Button(root, text="Add Task", command=add_task)
add_task_button.grid(row=4, column=0, columnspan=2, pady=10)

# Task Listbox and Buttons
task_listbox = tk.Listbox(root, width=60, height=10)
task_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

mark_complete_button = tk.Button(root, text="Mark Complete", command=mark_task_complete)
mark_complete_button.grid(row=6, column=0, pady=5)

delete_task_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_task_button.grid(row=6, column=1, pady=5)

# Save and Exit Button
save_exit_button = tk.Button(root, text="Save and Exit", command=save_and_exit)
save_exit_button.grid(row=7, column=0, columnspan=2, pady=10)

# Update task list when the app starts
update_task_list()

# Call check_overdue_tasks when the app starts
check_overdue_tasks()

# Start the Tkinter event loop
root.mainloop()

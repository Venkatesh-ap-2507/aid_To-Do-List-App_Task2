import tkinter as tk
from tkinter import messagebox, filedialog
import pickle

class Task:
    def __init__(self, title, description, status=False):
        self.title = title
        self.description = description
        self.status = status

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []

        self.title_label = tk.Label(root, text="Title:")
        self.title_label.pack()

        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.description_label = tk.Label(root, text="Description:")
        self.description_label.pack()

        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root)
        self.task_listbox.pack()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.load_button = tk.Button(root, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack()

        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack()

    def add_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get()

        if title and description:
            task = Task(title, description)
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, f"{task.title} - {task.description}")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Title and description cannot be empty.")

    def delete_task(self):
        selected_indices = self.task_listbox.curselection()

        if len(selected_indices) > 0:
            index = selected_indices[0]
            self.task_listbox.delete(index)
            del self.tasks[index]
        else:
            messagebox.showerror("Error", "No task selected.")

    def load_tasks(self):
        try:
            filename = tk.filedialog.askopenfilename(initialdir=".", title="Select file",
                                                     filetypes=(("Todo files", "*.todo"), ("All files", "*.*")))
            if filename:
                with open(filename, "rb") as file:
                    self.tasks = pickle.load(file)

                self.task_listbox.delete(0, tk.END)
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, f"{task.title} - {task.description}")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except pickle.UnpicklingError:
            messagebox.showerror("Error", "Invalid file format.")

    def save_tasks(self):
        if len(self.tasks) > 0:
            try:
                filename = tk.filedialog.asksaveasfilename(initialdir=".", title="Save file",
                                                           defaultextension=".todo",
                                                           filetypes=(("Todo files", "*.todo"), ("All files", "*.*")))
                if filename:
                    with open(filename, "wb") as file:
                        pickle.dump(self.tasks, file)
                        messagebox.showinfo("Success", "Tasks saved successfully.")
            except Exception:
                messagebox.showerror("Error", "An error occurred while saving tasks.")
        else:
            messagebox.showerror("Error", "No tasks to save.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)


root = tk.Tk()


todo_app = ToDoListApp(root)


root.mainloop()

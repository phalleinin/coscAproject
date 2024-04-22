from tkinter import * 
import tkinter.messagebox
import sqlite3


#Create the initial window
window = Tk()
window.title("I'm To-Do-List")

#Create a connection to the SQLite database
conn = sqlite3.connect('myList.db')
c = conn.cursor()

#Create a table to store tasks 
c.execute('''CREATE TABLE IF NOT EXISTS list (
             id INTEGER PRIMARY KEY,
             tasks TEXT
             )''')

#Function to add a task
def add_task():
    enter_task = task_entry.get()
    if enter_task != "":
        c.execute("INSERT INTO list (tasks) VALUES (?)", (enter_task,))
        conn.commit()
        list_tasks()
        task_entry.delete(0, END)
    else:
        tkinter.messagebox.showwarning(title="Warning!!", message="You must enter a task")
 
#Function to mark a task as completed
def mark_completed():
    try:
        selected_task = listbox_task.curselection()[0] + 1
        c.execute("SELECT tasks FROM list WHERE id=?", (selected_task,))
        task = c.fetchone()[0]
        updated_task = task + " ✔️"
        c.execute("UPDATE list SET tasks=? WHERE id=?", (updated_task, selected_task))
        conn.commit()
        list_tasks()
    except:
        tkinter.messagebox.showwarning(title="Warning!!", message="You must select a task.")

#Function to delete a task 
def delete_task():
    try:
        selected_task = listbox_task.curselection()[0] + 1
        c.execute("DELETE FROM list WHERE id=?", (selected_task,))
        conn.commit()
        list_tasks()
    except:
        tkinter.messagebox.showwarning(title="Warning!!", message="You must select a task.")


#Function to display tasks in the listbox
def list_tasks():
    listbox_task.delete(0, END)
    c.execute("SELECT * FROM list")
    for row in c.fetchall():
        listbox_task.insert(END, row[1])
        
#Function to save tasks to a text file
def save_tasks():
    task=listbox_task.delete(0, END)
    if task != "":
        c.execute("INSERT INTO list (tasks) VALUES (?)", (task,))
        conn.commit()
        tkinter.messagebox.showinfo(title="Tasks Saved", message="Tasks have been saved")
        window.destroy()
    else:
        tkinter.messagebox.showerror(title="Error", message="An error occurred while saving tasks: ")
        window.destroy()

# # Function to prompt user to save tasks before closing
def leave_app ():
    if tkinter.messagebox.askokcancel("Save Tasks", "Do you want to save your tasks?"):
        save_tasks()
    window.destroy()

# Bind the on_closing function to the window closing event
window.protocol("WM_DELETE_WINDOW", leave_app)


#Design GUI
frame_task = Frame(window)
frame_task.pack()

#Create listbox
listbox_task = Listbox(frame_task, bg="black", fg="lightblue", height=15, width=50, font="Arial")  
listbox_task.pack(side=LEFT)

#Create scrollbar in case the total list exceeds the size of the given window 
scrollbar_task = Scrollbar(frame_task)
scrollbar_task.pack(side=RIGHT, fill=Y)
listbox_task.config(yscrollcommand=scrollbar_task.set)
scrollbar_task.config(command=listbox_task.yview)


#Entry fields
task_entry = Entry(window, bg="pink", fg="black", width=45, font="Arial")
task_label = Label(window, text="Enter a task below")
task_label.pack()
task_entry.pack()

#Create button for adding task
add_button = Button(window, text="Add task", bg="cyan", fg="black", width=30, command=add_task)
add_button.pack(pady=3)

#Create a button for mark as completed
mark_button = Button(window, text="Mark as completed ", bg="orange", fg="black", width=30, command=mark_completed)
mark_button.pack(pady=3)

#Create button deleting selected task
delete_button = Button(window, text="Delete selected task", bg="yellow", fg="black", width=30, command=delete_task)
delete_button.pack(pady=3)

# Create a button for saving tasks
save_button = Button(window, text="Save tasks", bg="magenta", fg="black", width=30, command=save_tasks)
save_button.pack(pady=3)


list_tasks() 

window.mainloop() 

conn.close() 

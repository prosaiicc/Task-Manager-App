from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas
import os

#----------SAVE TASKS----------#

#File Path
PATH = "tasks.csv"

def save_tasks():
    """Checks if all the boxes have been filled and then if the file exists adds the task to the file , else creates the file and adds the new task"""
    global PATH
    #TaskInfo
    task_name = name_t.get()
    task_desc = desc_t.get()
    if len(task_name) == 0 :
        messagebox.showerror(title="OOPS",message="Please complement all the empty boxes!")
    else:

        task = pandas.DataFrame([{
            "Name": task_name,
            "Description": task_desc
        }])
        if os.path.exists(PATH):
            df = pandas.read_csv(PATH)
            df = pandas.concat([df,task],ignore_index=True)
            df.to_csv(PATH,index=False)
        else :
            task.to_csv(PATH,index=False)
        messagebox.showinfo(title="Success",message="Your task has been successfully added to the TaskBoard!")
        name_t.delete(first=0,last=len(task_name))
        desc_t.delete(first=0,last=len(task_desc))

def remove_tasks():
    """Reads the file and keeps only the tasks that don't have the name that we want to delete and then rewrites the file."""
    task_nam = name_t.get().strip()
    task_de = desc_t.get()
    df = pandas.read_csv(PATH)

    new_df = df[df["Name"] != task_nam]

    if len(new_df) == len(df):
        messagebox.showerror(title="OOPS",message="The task cannot be found!")
    else :
        messagebox.showinfo(title="Success",message="The task has been successfully deleted")

    new_df.to_csv(PATH,index=False)
    name_t.delete(first=0, last=len(task_nam))
    desc_t.delete(first=0, last=len(task_de))

#--------TaskBoard Setting-------#
def showTasks():
    TaskBoard()



def TaskBoard():
    """Creates the window that the Tasks are going to be shown"""
    global tree
    root = Tk()
    root.title("Tasks")

    cols = ("Name", "Description")
    tree = ttk.Treeview(root,columns=cols,show="headings")

    for col in cols:
        tree.heading(col,text=col)
        tree.column(col,width=120)

    tree.pack(fill="both",expand=True,padx=10,pady=10)


    RefreshBoard(tree)
    root.mainloop()

def RefreshBoard(tree):

    for row in tree.get_children():
        tree.delete(row)

    if os.path.exists(PATH):
        df = pandas.read_csv(PATH)
        for _, row in df.iterrows():
            tree.insert("","end",values=(row["Name"],row["Description"]))







#--------------UI-----------#
#Colors
GREEN = "#9bdeac"
BLUE = "#80EAED"
FONT_NAME = "Courier"

#Window
window = Tk()
window.title("Task Manager")
window.config(padx=70, pady=70, bg=BLUE)

#Canva
canvas = Canvas(width=200, height=200, bg=BLUE, highlightthickness=0)
logo = PhotoImage(file="logo2.png")
canvas.create_image(100,100,image=logo)
canvas.grid(row=0,column=1)

#Labels
task_name = Label(text="Task Name:", bg=BLUE)
task_name.focus()
task_name.grid(row=1,column=0)

task_desc = Label(text="Task Description:", bg=BLUE)
task_desc.grid(row=2,column=0)

view = Label(text="View Tasks:", bg=BLUE)
view.grid(row=3,column=0)

options = Label(text="Options:",bg=BLUE)
options.grid(row=4,column=0)

#Entries
name_t = Entry(width=35)
name_t.grid(row=1,column=1,columnspan=2,sticky="EW")

desc_t = Entry(width=35)
desc_t.grid(row=2,column=1,columnspan=2,sticky="EW")

#Buttons
view_button = Button(text="TaskBoard",width=35,command=showTasks)
view_button.grid(row=3,column=1,columnspan=2,sticky="EW")


add_button = Button(text="Add",width=35,command=save_tasks)
add_button.grid(row=4,column=1)

remove_button = Button(text="Remove Task",command=remove_tasks)
remove_button.grid(row=4,column=2,sticky="EW")


window.mainloop()
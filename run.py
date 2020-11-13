import tkinter as tk


class Interface(tk.Frame):
    def createWidgets(self):
        self.newTaskLabel = tk.Label(self, text="Add new task here!")
        self.newTaskLabel.grid(column=0, row=0, pady=10, sticky="N")
        self.writeEntry = tk.Entry(self)
        self.writeEntry.grid(row=0, column=1, columnspan=2, ipadx=50, padx=10, pady=10, sticky="N")
        self.ToDoTaskBox = tk.Listbox(self)
        self.ToDoTaskBox.grid(row=1, column=3, sticky="N")
        self.CompletedTaskBox = tk.Listbox(self)
        self.CompletedTaskBox.grid(row=3, column=3)
        self.AddingButton = tk.Button(self, text="Add new task", command=self.add_new_task)
        self.AddingButton.grid(row=1, column=1, sticky="N")
        self.DeletingTaskButton = tk.Button(self, text="Delete this task", command=self.delete_task)
        self.DeletingTaskButton.grid(row=1, column=2)
        self.MarkingCompleteTaskButton = tk.Button(self, text="Complete task", command=self.complete_task)
        self.MarkingCompleteTaskButton.grid(row=1, column=2, sticky="S")
        self.TitleToDoTaskLabel = tk.Label(self, text="To-Do:")
        self.TitleToDoTaskLabel.grid(row=0, column=3)
        self.TitleCompletedTaskLabel = tk.Label(self, text="Completed:")
        self.TitleCompletedTaskLabel.grid(row=2, column=3)

    def add_new_task(self):
        self.ToDoTaskBox.insert(0, self.writeEntry.get())
        self.writeEntry.delete(0, 'end')

    def delete_task(self):
        self.ToDoTaskBox.delete(self.ToDoTaskBox.index('anchor'))

    def complete_task(self):
        self.CompletedTaskBox.insert(0, self.ToDoTaskBox.get(self.ToDoTaskBox.index('anchor')))
        self.ToDoTaskBox.delete(self.ToDoTaskBox.index('anchor'))

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()


interface = Interface()
interface.master.title("To-Do App")
interface.mainloop()
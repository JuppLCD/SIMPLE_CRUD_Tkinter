from tkinter import LabelFrame, Label, Entry, StringVar

class MyInput:
    def __init__(self, master: LabelFrame, label_text: str, position=(0,0) ) -> None:
        row = position[0]
        column= position[1]

        label = Label(master, text=label_text, width=20)
        label.grid(row=row, column=column, padx=5, pady=3)

        column_entry = column + 1

        self.input_text = StringVar()
        self.entry = Entry(master, textvariable=self.input_text)
        self.entry.grid(row=row, column=column_entry, padx=5, pady=3)

    def get_text(self):
        return self.input_text.get()

    def set_text(self, input_text):
        self.input_text.set(input_text)

    def is_empty(self):
        return len(self.get_text()) == 0

    def clear_text(self):
        self.input_text.set('')

    def disabled(self):
        self.clear_text()
        self.entry.config(state='disabled')

    def enable(self):
        self.clear_text()
        self.entry.config(state='normal')


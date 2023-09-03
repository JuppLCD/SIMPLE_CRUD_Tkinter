from tkinter.ttk import Treeview
from tkinter import LabelFrame, Label, Entry, StringVar, Button, END, messagebox

import logging

from models.product import Product


class MyButton(Button):
    def __init__(self, master: LabelFrame, text, command,  position=(0, 0)):
        super().__init__(master, text=text, command=command)

        row = position[0]
        column = position[1]

        self.config(width=12, height=2)
        self.grid(row=row, column=column)


class MyInput:
    def __init__(self, master: LabelFrame, label_text: str, position=(0, 0)) -> None:
        row = position[0]
        column = position[1]

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


class MyTable(Treeview):
    def __init__(self, master: LabelFrame):
        super().__init__(master)

        self.config(columns=(1, 2, 3, 4), show="headings", height="5")
        self.pack()

        self.heading(1, text="ID Del Producto")
        self.heading(2, text="Nombre Del Producto")
        self.heading(3, text="Precio Del Producto")
        self.heading(4, text="Cantidad Del Producto")

    def clear_table(self):
        # get_children() retorna una lista, e * al inicio es el spreed operator
        self.delete(*self.get_children())

    def insert_product(self, product: Product):
        self.insert('', END, text=product.id, values=(
            product.id, product.name, product.price, product.quantity))

    def insert_all_products(self, all_products: list[Product]):
        for product in all_products:
            self.insert_product(product)

    def select_product(self):
        try:
            return self.item(self.selection())
        except IndexError:
            title = "Error al seleccionar un producto"
            msg = "No se a seleccionado ningun proucto en la tabla, seleccione y luego prosiga con la accion"

            messagebox.showerror(title, msg)
        except Exception as e:
            logging.exception(e)
            return

    def get_product(self):
        product = self.select_product()

        product_id = product['values'][0]
        name = product['values'][1]
        price = product['values'][2]
        quantity = product['values'][3]

        return Product(name, price, quantity, product_id)

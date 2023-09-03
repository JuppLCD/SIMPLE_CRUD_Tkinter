# Codigo de Programadork100
# Titulo del video
# Codigo base en github = https://github.com/programadork/codigo_ejemplo
# Link video YT = https://www.youtube.com/watch?v=M07_zpAL0vk

from tkinter import ttk
from tkinter import Tk, LabelFrame, Toplevel
import logging

from models.product import Product, ProductModel

from ui.my_widgets import MyInput, MyButton


class AppProductos:
    def __init__(self):
        self.window = Tk()
        self.window.title("Productos")
        self.window.geometry("850x600")

        ProductModel.create_table()

        frame_table = LabelFrame(
            self.window, text="Informacion Del Producto", font=("Calibri", 14))
        frame_form = LabelFrame(
            self.window, text="Datos Del Producto", font=("Calibri", 14))

        frame_table.pack(fill="both", expand="yes", padx=20, pady=10)
        frame_form.pack(fill="both", expand="yes", padx=20, pady=10)

        # Creando y colocando la tabla en el frame_table
        self.table = ttk.Treeview(frame_table, columns=(
            1, 2, 3, 4), show="headings", height="5")
        self.table.pack()

        self.table.heading(1, text="ID Del Producto")
        self.table.heading(2, text="Nombre Del Producto")
        self.table.heading(3, text="Precio Del Producto")
        self.table.heading(4, text="Cantidad Del Producto")

        self.get_all_data()

        # Creando y colocando los inputs en el frame_form
        self.inputs = dict()

        self.inputs['NAME'] = MyInput(
            master=frame_form,
            label_text="Nombre Del Producto",
            position=(0, 0)
        )
        self.inputs['PRICE'] = MyInput(
            master=frame_form,
            label_text="Precio Del Producto",
            position=(1, 0)
        )
        self.inputs['QUANTITY'] = MyInput(
            master=frame_form,
            label_text="Cantidad Del Producto",
            position=(2, 0)
        )

        # Colocando un focus por defecto al input nombre en el formulario
        self.inputs['NAME'].entry.focus()

        # Botones del formulario
        MyButton(
            master=frame_form,
            text="Agregar",
            command=self.add_product,
            position=(5, 0)
        )
        MyButton(
            master=frame_form,
            text="Eliminar",
            command=self.delete_product,
            position=(5, 1)
        )
        MyButton(
            master=frame_form,
            text="Actualizar",
            command=self.product_editing_window,
            position=(5, 2)
        )

    def get_all_data(self):
        book = self.table.get_children()
        for element in book:
            self.table.delete(element)

        rows = ProductModel.get_all()

        for row in rows:
            self.table.insert('', 0, text=row[1], values=row)

    def validate_inputs(self):
        return not (self.inputs["NAME"].is_empty() and self.inputs["PRICE"].is_empty() and self.inputs["QUANTITY"].is_empty())

    def add_product(self):
        if self.validate_inputs():
            name = self.inputs["NAME"].get_text()
            price = self.inputs["PRICE"].get_text()
            quantity = self.inputs["QUANTITY"].get_text()

            new_product = Product(name, price, quantity)
            ProductModel.store(new_product)

            self.inputs["NAME"].clear_text()
            self.inputs["PRICE"].clear_text()
            self.inputs["QUANTITY"].clear_text()
        else:
            print("Los campos estan vacios")
        self.get_all_data()

    def delete_product(self):
        try:
            self.table.item(self.table.selection())['text']
        # except IndexError as e:
        #     return
        except Exception as e:
            logging. exception(e)
            return

        product_id = self.table.item(self.table.selection())['values'][0]

        ProductModel.delete(product_id)

        self.get_all_data()

    def product_editing_window(self):
        try:
            self.table.item(self.table.selection())[
                'values'][0]    # product_id
        # except IndexError as e:
        #     print(e)
        #     return
        except Exception as e:
            logging. exception(e)
            return

        self.edit_window = Toplevel()
        self.edit_window.title("Actualizar")
        self.edit_window.geometry("400x200")

        product_id = self.table.item(self.table.selection())['values'][0]
        old_price = self.table.item(self.table.selection())['values'][2]
        old_quantity = self.table.item(self.table.selection())['values'][3]

        frame = LabelFrame(
            self.edit_window, text="Actualizar Producto",  font=("Calibri", 12))
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        input_old_price = MyInput(
            master=frame, label_text="Antiguo Precio: ", position=(2, 1))
        input_old_price.disabled()
        input_old_price.set_text(old_price)

        input_new_price = MyInput(
            master=frame, label_text="Nuevo Precio: ", position=(3, 1))

        input_old_quantity = MyInput(
            master=frame, label_text="Antiguo Precio: ", position=(4, 1))
        input_old_quantity.disabled()
        input_old_quantity.set_text(old_quantity)

        input_new_quantity = MyInput(
            master=frame, label_text="Nuevo Precio: ", position=(5, 1))

        # Colocando un focus por defecto al input nuevo precio en el formulario de edicion
        input_new_price.entry.focus()

        MyButton(
            master=frame,
            text="Actualizar",
            command=lambda: self.update_product(
                input_new_price.get_text(),
                input_new_quantity.get_text(),
                product_id
            ),
            position=(7, 1)
        )
        MyButton(
            master=frame,
            text="Cancelar",
            command=self.edit_window.destroy,
            position=(7, 2)
        )

    def update_product(self, new_price, new_quantity, product_id):
        ProductModel.update(new_price, new_quantity, product_id)

        self.edit_window.destroy()
        self.get_all_data()


if __name__ == '__main__':
    my_app = AppProductos()
    my_app.window.mainloop()

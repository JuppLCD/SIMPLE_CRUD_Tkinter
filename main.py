from tkinter import Tk, LabelFrame, Toplevel

from models.product import Product, ProductModel

from ui.my_widgets import MyInput, MyButton, MyTable


class AppProductos:
    def __init__(self):
        self.window = Tk()
        self.window.title("Productos")

        # Tamaño de la ventana principal
        window_width = 850
        window_height = 600

        # Tamaño de la pantalla del usuario
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Obteniendo la cordenada en la cual se va a colocar la punta izquierda de la pantalla (se busca centrarla)
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2) - 30)
        # -30 por la barra  de tareas en la parte inferior

        # Colocando el ancho, alto de la ventana y la cordenada en la que se va a ubicar la misma
        self.window.geometry(
            f"{window_width}x{window_height}+{x}+{y}"
        )

        ProductModel.create_table()

        frame_table = LabelFrame(
            self.window, text="Informacion Del Producto", font=("Calibri", 14))
        frame_form = LabelFrame(
            self.window, text="Datos Del Producto", font=("Calibri", 14))

        frame_table.pack(fill="both", expand="yes", padx=20, pady=10)
        frame_form.pack(fill="both", expand="yes", padx=20, pady=10)

        # Creando y colocando la tabla en el frame_table
        self.table = MyTable(frame_table)

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
        self.table.clear_table()

        all_products = ProductModel.get_all()
        self.table.insert_all_products(all_products)

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
        product = self.table.get_product()

        ProductModel.delete(product.id)

        self.get_all_data()

    def product_editing_window(self):
        product = self.table.get_product()

        self.edit_window = Toplevel()
        self.edit_window.title("Actualizar")
        self.edit_window.geometry("400x200")

        frame = LabelFrame(
            self.edit_window, text="Actualizar Producto",  font=("Calibri", 12))
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        input_old_price = MyInput(
            master=frame, label_text="Antiguo Precio: ", position=(2, 1))
        input_old_price.disabled()
        input_old_price.set_text(product.price)

        input_new_price = MyInput(
            master=frame, label_text="Nuevo Precio: ", position=(3, 1))

        input_old_quantity = MyInput(
            master=frame, label_text="Antiguo Precio: ", position=(4, 1))
        input_old_quantity.disabled()
        input_old_quantity.set_text(product.quantity)

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
                product.id
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

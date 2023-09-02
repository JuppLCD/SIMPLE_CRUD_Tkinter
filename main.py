# Codigo de Programadork100
# Titulo del video
# Codigo base en github = https://github.com/programadork/codigo_ejemplo
# Link video YT = https://www.youtube.com/watch?v=M07_zpAL0vk

from tkinter import ttk
from tkinter import Tk, LabelFrame, Button, Toplevel
import logging

from models.product import Product, ProductModel
from ui.my_widgets import MyInput

class AppProductos:
    base = 'productos.db'

    def __init__(self, root):
        self.wind = root
        self.wind.title("Productos")
        self.wind.geometry("850x600")

        ProductModel.create_table()

        frame1 = LabelFrame(
            self.wind, text="Informacion Del Producto", font=("Calibri", 14))
        frame2 = LabelFrame(
            self.wind, text="Datos Del Producto", font=("Calibri", 14))

        frame1.pack(fill="both", expand="yes", padx=20, pady=10)
        frame2.pack(fill="both", expand="yes", padx=20, pady=10)

        self.trv = ttk.Treeview(frame1, columns=(
            1, 2, 3, 4), show="headings", height="5")
        self.trv.pack()

        self.trv.heading(1, text="ID Del Producto")
        self.trv.heading(2, text="Nombre Del Producto")
        self.trv.heading(3, text="Precio Del Producto")
        self.trv.heading(4, text="Cantidad Del Producto")

        self.consulta()

        self.inputs = dict()
        self.inputs['ID'] = MyInput(
            master=frame2,
            label_text="ID Del Producto",
            position=(0,0)
        )
        self.inputs['NAME'] = MyInput(
            master=frame2,
            label_text="Nombre Del Producto",
            position=(1,0)
        )
        self.inputs['PRICE'] = MyInput(
            master=frame2,
            label_text="Precio Del Producto",
            position=(2,0)
        )
        self.inputs['QUANTITY'] = MyInput(
            master=frame2,
            label_text="Cantidad Del Producto",
            position=(3,0)
        )


        btn1 = Button(frame2, text="Agregar",
                      command=self.Agregar, width=12, height=2)
        btn1.grid(row=5, column=0)
        btn2 = Button(frame2, text="Eliminar",
                      command=self.Eliminar, width=12, height=2)
        btn2.grid(row=5, column=1)
        btn3 = Button(frame2, text="Actualizar",
                      command=self.Actualizar, width=12, height=2)
        btn3.grid(row=5, column=2)

    def consulta(self):
        book = self.trv.get_children()
        for element in book:
            self.trv.delete(element)

        rows = ProductModel.get_all()

        for row in rows:
            self.trv.insert('', 0, text=row[1], values=row)

    def validar(self):
        return not (self.inputs["ID"].is_empty() and self.inputs["NAME"].is_empty() and self.inputs["PRICE"].is_empty() and self.inputs["QUANTITY"].is_empty())

    def Agregar(self):
        if self.validar():
            name=self.inputs["NAME"].get_text()
            price=self.inputs["PRICE"].get_text()
            quantity=self.inputs["QUANTITY"].get_text()
            product_id=self.inputs["ID"].get_text()

            new_product = Product(name, price, quantity, product_id)
            ProductModel.store(new_product)

            self.inputs["ID"].clear_text()
            self.inputs["NAME"].clear_text()
            self.inputs["PRICE"].clear_text()
            self.inputs["QUANTITY"].clear_text()
        else:
            print("Los campos estan vacios")
        self.consulta()

    def Eliminar(self):
        try:
            self.trv.item(self.trv.selection())['text']
        # except IndexError as e:
        #     return
        except Exception as e:
            logging. exception(e)
            return
        
        product_id = self.trv.item(self.trv.selection())['values'][0]

        ProductModel.delete(product_id)

        self.consulta()

    def Actualizar(self):
        try:
            self.trv.item(self.trv.selection())['text']
        # except IndexError as e:
        #     print(e)
        #     return
        except Exception as e:
            logging. exception(e)
            return

        product_id = self.trv.item(self.trv.selection())['values'][0]
        old_price = self.trv.item(self.trv.selection())['values'][2]
        old_quantity = self.trv.item(self.trv.selection())['values'][3]

        self.edit_wind = Toplevel()
        self.edit_wind.title("Actualizar")
        self.edit_wind.geometry("400x300")

        frame = LabelFrame(
            self.edit_wind, text="Actualizar Producto",  font=("Calibri", 12))
        frame.pack(fill="both", expand="yes", padx=20, pady=10)

        input_old_price = MyInput(master=frame, label_text="Antiguo Precio: ",position=(2,1))
        input_old_price.disabled()
        input_old_price.set_text(old_price)

        input_new_price = MyInput(master=frame, label_text="Nuevo Precio: ",position=(3,1))

        input_old_quantity = MyInput(master=frame, label_text="Antiguo Precio: ",position=(4,1))
        input_old_quantity.disabled()
        input_old_quantity.set_text(old_quantity)

        input_new_quantity = MyInput(master=frame, label_text="Nuevo Precio: ",position=(5,1))

        Button(
            frame,
            text="Actualizar",
            command=lambda: self.edit_record(input_new_price.get_text(),
                                             input_new_quantity.get_text(),
                                             product_id
                                             ),
            width=12,
            height=2
            ).grid(
                row=7,
                column=2,
                pady=20
            )

    def edit_record(self, new_price, new_quantity, product_id):
        ProductModel.update(new_price, new_quantity, product_id)

        self.edit_wind.destroy()
        self.consulta()


if __name__ == '__main__':
    root = Tk()
    product = AppProductos(root)
    root.mainloop()
from .connection import Connection

class Product:
    def __init__(self, name, price, quantity, product_id = None ):
        self.name = name
        self.price = price
        self.quantity = quantity

        if product_id != None:
            self.id = product_id


class ProductModel:
    _conn = Connection()

    @staticmethod
    def create_table():
        query = """
            CREATE TABLE IF NOT EXISTS products(
            id INTEGER,
            name varchar(100) NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT))
            """

        ProductModel._conn.run_query(query)

    @staticmethod
    def get_all():
        query = 'SELECT id, name, price, quantity FROM products'
        products = ProductModel._conn.run_query(query)

        # TODO: Luego cambiar a retornar la lista formateada
        # all_products = []
        # for product_db in products:
        #     product = Product(product_id=product_db[0], name=product_db[1], price=product_db[2], quantity=product_db[3])
        #     all_products.append(product)
        
        return products

    @staticmethod
    def store(product : Product):
        query = 'INSERT INTO products VALUES(?,?,?,?)'
        parameters = (product.id, product.name, product.price, product.quantity)

        ProductModel._conn.run_query(query, parameters)

    @staticmethod
    def update(new_price, new_quantity, product_id):
        query = 'UPDATE products SET price = ?, quantity = ? WHERE id = ?'
        parameters =  ( new_price, new_quantity, product_id)

        ProductModel._conn.run_query(query, parameters)

    @staticmethod
    def delete(product_name):
        query = 'DELETE FROM products WHERE name = ?'
        ProductModel._conn.run_query(query, (product_name))


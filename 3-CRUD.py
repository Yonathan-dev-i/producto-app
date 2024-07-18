from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3

class ProductoApp:
    db_name = 'database_proyecto.db'

    def __init__(self, root):
        self.window = root
        self.window.title("APLICACIÓN")
        self.window.geometry("800x670")
        self.window.resizable(0, 0)
        self.window.config(bd=10)

        self.create_widgets()
        self.create_table()
        self.fetch_products()

    def create_widgets(self):
        # Título
        Label(self.window, text="REGISTRO DE PRODUCTOS ELECTRÓNICOS", fg="black", font=("Comic Sans", 17, "bold"), pady=10).pack()

        # Logos de productos
        self.create_logo_frame()

        # Formulario
        self.create_form_frame()

        # Botones
        self.create_button_frame()

        # Tabla
        self.create_table_frame()

    def create_logo_frame(self):
        frame_logo_productos = LabelFrame(self.window, bd=0)
        frame_logo_productos.pack()

        logos = [("arduino-logo.png", 0), ("nodemcu-logo.png", 1), ("raspberry-logo.png", 2)]
        for logo, col in logos:
            image = Image.open(f"C:/Users/hp/Downloads/{logo}")
            resized_image = image.resize((60, 60))
            render = ImageTk.PhotoImage(resized_image)
            label = Label(frame_logo_productos, image=render)
            label.image = render
            label.grid(row=0, column=col, padx=15, pady=5)

    def create_form_frame(self):
        frame = LabelFrame(self.window, text="Información del producto", font=("Comic Sans", 10, "bold"), pady=5)
        frame.config(bd=2)
        frame.pack()

        fields = [
            ("Código del producto: ", self.create_entry, 0, 0),
            ("Nombre del producto: ", self.create_entry, 1, 0),
            ("Categoría: ", self.create_combobox, 2, 0),
            ("Cantidad: ", self.create_entry, 0, 2),
            ("Precio (S/.): ", self.create_entry, 1, 2),
            ("Descripción: ", self.create_entry, 2, 2)
        ]

        for text, method, row, col in fields:
            Label(frame, text=text, font=("Comic Sans", 10, "bold")).grid(row=row, column=col, sticky='s', padx=5, pady=8)
            method(frame, row, col + 1)

    def create_entry(self, frame, row, col):
        entry = Entry(frame, width=25)
        entry.grid(row=row, column=col, padx=5, pady=8)
        if row == 0 and col == 1:
            self.codigo = entry
            self.codigo.focus()
        elif row == 1 and col == 1:
            self.nombre = entry
        elif row == 0 and col == 3:
            self.cantidad = entry
        elif row == 1 and col == 3:
            self.precio = entry
        elif row == 2 and col == 3:
            self.descripcion = entry

    def create_combobox(self, frame, row, col):
        self.combo_categoria = ttk.Combobox(frame, values=["Microcontrolador", "Microordenador", "Sensores", "Accesorios"], width=22, state="readonly")
        self.combo_categoria.current(0)
        self.combo_categoria.grid(row=row, column=col, padx=5, pady=0)

    def create_button_frame(self):
        frame = Frame(self.window)
        frame.pack()

        buttons = [
            ("REGISTRAR", self.add_product, "green"),
            ("EDITAR", self.edit_product, "gray"),
            ("ELIMINAR", self.delete_product, "red")
        ]

        for text, command, color in buttons:
            Button(frame, text=text, command=command, height=2, width=10, bg=color, fg="white", font=("Comic Sans", 10, "bold")).pack(side=LEFT, padx=10, pady=15)

    def create_table_frame(self):
        self.tree = ttk.Treeview(height=13, columns=("columna1", "columna2", "columna3", "columna4", "columna5"))
        self.tree.heading("#0", text='Código', anchor=CENTER)
        self.tree.column("#0", width=90, minwidth=75, stretch=NO)

        self.tree.heading("columna1", text='Nombre', anchor=CENTER)
        self.tree.column("columna1", width=150, minwidth=75, stretch=NO)

        self.tree.heading("columna2", text='Categoría', anchor=CENTER)
        self.tree.column("columna2", width=150, minwidth=75, stretch=NO)

        self.tree.heading("columna3", text='Cantidad', anchor=CENTER)
        self.tree.column("columna3", width=70, minwidth=60, stretch=NO)

        self.tree.heading("columna4", text='Precio', anchor=CENTER)
        self.tree.column("columna4", width=70, minwidth=60, stretch=NO)

        self.tree.heading("columna5", text='Descripción', anchor=CENTER)
        self.tree.pack()

    def execute_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def fetch_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM Productos ORDER BY Nombre desc'
        db_rows = self.execute_query(query)
        for row in db_rows:
            self.tree.insert("", 0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))

    def validate_form(self):
        return all([self.codigo.get(), self.nombre.get(), self.combo_categoria.get(), self.cantidad.get(), self.precio.get(), self.descripcion.get()])

    def clear_form(self):
        self.codigo.delete(0, END)
        self.nombre.delete(0, END)
        self.cantidad.delete(0, END)
        self.precio.delete(0, END)
        self.descripcion.delete(0, END)

    def add_product(self):
        if self.validate_form():
            query = 'INSERT INTO Productos VALUES(NULL, ?, ?, ?, ?, ?, ?)'
            parameters = (self.codigo.get(), self.nombre.get(), self.combo_categoria.get(), self.cantidad.get(), self.precio.get(), self.descripcion.get())
            self.execute_query(query, parameters)
            messagebox.showinfo("Registro exitoso", f'Producto registrado: {self.nombre.get()}')
            self.clear_form()
            self.fetch_products()
        else:
            messagebox.showerror("Error", "Complete todos los campos del formulario")

    def delete_product(self):
        try:
            selected_item = self.tree.selection()[0]
            codigo = self.tree.item(selected_item)['text']
            nombre = self.tree.item(selected_item)['values'][0]
            query = "DELETE FROM Productos WHERE Codigo = ?"
            response = messagebox.askquestion("Advertencia", f"¿Seguro que desea eliminar el producto: {nombre}?")
            if response == 'yes':
                self.execute_query(query, (codigo,))
                self.fetch_products()
                messagebox.showinfo('Éxito', f'Producto eliminado: {nombre}')
        except IndexError:
            messagebox.showerror("Error", "Por favor seleccione un elemento")

    def edit_product(self):
        try:
            selected_item = self.tree.selection()[0]
            codigo = self.tree.item(selected_item)['text']
            nombre = self.tree.item(selected_item)['values'][0]
            categoria = self.tree.item(selected_item)['values'][1]
            cantidad = self.tree.item(selected_item)['values'][2]
            precio = self.tree.item(selected_item)['values'][3]
            descripcion = self.tree.item(selected_item)['values'][4]

            self.edit_window = Toplevel()
            self.edit_window.title('Editar Producto')
            self.edit_window.resizable(0, 0)

            fields = [
                ("Código del producto: ", codigo, 0, 0),
                ("Nombre del producto: ", nombre, 1, 0),
                ("Categoría: ", categoria, 2, 0),
                ("Cantidad: ", cantidad, 0, 2),
                ("Precio (S/.): ", precio, 1, 2),
                ("Descripción: ", descripcion, 2, 2)
            ]

            self.edit_entries = {}
            for text, value, row, col in fields:
                Label(self.edit_window, text=text, font=("Comic Sans", 10, "bold")).grid(row=row, column=col, sticky='s', padx=5, pady=8)
                entry = Entry(self.edit_window, textvariable=StringVar(self.edit_window, value=value), width=25)
                entry.grid(row=row, column=col + 1, padx=5, pady=8)
                self.edit_entries[text] = entry

            ttk.Combobox(self.edit_window, values=["Microcontrolador", "Microordenador", "Sensores", "Accesorios"], width=22, state="readonly").set(categoria)

            Button(self.edit_window, text="Actualizar", command=lambda: self.update_product(codigo, nombre), height=2, width=20, bg="black", fg="white", font=("Comic Sans", 10, "bold")).grid(row=3, column=1, columnspan=2, padx=10, pady=15)
        except IndexError:
            messagebox.showerror("Error", "Por favor seleccione un elemento")

    def update_product(self, old_codigo, old_nombre):
        new_values = {k: v.get() for k, v in self.edit_entries.items()}
        query = 'UPDATE Productos SET Codigo = ?, Nombre = ?, Categoria = ?, Cantidad =?, Precio=?, Descripcion =? WHERE Codigo = ? AND Nombre =?'
        parameters = (new_values["Código del producto: "], new_values["Nombre del producto: "], self.combo_categoria.get(), new_values["Cantidad: "], new_values["Precio (S/.): "], new_values["Descripción: "], old_codigo, old_nombre)
        self.execute_query(query, parameters)
        messagebox.showinfo('Éxito', f'Producto actualizado: {new_values["Nombre del producto: "]}')
        self.edit_window.destroy()
        self.fetch_products()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS Productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Codigo TEXT NOT NULL,
            Nombre TEXT NOT NULL,
            Categoria TEXT NOT NULL,
            Cantidad INTEGER NOT NULL,
            Precio REAL NOT NULL,
            Descripcion TEXT NOT NULL
        )
        '''
        self.execute_query(query)

if __name__ == '__main__':
    root = Tk()
    app = ProductoApp(root)
    root.mainloop()

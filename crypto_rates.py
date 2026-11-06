from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Курсы криптовалют к USD')
root.geometry('420x380')

Label(root, text='Криптовалюты к доллару США',
      font=('Arial', 12, 'bold')).pack(pady=15)

tree = ttk.Treeview(root, columns=('name', 'price'), show='headings')
tree.heading('name', text='Монета')
tree.heading('price', text='Цена (USD)')
tree.pack()

Button(root, text='Обновить курсы').pack(pady=10)

root.mainloop()

import tkinter as tk
from tkinter import messagebox

class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        self.items[item_name] = price

    def remove_item(self, item_name):
        if item_name in self.items:
            del self.items[item_name]

    def get_price(self, item_name):
        return self.items.get(item_name, None)

    def update_price(self, item_name, new_price):
        if item_name in self.items:
            self.items[item_name] = new_price

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер магазинов")
        self.root.configure(bg="light gray")

        self.stores = []
        self.selected_store_index = None

        self.store_name_label = tk.Label(root, text="Название магазина:", bg="light gray")
        self.store_name_label.grid(row=0, column=0)
        self.store_name_entry = tk.Entry(root)
        self.store_name_entry.grid(row=0, column=1)

        self.store_address_label = tk.Label(root, text="Адрес магазина:", bg="light gray")
        self.store_address_label.grid(row=1, column=0)
        self.store_address_entry = tk.Entry(root)
        self.store_address_entry.grid(row=1, column=1)

        self.add_store_button = tk.Button(root, text="Добавить магазин", command=self.add_store)
        self.add_store_button.grid(row=2, column=0, columnspan=2)

        self.remove_store_button = tk.Button(root, text="Удалить магазин", bg="light pink", command=self.remove_store)
        self.remove_store_button.grid(row=3, column=0, columnspan=2)

        self.stores_listbox = tk.Listbox(root, width=50, height=10)
        self.stores_listbox.grid(row=4, column=0, columnspan=2)
        self.stores_listbox.bind("<<ListboxSelect>>", self.show_store_items)

        self.item_name_label = tk.Label(root, text="Наименование товара:", bg="light gray")
        self.item_name_label.grid(row=5, column=0)
        self.item_name_entry = tk.Entry(root)
        self.item_name_entry.grid(row=5, column=1)

        self.item_price_label = tk.Label(root, text="Цена товара:", bg="light gray")
        self.item_price_label.grid(row=6, column=0)
        self.item_price_entry = tk.Entry(root)
        self.item_price_entry.grid(row=6, column=1)

        self.add_item_button = tk.Button(root, text="Добавить товар", command=self.add_item)
        self.add_item_button.grid(row=7, column=0, columnspan=2)

        self.items_listbox = tk.Listbox(root, width=50, height=10)
        self.items_listbox.grid(row=8, column=0, columnspan=2)
        self.items_listbox.bind("<<ListboxSelect>>", self.on_item_select)

        self.remove_item_button = tk.Button(root, text="Удалить товар", bg="light pink", command=self.remove_item)
        self.remove_item_button.grid(row=9, column=0, columnspan=2)

        self.update_price_label = tk.Label(root, text="Новая цена:", bg="light gray")
        self.update_price_label.grid(row=10, column=0)
        self.update_price_entry = tk.Entry(root)
        self.update_price_entry.grid(row=10, column=1)

        self.update_price_button = tk.Button(root, text="Обновить цену", command=self.update_price)
        self.update_price_button.grid(row=11, column=0, columnspan=2)

    def add_store(self):
        name = self.store_name_entry.get()
        address = self.store_address_entry.get()
        if name and address:
            store = Store(name, address)
            self.stores.append(store)
            self.refresh_stores()
        else:
            messagebox.showerror("Error", "Пожалуйста, введите название и адрес")

    def remove_store(self):
        selected_index = self.stores_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Магазин не выбран")
            return

        store_index = selected_index[0]
        del self.stores[store_index]
        self.refresh_stores()
        self.selected_store_index = None
        self.items_listbox.delete(0, tk.END)

    def refresh_stores(self):
        self.stores_listbox.delete(0, tk.END)
        for store in self.stores:
            self.stores_listbox.insert(tk.END, f"{store.name} - {store.address}")

    def show_store_items(self, event):
        selected_index = self.stores_listbox.curselection()
        if not selected_index:
            return
        self.selected_store_index = selected_index[0]
        self.refresh_items(self.selected_store_index)

    def on_item_select(self, event):
        selected_index = self.items_listbox.curselection()
        if not selected_index:
            return

    def add_item(self):
        if self.selected_store_index is None:
            messagebox.showerror("Error", "Магазин не выбран")
            return

        item_name = self.item_name_entry.get()
        try:
            item_price = float(self.item_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Неправильная цена")
            return

        if item_name and item_price >= 0:
            self.stores[self.selected_store_index].add_item(item_name, item_price)
            self.refresh_items(self.selected_store_index)
        else:
            messagebox.showerror("Error", "Пожалуйста, введите товар и цену")

    def refresh_items(self, store_index):
        self.items_listbox.delete(0, tk.END)
        store = self.stores[store_index]
        for item_name, item_price in store.items.items():
            self.items_listbox.insert(tk.END, f"{item_name}: {item_price:.2f} Руб.")

    def remove_item(self):
        if self.selected_store_index is None:
            messagebox.showerror("Error", "Магазин не выбран")
            return

        selected_item_index = self.items_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror("Error", "Товар не выбран")
            return

        item_index = selected_item_index[0]
        item_name = list(self.stores[self.selected_store_index].items.keys())[item_index]
        self.stores[self.selected_store_index].remove_item(item_name)
        self.refresh_items(self.selected_store_index)

    def update_price(self):
        if self.selected_store_index is None:
            messagebox.showerror("Error", "Магазин не выбран")
            return

        selected_item_index = self.items_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror("Error", "Товар не выбран")
            return

        try:
            new_price = float(self.update_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Неправильная цена")
            return

        if new_price < 0:
            messagebox.showerror("Error", "Цена не может быть отрицательной")
            return

        item_index = selected_item_index[0]
        item_name = list(self.stores[self.selected_store_index].items.keys())[item_index]
        self.stores[self.selected_store_index].update_price(item_name, new_price)
        self.refresh_items(self.selected_store_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()

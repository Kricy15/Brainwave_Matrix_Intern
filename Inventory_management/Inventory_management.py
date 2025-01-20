
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os


class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.user_data = self.load_user_data()
        self.current_user = None
        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Inventory Management System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.login, width=30).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.sign_up, width=30).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=30).pack(pady=5)

    def load_user_data(self):
        if os.path.exists("user_Inventory.json"):
            with open("user_Inventory.json", "r") as file:
                return json.load(file)
        return {}

    def save_user_data(self):
        with open("user_Inventory.json", "w") as file:
            json.dump(self.user_data, file, indent=4)

    def login(self):
        username = simpledialog.askstring("Login", "Enter Username:")
        password = simpledialog.askstring("Login", "Enter Password:", show="*")

        if username in self.user_data and self.user_data[username]['password'] == password:
            self.current_user = username
            self.user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def sign_up(self):
        username = simpledialog.askstring("Sign Up", "Enter Username:")
        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists.")
            return
        password = simpledialog.askstring("Sign Up", "Enter Password:", show="*")
        self.user_data[username] = {'password': password, 'inventory': {}}
        self.save_user_data()
        messagebox.showinfo("Success", "Account created successfully!")

    def user_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Add Product", command=self.add_product, width=30).pack(pady=5)
        tk.Button(self.root, text="Edit Product", command=self.edit_product, width=30).pack(pady=5)
        tk.Button(self.root, text="Delete Product", command=self.delete_product, width=30).pack(pady=5)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory, width=30).pack(pady=5)
        tk.Button(self.root, text="Generate Low-Stock Report", command=self.low_stock_report, width=30).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout, width=30).pack(pady=5)

    def logout(self):
        self.save_user_data()
        self.current_user = None
        self.main_menu()

    def add_product(self):
        product_id = simpledialog.askstring("Add Product", "Enter Product ID:")
        if not product_id:
            return
        name = simpledialog.askstring("Add Product", "Enter Product Name:")
        if not name:
            return
        name = name.lower()
        quantity = simpledialog.askinteger("Add Product", "Enter Quantity:", minvalue=0)
        price = simpledialog.askfloat("Add Product", "Enter Price:", minvalue=0)

        if product_id and name and quantity is not None and price is not None:
            user_inventory = self.user_data[self.current_user]['inventory']
            for pid, details in user_inventory.items():
                if details['name'].lower() == name:
                    messagebox.showerror("Error", f"Product '{name}' already exists.")
                    return
            user_inventory[product_id] = {'name': name, 'quantity': quantity, 'price': price}
            self.save_user_data()
            messagebox.showinfo("Success", f"Product '{name}' added successfully.")
        else:
            messagebox.showerror("Error", "Please provide valid inputs.")

    def edit_product(self):
        product_id = simpledialog.askstring("Edit Product", "Enter Product ID to Edit:")
        user_inventory = self.user_data[self.current_user]['inventory']
        if not product_id or product_id not in user_inventory:
            messagebox.showerror("Error", "Product ID not found.")
            return

        name = simpledialog.askstring("Edit Product", "Enter New Name (Leave blank to keep current):")
        if name:
            name = name.lower()
        quantity = simpledialog.askinteger("Edit Product", "Enter New Quantity (Leave blank to keep current):", minvalue=0)
        price = simpledialog.askfloat("Edit Product", "Enter New Price (Leave blank to keep current):", minvalue=0)

        if name:
            for pid, details in user_inventory.items():
                if pid != product_id and details['name'].lower() == name:
                    messagebox.showerror("Error", f"Product with name '{name}' already exists.")
                    return
        if name:
            user_inventory[product_id]['name'] = name
        if quantity is not None:
            user_inventory[product_id]['quantity'] = quantity
        if price is not None:
            user_inventory[product_id]['price'] = price

        self.save_user_data()
        messagebox.showinfo("Success", "Product updated successfully.")

    def delete_product(self):
        product_id = simpledialog.askstring("Delete Product", "Enter Product ID to Delete:")
        user_inventory = self.user_data[self.current_user]['inventory']
        if not product_id or product_id not in user_inventory:
            messagebox.showerror("Error", "Product ID not found.")
            return

        del user_inventory[product_id]
        self.save_user_data()
        messagebox.showinfo("Success", "Product deleted successfully.")

    def view_inventory(self):
        user_inventory = self.user_data[self.current_user]['inventory']
        if not user_inventory:
            messagebox.showinfo("Inventory", "No products in inventory.")
            return

        inventory_list = "ID\tName\tQuantity\tPrice\tTotal Price\n"
        inventory_list += "-" * 50 + "\n"
        grand_total = 0
        for pid, details in user_inventory.items():
            total_price = details['quantity'] * details['price']
            grand_total += total_price
            inventory_list += f"{pid}\t{details['name']}\t{details['quantity']}\t{details['price']:.2f}\t{total_price:.2f}\n"

        inventory_list += "-" * 50 + "\n"
        inventory_list += f"Grand Total:\t\t\t\t{grand_total:.2f}\n"

        messagebox.showinfo("Inventory", inventory_list)

    def low_stock_report(self):
        threshold = simpledialog.askinteger("Low-Stock Report", "Enter Threshold:", minvalue=0)
        if threshold is None:
            return

        user_inventory = self.user_data[self.current_user]['inventory']
        low_stock_data = [
            f"{pid}: {details['name']} (Qty: {details['quantity']})"
            for pid, details in user_inventory.items()
            if details['quantity'] <= threshold
        ]

        if low_stock_data:
            messagebox.showinfo("Low Stock Report", "\n".join(low_stock_data))
        else:
            messagebox.showinfo("Low Stock Report", "No low-stock products found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib import pyplot as plt
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import json

class Product:
    def __init__(self, code, name, quantity, value, description, category, min_stock=10):
        self.code = code
        self.name = name
        self.quantity = quantity
        self.value = value
        self.description = description
        self.category = category
        self.min_stock = min_stock

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "quantity": self.quantity,
            "value": self.value,
            "description": self.description,
            "category": self.category
        }

class ProductApp:
    def __init__(self, root):
        self.products = []
        self.root = root
        self.root.title("Professional Product Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#F7F9FC")  # Background color

        # Main Frame Layout
        self.main_frame = tk.Frame(root, padx=10, pady=10, bg="#F7F9FC")
        self.main_frame.pack(fill="both", expand=True)

        # Adding the title
        tk.Label(self.main_frame, text="Product Management System", font=("Arial", 16, "bold"), bg="#F7F9FC").pack(pady=10)

        # Tabs for different functions
        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.pack(fill="both", expand=True)

        # Adding Product Tab
        self.add_product_tab = tk.Frame(self.tabs, bg="#F7F9FC")
        self.tabs.add(self.add_product_tab, text="Add Product")
        self.create_add_product_tab()

        # List Products Tab
        self.list_product_tab = tk.Frame(self.tabs, bg="#F7F9FC")
        self.tabs.add(self.list_product_tab, text="List Products")
        self.create_list_product_tab()

        # Alert Low Stock Tab
        self.low_stock_tab = tk.Frame(self.tabs, bg="#F7F9FC")
        self.tabs.add(self.low_stock_tab, text="Low Stock Alert")
        self.create_low_stock_tab()

        # Export and Plot Tab
        self.export_plot_tab = tk.Frame(self.tabs, bg="#F7F9FC")
        self.tabs.add(self.export_plot_tab, text="Export & Plot")
        self.create_export_plot_tab()

    def create_add_product_tab(self):
        tk.Label(self.add_product_tab, text="Add New Product", font=("Arial", 14), bg="#F7F9FC").grid(row=0, columnspan=2, pady=10)

        # Frame for entry fields
        entry_frame = tk.Frame(self.add_product_tab, padx=20, pady=20, bg="#FFFFFF", relief="sunken", bd=2)
        entry_frame.grid(row=1, column=0, columnspan=2, pady=10)

        fields = ["Code", "Name", "Quantity", "Value", "Description", "Category", "Min Stock"]
        self.entries = {}
        for i, field in enumerate(fields):
            label = tk.Label(entry_frame, text=field, font=("Arial", 12), bg="#FFFFFF")
            label.grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = tk.Entry(entry_frame, font=("Arial", 12), bd=2, relief="solid")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[field] = entry

        tk.Button(self.add_product_tab, text="Add Product", command=self.add_product, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=len(fields) + 2, columnspan=2, pady=10)

    def create_list_product_tab(self):
        tk.Label(self.list_product_tab, text="List of Products", font=("Arial", 14), bg="#F7F9FC").grid(row=0, columnspan=2, pady=10)
        self.tree = ttk.Treeview(self.list_product_tab, columns=("Code", "Name", "Quantity", "Value", "Category"), show="headings")
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")  # Center align the columns
            
        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.list_product_tab, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')

        # Configure grid to expand properly
        self.list_product_tab.grid_rowconfigure(1, weight=1)
        self.list_product_tab.grid_columnconfigure(0, weight=1)

        tk.Button(self.list_product_tab, text="Refresh List", command=self.populate_list, bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=2, column=1, pady=5)

    def create_low_stock_tab(self):
        tk.Label(self.low_stock_tab, text="Low Stock Products", font=("Arial", 14), bg="#F7F9FC").grid(row=0, columnspan=2, pady=10)
        self.low_stock_tree = ttk.Treeview(self.low_stock_tab, columns=("Code", "Name", "Quantity", "Min Stock"), show="headings")
        
        for col in self.low_stock_tree["columns"]:
            self.low_stock_tree.heading(col, text=col)
            self.low_stock_tree.column(col, anchor="center")  # Center align the columns
            
        self.low_stock_tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Add a vertical scrollbar
        low_stock_scrollbar = ttk.Scrollbar(self.low_stock_tab, orient="vertical", command=self.low_stock_tree.yview)
        self.low_stock_tree.configure(yscroll=low_stock_scrollbar.set)
        low_stock_scrollbar.grid(row=1, column=2, sticky='ns')

        # Configure grid to expand properly
        self.low_stock_tab.grid_rowconfigure(1, weight=1)
        self.low_stock_tab.grid_columnconfigure(0, weight=1)

        tk.Button(self.low_stock_tab, text="Check Low Stock", command=self.alert_low_stock, bg="#F44336", fg="white", font=("Arial", 12)).grid(row=2, column=1, pady=5)

    def create_export_plot_tab(self):
        tk.Button(self.export_plot_tab, text="Export to Excel", command=self.export_to_excel, width=20, bg="#FFC107", fg="black", font=("Arial", 12)).grid(row=0, column=0, pady=20)
        tk.Button(self.export_plot_tab, text="Plot Quantity by Category", command=self.plot_quantity_by_category, width=20, bg="#673AB7", fg="white", font=("Arial", 12)).grid(row=1, column=0, pady=20)

    def add_product(self):
        try:
            code = int(self.entries["Code"].get())
            name = self.entries["Name"].get()
            quantity = int(self.entries["Quantity"].get())
            value = float(self.entries["Value"].get())
            description = self.entries["Description"].get()
            category = self.entries["Category"].get()
            min_stock = int(self.entries["Min Stock"].get())

            product = Product(code, name, quantity, value, description, category, min_stock)
            self.products.append(product)
            messagebox.showinfo("Success", "Product added successfully!")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid data.")

    def populate_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for product in self.products:
            self.tree.insert("", tk.END, values=(product.code, product.name, product.quantity, product.value, product.category))

    def alert_low_stock(self):
        for row in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(row)
        low_stock_products = [p for p in self.products if p.quantity < p.min_stock]
        if low_stock_products:
            for product in low_stock_products:
                self.low_stock_tree.insert("", tk.END, values=(product.code, product.name, product.quantity, product.min_stock))
        else:
            messagebox.showinfo("Stock Status", "All products have sufficient stock.")

    def export_to_excel(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Products"

        # Define the headers
        headers = ["Code", "Name", "Quantity", "Value", "Description", "Category"]
        sheet.append(headers)

        for product in self.products:
            sheet.append(product.to_dict().values())

        # Apply formatting to the header row
        for cell in sheet[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')

        # Auto-adjust column widths
        for column in sheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width

        # Save the workbook
        workbook.save("products.xlsx")
        messagebox.showinfo("Export Successful", "Products exported to products.xlsx")

    def plot_quantity_by_category(self):
        categories = {}
        for product in self.products:
            if product.category in categories:
                categories[product.category] += product.quantity
            else:
                categories[product.category] = product.quantity

        plt.bar(categories.keys(), categories.values())
        plt.title("Quantity of Products by Category")
        plt.xlabel("Category")
        plt.ylabel("Quantity")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()

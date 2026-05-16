import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import database
from datetime import datetime
from subprocess import call


#-------------------------------------------------------------------------------------------------------------------------------------------


# Create the main window
root = ctk.CTk()
root.title("PyHorseᴳ¹ POS")
root.iconbitmap("PyHorse Logo.ico")
root.configure(bg="#0A0B0C")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (screen_width, screen_height))
root.focus_set()


#--------------------------------------------------------------------------------------------------------------------------------------------


font1 = ('Arial', 25, 'bold')
font2 = ('Arial', 18, 'bold')
font3 = ('Arial', 13, 'bold')


def create_chart():
    product_details = database.fetch_products()
    product_names = [product[1] for product in product_details]
    stock_values = [product[3] for product in product_details]

    figure = Figure(figsize=(10, 5), dpi=110, facecolor="#0A0B0C")
    ax = figure.add_subplot(111)
    ax.bar(product_names, stock_values, width=0.5, color='#f01e2c')
    ax.set_xlabel("Product Name", color='#fff', fontsize=15)
    ax.set_ylabel("Stock Value", color='#fff', fontsize=15)
    ax.set_title("Product Stock Levels", color='#fff', fontsize=15)
    ax.tick_params(axis='y', labelcolor='#fff', labelsize=12)
    ax.tick_params(axis='x', labelcolor='#fff', labelsize=12)
    ax.set_facecolor('#1b181b')

    canvas = FigureCanvasTkAgg(figure)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6, column=6, padx=790, pady=(510,0))


def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        category_entry.insert(0, row[2])
        stock_entry.insert(0, row[3])
        price_entry.insert(0, row[4])
        date_added_entry.insert(0, row[5])
    else:
        pass


def add_to_treeview():
    products = database.fetch_products()
    tree.delete(*tree.get_children())
    for product in products: 
        tree.insert('', END, values=product)


def insert():
    name = name_entry.get()
    category = category_entry.get()
    stock = stock_entry.get()
    price = price_entry.get()
    date = date_added_entry.get()


    # Check if the product name already exists
    existing_product = database.name_exist(name) # Assuming this function checks if name exists
    if existing_product:
        messagebox.showerror("Error", "Product name already exists.")
        return
            

    # Check if all fields are filled
    elif not (name and category and stock and price and date):
        messagebox.showerror('Error', 'Enter all fields')
        return

    # Convert stock and price to integers
    try:
        stock_values = int(stock)
        price_values = int(price)
    except ValueError:
        messagebox.showerror('Error', 'Stock and Price should be an integer.')
        return
    
    #Validate date format and convert to desired format
    try:
        date_added_obj = datetime.strptime(date, '%Y-%m-%d')  # Parse date string into a datetime object
        date = date_added_obj.strftime('%Y-%m-%d')    # Format datetime object into YYYY-MM-DD string
    except ValueError:
        messagebox.showwarning('Warning', 'Date should be in YYYY-MM-DD format.')
        return

    # Insert the new product
    database.insert_product(name, category, stock_values, price_values, date)
    add_to_treeview()
    clear()
    create_chart()
    messagebox.showinfo('Success', 'Data has been Added.')
    return




def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    category_entry.delete(0, END)
    price_entry.delete(0, END)
    stock_entry.delete(0, END)
    date_added_entry.delete(0, END)


def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to delete.')
    else:
        id = tree.item(selected_item)['values'][0]
        database.delete_product(id)
        tree.delete(selected_item)
        create_chart()
        messagebox.showinfo('Success', 'Data has bee deleted.')


def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a product to update.')
    else:
        id = id_entry.get()
        name = name_entry.get()
        category = category_entry.get()
        stock = stock_entry.get()
        price = price_entry.get()
        date = date_added_entry.get()
    try:
        stock_values = int(stock)
        price_values = int(price)
    except ValueError:
        messagebox.showerror('Error', 'Stock and Price should be an integer.')

   # Validate date format and convert to desired format
    try:
        date_added_obj = datetime.strptime(date, '%Y-%m-%d')  # Parse date string into a datetime object
        date = date_added_obj.strftime('%Y-%m-%d')    # Format datetime object into YYYY-MM-DD string
    except ValueError:
        messagebox.showwarning('Warning', 'Date should be in YYYY-MM-DD format.')
        return

    
    database.update_product(name, category, stock_values, price_values, date, id)
    add_to_treeview()
    clear()
    create_chart()
    messagebox.showinfo('Success', 'Data has been updated.')




def log_out():
    sure = messagebox.askyesno("Exit","Are you sure you want to go back?", parent=root)
    if sure is None:
        return
    elif sure == True:
        save_changes()
        main_file()
        root.destroy()
        

def main_file():
    call(["python", "PyHorse Admin.py"])
    root.deiconify()

def save_changes():
    messagebox.showinfo("Saved", "Saved Successfully")

title_label = ctk.CTkLabel(root, font=font1, text='PyHorse Liquor Details', text_color='#fff', bg_color='#0A0B0C')
title_label.place(x=35, y=0)

frame = ctk.CTkFrame(root, bg_color='#0A0B0C', fg_color='#1B1B21', corner_radius=10, border_width=2, border_color='#fff', width=475, height=400)
frame.place(x=25, y=35)

stock_entry = ctk.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
stock_entry.place(x=255, y=230)

image1 = PhotoImage(file="PyHorse Logo.png")
resized_image = image1.subsample(2, 3)  # Adjust these values according to your desired size
image1_label = Label(frame, image=resized_image, bg='#1B1B21')
image1_label.place(x=230, y=20)

id_label = ctk.CTkLabel(frame, font=font2, text='Liquor ID:', text_color='#fff', bg_color='#1B1B21')
id_label.place(x=85, y=140)



id_entry = ctk.CTkEntry(frame, font=font2, text_color='#000', placeholder_text="AUTO", fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
id_entry.place(x=30, y=170)



name_label = ctk.CTkLabel(frame, font=font2, text='Liquor Name:', text_color='#fff', bg_color='#1B1B21')
name_label.place(x=70, y=200)

name_entry = ctk.CTkEntry(frame, font=font2, text_color='#000', placeholder_text="Product Name", fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
name_entry.place(x=30, y=230)

category_label = ctk.CTkLabel(frame, font=font2, text='Category:', text_color='#fff', bg_color='#1B1B21')
category_label.place(x=85, y=260)

category_entry = ctk.CTkEntry(frame, font=font2, text_color='#000', placeholder_text="Product Category", fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
category_entry.place(x=30,y=290)

price_label = ctk.CTkLabel(frame, font=font2, text='Price:', text_color='#fff', bg_color='#1B1B21')
price_label.place(x=328, y=140)

price_entry = ctk.CTkEntry(frame, font=font2, text_color='#000', placeholder_text="₱", fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
price_entry.place(x=255, y=170)

stock_label = ctk.CTkLabel(frame, font=font2, text='Stock:', text_color='#fff', bg_color='#1B1B21')
stock_label.place(x=325, y=200)

stock_entry = ctk.CTkEntry(frame, font=font2, text_color='#000', placeholder_text="Qty.", fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
stock_entry.place(x=255, y=230)

date_label = ctk.CTkLabel(frame, font=font2, text='Date Added:', text_color='#fff', bg_color='#1B1B21')
date_label.place(x=300, y=260)

date_added_entry = ctk.CTkEntry(frame, font=font2, text_color='#000',  placeholder_text="YYYY-MM-DD", fg_color='#fff', border_color='#B2016C', border_width=2, width=190)
date_added_entry.place(x=255, y=290)

add_button = ctk.CTkButton(frame, command=insert,  font=font2, text_color='#fff', text='Add', fg_color='#047E43', hover_color='#025B30', bg_color='#1B1B21', cursor='hand2', corner_radius=8, width=95)
add_button.place(x=30, y=350)

new_button = ctk.CTkButton(frame, command=lambda: clear(True), font=font2, text_color='#fff', text='New', fg_color='#E93E05', hover_color='#A82A00', bg_color='#1B1B21', cursor='hand2', corner_radius=8, width=95)
new_button.place(x=135, y=350)

update_button = ctk.CTkButton(frame, command=update, font=font2, text_color='#fff', text='Update', fg_color='#D20B02', hover_color='#A82A00', bg_color='#1B1B21', cursor='hand2', corner_radius=8, width=95)
update_button.place(x=243, y=350)

delete_button = ctk.CTkButton(frame, command=delete, font=font2, text_color='#fff', text='Delete', fg_color='#E93E05', hover_color='#8F0600', bg_color='#1B1B21', cursor='hand2', corner_radius=8, width=95)
delete_button.place(x=350, y=350)


out_button = ctk.CTkButton(root, command=log_out, font=('Arial Black', 15, "bold"), text_color='#fff', text='<', fg_color='Red', hover_color='#8F0600', bg_color='#1B1B21', cursor='hand2', corner_radius=8, width=60)
out_button.place(x=25, y=650)





style = ttk.Style(root)
style.theme_use('clam')
style.configure('Treeview', font=font3, foreground='#fff', background='#0A0BAC', fieldbackground='#1B1B21')
style.map('Treeview', background=[('selected', '#AA04A7')])

tree = ttk.Treeview(root, height=21)
tree['columns'] = ('ID', "Product Name",'Category', 'In Stock', 'Price', 'Date Added')

tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=100)
tree.column('Product Name', anchor=tk.CENTER, width=350)
tree.column('Category', anchor=tk.CENTER, width=150)
tree.column('In Stock', anchor=tk.CENTER, width=110)
tree.column('Price', anchor=tk.CENTER, width=170)
tree.column('Date Added', anchor=tk.CENTER, width=210)


tree.heading('ID', text='ID')
tree.heading('Product Name', text='Product Name')
tree.heading('Category', text='Category')
tree.heading('In Stock', text='In Stock')
tree.heading('Price', text='Price')
tree.heading('Date Added', text='Date Added')



tree.place(x=795, y=35)
tree.bind('<ButtonRelease-1>', display_data)
add_to_treeview()
create_chart()




root.mainloop()
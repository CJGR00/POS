import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import PhotoImage
import random
from datetime import date
import json
import smtplib
from email.message import EmailMessage
import ssl


class Item:
    def __init__(self, item, unit_cost):
        self.item = item
        self.unit_cost = unit_cost

    def add_item(self):
        item = self.item
        unit_cost = self.unit_cost
        quantity = 1

        # Check if the item is already in the treeview
        for child in tree.get_children():
            if tree.item(child, "text") == item:
                # If the item is already in the treeview, increment its quantity and update the display
                current_quantity = int(tree.item(child, "values")[1])
                tree.item(child, values=(item, current_quantity + 1, unit_cost))
                return

        # If the item is not in the treeview, add it as a new row
        tree.insert("", "end", text=item, values=(item, quantity, unit_cost))


class ItemDescription:
    def __init__(self, name, price, description, image_path):
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path


def show_popup(item_description):
    global popup
    popup = tk.Toplevel(root)
    popup.title(item_description.name)
    popup.geometry("250x490+1100+155")
    popup.resizable(False,False)
    popup.configure(bg="#fcf7f0")
    popup.iconbitmap("ui_images\\main_icon.ico")

    popupFrame = tk.Frame(popup)
    popupFrame.configure(bg="#fcf7f0")
    popupFrame.pack(pady=10)

    image = tk.PhotoImage(file=item_description.image_path)
    label_image = tk.Label(popupFrame, image=image, compound="center", bg="#fcf7f0")
    label_image.image = image  # Keep a reference to the image to prevent garbage collection
    label_image.grid(row=0, column=0, sticky=tk.NSEW)

    label_name = tk.Label(popupFrame, text=f"{item_description.name}", bg="#fcf7f0", font="Rockwell 17 bold", wraplength=200)
    label_name.grid(row=1, column=0, pady=(3,0))

    label_description = tk.Label(popupFrame, text=f"{item_description.description}", bg="#fcf7f0", font="Helvetica 11 italic", wraplength=170)
    label_description.grid(row=2, column=0, pady=(12, 0))

    label_price = tk.Label(popup, text=f"₱ {item_description.price}", bg="#745D42", font="Britannic 25 bold", fg="#FFFFFF")
    label_price.place(relwidth=1, y=420)

    # Load and display image


def on_enter(event):
    global enter_time
    button_descriptions = button_to_description[event.widget]
    enter_time = root.after(1000, lambda: show_popup(button_descriptions))


def on_leave(event):
    root.after_cancel(enter_time)
    root.after(500, destroy_popup)


def destroy_popup():
    global popup
    if 'popup' in globals():
        popup.destroy()


def calculate_total_cost():
    
    global total_cost, finaltax, actual_cost
    
    total_cost = 0.0

    # Iterate through each item in the treeview
    for item_id in tree.get_children():
        # Extract quantity and unit price from each item
        quantity = float(tree.item(item_id, "values")[1])
        unit_price = float(tree.item(item_id, "values")[2])

        # Calculate cost for this item and add it to the total
        item_cost = quantity * unit_price
        total_cost += item_cost

    #config the labels to show real time cost
    SubTotalAmont.config(text="\u20b1 " + str(total_cost))

    tax = total_cost * 0.12
    finaltax = round(tax, 2)

    VatTaxAmount.config(text="\u20b1 " + str(finaltax))

    final_cost = total_cost + tax
    actual_cost = round(final_cost)

    TotalCostAmount.config(text="\u20b1 " + str(actual_cost))

    return actual_cost


def remove_selected_item():
    selection = tree.selection()
    for item in selection:
        tree.delete(item)


def clear_all_items():
    answer = messagebox.askyesno("Clear", "Are you sure you want to clear your checkout list?")

    if answer:
        if not tree.get_children():
            messagebox.showinfo("Empty List", "The list is already empty.")
        else:
            for item in tree.get_children():
                tree.delete(item)


def CheckEntries():
    if due_date_combobox.get() == "Select Due Date":
        messagebox.showerror("Error", "Due Date is empty!")
    elif payment_combobox.get() == "Select Payment Method":
        messagebox.showerror("Error", "Payment Method is empty!")
    elif not tree.get_children():
        messagebox.showerror("Error", "Checkout List is empty!")
    else:
        PaymentWindow()


def validate_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False


def PaymentWindow():
    global name_entry, address_entry, postal_entry, phone_entry, email_entry, payment_window 

    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Window")
    payment_window.geometry("800x580")
    payment_window.configure(bg="#c4af84")
    payment_window.resizable(False, False)
    payment_window.iconbitmap("ui_images\\main_icon.ico")

    validate_cmd = payment_window.register(validate_input)

    paymentframe = tk.Frame(payment_window, bg="#c4af84")
    paymentframe.pack(fill=tk.BOTH, expand=True, padx=200, pady=40)

    paymentframe.columnconfigure((0,1), weight=1)
    paymentframe.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)

    paymentframe_image = tk.PhotoImage(file='ui_images\\paymentframe.png')
    bg_label = tk.Label(paymentframe, image=paymentframe_image, bg="#c4af84")
    bg_label.place(relwidth=1, relheight=1)
    paymentframe.image = paymentframe_image

    paymenttitle = tk.Label(paymentframe, text="PAYMENT DETAILS", font="Euphemia 18 bold", fg="#1c0a00", bg="#fcf7f0")
    paymenttitle.grid(row=0, column=0, columnspan=2, pady=(30, 0), padx=25, sticky=tk.W)

    name = tk.Label(paymentframe, text="Name", font="Courier 13 bold", fg="#1c0a00", bg="#fcf7f0")
    name.grid(row=1, column=0, pady=(15, 0), padx=25, sticky=tk.W)

    name_entry = tk.Entry(paymentframe, bd=2, font="Latha 12")
    name_entry.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=(0,20), padx=28)

    address = tk.Label(paymentframe, text="Address", font="Courier 13 bold", fg="#1c0a00", bg="#fcf7f0")
    address.grid(row=3, column=0, sticky=tk.W, pady=0, padx=25)

    address_entry = tk.Entry(paymentframe, bd=2, font="Latha 12")
    address_entry.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, pady=(0,20), padx=28)

    phonenumber = tk.Label(paymentframe, text="Phone Number", font="Courier 13 bold", fg="#1c0a00", bg="#fcf7f0")
    phonenumber.grid(row=5, column=0, pady=0, sticky=tk.W, padx=25)

    phone_entry = tk.Entry(paymentframe, validate="key", validatecommand=(validate_cmd, '%P'), bd=2, font="Latha 12")
    phone_entry.grid(row=6, column=0, sticky=tk.NSEW, pady=(0,20), padx=28)

    postal = tk.Label(paymentframe, text="Postal ID", font="Courier 13 bold", fg="#1c0a00", bg="#fcf7f0")
    postal.grid(row=5, column=1, pady=0, sticky=tk.W)

    postal_entry = tk.Entry(paymentframe, validate="key", validatecommand=(validate_cmd, '%P'), bd=2, font="Latha 12")
    postal_entry.grid(row=6, column=1, sticky=tk.NSEW, pady=(0,20), padx=(3, 28))

    email = tk.Label(paymentframe, text="Email Address", font="Courier 13 bold", fg="#1c0a00", bg="#fcf7f0")
    email.grid(row=7, column=0, pady=0, padx=25, sticky=tk.W)

    email_entry = tk.Entry(paymentframe, bd=2, font="Latha 12")
    email_entry.grid(row=8, column=0, columnspan=2, sticky=tk.NSEW, pady=(0,20), padx=28)

    checkoutpic = tk.PhotoImage(file="ui_images\\checkoutdb.png")

    confirm_checkout = tk.Button(paymentframe, bg="#fcf7f0", command=CheckPaymentCredentials, image=checkoutpic, bd=0)
    confirm_checkout.grid(row=9, column=0, columnspan=2, sticky=tk.NSEW, padx=30, pady=(0,40))
    confirm_checkout.image = checkoutpic


def CheckPaymentCredentials():
    if name_entry.get() and address_entry.get() and postal_entry.get() and phone_entry.get() and email_entry.get():
        ConfirmCheckout()
    else:    
        messagebox.showerror("Insufficient Information", "Kindly ensure all necessary credentials are provided before proceeding with the checkout process.")


def print_product_list():
    receipt = []
    items = tree.get_children()
    receipt.append("Item Description - Quantity - Unit Price")
    for item in items:
        values = tree.item(item, 'values')
        receipt.append(f"{values[0]} - {values[1]} - \u20b1{values[2]}")
    receipt_str = "\n".join(receipt)
    return receipt_str


def create_email_content():

    random_number = random.randint(100000, 999999)

    # Get user inputs from entry widgets
    invoice_number = "CS1C-" + str(random_number)
    today_date = date.today()
    invoice_date = today_date.strftime("%m-%d-%Y")
    client_name = name_entry.get()
    client_address = address_entry.get()
    client_number = phone_entry.get()
    client_email = email_entry.get()
    client_postal = postal_entry.get()
    subtotal = total_cost
    tax = finaltax
    total_amount = actual_cost
    payment_terms = due_date_combobox.get()
    payment_method = payment_combobox.get()
    products = print_product_list()
    email_content = f"""\
CRE4MY LATER
Imus City, Cavite, Philippines 4103
(+63) 945 0521 215 
crea4mylater@gmail.com

INVOICE
-----------------------------------------
Invoice Number: {invoice_number}
Date: {invoice_date}

Billed To:
{client_name}
{client_address}, {client_postal}
{client_number}
{client_email}

List of Products:
-----------------------------------------
{products}

Subtotal: ₱{subtotal}
VAT (12%): ₱{tax}
-----------------------------------------
Total Amount Due: ₱{total_amount}

Payment Due Date: {payment_terms}
Payment Method: {payment_method}

Thank you for your business!
"""

    # Email configuration
    #Currently print only, edit it later to integrate the email function
    
    return email_content


def ConfirmCheckout():
    final_cost = calculate_total_cost()
    response = messagebox.askyesno("Checkout", "Confirm Checkout?\nYour total bill is \u20b1 " + str(final_cost))

    if response:
        receipt = create_email_content()
        PrintReceipt()
        save_receipt(receipt)
        send_email()
        update_stock()
        clear_cart()
        payment_window.destroy()

    else:
        return


def clear_cart():
    # Get all item IDs in the treeview
    checkout_list = tree.get_children()

    # Delete each item from the treeview
    for item in checkout_list:
        tree.delete(item)
    
    due_date_combobox.set('Select Due Date') 
    payment_combobox.set('Select Payment Method')


def PrintReceipt():
    label = Toplevel()
    label.iconbitmap("ui_images\\main_icon.ico")
    label.configure(bg='#fcf7f0', pady=12, padx=28)
    text = Label(label, text=create_email_content(), bg='#fcf7f0').pack()


def hide_tab():
    for i in range(5):
        ShopFrame.hide(i)


def select_tab(i):
    ShopFrame.select(i)


def save_receipt(receipt):
    try:
        with open('purchase_history.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []

    data.append({'receipt': receipt})
    
    with open('purchase_history.json', 'w') as file:
        json.dump(data, file, indent=4)


def clear_json_file():
    result = messagebox.askquestion("Clear History", "Do you want to clear the history?")
    if result == "yes":    
        try:
            with open('purchase_history.json', 'w') as file:
                json.dump([], file)
            
            messagebox.showinfo("History Cleared", "Purchase history has been\ncleared succesfully!")

        except Exception as e:
            print(f"An error occurred while clearing data: {e}")
    
    else:
        return


def show_receipt(index):
    with open('purchase_history.json', 'r') as file:
        data = json.load(file)
    
    receipt = data[index - 1]  # Adjusting index to 0-based
    
    # Create another toplevel window to display the receipt details
    receipt_window = tk.Toplevel(root)
    receipt_window.title(f"Receipt {index}")
    receipt_window.configure(bg="#fcf7f0", padx=28)
    receipt_window.iconbitmap("ui_images\\main_icon.ico")
    
    # Create a label to display the receipt content
    receipt_label = tk.Label(receipt_window, text=receipt['receipt'], padx=20, pady=10, bg="#fcf7f0")
    receipt_label.pack(anchor=tk.CENTER)


def display_receipt_buttons():
    with open('purchase_history.json', 'r') as file:
        data = json.load(file)

    # Create a toplevel window to display buttons
    history_window = tk.Toplevel(root)
    history_window.title("Purchase History")
    history_window.geometry("500x550")  # Set specific size
    history_window.resizable(False, False)  # Make window non-resizable
    history_window.configure(bg="#B07038", padx=20,pady=20)
    history_window.iconbitmap("ui_images\\main_icon.ico")

    clear_image = tk.PhotoImage(file="ui_images\\clearhistory.png")
    clear_history = tk.Button(history_window, command=clear_json_file, image=clear_image, bd=0, bg="#B07038")
    clear_history.pack(pady=(0,12), anchor=tk.E)
    clear_history.image = clear_image

    canvas = tk.Canvas(history_window, bg="#FDF7F0", borderwidth=4, relief="ridge", highlightbackground="#626262", highlightcolor="#626262")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(history_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = tk.Frame(canvas, bg="#FDF7F0", pady=16)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    buttons = [] 

    for index, receipt in enumerate(data, start=1):
        button = tk.Button(frame, text=f"Receipt {index}",
                           command=lambda i=index: show_receipt(i), bg="#FDF6B8", width=23, bd=2, font="Century 11") 
        buttons.append(button)  

    for button in reversed(buttons):
        button.pack(pady=10, fill=tk.X, padx=(110,0))


def send_email():
    # Set up your Gmail account credentials
    sender_email = 'cre4mylater@gmail.com'
    sender_password = 'nvwh yjfj fjsv njux'

    # Recipient's email address
    recipient_email = email_entry.get()

    # Create a plain-text email message
    subject = 'Cre4my Later Purchase Invoice'
    body = create_email_content()

    em = EmailMessage()
    em['Subject'] = subject
    em['From'] = sender_email
    em['To'] = recipient_email
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        # Establish a secure connection with Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, recipient_email, em.as_string())
        messagebox.showinfo("Invoice sent", "Purchase invoice has been successfully sent\nto the designated email address.")
    except Exception as e:
        messagebox.showerror("Error sending email", f"{e}")  


def update_stock():
    # Get selected item from Treeview
    for item_id in tree.get_children():
        item_name = tree.item(item_id, 'values')[0]
        quantity = int(tree.item(item_id, 'values')[1])

        # Read JSON file
        with open("product_inventory.json", 'r') as file:
            data = json.load(file)
        
        # Update stock in JSON data
        for item_data in data:
            if item_name in item_data:  # Check if item_name is in the current item_data dictionary
                item_data[item_name] -= quantity
        
        # Write updated JSON data back to file
        with open("product_inventory.json", 'w') as file:
            json.dump(data, file)





root = tk.Tk()
root.title("CRE4MY LATER")
root.geometry("1100x650+5+30")
root.resizable(False, False)
root.grid_propagate(False)
root.configure(bg="#FFFFFF")
root.iconbitmap("ui_images\\main_icon.ico")

style = ttk.Style()
style.layout("TNotebook.Tab", [])
style.configure("TNotebook", tabmargins=-1)

HeaderFrame = tk.Frame(root, height=70, width=1100, bg="#DDD1B8")
HeaderFrame.grid(row=0, column=0)
HeaderFrame.grid_rowconfigure(0, weight=1)
HeaderFrame.grid_columnconfigure(0, weight=1)
HeaderFrame.grid_propagate(False)

creamylaterlogo = tk.PhotoImage(file='ui_images\\clogo.png')

bgcolor = tk.Label(HeaderFrame, bg='#DDD1B8', justify="left")
bgcolor.grid(row=0, column=0, sticky=tk.NSEW)

logo_image = tk.PhotoImage(file="ui_images\\clogo.png")

brand = tk.Label(HeaderFrame, bg='#DDD1B8', justify="left", image=logo_image)
brand.grid(row=0, column=0, sticky="w", padx=20, pady=(12,0))

bgcolorcheckout = tk.Label(HeaderFrame, bg='#DDD1B8', justify="left")
bgcolorcheckout.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)

cart_image = tk.PhotoImage(file="ui_images\\cart.png")
cartbutton = tk.Button(HeaderFrame, command=lambda:(select_tab(4)), bg='#DDD1B8', border=0, image=cart_image, width=70)
cartbutton.grid(row=0, column=3, sticky=tk.NSEW, padx=23, pady=10)

history_image = tk.PhotoImage(file="ui_images\\history.png")
historybutton = tk.Button(HeaderFrame, command=display_receipt_buttons, bg='#DDD1B8', border=0, image=history_image, width=70)
historybutton.grid(row=0, column=2, sticky=tk.NSEW, padx=23, pady=10)




ContentFrame = tk.Frame(root, height=525, width=100, bg='#DDD1B8')
ContentFrame.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
ContentFrame.grid_columnconfigure(0, weight=1)
ContentFrame.grid_rowconfigure(0, weight=1)
ContentFrame.grid_propagate(False)

ShopFrame = ttk.Notebook(ContentFrame, height=500, width=1050)
ShopFrame.grid(row=0, column=0, sticky="nsew")


MenuTab = tk.Frame(ShopFrame)
MenuTab.pack(fill="both")

MenuFrame = tk.Frame(MenuTab, height=550, width=1050, bg="#FFFFFF")
MenuFrame.pack(anchor=tk.N, fill=tk.X, expand=True)
MenuFrame.grid_propagate(False)
MenuFrame.grid_columnconfigure(0, weight=1)
MenuFrame.grid_rowconfigure(0, weight=8)
MenuFrame.grid_rowconfigure(1, weight=1)
MenuFrame.grid_rowconfigure(2, weight=1)
MenuFrame.grid_rowconfigure(3, weight=1)

creamylater = tk.PhotoImage(file='ui_images\\CreamyLater.png')

Logo = tk.Label(MenuFrame, text="Logo and Name", bg="#FFFFFF", image=creamylater)
Logo.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)


pastrybut = tk.PhotoImage(file='ui_images\\pastries.png')
PastryButton = tk.Button(MenuFrame, command=lambda:(select_tab(1)), width=450, height=60, image=pastrybut, bd=0, bg="#FFFFFF")
PastryButton.grid(row=1, column=0, columnspan=2)

dessertbut = tk.PhotoImage(file="ui_images\\desserts.png")
DessertButton = tk.Button(MenuFrame, command=lambda:(select_tab(2)), width=450, height=60, bg="#FFFFFF", image=dessertbut, bd=0)
DessertButton.grid(row=2, column=0, columnspan=2)

drinkbut = tk.PhotoImage(file="ui_images\\drinks.png")
DrinkButton = tk.Button(MenuFrame, command=lambda:(select_tab(3)), width=450, height=60, bg="#FFFFFF", image=drinkbut, bd=0)
DrinkButton.grid(row=3, column=0, columnspan=2, pady=(0, 20))




PastriesTab = tk.Frame(ShopFrame)

PastryButtonFrame = tk.Frame(PastriesTab, width=1138, height=50, border=0)
PastryButtonFrame.pack(anchor=tk.N, fill=tk.X, expand=True)
PastryButtonFrame.grid_propagate(False)


PastryItemFrame = tk.Frame(PastriesTab, bg="#DDD1B8", border=0, width=858, height=520, bd=3, padx=10, pady=10, relief=tk.RIDGE)
PastryItemFrame.pack(fill=tk.BOTH, expand=True)
PastryItemFrame.grid_propagate(False)

for i in range(3):  # Adjust the range as needed
    PastryButtonFrame.columnconfigure(i, weight=1)

PastryButtonFrame.rowconfigure(0, weight=1)

pr_label = tk.Label(PastryButtonFrame, text ="Pastries", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#FFFFFF", anchor="center", bg="#626262")
pr_label.grid(row = 0, column = 0, sticky=tk.NSEW)

Pr_button2 = tk.Button(PastryButtonFrame, text ="Desserts",  font="-family {Poppins Semibold} -size 15 -weight bold", fg="#C4643E", bg="#DDD1B8", command = lambda : select_tab(2))
Pr_button2.grid(row = 0, column = 1, sticky=tk.NSEW)

Pr_button3 = tk.Button(PastryButtonFrame, text ="Drinks", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#C4643E", bg="#DDD1B8", command = lambda : select_tab(3))
Pr_button3.grid(row = 0, column = 2, sticky=tk.NSEW)

#################################

for i in range(5):  # Adjust the range as needed
    PastryItemFrame.columnconfigure(i, weight=1)

    for i in range(3):  # Adjust the range as needed
        PastryItemFrame.rowconfigure(i, weight=1)

Pr_item1 = Item("Croissant", 135)
croissant = tk.PhotoImage(file='product_images\\croissant.png')
Pr_description1 = ItemDescription("Croissant", 147, "Indulge the sweetness of Glazed Croissant. Best Quaso You’ll ever get so.", 'product_images\\croissant.png')
Pr_itembut1 = tk.Button(PastryItemFrame, command=lambda: (Pr_item1.add_item(), calculate_total_cost()), image=croissant, compound="center", bg="#DDD1B8", border=0)
Pr_itembut1.grid(row=0, column=0, padx=7, pady=7, sticky=tk.NSEW)

Pr_item2 = Item("Cream Cheese Bagel", 175)
bagel = tk.PhotoImage(file='product_images\\bagel.png')
Pr_description2 = ItemDescription("Cream Cheese Bagel", 175, "You like it Creamy, You Cheesy. Cream Cheese Bagel all you need.", 'product_images\\bagel.png')
Pr_itembut2 = tk.Button(PastryItemFrame, command=lambda: (Pr_item2.add_item(), calculate_total_cost()), image=bagel, compound="center", bg="#DDD1B8", border=0)
Pr_itembut2.grid(row=0, column=1, padx=7, pady=7, sticky=tk.NSEW)

Pr_item3 = Item("Cinnamon Roll", 155)
cinnamon = tk.PhotoImage(file='product_images\\cinnamon.png')
Pr_description3 = ItemDescription("Cinnamon Roll", 155, "Take a break after a long stroll, Have a piece of our Cinnamoroll.", 'product_images\\cinnamon.png')
Pr_itembut3 = tk.Button(PastryItemFrame, command=lambda: (Pr_item3.add_item(), calculate_total_cost()), image=cinnamon, compound="center", bg="#DDD1B8", border=0)
Pr_itembut3.grid(row=0, column=2, padx=7, pady=7, sticky=tk.NSEW)

Pr_item4 = Item("Strawberry Muffin", 115)
muffin = tk.PhotoImage(file='product_images\\muffin.png')
Pr_description4 = ItemDescription("Strawberry Muffin", 115, "Stuff some in our Strawberry Muffin. Hot and Fresh, always the Best.", 'product_images\\muffin.png')
Pr_itembut4 = tk.Button(PastryItemFrame, command=lambda: (Pr_item4.add_item(), calculate_total_cost()), image=muffin, compound="center", bg="#DDD1B8", border=0)
Pr_itembut4.grid(row=0, column=3, padx=7, pady=7, sticky=tk.NSEW)

Pr_item5 = Item("Blueberry Pie", 150)
pie = tk.PhotoImage(file='product_images\\pie.png')
Pr_description5 = ItemDescription("Blueberry Pie", 150, "Our Very Blue and Very Berry Creamy (Blueberry) Pie. It’s BLUE and you’ll love it too.", 'product_images\\pie.png')
Pr_itembut5 = tk.Button(PastryItemFrame, command=lambda: (Pr_item5.add_item(), calculate_total_cost()), image=pie, compound="center", bg="#DDD1B8", border=0)
Pr_itembut5.grid(row=0, column=4, padx=7, pady=7, sticky=tk.NSEW)

Pr_item6 = Item("4 Seasons Cheesecake", 199)
cheesecake = tk.PhotoImage(file='product_images\\cheesecake.png')
Pr_description6 = ItemDescription("4 Seasons Cheesecake", 199, "Don’t let your time go to waste. 4 Seasons, More Reasons to get a taste.", 'product_images\\cheesecake.png')
Pr_itembut6 = tk.Button(PastryItemFrame, command=lambda: (Pr_item6.add_item(), calculate_total_cost()), image=cheesecake, compound="center", bg="#DDD1B8", border=0)
Pr_itembut6.grid(row=1, column=0, padx=7, pady=7, sticky=tk.NSEW)

Pr_item7 = Item("Macarons", 320)
macarons = tk.PhotoImage(file='product_images\\macarons.png')
Pr_description7 = ItemDescription("Macarons", 320, "Take a bite of our Cute Delectable Assorted Macarons. Comes with Different colors and flavors.", 'product_images\\macarons.png')
Pr_itembut7 = tk.Button(PastryItemFrame, command=lambda: (Pr_item7.add_item(), calculate_total_cost()), image=macarons, compound="center", bg="#DDD1B8", border=0)
Pr_itembut7.grid(row=1, column=1, padx=7, pady=7, sticky=tk.NSEW)

Pr_item8 = Item("Choco Almond Cookies", 375)
cookies = tk.PhotoImage(file='product_images\\cookies.png')
Pr_description8 = ItemDescription("Choco Almond Cookies", 375, "Chocolate Chip Cookies with Delectable Almond inside.", 'product_images\\cookies.png')
Pr_itembut8 = tk.Button(PastryItemFrame, command=lambda: (Pr_item8.add_item(), calculate_total_cost()), image=cookies, compound="center", bg="#DDD1B8", border=0)
Pr_itembut8.grid(row=1, column=2, padx=7, pady=7, sticky=tk.NSEW)

Pr_item9 = Item("Garlic Butter Baguette", 399)
baguette = tk.PhotoImage(file='product_images\\baguette.png')
Pr_description9 = ItemDescription("Garlic Butter Baguette", 399, "Get a hold of our Looonnnggg Garlic Baguette. The Longer, The Better.", 'product_images\\baguette.png')
Pr_itembut9 = tk.Button(PastryItemFrame, command=lambda: (Pr_item9.add_item(), calculate_total_cost()), image=baguette, compound="center", bg="#DDD1B8", border=0)
Pr_itembut9.grid(row=1, column=3, padx=7, pady=7, sticky=tk.NSEW)

comingsoon_description = ItemDescription("Coming Soon", "???", "Don't Be Gone, Soon To Come!", 'product_images\\comingsoon.png')
comingsoon = tk.PhotoImage(file='product_images\\comingsoon.png')
Pr_itembut10 = tk.Button(PastryItemFrame, image=comingsoon, compound="center", bg="#DDD1B8", border=0)
Pr_itembut10.grid(row=1, column=4, padx=7, pady=7, sticky=tk.NSEW)



DessertsTab = tk.Frame(ShopFrame)

DessertButtonFrame = tk.Frame(DessertsTab, bg='white', width=1138, height=50)
DessertButtonFrame.pack(anchor=tk.N, fill=tk.X, expand=True)
DessertButtonFrame.grid_propagate(False)

DessertItemFrame = tk.Frame(DessertsTab, bg="#DDD1B8", width=858, height=520, bd=3, padx=10, pady=10, relief=tk.RIDGE)
DessertItemFrame.pack(fill=tk.BOTH, expand=True)
DessertItemFrame.grid_propagate(False)

for i in range(3):  # Adjust the range as needed
    DessertButtonFrame.columnconfigure(i, weight=1)

DessertButtonFrame.rowconfigure(0, weight=1)


De_label = tk.Button(DessertButtonFrame, text ="Pastries", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#C4643E", bg="#DDD1B8", command = lambda : select_tab(1))
De_label.grid(row = 0, column = 0, sticky=tk.NSEW)

De_label2 = tk.Label(DessertButtonFrame, text ="Desserts", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#FFFFFF", anchor="center", bg="#626262")
De_label2.grid(row = 0, column = 1, sticky=tk.NSEW)

De_button3 = tk.Button(DessertButtonFrame, text ="Drinks", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#C4643E", bg="#DDD1B8", command = lambda : select_tab(3))
De_button3.grid(row = 0, column = 2, sticky=tk.NSEW)


#################################

for i in range(5):  # Adjust the range as needed
    DessertItemFrame.columnconfigure(i, weight=1)

    for i in range(3):  # Adjust the range as needed
        DessertItemFrame.rowconfigure(i, weight=1)


De_item1 = Item("Nutella Crepe Cone", 165)
crepe = tk.PhotoImage(file='product_images\\crepe.png')
De_description1 = ItemDescription("Nutella Crepe Cone", 147, "Sweet Nutella Crepe Cone, Taste the Chocolatey Sweetness in a Cone.", 'product_images\\crepe.png')
De_itembut1 = tk.Button(DessertItemFrame, command=lambda: (De_item1.add_item(), calculate_total_cost()), image=crepe, compound="center", bg="#DDD1B8", border=0)
De_itembut1.grid(row=0, column=0, padx=7, pady=7, sticky=tk.NSEW)

De_item2 = Item("Caramel Pudding", 299)
pudding = tk.PhotoImage(file='product_images\\pudding.png')
De_description2 = ItemDescription("Caramel Pudding", 299, "Softest and Sweetest Caramel Pudding. Ready for Serving.", 'product_images\\pudding.png')
De_itembut2 = tk.Button(DessertItemFrame, command=lambda: (De_item2.add_item(), calculate_total_cost()), image=pudding, compound="center", bg="#DDD1B8", border=0)
De_itembut2.grid(row=0, column=1, padx=7, pady=7, sticky=tk.NSEW)

De_item3 = Item("Tiramisu", 350)
tiramisu = tk.PhotoImage(file='product_images\\tiramisu.png')
De_description3 = ItemDescription("Tiramisu", 350, "– Bittersweet Dessert you’ll never want to miss. Sweet and Creamy Tiramisu", 'product_images\\tiramisu.png')
De_itembut3 = tk.Button(DessertItemFrame, command=lambda: (De_item3.add_item(), calculate_total_cost()), image=tiramisu, compound="center", bg="#DDD1B8", border=0)
De_itembut3.grid(row=0, column=2, padx=7, pady=7, sticky=tk.NSEW)

De_itembut4 = tk.Button(DessertItemFrame, image=comingsoon, compound="center", bg="#DDD1B8", border=0)
De_itembut4.grid(row=0, column=3, padx=7, pady=7, sticky=tk.NSEW)

De_itembut5 = tk.Button(DessertItemFrame, image=comingsoon, compound="center", bg="#DDD1B8", border=0)
De_itembut5.grid(row=0, column=4, padx=7, pady=7, sticky=tk.NSEW)

De_itembut6 = tk.Button(DessertItemFrame, image=comingsoon, compound="center", bg="#DDD1B8", border=0)
De_itembut6.grid(row=1, column=0, padx=7, pady=7, sticky=tk.NSEW)





DrinksTab = tk.Frame(ShopFrame)

DrinkButtonFrame = tk.Frame(DrinksTab, bg='white', width=1138, height=50)
DrinkButtonFrame.pack(anchor=tk.N, fill=tk.X, expand=True)
DrinkButtonFrame.grid_propagate(False)

DrinkItemFrame = tk.Frame(DrinksTab, bg="#DDD1B8", width=858, height=520, bd=3, padx=10, pady=10, relief=tk.RIDGE)
DrinkItemFrame.pack(fill=tk.BOTH, expand=True)
DrinkItemFrame.grid_propagate(False)

for i in range(3):  # Adjust the range as needed
    DrinkButtonFrame.columnconfigure(i, weight=1)

DrinkButtonFrame.rowconfigure(0, weight=1)


Dr_label = tk.Button(DrinkButtonFrame, text ="Pastries", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#C4643E", bg="#DDD1B8", command = lambda : select_tab(1))
Dr_label.grid(row = 0, column = 0, sticky=tk.NSEW)

Dr_button2 = tk.Button(DrinkButtonFrame, text ="Desserts", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#C4643E", bg="#DDD1B8", command = lambda : select_tab(2))
Dr_button2.grid(row = 0, column = 1, sticky=tk.NSEW)

Dr_button3 = tk.Label(DrinkButtonFrame, text ="Drinks", font="-family {Poppins Semibold} -size 15 -weight bold", fg="#FFFFFF", anchor="center", bg="#626262")
Dr_button3.grid(row = 0, column = 2, sticky=tk.NSEW)

#################################

for i in range(5):  # Adjust the range as needed
    DrinkItemFrame.columnconfigure(i, weight=1)

    for i in range(3):  # Adjust the range as needed
        DrinkItemFrame.rowconfigure(i, weight=1)


Dr_item1 = Item("Brewed Coffee", 160)
coffee = tk.PhotoImage(file='product_images\\coffee.png')
Dr_description1 = ItemDescription("Brewed Coffee", 160, "Start your day with a nice sip of Brewed Coffee. Strong Start for a Long day.", 'product_images\\coffee.png')
Dr_itembut1 = tk.Button(DrinkItemFrame, command=lambda: (Dr_item1.add_item(), calculate_total_cost()), image=coffee, compound="center", bg="#DDD1B8", border=0)
Dr_itembut1.grid(row=0, column=0, padx=7, pady=7, sticky=tk.NSEW)

Dr_item2 = Item("Hot Chocolate", 200)
choco = tk.PhotoImage(file='product_images\\choco.png')
Dr_description2 = ItemDescription("Hot Chocolate", 200, "It’s not too late for a cup of Hot Chocolate. Nothing beats something Hot and Sweet.", 'product_images\\choco.png')
Dr_itembut2 = tk.Button(DrinkItemFrame, command=lambda: (Dr_item2.add_item(), calculate_total_cost()), image=choco, compound="center", bg="#DDD1B8", border=0)
Dr_itembut2.grid(row=0, column=1, padx=7, pady=7, sticky=tk.NSEW)

Dr_item3 = Item("Matcha Green Tea", 265)
matcha = tk.PhotoImage(file='product_images\\matcha.png')
Dr_description3 = ItemDescription("Matcha Green Tea", 265, "Experience the Bittersweet Taste of Matcha in a cup. MATCHABLE for your mood these rainy season.", 'product_images\\matcha.png')
Dr_itembut3 = tk.Button(DrinkItemFrame, command=lambda: (Dr_item3.add_item(), calculate_total_cost()), image=matcha, compound="center", bg="#DDD1B8", border=0)
Dr_itembut3.grid(row=0, column=2, padx=7, pady=7, sticky=tk.NSEW)

comingsoon_description_drinks = ItemDescription("Coming Soon", "???", "Don't Be Gone, Soon To Come!", 'product_images\\csdrink.png')
csdrink = tk.PhotoImage(file='product_images\\csdrink.png')
Dr_itembut4 = tk.Button(DrinkItemFrame, image=csdrink, compound="center", bg="#DDD1B8", border=0)
Dr_itembut4.grid(row=0, column=3, padx=7, pady=7, sticky=tk.NSEW)

Dr_itembut5 = tk.Button(DrinkItemFrame, image=csdrink, compound="center", bg="#DDD1B8", border=0)
Dr_itembut5.grid(row=0, column=4, padx=7, pady=7, sticky=tk.NSEW)

Dr_itembut6 = tk.Button(DrinkItemFrame, image=csdrink, compound="center", bg="#DDD1B8", border=0)
Dr_itembut6.grid(row=1, column=0, padx=7, pady=7, sticky=tk.NSEW)






ItemCartTab = tk.Frame(ShopFrame, bg="#FFFFFF")

CartButtonFrame = tk.Frame(ItemCartTab, bg='#FFFFFF', width=1138, height=50, border=0)
CartButtonFrame.pack(anchor=tk.N, fill=tk.X, expand=True)
CartButtonFrame.grid_propagate(False)

ItemList = tk.Frame(ItemCartTab, bg='#FFFFFF', width=858, height=470, border=0)
ItemList.pack(fill=tk.BOTH, expand=True, pady=5)
ItemList.grid_propagate(False)

CostFrame = tk.Frame(ItemCartTab, bg='#E8E3D8', width=1138, height=150, border=0)
CostFrame.pack(anchor=tk.N, fill=tk.X, expand=True, pady=5)
CostFrame.grid_propagate(False)




CartButtonFrame.columnconfigure(0, weight=1)
CartButtonFrame.columnconfigure(1, weight=1)
CartButtonFrame.columnconfigure(2, weight=1)
CartButtonFrame.columnconfigure(3, weight=2)
CartButtonFrame.rowconfigure(0, weight=1)


returnbutton = tk.Button(CartButtonFrame, text ="Return", bg='#626262', font=("Hussar 12 bold"), fg="#FFFFFF", command = lambda : select_tab(0))
returnbutton.grid(row = 0, column = 0, sticky=tk.NSEW, padx=(0,5), pady=4)

remove = tk.Button(CartButtonFrame, text="Remove Selected Item", bg='#DDD1B8', font=("Hussar 12 bold"), fg="#C4643E", command=remove_selected_item)
remove.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=4)

clear = tk.Button(CartButtonFrame, text="Clear", bg='#DDD1B8', font=("Hussar 12 bold"), fg="#C4643E", command=clear_all_items)
clear.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=4)

checkout = tk.Button(CartButtonFrame, text="Checkout", bg='#DDD1B8', font=("Hussar 12 bold"), fg="#C4643E", command=CheckEntries)
checkout.grid(row=0, column=3, sticky=tk.NSEW, padx=(5,0), pady=4)

tree = ttk.Treeview(ItemList, columns=("Item Description", "Quantity", "Unit Price"), show="headings", height=10, style="My.Treeview")
tree.heading("Item Description", text="Item Name")
tree.heading("Quantity", text="Quantity")
tree.heading("Unit Price", text="Unit Price (\u20b1)")
tree.column("Item Description", anchor=tk.CENTER, width=130)  # Set width of Item Description column
tree.column("Quantity", anchor=tk.CENTER, width=70)  # Set width of Quantity column
tree.column("Unit Price", anchor=tk.CENTER, width=100)  # Set width of Unit Price column
tree.pack(fill="both", expand=True)

style.configure("My.Treeview", font=("Helvetica", 10), rowheight=30, bg='#DDD1B8', fg="#C4643E")
style.configure("My.Treeview.Heading", font=("Hussar", 13), bg='#DDD1B8', fg="#C4643E")
style.layout("My.Treeview", [('My.Treeview.treearea', {'sticky ': 'nswe'})])  


CostFrame.rowconfigure(0, weight=1)
CostFrame.rowconfigure(1, weight=1)
CostFrame.rowconfigure(2, weight=1)
CostFrame.columnconfigure(1, minsize=213)
CostFrame.columnconfigure(2, weight=1)
CostFrame.columnconfigure(3, weight=1)
CostFrame.columnconfigure(4, weight=1)

SubTotal = tk.Label(CostFrame, text='Subtotal:', bg='#E8E3D8', fg="#C4643E", font="Helvetica 12 bold")
SubTotal.grid(column=0, row=0, pady=5, padx=5, sticky="e")

SubTotalAmont = tk.Label(CostFrame, text='', bg='#FAF8F2', fg="#C4643E", font="Helvetica 12")
SubTotalAmont.grid(column=1, row=0, pady=5, padx=5, sticky=tk.NSEW)

VatTax = tk.Label(CostFrame, text='VAT (12%):', bg='#E8E3D8', fg="#C4643E", font="Helvetica 11 bold")
VatTax.grid(column=0, row=1, pady=5, padx=5, sticky="e")

VatTaxAmount = tk.Label(CostFrame, text='', bg='#FAF8F2', fg="#C4643E", font="Helvetica 12")
VatTaxAmount.grid(column=1, row=1, pady=5, padx=5, sticky=tk.NSEW)

TotalCost = tk.Label(CostFrame, text='Total Cost:', bg='#E8E3D8', fg="#C4643E", font="Helvetica 12 bold")
TotalCost.grid(column=0, row=2, pady=5, padx=5, sticky="e")

TotalCostAmount = tk.Label(CostFrame, text="", bg='#FAF8F2', font="Helvetica 12 bold")
TotalCostAmount.grid(column=1, row=2, pady=5, padx=5, sticky=tk.NSEW)



paymentterms = tk.Label(CostFrame, text="Payment Terms", bg='#E8E3D8', fg="#C4643E", font="Helvetica 12 bold")
paymentterms.grid(row=0, column=2, columnspan=2)

custom_font = ("Helvetica", 11)

duedate = tk.Label(CostFrame, text="Payment Deadline", bg='#E8E3D8', fg="#C4643E", font="Helvetica 12 bold")
duedate.grid(row=1, column=2, sticky=tk.E, padx=(40, 10))

due_date_options = ["Due Upon Invoice", "Upon Delivery"]
due_date_combobox = ttk.Combobox(CostFrame, values=due_date_options, state="readonly", width=25, font=custom_font)
due_date_combobox.set("Select Due Date")
due_date_combobox.grid(row=1, column=3, sticky=tk.NSEW, padx=(5, 30), pady=5)

paymentterms = tk.Label(CostFrame, text="Payment Method", bg='#E8E3D8', fg="#C4643E", font="Helvetica 12 bold")
paymentterms.grid(row=2, column=2, sticky=tk.E, padx=(40, 10))

payment_options = ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "PayPal", "GCash"]
payment_combobox = ttk.Combobox(CostFrame, values=payment_options, state="readonly", width=25, font=custom_font)
payment_combobox.set("Select Payment Method")
payment_combobox.grid(row=2, column=3, sticky=tk.NSEW, padx=(5, 30), pady=5)


button_to_description = {
    Pr_itembut1: Pr_description1,
    Pr_itembut2: Pr_description2,
    Pr_itembut3: Pr_description3,
    Pr_itembut4: Pr_description4,
    Pr_itembut5: Pr_description5,
    Pr_itembut6: Pr_description6,
    Pr_itembut7: Pr_description7,
    Pr_itembut8: Pr_description8,
    Pr_itembut9: Pr_description9,
    Pr_itembut10: comingsoon_description,
    De_itembut1: De_description1,
    De_itembut2: De_description2,
    De_itembut3: De_description3,
    De_itembut4: comingsoon_description,
    De_itembut5: comingsoon_description,
    De_itembut6: comingsoon_description,
    Dr_itembut1: Dr_description1,
    Dr_itembut2: Dr_description2,
    Dr_itembut3: Dr_description3,
    Dr_itembut4: comingsoon_description_drinks,
    Dr_itembut5: comingsoon_description_drinks,
    Dr_itembut6: comingsoon_description_drinks,
}


for button in [
    Pr_itembut1,
    Pr_itembut2,
    Pr_itembut3,
    Pr_itembut4,
    Pr_itembut5,
    Pr_itembut6,
    Pr_itembut7,
    Pr_itembut8,
    Pr_itembut9,
    Pr_itembut10,
    De_itembut1,
    De_itembut2,
    De_itembut3,
    De_itembut4,
    De_itembut5,
    De_itembut6,
    Dr_itembut1,
    Dr_itembut2,
    Dr_itembut3,
    Dr_itembut4,
    Dr_itembut5,
    Dr_itembut6
    ]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


ShopFrame.add(MenuTab)
ShopFrame.add(PastriesTab, text="Pastries")
ShopFrame.add(DessertsTab, text="Desserts")
ShopFrame.add(DrinksTab, text="Drinks")
ShopFrame.add(ItemCartTab, text="Item Cart")


root.mainloop()

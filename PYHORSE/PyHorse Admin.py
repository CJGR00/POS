from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from subprocess import call



cart = []
total = 0.0
products = {
    "b1": {"name1":"San Mig", "name2":"Light", "hidden_name": "San Mig Light", "category": "Beer", "size": "300ml", "price": 45, "image": "beer1.png", "stock": 5, "quantity": 1,"image_size": (100, 100)},
    "b2": {"name1":"San Miguel" , "name2":"Pale Pilsen" ,"hidden_name": "San Miguel Pale Pilsen", "category": "Beer", "size": "320ml", "price": 49, "image": "beer2.png", "stock": 5, "quantity": 1, "image_size": (100, 100)},
    "b3": {"name1":"San Mig" , "name2":"Light Apple" ,"hidden_name": "San Mig Light Apple", "category": "Beer", "size": "330ml", "price": 38, "image": "beer3.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "b4": {"name1":"San Mig" , "name2":"Premium Malt" ,"hidden_name": "San Miguel Premium All Malt Beer", "category": "Beer", "size": "330ml", "price": 72, "image": "beer4.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "b5": {"name1":"Strong San Mig" , "name2":"Strong Ice" ,"hidden_name": "Strong San Mig Strong Ice", "category": "Beer", "size": "330ml", "price": 38, "image": "beer5.png", "stock": 0, "quantity": 1, "image_size": (150, 100)},
    "b6": {"name1":"Red Horse" , "name2":"Beer" ,"hidden_name": "Red Horse Beer", "category": "Beer", "size": "300ml", "price": 118, "image": "beer6.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "c1": {"name1":"Hennessy " , "name2":" Privilege" ,"hidden_name": "Hennessy VSOP Privilege", "category": "Cognac", "size": "700ml", "price": 3799, "image": "cog1.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "c2": {"name1":"Remy Martin" , "name2":"" ,"hidden_name": "Remy Martin - XO", "category": "Cognac", "size": "700ml", "price": 13570, "image": "cog2.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "c3": {"name1":"Courvoisier" , "name2":"XO" ,"hidden_name": "Courvoisier - XO", "category": "Cognac", "size": "700ml", "price": 7990, "image": "cog3.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "c4": {"name1":"Martell Cordon" , "name2":"Blue Extra Old" ,"hidden_name": "Martell - Cordon Blue - Extra Old", "category": "Cognac", "size": "700ml", "price": 7990, "image": "cog4.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "c5": {"name1":"Pierre Ferrand" , "name2":" Ambre" ,"hidden_name": "Pierre Ferrand - Ambre", "category": "Cognac", "size": "700ml", "price": 3490, "image": "cog5.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "c6": {"name1":"Hine - Rare" , "name2":"VSOP" ,"hidden_name": "Hine - Rare VSOP", "category": "Cognac", "size": "700ml", "price": 3090, "image": "cog6.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "g1": {"name1":"Hendrick's Gin" , "name2":"" ,"hidden_name": "Hendrick's Gin", "category": "Gin", "size": "700ml", "price": 2890, "image": "g1.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "g2": {"name1":"Bombay " , "name2":"Sapphire" ,"hidden_name": "Bombay Sapphire", "category": "Gin", "size": "750ml", "price": 1500, "image": "g2.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "g3": {"name1":"Tanquray Ten" , "name2":"" ,"hidden_name": "Tanquray Ten", "category": "Gin", "size": "700ml", "price": 2250, "image": "g3.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "g4": {"name1":"Aviation " , "name2":"American" ,"hidden_name": "Aviation American Gin", "category": "Gin", "size": "700ml", "price": 2249, "image": "g4.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "g5": {"name1":"Monkey 47 Gin" , "name2":"" ,"hidden_name": "Monkey 47 Gin", "category": "Gin", "size": "500ml", "price": 3099, "image": "g5.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "g6": {"name1":"Beefeater" , "name2":"London" ,"hidden_name": "Beefeater London Dry Gin", "category": "Gin", "size": "70ml", "price": 799, "image": "g6.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "l1": {"name1":"Bailys" , "name2":"Irish Cream" ,"hidden_name": "Bailys Irish Cream", "category": "Liqueur", "size": "700ml", "price": 835, "image": "l1.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "l2": {"name1":"Kahlua" , "name2":"" ,"hidden_name": "Kahlua", "category": "Liqueur", "size": "700ml", "price": 829, "image": "l2.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "l3": {"name1":"Grand Marnier" , "name2":"" ,"hidden_name": "Grand Marnier", "category": "Liqueur", "size": "700ml", "price": 1820, "image": "l3.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "l4": {"name1":"Walsh" , "name2":"Amaretto" ,"hidden_name": "Walsh - Amaretto", "category": "Liqueur", "size": "750ml", "price": 329, "image": "l4.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "l5": {"name1":"Cointreau" , "name2":"" ,"hidden_name": "Cointreau", "category": "Liqueur", "size": "700ml", "price": 1249, "image": "l5.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "l6": {"name1":"Drambuie" , "name2":"" ,"hidden_name": "Drambuie", "category": "Liqueur", "size": "700ml", "price": 2250, "image": "l6.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "r1": {"name1":"Bacardi" , "name2":"8 Year Old" ,"hidden_name": "Bacardi 8 Year Old", "category": "Rum", "size": "75ml", "price": 2125, "image": "r1.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "r2": {"name1":"Mount Gay" , "name2":"Reserve Cask" ,"hidden_name": "Mount Gay - XO Reserve Cask", "category": "Rum", "size": "700ml", "price": 4490, "image": "r2.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "r3": {"name1":"Diplomatico" , "name2":"Reserva exclsv" ,"hidden_name": "Diplomatico - Reserva Exclusiva", "category": "Rum", "size": "700ml", "price": 2497, "image": "r3.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "r4": {"name1":"Plantation" , "name2":"Pineapple Rum" ,"hidden_name": "Plantation Fancy Pineapple Rum", "category": "Rum", "size": "700ml", "price": 1890, "image": "r4.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "r5": {"name1":"Appleton " , "name2":"Estate" ,"hidden_name": "Appleton Estate 12 Year Old Rare Blend", "category": "Rum", "size": "700ml", "price": 2499, "image": "r5.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "r6": {"name1":"Ron Zacapa" , "name2":"Solera" ,"hidden_name": "Ron Zacapa XO Solera Gran Reserva Especial", "category": "Rum", "size": "750ml", "price": 4690, "image": "r6.png", "stock": 0, "quantity": 1, "image_size": (100, 100)},
    "t1": {"name1":"Don Julio " , "name2":"Blanco" ,"hidden_name": "Don Julio Blanco", "category": "Tequila", "size": "700ml", "price": 3999, "image": "t1.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "t2": {"name1":"Patron" , "name2":" Reposado" ,"hidden_name": "Patron Reposado", "category": "Tequila", "size": "1.75 L", "price": 8690, "image": "t2.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "t3": {"name1":"Casamigos  " , "name2":"Anejo" ,"hidden_name": "Casamigos Anejo Tequila", "category": "Tequila", "size": "700 ml", "price": 3949, "image": "t3.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "t4": {"name1":"Espolon " , "name2":"Reposado" ,"hidden_name": "Espolon Reposado Tequila", "category": "Tequila", "size": "750 ml", "price": 2599, "image": "t4.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "t5": {"name1":"Herradura " , "name2":"Anejo" ,"hidden_name": "Herradura Anejo", "category": "Tequila", "size": "750 ml", "price": 3150, "image": "t5.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "t6": {"name1":"Clase Azul" , "name2":"Reposado" ,"hidden_name": "Clase Azul Reposado", "category": "Tequila", "size": "750 ml", "price": 12500, "image": "t6.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "wi1": {"name1":"Caymus " , "name2":"Vineyards" ,"hidden_name": "Caymus Vineyards Special Selections", "category": "Wine", "size": "750 ml", "price": 22630, "image": "wi1.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "wi2": {"name1":"Three Palms" , "name2":"Vineyards" ,"hidden_name": "Three Palms Vineyards Merlot", "category": "Wine", "size": "750 ml", "price": 10900, "image": "wi2.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "wi3": {"name1":"Domaine de la" , "name2":"Romanee" ,"hidden_name": "Domaine de la Romanee -Conti", "category": "Wine", "size": "750 ml", "price": 398563, "image": "wi3.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "wi4": {"name1":"Chevalier " , "name2":"Montrachet" ,"hidden_name": "Chevalier Montrachet Grand Cru", "category": "Wine", "size": "750 ml", "price": 398563, "image": "wi4.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "wi5": {"name1":"Cloudy Bay" , "name2":"Sauvignon" ,"hidden_name": "Cloudy Bay - Sauvignon blanc", "category": "Wine", "size": "750 ml", "price": 2089, "image": "wi5.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "wi6": {"name1":"Novellino" , "name2":"Sparkling Red" ,"hidden_name": "Novellino Sparkling Red", "category": "Wine", "size": "750 ml", "price": 250, "image": "wi6.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "w1": {"name1":"The Glenlivet" , "name2":" 18 Year Old" ,"hidden_name": "The Glenlivet - 18 Year Old", "category": "Whisky", "size": "700 ml", "price": 5999, "image": "w1.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "w2": {"name1":"Woodford  " , "name2":"Reserve" ,"hidden_name": "Woodford Reserve Distiller's Select -1L", "category": "Whisky", "size": "1 L", "price": 3299, "image": "w2.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "w3": {"name1":"Irish Jameson" , "name2":"18 Year Old" ,"hidden_name": "Irish Jameson 18 Year Old", "category": "Whisky", "size": "70 cl", "price": 7379, "image": "w3.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "w4": {"name1":"Bulleit Rye" , "name2":"Small Batch" ,"hidden_name": "Bulleit Rye - Small Batch", "category": "Whisky", "size": "1L", "price": 2890, "image": "w4.png", "stock": 0, "quantity": 1, "image_size": (75, 100)},
    "w5": {"name1":"Hibiki" , "name2":"Harmony" ,"hidden_name": "Hibiki Harmony", "category": "Whisky", "size": "1L", "price": 2890, "image": "w5.png", "stock": 70, "quantity": 1, "image_size": (75, 100)},
    "w6": {"name1":"Crown Royal" , "name2":"" ,"hidden_name": "Crown Royal", "category": "Whisky", "size": "750ml", "price": 2907, "image": "w6.png", "stock": 50, "quantity": 1, "image_size": (75, 100)},
    "v1": {"name1":"Belvedere", "name2":"Vodka", "hidden_name": "Belvedere Vodka", "category": "Vodka", "size": "700ml", "price": 1999, "image": "v1.png", "stock": 50, "quantity": 1, "image_size": (75, 100)},
    "v2": {"name1":"Grey Goose", "name2":"Original Vodka", "hidden_name": "Grey Goose Original Vodka", "category": "Vodka", "size": "750ml", "price": 2460, "image": "v2.png", "stock": 50,  "quantity": 1, "image_size": (75, 100)},
    "v3": {"name1":"Absolut", "name2":"Elyx", "hidden_name": "Absolut Elyx", "category": "Vodka", "size": "1 L", "price": 1799, "image": "v3.png", "stock": 50, "quantity": 1, "image_size": (75, 100)},
    "v4": {"name1":"Ketel", "name2":"One", "hidden_name": "Ketel One", "category": "Vodka", "size": "750ml", "price": 1499, "image": "v4.png", "stock": 50,  "quantity": 1, "image_size": (75, 100)},
    "v5": {"name1":"Tito's", "name2":"Handmade", "hidden_name": "Tito's Handmade Vodka", "category": "Vodka", "size": "1.75 L", "price": 2790, "image": "v5.png", "stock": 50,  "quantity": 1, "image_size": (75, 100)},
    "v6": {"name1":"Ciroc", "name2":"Vodka", "hidden_name": "Ciroc Vodka", "category": "Vodka", "size": "750ml", "price": 2650, "image": "v6.png", "stock": 50, "quantity": 1, "image_size": (75, 100)},
}

def on_canvas_configure1(event):
    mycanvas1.configure(scrollregion=mycanvas1.bbox('all'))

def show_frame(frame):
    frame.tkraise()

def inventory_file():
    call(["python", "Inventory.py"])
    root.deiconify()

def save_changes():
    messagebox.showinfo("Saved", "Saved Successfully")


def log_out():
    sure = messagebox.askyesno("Exit","Are you sure you want to Log Out?", parent=root)
    if sure is None:
        return
    elif sure == True:
        save_changes()
        root.destroy()


def changemode():
    global dark_mode
    dark_mode = not dark_mode  # Toggle the mode
    
    if dark_mode:
        ctk.set_appearance_mode("dark")
        button_switch.configure(image=icon_theme_on_off)

        # Change the images to their white versions for dark theme
        
        tab1_button.configure(image=stock_on)
        tab2_button.configure(image=inventory_on)
        logout_button.configure(image=log_out_on)
        database_button.configure(image=database_on)

        
    else: 
        ctk.set_appearance_mode("light")
        button_switch.configure(image=icon_theme_on_off)

        # Change the images back to their original versions for light theme
      
        tab1_button.configure(image=stock_off)
        tab2_button.configure(image=inventory_off)
        logout_button.configure(image=log_out_off)
        database_button.configure(image=database_off)





def clear_treeview():
    # Clear all items in the TreeView
    for item in cart_listbox.get_children():
        cart_listbox.delete(item)
    # Update the total after clearing the TreeView
    update_total()


def clear_treeview_above():
    if not cart_listbox.get_children():
        messagebox.showinfo("Info", "Cart is empty!")
    # Clear all items in the TreeView
    else:
        response = messagebox.askyesno("Warning", "Are you sure you want to clear your cart?")
        if response:
            for item in cart_listbox.get_children():
                cart_listbox.delete(item)
        # Update the total after clearing the TreeView
            update_total()
        else:
            return



def cash_button_clicked():
    global payment_method
    if not cart_listbox.get_children():
        messagebox.showinfo("Info", "Cart is empty!")
    else:   
        payment_method = "Cash"
        debbit_button.configure(state="disabled")
        online_button.configure(state="disabled")
        pay_button.configure(state="normal")
        messagebox.showinfo("Success", "Checkout successful with payment method: " + payment_method)

def debit_button_clicked():
    global payment_method
    if not cart_listbox.get_children():
        messagebox.showinfo("Info", "Cart is empty!")
    else:
        payment_method = "Debit"
        cash_button.configure(state="disabled")
        online_button.configure(state="disabled")
        pay_button.configure(state="normal")
        messagebox.showinfo("Success", "Checkout successful with payment method: " + payment_method)

def online_button_clicked():
    global payment_method
    if not cart_listbox.get_children():
        messagebox.showinfo("Info", "Cart is empty!")
    else:
        payment_method = "Online"
        cash_button.configure(state="disabled")
        debbit_button.configure(state="disabled")
        pay_button.configure(state="normal")
        messagebox.showinfo("Success", "Checkout successful with payment method: " + payment_method)

def checkout_main():
    global cart, total, payment_method  
    update_total()
    if not cart_listbox.get_children():
        messagebox.showinfo("Info", "Cart is empty!")
    else:
    
        # Display message box with the correct total
        messagebox.showinfo("Info", f"Total amount: ₱{total:.2f}\nThank you for your purchase!") # Clear the cart after checkout
        debbit_button.configure(state="disabled")
        online_button.configure(state="disabled")
        cash_button.configure(state="disabled")
        pay_button.configure(state="disabled")
        print_button.configure(state="normal")
        email_button.configure(state="normal")
        reset_button.configure(state="disabled")
            

def reset():
    global payment_method
    payment_method = None
    cash_button.configure(state="normal")
    debbit_button.configure(state="normal")
    online_button.configure(state="normal")
    pay_button.configure(state="disabled")



def print_resit():
    messagebox.showinfo("Successful","Receipt print successfully!")
    debbit_button.configure(state="normal")
    online_button.configure(state="normal")
    cash_button.configure(state="normal")
    print_button.configure(state="disabled")
    email_button.configure(state="disabled")
    pay_button.configure(state="disabled")
    clear_treeview() 


def add_to_cart(hidden_name, quantity, price, product_data, product_stock_label, stock_label):
    decrement_stock(hidden_name, quantity, price, product_data, product_stock_label, stock_label)
    update_total()
    


def decrement_stock(hidden_name, quantity, price, product_data, product_stock_label, stock_label):
    if product_data['stock'] - 1 < 0:
        messagebox.showerror("ERROR", "STOCK INSUFFICIENT")
    else:
        product_data['stock'] -= 1
        product_stock_label.configure(text=f"Stock: {product_data['stock']}")
        stock_label.configure(text=f"Stock: {product_data['stock']}")
        add_to_treeview(hidden_name, quantity, price)



def add_to_treeview(hidden_name, quantity, price):
    for item in cart_listbox.get_children():
        item_values = cart_listbox.item(item, "values")
        if item_values[0] == hidden_name:
            # Update the quantity
            new_quantity = int(item_values[1]) + quantity
            cart_listbox.item(item, values=(hidden_name, new_quantity, price))
            return
    # If the product is not in the cart, add it
    cart_listbox.insert("", "end", values=(hidden_name, quantity, price))

def update_total():
    global total
    total = 0 
    for item in cart_listbox.get_children():
        item_values = cart_listbox.item(item, "values")
        total += int(item_values[1]) * float(item_values[2])
    subtotal_label.config(text=f"SubTotal:                           ₱{total:.2f}")
    total_label.config(text=f"Total:                                  ₱{total:.2f}")
   

def update_pstock(entry, product_stock_label, product_data):
    entered_text1 = entry.get()
    if entered_text1 != "":
        new_stock = int(entered_text1)
        product_data['stock'] = new_stock
        product_stock_label.configure(text=f"New Stock: {new_stock}")

def update_stockl(entry, stock_label):
    """Updates the stock label with the entered value."""
    entered_text1 = entry.get()
    if entered_text1 != "":
        stock_label.configure(text=f"New Stock: {entered_text1}")

def updatelabels_new(entry, stock_label, product_stock_label, product_data):
    entry_text = entry.get()
    if any(char.isalpha() for char in entry_text):
          messagebox.showwarning("Invalid Input", "Letters are not allowed.")

    else:
        update_pstock(entry, product_stock_label, product_data)
        update_stockl(entry, stock_label)



def check_entry():
    entry_text = entry.get()
    if any(char.isalpha() for char in entry_text):
        messagebox.showwarning("Invalid Input", "Letters are not allowed.")
    else:
        messagebox.showinfo("Valid Input", "No letters found in the input.")

def scroll_to_product(product_key):
    product_index = list(products.keys()).index(product_key)
    y = (product_index // 3) * 180  # Assuming each row's height is 180 pixels
    mycanvas1.yview_moveto(y / ((len(products) // 3) * 180))

def email_win():
    import os
    from email.message import EmailMessage
    import ssl
    import smtplib
    from tkinter import messagebox 

    new_window = ctk.CTkToplevel(root)
    new_window.title("Email Receipt")
    new_window.geometry("630x710")
    new_window.configure(fg_color="#2b2b2b")

    new_window.lift()
    new_window.focus_force()
    new_window.attributes('-topmost', True)
   
    emailsender = "pyhorseg1devteam@gmail.com"
    email_password = "tset yhiy pchl nipj"   #

    font = ("Times New Roman", 13)

    image = ctk.CTkImage(Image.open('PyHorse Logo.png'), size=(200, 150))
    Label_0 = ctk.CTkLabel(new_window, text="", image=image, width=20, fg_color="green")
    Label_0.pack(side="top", pady=(15, 10), padx=(25, 0))

    Label_1 = ctk.CTkLabel(new_window, text="Your Email Account:", text_color='white', font=font, width=20)
    Label_1.place(x=177, y=200)

    emailE = ctk.CTkEntry(new_window, width=220)
    emailE.place(x=310, y=200)
    emailE.insert(0, "pyhorseg1devteam@gmail.com")

    Label_2 = ctk.CTkLabel(new_window, text="Compose", text_color='white', font=('Arial Black', 15, 'bold'), width=20)
    Label_2.place(x=310, y=250)

    def showmsg_sent():
        messagebox.showinfo("Email Sent", "Your Receipt Email has been sent successfully!")
        
    def send_email():
        email_receiver = cemailE.get()
        subject = subjectE.get()
        message = message_text.get('1.0', 'end-1c')

        em = EmailMessage()
        em['From'] = emailsender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(message)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(emailsender, email_password)
                smtp.sendmail(emailsender, email_receiver, em.as_string())
            print("Email sent successfully!")
            showmsg_sent()
            new_window.destroy()
        except Exception as e:
            print("Error sending email:", e)
            messagebox.showerror("Email Error", f"Error sending email: {e}")

    def intro():
        
        message_text.insert(END,"\t                        WELCOME TO PYHORSE LIQUOR POS")
        message_text.insert(END,f"\n\n                                          OWNED BY: PYHORSE G1 DEV TEAM")
        message_text.insert(END,f"\n\n                                                       CvSU IMUS CAMPUS")
        message_text.insert(END,f"\n\nBill no. : 1007652")
        message_text.insert(END,f"\nCustomer Name :")
        message_text.insert(END,f"\nPhone No. :#09992228798")
        message_text.insert(END,"\n=================================================================\n")
        message_text.insert(END,"\nProduct\t\t                                                   Qty.                          \t Price\n")
        message_text.insert(END,"\n=================================================================\n")

    def transfer_to_textbox():
        intro()
        for child in cart_listbox.get_children():
            product, quantity, price = cart_listbox.item(child)["values"]
            message_text.insert(tk.END, f"\n{product}         \t\t\t\t\t{quantity}    \t\t{price}")



    Label_3 = ctk.CTkLabel(new_window, text="Send to Email:", text_color='white', font=font, width=20)
    Label_3.place(x=210, y=295)

    cemailE = ctk.CTkEntry(new_window, width=220)
    cemailE.place(x=310, y=295)

    Label_4 = ctk.CTkLabel(new_window, text="Subject:", text_color='white', font=font, width=20)
    Label_4.place(x=245, y=330)

    subjectE = ctk.CTkEntry(new_window, width=220)
    subjectE.place(x=310, y=330)
    subjectE.insert(0, "PyHorse G1 Email Receipt")

    Label_5 = ctk.CTkLabel(new_window, text="Message:", text_color='white', font=font, width=20)
    Label_5.place(x=320, y=370)

    message_text = ctk.CTkTextbox(new_window, width=500, height=180)
    message_text.place(x=100, y=410)

    send_button = ctk.CTkButton(new_window, text="Send Email", border_color="white", border_width=2, fg_color="black", hover_color='red', command=send_email, width=20)
    send_button.place(x=205, y=610)

    paste_receipt_button = ctk.CTkButton(new_window, text="Input Receipt", border_color="white", border_width=2, fg_color="black", hover_color='red', command=transfer_to_textbox, width=20)
    paste_receipt_button.place(x=100, y=610)

    





    

root = ctk.CTk()
root.title("PyHorseᴳ¹ POS")
root.iconbitmap("PyHorse Logo.ico")
root.config(background="red")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (screen_width, screen_height))
root.focus_set()

# Load the image
original_image = Image.open("Frame Background.png")

# Create a CTkImage with the original image and appropriate size
main_background_path = ctk.CTkImage(light_image=original_image, size=(screen_width, screen_height))

# Create a label to hold the background image
main_background = ctk.CTkLabel(root, image=main_background_path, text="")
main_background.place(x=0, y=0, relwidth=1, relheight=1)



#<<<<< Function Area for our button switch dark theme for appearance mode and color theme >>>>> 
ctk.set_appearance_mode("light")  # Start with light mode
dark_mode = False  # Variable to track the current mode



# Create a container frame for the tab buttons and pack it to the left
left_frame = ctk.CTkFrame(root, corner_radius=0, border_color="maroon", border_width=2)
left_frame.pack(side="left", fill="y", padx=(8,0), pady=12)

# Create a container frame for the tab content
content_frame = ctk.CTkFrame(root)
content_frame.pack(side="right", expand=1, fill='both')

# Add tab buttons and link them to show the respective frames
tab0_img = ctk.CTkImage(Image.open("PyHorse Logo.png"), size=(60, 55))
tab0_button = ctk.CTkButton(left_frame, text="", command=lambda: show_frame(tab0), width=40, height=40, image=tab0_img, fg_color="transparent", hover_color="gray")
tab0_button.pack(pady=(15,40), padx=8)



stock_on = ctk.CTkImage(light_image=Image.open("stockwhite.png"), size=(27,30)) 
stock_off = ctk.CTkImage(dark_image=Image.open("stock.png"), size=(27,30))

tab1_img = ctk.CTkImage(Image.open("stockwhite.png"), size=(25, 25))
tab1_button = ctk.CTkButton(left_frame, text="", command=lambda: show_frame(tab1), width=60, height=40, image=stock_off, fg_color="transparent", hover_color="#d4172b", compound="top")
tab1_button.pack(pady=10, padx=10)


inventory_on = ctk.CTkImage(light_image=Image.open("whiteinventory.png"), size=(25,27))
inventory_off = ctk.CTkImage(dark_image=Image.open("inventory.png"), size=(24,27))

tab2_button = ctk.CTkButton(left_frame, command=inventory_file, text="", width=60, height=40, image=inventory_off, fg_color="transparent", hover_color="#d4172b")
tab2_button.pack(pady=0, padx=10)

database_on = ctk.CTkImage(Image.open("whitedatabase.png"), size=(24, 25))
database_off = ctk.CTkImage(Image.open("database.png"), size=(24, 25))

database_button = ctk.CTkButton(left_frame, command=lambda: show_frame(tab2), text="", width=60, height=40, image=database_off, fg_color="transparent", hover_color="#d4172b", compound="top")
database_button.pack(pady=10, padx=10)



log_out_on = ctk.CTkImage(light_image=Image.open("whitelog-in.png"), size=(25,24))
log_out_off = ctk.CTkImage(dark_image=Image.open("log-in.png"), size=(25,24))

logout_button = ctk.CTkButton(left_frame, text="", width=60, height=40, image=log_out_off, fg_color="transparent", hover_color="#d4172b", command=log_out)
logout_button.pack(side=BOTTOM, pady=15)



font1 = ctk.CTkFont("Arial Black", 25)
font2 = ctk.CTkFont("Arial Black", 15)
stock_font = ctk.CTkFont("Montserrat", 11)

tab0 = ctk.CTkFrame(content_frame)
tab0.place(in_=content_frame, x=0, y=0, relwidth=1, relheight=1)


main_background1 = ctk.CTkLabel(tab0, image=main_background_path, text="")
main_background1.place(x=0, y=0, relwidth=1, relheight=1)

upper_frame0 = ctk.CTkFrame(tab0, height=600, width=60, fg_color="maroon", corner_radius=0)
upper_frame0.pack(side="top", fill=BOTH, pady=(12,0), padx=(0,8))


orderlabel = ctk.CTkLabel(upper_frame0, text="Order", font=font1)
orderlabel.pack(side=LEFT, pady=25, padx=40)



icon_theme_on_off = ctk.CTkImage(light_image=Image.open("night-mode.png"), size=(30,27)) 


button_switch = ctk.CTkButton(upper_frame0, image=icon_theme_on_off, corner_radius=7, text="Dark Mode", text_color="black", bg_color="transparent", fg_color="gray", hover_color="#FFFFF0", font=font2, command=changemode)
button_switch.place(x=900, y=28)

bill_frame = ctk.CTkFrame(tab0, width=360)
bill_frame.pack(side="right", anchor="s", fill="y", padx=(5,9), pady=(0,13))

bill_frame1 = ctk.CTkFrame(bill_frame, corner_radius=40, fg_color="transparent", border_color="gray", border_width=1)
bill_frame1.place(x=10, y=5, relwidth=.95, relheight=.975)




subtotal_label = tk.Label(bill_frame1, text="Sub Total:                           ₱0.00", font=('Arial', 14))
subtotal_label.place(x=120, y=425)

total_label = tk.Label(bill_frame1, text="Total:                                   ₱0.00", font=('Arial', 17))
total_label.place(x=90, y=460)

total_line = ctk.CTkLabel(bill_frame1, text="--------------------------------------------------------", text_color='black', fg_color="transparent", font=('Arial', 14))
total_line.place(x=40, y=325)

payment_bel = ctk.CTkLabel(bill_frame1, text="Payment Methods:", text_color='red', fg_color="transparent", font=('Arial', 14, 'bold'))
payment_bel.place(x=40, y=345)


customerlabel =  ctk.CTkLabel(bill_frame1, text="Customer Bill                               ", font=('Arial', 12), fg_color="white", text_color="black", width=250, corner_radius=20)
customerlabel.place(x=40, y=9)

clear_button = ctk.CTkButton(bill_frame1, text="Clear", text_color="black", width=50,height=10 ,fg_color="white", border_width=2, border_color="gray", bg_color="white",hover_color="gray", corner_radius=40, command=clear_treeview_above)
clear_button.place(x=230, y=11)


cash = ctk.CTkImage(light_image=Image.open("cash.png"), dark_image=Image.open("cash.png"), size=(31,27))

cash_button = ctk.CTkButton(bill_frame1, command=cash_button_clicked, text="Cash", font = ("Arial Black", 11), image=cash, compound="top", text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=75, height=10)
cash_button.place(x=10, y=405)
debbit = ctk.CTkImage(light_image=Image.open("credit-card.png"), dark_image=Image.open("credit-card.png"), size=(30,25))

debbit_button = ctk.CTkButton(bill_frame1, command=debit_button_clicked, text="Debbit", font = ("Arial Black", 11), image=debbit, compound="top", text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=75, height=10)
debbit_button.place(x=93, y=405)
online = ctk.CTkImage(light_image=Image.open("white-mobile-payment.png"), dark_image=Image.open("white-mobile-payment.png"), size=(30,25))

online_button = ctk.CTkButton(bill_frame1, command=online_button_clicked, text="Online", font = ("Arial Black", 11), image=online, compound="top", text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=75, height=10)
online_button.place(x=177, y=405)


resetm = ctk.CTkImage(light_image=Image.open("reset.png"), dark_image=Image.open("reset.png"), size=(30,25))

reset_button = ctk.CTkButton(bill_frame1, command=reset, text="Reset", font = ("Arial Black", 11), image=resetm, compound="top", text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=75, height=10)
reset_button.place(x=260, y=405)


pay_button = ctk.CTkButton(bill_frame1, command=checkout_main, state="disabled",text="Pay", corner_radius=20, font = ("Arial Black", 12), text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=80, height=38)
pay_button.place(x=30, y=500)

email_button = ctk.CTkButton(bill_frame1, command=email_win, text="Email", corner_radius=20, state="disabled", font = ("Arial Black", 12), text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=80, height=38)
email_button.place(x=132, y=500)

print_button = ctk.CTkButton(bill_frame1, command=print_resit, text="Print", state="disabled",corner_radius=20, font = ("Arial Black", 12), text_color="#FFFFFF" , hover_color="red", fg_color="black", border_color="white", border_width=2, width=80, height=38)
print_button.place(x=238, y=500)


product_frame1 = ctk.CTkFrame(tab0, corner_radius=0)
product_frame1.place(in_=tab0, x=0, y=275, relwidth=.688, relheight=.600)


mycanvas1 = ctk.CTkCanvas(product_frame1, highlightthickness=0)
mycanvas1.pack(side=LEFT,fill=BOTH,expand=True, padx=(5,0), pady=5)


scrollbar1 = ctk.CTkScrollbar(product_frame1, orientation="vertical", command=mycanvas1.yview)
scrollbar1.pack(side=RIGHT, fill="y")

mycanvas1.configure(yscrollcommand=scrollbar1.set)

mycanvas1.bind("<Configure>", on_canvas_configure1)



myframe1 = ctk.CTkFrame(mycanvas1, corner_radius=0)
mycanvas1.create_window((0,0), window=myframe1, anchor=NW)

mycanvas1.create_window((0,0), window=myframe1, anchor=NW)



columns = ("Name", "Quantity", "Price")
cart_listbox = ttk.Treeview(bill_frame1, columns=columns, show="headings", height=15)
cart_listbox.heading("Name", text="Product Name")
cart_listbox.heading("Quantity", text="Quantity")
cart_listbox.heading("Price", text="Price")

cart_listbox.column("Name", anchor=tk.CENTER, width=200)      # Set width of "Name" column
cart_listbox.column("Quantity", anchor=tk.CENTER, width=100)  # Set width of "Quantity" column
cart_listbox.column("Price", anchor=tk.CENTER, width=150) 

# Pack the Treeview widget
cart_listbox.place(x=30, y=75)

    

tab1 = ctk.CTkFrame(content_frame, fg_color="transparent")
tab1.place(in_=content_frame, x=0, y=14, relwidth=.994, relheight=.961)

tab2 = ctk.CTkFrame(content_frame, fg_color="transparent")
tab2.place(in_=content_frame, x=0, y=14, relwidth=.994, relheight=.961)


dataframe = ctk.CTkFrame(tab2, fg_color="transparent", corner_radius=10, border_width=3, border_color="maroon", width=340)
dataframe.pack(side="left", padx=(380,0))

username_label = ctk.CTkLabel(dataframe, text="Username:", font=("Arial Black", 15))
username_label.place(x=20, y=40)

username_entry = ctk.CTkEntry(dataframe, placeholder_text="root", border_width=2, border_color="yellow", font=("Arial Black", 15), width=200)
username_entry.place(x=120, y=40)

password_label = ctk.CTkLabel(dataframe, text="Password:", font=("Arial Black", 15))
password_label.place(x=20, y=100)

password_entry = ctk.CTkEntry(dataframe, placeholder_text="#@01001ej47bloom", border_color="yellow", font=("Arial Black", 15), width=200)
password_entry.place(x=120, y=100)

# Create upper frame for stock label
upper_frame_stock = ctk.CTkFrame(tab1, fg_color="Maroon", corner_radius=0, bg_color="maroon")
upper_frame_stock.pack(side="top", fill=tk.BOTH)

# Stock label
font1 = ("Arial Black", 25)
stock_label = ctk.CTkLabel(upper_frame_stock, fg_color="transparent", text="Stock", font=font1, text_color="Gold")
stock_label.pack(side=tk.LEFT, pady=30, padx=40, fill=tk.BOTH)

# Edit stock frame
editstock_frame = ctk.CTkFrame(tab1, width=500, corner_radius=0, fg_color="transparent", height=100)
editstock_frame.pack(side="bottom", fill=tk.BOTH, expand=True, pady=5)

# Main items frame for products
main_items_frame = ctk.CTkScrollableFrame(editstock_frame, fg_color="transparent")
main_items_frame.pack(side="bottom", fill=tk.BOTH, expand=True, pady=5, padx=(70,0))



# Function to create product buttons dynamically
def create_product_button(product_key, row, column):
    """Creates a product button with its image, name, category, size, and price."""
    product_data = products.get(product_key)

    
        
    if product_data:
        product_frame = ctk.CTkFrame(myframe1, width=250, corner_radius=20, height=180, border_width=2, border_color="#ffd700", fg_color="#fffff0")
        product_frame.grid(row=row, column=column, padx=(8, 8), pady=25)

        product_img = ctk.CTkImage(light_image=Image.open(product_data["image"]), dark_image=Image.open(product_data["image"]), size=product_data["image_size"])
        product_img_label = ctk.CTkLabel(product_frame, image=product_img, text="", compound=TOP)
        product_img_label.place(x=5, y=40, relwidth=.3)

        product_button = ctk.CTkButton(product_frame, hover_color="#5a0000", text_color="#ffd700", text="Add to Cart", width=100, height=40, fg_color="#ff0000", command=lambda: add_to_cart(product_data['hidden_name'], product_data['quantity'], product_data['price'], product_data, product_stock_label, stock_label))
        product_button.place(x=100, y=130)

        product_name_hidden = ctk.CTkLabel(product_frame, text=product_data["hidden_name"], text_color="#fffff0", font=("Arial Black", 17))
        product_name_hidden.place(x=10000, y=20)

        product_name_label1 = ctk.CTkLabel(product_frame, text=product_data["name1"], text_color="Black", font=("Arial Black", 17))
        product_name_label1.place(x=100, y=10)

        product_name_label2 = ctk.CTkLabel(product_frame, text=product_data["name2"], text_color="black", font=("Arial Black", 17))
        product_name_label2.place(x=100, y=35)


        product_category_label = ctk.CTkLabel(product_frame, text=f"{product_data['category']} | {product_data['size']}", font=("Arial Black", 13), text_color="black")
        product_category_label.place(x=100, y=60)

        product_price_label = ctk.CTkLabel(product_frame, text=f"₱{product_data['price']}", font=("Arial Black", 17), text_color="#ffd700")
        product_price_label.place(x=100, y=81)

        product_stock_label = ctk.CTkLabel(product_frame, text=f"Stock: {product_data['stock']}", font=("Arial Black", 12), fg_color="transparent", text_color="#808080")
        product_stock_label.place(x=100, y=102)

        frame = ctk.CTkFrame(main_items_frame, width=300, corner_radius=15, border_color="#ffd700", fg_color="#fffff0", border_width=2)
        frame.grid(row=row, column=column, padx=15, pady=(30, 10))

        product_img = ctk.CTkImage(light_image=Image.open(product_data["image"]), dark_image=Image.open(product_data["image"]), size=product_data["image_size"])
        product_img_label = ctk.CTkLabel(frame, image=product_img, text="", compound=TOP)
        product_img_label.place(x=5, y=40, relwidth=.3)

        ctk.CTkLabel(frame, text=product_data["name1"], font=("Arial Black", 17)).place(x=120, y=20)
        ctk.CTkLabel(frame, text=product_data["name2"], font=("Arial Black", 17)).place(x=120, y=45)
        ctk.CTkLabel(frame, text=product_data["category"], font=("Arial Black", 14), text_color="#808080").place(x=123, y=85)

        stock_label = ctk.CTkLabel(frame, text=f"Stock: {product_data['stock']}", font=("Arial Black", 12), fg_color="#fffff0", text_color="black")
        stock_label.place(x=125, y=110)

        entry = ctk.CTkEntry(frame, width=60)
        entry.place(x=120, y=145)

        save_button = ctk.CTkButton(frame, fg_color="#ff0000", hover_color="#5a0000", text_color="#ffd700", height=30, width=50, text="Save Stock", command=lambda: updatelabels_new(entry, stock_label, product_stock_label, product_data))
        save_button.place(x=190, y=145)



# Function to search products
def search_products(query):

    search_results = {}

    for product, product_data in products.items():
        # Check if the query matches any of the product's names or hidden name
        matched_products = [product for product in product_key if query in product_data['name1'].lower() or
            query in product_data['name2'].lower() or
            query in product_data['category'].lower()]
        
        if matched_products:
            search_results[product] = matched_products
    
    return search_results

# Function to display search results
def display_search_results(search_results):
    # Clear the previous search results
    for widget in myframe1.winfo_children():
        widget.destroy()

    row = 0
    column = 0
    for product_key in search_results:
        create_product_button(product_key, row, column)
        column += 1
        if column == 3:
            column = 0
            row += 1

    # If search results are empty, display a message indicating that the product is not found
    if not search_results:
        label = ctk.CTkLabel(myframe1, text="Search Product is Not Found!", font=("Helvetica", 14))
        label.place(x=320, y=120)


# Create a function to handle search queries
def handle_search(event):
    query = entry.get().strip()  # Get the search query from the entry widget
    if query:
        search_results = search_products(query)
        display_search_results(search_results)
    



search_frame = ctk.CTkFrame(tab0, corner_radius=0)
search_frame.place(x=0, y=99, relwidth=.688, relheight=.25)

entry = ctk.CTkEntry(search_frame, placeholder_text="Search Product", font=("Arial Black", 14, "bold"), corner_radius=8, width=600, height=35, border_width=2, border_color="gold", placeholder_text_color="gray")
entry.place(x=50, y=15)

button_all_products = ctk.CTkButton(search_frame, text="All Products", font = ("Arial Black", 12, "bold"), text_color="white",hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39,command=lambda: scroll_to_product("b1"))
button_all_products.grid(row=1, column=0, pady=(70,20),padx=(50, 0),  sticky=W)

button_all_cognac = ctk.CTkButton(search_frame, text="Cognac", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("c1"))
button_all_cognac.grid(row=1, column=1,pady=(70, 20), padx=(20, 0),  sticky=W)

button_all_gin = ctk.CTkButton(search_frame, text="Gin", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("g1"))
button_all_gin.grid(row=1, column=2, pady=(70, 20), padx=(20, 0),  sticky=W)

button_all_vodka = ctk.CTkButton(search_frame, text="Vodka", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("v1") )
button_all_vodka.grid(row=1, column=3, pady=(70, 20), padx=(20, 0),  sticky=W)

button_all_whiskey = ctk.CTkButton(search_frame, text="Whiskey", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("w1"))
button_all_whiskey.grid(row=1, column=4, pady=(70, 20), padx=(20, 500),  sticky=W)

button_all_rum = ctk.CTkButton(search_frame, text="Rum", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold",width=130, height=39, command=lambda: scroll_to_product("r1"))
button_all_rum.grid(row=2, column=0, pady=(0,50), padx=(50, 0), sticky=W)

button_all_tequila = ctk.CTkButton(search_frame, text="Tequila", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold",width=130, height=39, command=lambda: scroll_to_product("t1"))
button_all_tequila.grid(row=2, column=1, pady=(0,50), padx=(20, 0),  sticky=W)

button_all_beer = ctk.CTkButton(search_frame, text="Beer", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("b1"))
button_all_beer.grid(row=2, column=2, pady=(0,50), padx=(20, 0),  sticky=W)

button_all_liqueurs = ctk.CTkButton(search_frame, text="Liqueurs", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("l1"))
button_all_liqueurs.grid(row=2, column=3, pady=(0,50), padx=(20, 0),  sticky=W)

button_all_wine = ctk.CTkButton(search_frame, text="Wine", font = ("Arial Black", 12, "bold"), text_color="white", hover_color="red", fg_color="#d4172b", border_width=2, border_color="gold", width=130, height=39, command=lambda: scroll_to_product("wi1"))
button_all_wine.grid(row=2, column=4, pady=(0,50), padx=(20, 0), sticky=W) 







# Populate the product frame with buttons
row = 0
column = 0
for product_key in products:
    create_product_button(product_key, row, column)
    column += 1
    if column == 3:
        column = 0
        row += 1








show_frame(tab0)

entry.bind("<Return>", handle_search)


root.mainloop()

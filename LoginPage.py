import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from tkinter import Toplevel, Label
from tkinter import ttk
from subprocess import call


def login():

    with open("login_credentials.json", 'r') as file:
        credentials = json.load(file)[0]

    entered_username = username_entry.get()
    entered_password = password_entry.get()

# Check if the entered credentials are valid
    if entered_username in credentials and entered_password == credentials[entered_username]:
        messagebox.showinfo('Login Successful', "You are successfully logged in!")
        root.destroy()
        record_login(entered_username)
        load()

    else:
        adminlogin()


def adminlogin():

    with open("login_credentials.json", 'r') as file:
        credentials = json.load(file)[1]

    entered_username = username_entry.get()
    entered_password = password_entry.get()

# Check if the entered credentials are valid
    if entered_username in credentials and entered_password == credentials[entered_username]:
        messagebox.showinfo('Admin Login Successful', "Welcome back, admin!")
        root.destroy()
        record_login(entered_username)
        open_admin_main()

    else:
        messagebox.showinfo('Login failed', "Invalid username or password")



def load():
    loading()
    root.after(5000, open_main)

def open_main():
    call(["python", "main.py"])

def open_admin_main():
    call(["python", "admin_main.py"])

def record_login(username):
    # Record login time
    login_time = datetime.now().strftime("%B %d, %Y - %I:%M:%S %p")

    # Load existing login history or initialize an empty list
    try:
        with open('login_history.json', 'r') as file:
            login_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        login_history = []

    # Add current login to history
    login_history.append({"username": username, "time": login_time})

    # Save updated login history to JSON file
    with open('login_history.json', 'w') as file:
        json.dump(login_history, file)





def loading():
    loading_screen = tk.Tk()
    loading_screen.geometry("1100x650+5+30")
    loading_screen.title("Loading...")
    loading_screen.iconbitmap("ui_images\\main_icon.ico")

    loading_image = tk.PhotoImage(file="ui_images\\loading.png")
    loading_background = tk.Label(loading_screen, image=loading_image)
    loading_background.image = loading_image
    loading_background.pack()

    loading_bar = ttk.Progressbar(loading_screen, orient="horizontal", length=300, mode="determinate")
    loading_bar.place(x=400, y=400)

    def update_progress(value):
        loading_bar['value'] = value
        if value < 100:
            loading_screen.after(1000, update_progress, value + 25)

    update_progress(0)  # Start updating progress

    loading_screen.after(5000, loading_screen.destroy)  


    
#Create the main window
root = tk.Tk()
root.title("Login Form")
root.resizable(False,False)
root.geometry("900x630")
root.configure(bg="#DDD1B8")
root.iconbitmap("ui_images\\main_icon.ico")

# the third label that expands horizontally when frame is resized

LoginFrame = tk.Frame(root, bg="#DDD1B8")
LoginFrame.pack(fill=tk.BOTH, padx=250, pady=(60,60), expand=True)

loginframe_image = tk.PhotoImage(file='ui_images\\loginframe.png')
bg_label = tk.Label(LoginFrame, image=loginframe_image, bg="#DDD1B8")
bg_label.place(relwidth=1, relheight=1)
LoginFrame.image = loginframe_image


welcome = tk.Label(LoginFrame, text="WELCOME", bg="#fcf7f0", font="-family {Poppins SemiBold} -size 25 -weight bold", fg="#9A7754")
welcome.pack(anchor=tk.CENTER, pady=(55, 0))

picture = tk.PhotoImage(file='ui_images\\welcome.png')
picture_label = tk.Label(LoginFrame, image=picture, bg="#fcf7f0")
picture_label.pack(pady=18)

#Create amd place labels and entry widgets for username and password
username = tk.Label(LoginFrame, text="Username", font=("Courier New Bold", 14), bg="#fcf7f0")
username.pack(anchor=tk.W, padx=85)
username_entry = tk.Entry(LoginFrame, font=("Courier", 14), bd=2, highlightbackground="red")
username_entry.pack(pady=4)

password = tk.Label(LoginFrame, text="Password", font=("Courier New Bold", 14), bg="#fcf7f0")
password.pack(anchor=tk.W, padx=85, pady=(12,0))
password_entry = tk.Entry(LoginFrame, show="*", font=("Courier", 14), bd=2) #Entry for password "*" as mask
password_entry.pack(pady=4)

#Create the login button
login_pic = tk.PhotoImage(file='ui_images\\login.png')
login_button = tk.Button(LoginFrame, width=200, height=50, bd=0, image=login_pic, bg="#fcf7f0", command=login)
login_button.pack(pady=(28,6))

#Run the tkinter
root.mainloop()


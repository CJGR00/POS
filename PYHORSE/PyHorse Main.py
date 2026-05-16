#==========================Dependencies=============================

#import mysql.connector     - dependencies for our database MySql

from customtkinter import *
import customtkinter as ctk  
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

from subprocess import call 

#===================================================================



# Function to show the login screen
def show_login_screen():


    # Create the main window
    pyhorse_main = ctk.CTk()
    pyhorse_main.title("PyHorseᴳ¹ POS")
    pyhorse_main.iconbitmap("PyHorse Logo.ico")

    screen_width = pyhorse_main.winfo_screenwidth()
    screen_height = pyhorse_main.winfo_screenheight()

    # Set the geometry of the window fullscreen
    pyhorse_main.geometry("%dx%d+0+0" % (screen_width,screen_height))

    # Load the image
    original_image = Image.open("Frame Log In.png")

    # Create a CTkImage with the original image and appropriate size
    main_background_path = ctk.CTkImage(light_image=original_image, size=(screen_width, screen_height))

    # Create a label to hold the background image
    main_background = ctk.CTkLabel(pyhorse_main, image=main_background_path, text="")
    main_background.place(x=0, y=0, relwidth=1, relheight=1)



    # Exit function
    def Exit():
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=pyhorse_main)
        if sure:
            pyhorse_main.destroy()
        
    pyhorse_main.protocol("WM_DELETE_WINDOW", Exit)


    # Function to call our certain files, whether for Admin or Employee
    def admin_file():
        call(["python", "PyHorse Admin.py"])
        pyhorse_main.deiconify()



    def employee_file():
        call(["python", "PyHorse Employee.py"])
        pyhorse_main.deiconify()

        
    # User Entry
    def user_enter(e):
        e1.delete(0, END)

    def user_leave(e):
        name = e1.get()
        if name == '':
            e1.insert(0, "Username")

    def login_user():
        username = e1.get()
        password = p1.get()

        if (username == "" or username == "Username") or (password == "" or password == "Password"):
            messagebox.showerror("Entry Error", "Wrong Username or Password")
        else:
            if username == "Admin" and password == "PyHorseG1":  
                messagebox.showinfo("Login", "Admin Login Successful")
                pyhorse_main.withdraw()
                admin_file()
            elif username == "Employee" and password == "Employee1":  
                messagebox.showinfo("Login", "Employee Login Successful")
                pyhorse_main.withdraw()
                employee_file()
            else:
                messagebox.showerror("Login Failed", "Invalid Username or Password")



    e1 = ctk.CTkEntry(pyhorse_main, text_color="gray", font=("Arial", 15, "bold"), width=200, height=40, fg_color="#F5F5F7", corner_radius=0, border_width=0)
    e1.insert(0, "Username")
    e1.bind("<FocusIn>", user_enter)
    e1.bind("<FocusOut>", user_leave)
    e1.place(x=923, y=214)



    # Password Entry
    def password_enter(e):
        p1.delete(0, END)

    def password_leave(e):
        if p1.get() == '':
            p1.insert(0, "Password")

    p1 = ctk.CTkEntry(pyhorse_main, text_color="gray", font=("Arial", 15, "bold"), width=200, height=40, fg_color="#F5F5F7", corner_radius=0, border_width=0)
    p1.insert(0, "Password")
    p1.bind("<FocusIn>", password_enter)
    p1.bind("<FocusOut>", password_leave)
    p1.pack(side="right", anchor="e", padx=(0, 155), pady=(0, 8))


    # Hide and Show Button for Password
    button_mode = True

    def hide():
        nonlocal button_mode
        if button_mode:
            eye_button.configure(image=close_eye)
            p1.configure(show="*")
            button_mode = False
        else:
            eye_button.configure(image=open_eye)
            p1.configure(show="")
            button_mode = True

    open_eye = ctk.CTkImage(Image.open("eye.png"), size=(20, 20))
    close_eye = ctk.CTkImage(Image.open("hide.png"), size=(20, 20))

    eye_button = ctk.CTkButton(pyhorse_main, text="", corner_radius=0, border_width=0, image=open_eye, hover_color="red", fg_color="#F5F5F7", bg_color="#F5F5F7", width=5, height=5, command=hide)
    eye_button.place(x=1130, y=305)

    log_in_button = ctk.CTkButton(pyhorse_main, text="Log In   >", font=("Arial Black", 18, "bold"), text_color="black", hover_color="red", fg_color="red", width=100, height=40, corner_radius=0, border_width=0, command=login_user)
    log_in_button.place(x=1067, y=408)

    
    pyhorse_main.mainloop()





#-------------------------------------------Opening Gif----------------------------------------------


# Function to play the GIF

def play_gif():
    gif_window = ctk.CTk()
    gif_window.overrideredirect(True)

    screen_width = gif_window.winfo_screenwidth()
    screen_height = gif_window.winfo_screenheight()


    # Set the geometry of the window fullscreen
    gif_window.geometry("%dx%d+0+0" % (screen_width,screen_height))

    # Load the image
    original_image = Image.open("Frame Background.png")

    # Create a CTkImage with the original image and appropriate size
    main_background_path = ctk.CTkImage(light_image=original_image, size=(screen_width, screen_height))

    # Create a label to hold the background image
    main_background = ctk.CTkLabel(gif_window, image=main_background_path, text="")
    main_background.place(x=0, y=0, relwidth=1, relheight=1)


    gif_label = ctk.CTkLabel(gif_window, text="")
    gif_label.pack(expand=True)

    gif = Image.open("Logo GIF.gif")

    # Resize each frame to fit the screen dimensions and convert to PhotoImage
    gif_frames = [ImageTk.PhotoImage(frame.copy().resize((screen_width, screen_height), Image.LANCZOS)) for frame in ImageSequence.Iterator(gif)]

    def update_frame(ind):
        gif_label.configure(image=gif_frames[ind])
        ind += 1
        if ind < len(gif_frames):
            gif_window.after(13, update_frame, ind)  # Adjust update rate here
        else:
            gif_window.destroy()
            show_login_screen()


    update_frame(0)
    gif_window.mainloop()

# Run the GIF first
play_gif()
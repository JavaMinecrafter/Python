from tkinter import *
from tkinter import messagebox
import random
import pyperclip
def search_wrapper():
    email_to_find = eEnt.get()  # Get the email from the Entry widget
    website, email, password = search(email_to_find)  # Call the search function with the email
    if website and email and password:  # Check if login details are found
        # Fill in the Entry widgets with the found details
        wEnt.delete(0, END)
        wEnt.insert(0, website)
        pEnt.delete(0, END)
        pEnt.insert(0, password)
    else:
        # Notify the user if the email is not found
        messagebox.showinfo(title="Not Found", message=f"No login details found for email: {email_to_find}")
def search(email_to_find):
    found_details = []  # List to store all found login details
    try:
        with open("textbook.txt", "r") as data_file:
            for line in data_file:
                if "Email:" in line:
                    email = line.split("||")[1].split(":")[1].strip()
                    if email == email_to_find:
                        # Extract website and password from the line
                        website = line.split("||")[0].split(":")[1].strip()
                        password = line.split("||")[2].split(":")[1].strip()
                        found_details.append((website, password))  # Add to found_details list
        return found_details
    except FileNotFoundError:
        return []


def select_login():
    email_to_find = eEnt.get()  # Get the email from the Entry widget
    login_options = search(email_to_find)  # Get all login details for that email

    if login_options:
        # Create a popup window to display login options
        popup = Toplevel()
        popup.title("Select Login Details")
        popup.geometry("300x200")

        # Display login options using radio buttons
        selected_login = StringVar()
        selected_login.set(login_options[0][0] + ":" + login_options[0][1])  # Set the default value
        for i, (website, password) in enumerate(login_options):
            Radiobutton(popup, text=f"{website}: {password}", variable=selected_login, value=f"{website}:{password}").pack(anchor=W)

        # Function to save selected login details
        def save_selected():
            login_info_string = selected_login.get()

            # Split the string to extract website and password
            website, password = login_info_string.split(":")

            wEnt.delete(0, END)
            wEnt.insert(0, website.strip())
            pEnt.delete(0, END)
            pEnt.insert(0, password.strip())
            popup.destroy()

        Button(popup, text="Select", command=save_selected).pack()  # Associate save_selected function with the "Select" button

    else:
        messagebox.showinfo("No Login Details", f"No login details found for email: {email_to_find}")



# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 16)
    nr_symbols = random.randint(2, 16)
    nr_numbers = random.randint(2, 16)

    password_list = []

    for char in range(nr_letters):
      password_list.append(random.choice(letters))

    for char in range(nr_symbols):
      password_list += random.choice(symbols)

    for char in range(nr_numbers):
      password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
      password += char
    pyperclip.copy(password)
    messagebox.showinfo(title="For your convenience", message="We have copied this password for you!")
    pEnt.insert(0, f"{password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def get_last_email():
    try:
        with open("textbook.txt", "r") as data_file:
            lines = data_file.readlines()
            if lines:
                last_line = lines[-1]
                last_email = last_line.split("||")[1].split(":")[1].strip()
            else:
                last_email = ""
    except FileNotFoundError:
        last_email = ""
    return last_email
def save():
    website = wEnt.get()
    email = eEnt.get()
    password = pEnt.get()

    if website and email and password:
        is_ok = messagebox.askokcancel(title="Do you want to submit this information?",
                                       message=f"Website: {website}. Email/Username: {email}. Password: {password}.")
        if is_ok:
            with open("textbook.txt", "a") as data_file:
                data_file.write(f"Website: {website}||Email: {email}||Password: {password}\n")
            wEnt.delete(0, END)
            pEnt.delete(0, END)
    else:
        messagebox.showinfo(title="Uh Oh!", message="Please fill in all the fields.")


# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=50,pady=50, background="gray")
canvas = Canvas(height=200, width=200, background="gray")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=logo_img)
canvas.grid(row=0, column = 1)
wt=Label(text="Website: ", background="gray")
et=Label(text="Email/Username: ", background="gray")
pt=Label(text="Password: ", background="gray")
wt.grid(row=1, column=0)
et.grid(row=2, column=0)
pt.grid(row=3, column=0)
wEnt=Entry(width=50, background="gray")
wEnt.grid(row=1, column=1, columnspan=2)
wEnt.focus()
eEnt=Entry(width=40, background="gray")
eEnt.grid(row=2, column=1, columnspan=2)
try:
    last_email = get_last_email()
    eEnt.insert(0, last_email)
except Exception as e:
    # Handle the exception here
    print(f"An error occurred: {e}")
eEnt.insert(0, f"")
pEnt=Entry(width=27, background="gray")
pEnt.grid(row=3, column=1)
s_b=Button(text="Search: ", background="gray", command=select_login)
s_b.grid(row=2,column=3)
g_p_b=Button(text="Generate Password: ", background="gray", command=generator)
g_p_b.grid(row=3,column=2)
a_b= Button(text="Add", width=36, background="gray", command=save)
a_b.grid(row=4, column=1, columnspan=2)



window.mainloop()

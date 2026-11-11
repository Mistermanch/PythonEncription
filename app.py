from tkinter import *
from tkinter import messagebox
import base64

def open_result_window(title, bg_color, label_text, result_text):
    popup = Toplevel(screen)
    popup.title(title)
    popup.geometry("400x200")
    popup.minsize(250, 150)
    popup.configure(bg=bg_color)

    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(1, weight=1)

    Label(popup, text=label_text, font=("arial", 12, "bold"), fg="white", bg=bg_color). grid(row=0, column=0, sticky="w", padx=10, pady=(10,5))

    text_out = Text(popup, font=("Roboto", 10), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text_out.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    text_out.insert(END, result_text)

def decrypt():
    password=code.get()

    if password=="1234":
        message = text1.get("1.0", "end-1c")
        try:
            decode_message = message.encode("ascii")
            base64_bytes = base64.b64decode(decode_message)
            decrypted_msg = base64_bytes.decode("ascii")
            open_result_window("Decryption", "#00bd56", "DECRYPT", decrypted_msg)
        except:
            messagebox.showerror("Decryption", "Invalid Base64 text")
        
    elif password=="":
        messagebox.showerror("Encryption", "Input Password")
    else:
        messagebox.showerror("Encryption", "Invalid Password")

def encrypt():
    password=code.get()

    if password=="1234":
        message = text1.get("1.0", "end-1c")
        encode_message = message.encode("ascii")
        base64_bytes = base64.b64encode(encode_message)
        encrypted_msg = base64_bytes.decode("ascii")
        open_result_window("Encryption", "#ed3833", "ENCRYPT", encrypted_msg)

   
    elif password=="":
        messagebox.showerror("Encryption", "Input Password")
    else:
        messagebox.showerror("Encryption", "Invalid Password")


def main_screen():

    global screen
    global code
    global text1

    screen=Tk()
    screen.geometry("375x398")
    screen.minsize(320, 320)
    screen.title("EncApp")

    screen.columnconfigure(0, weight=1)
    screen.columnconfigure(1, weight=1)
    screen.rowconfigure(1,weight=1)

    def reset():
        code.set("")
        text1.delete(1.0,END)

    Label(text="Enter text for encryption and decryption", fg="black", font=("calibri", 13)).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10,5))

    text1 = Text(screen, font=("Roboto", 14), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text1.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
 

    Label(text="Enter secret key for encryption and decryption", fg="black", font=("calibri", 13)).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(10,5))

    code=StringVar()
    Entry(screen, textvariable=code, width=19, bd=0, font=("arial", 25),show="*").grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    Button(text="ENCRYPT", height=2,  bg="#ed3833", fg="white", bd=0, command=encrypt).grid(row=4, column=0, sticky="ew", padx=(10, 5), pady=(10, 5))
    Button(text="DECRYPT",  height=2, bg="#00bd56", fg="white", bd=0, command=decrypt).grid(row=4, column=1, sticky="ew", padx=(5, 10), pady=(10, 5))
    Button(text="RESET", height=2, bg="#1089ff", fg="white", bd=0, command=reset).grid(row=5, column=0, columnspan=2, sticky="ew", padx=(10), pady=(5, 10))

    screen.mainloop()

main_screen()
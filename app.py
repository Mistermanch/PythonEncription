from tkinter import *
from tkinter import messagebox
import base64
import hashlib
import os

PASSWORD_FILE = "secret.key"

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def password_exists():
    return os.path.exists(PASSWORD_FILE) and os.path.getsize(PASSWORD_FILE) > 0

def verify_password(input_password):
    if not password_exists():
        return False
    with open(PASSWORD_FILE, "r") as f:
        stored_hash = f.read().strip()
        return hash_password(input_password) == stored_hash

def open_password_setup(is_change=False):
    setup_win = Toplevel(screen)
    setup_win.title("Change password" if is_change else "Create Password")
    setup_win.geometry("320x260" if is_change else "320x210")
    setup_win.resizable(False, False)
    setup_win.grab_set()

    if not is_change:
        setup_win.protocol("WM_DELETE_WINDOW", screen.destroy)

    row_idx = 0
    old_pass_var = StringVar()
    new_pass_var = StringVar()
    confirm_pass_var = StringVar()

    if is_change:
        Label(setup_win, text="Current Password:", font=("calibri", 11)).grid(row=row_idx, column=0, sticky="w", padx=15, pady=(10, 0))
        row_idx += 1
        Entry(setup_win, textvariable=old_pass_var, show="*", font=("arial", 12)).grid(row=row_idx, column=0, sticky="ew", padx=15, pady=2)
        row_idx += 1

    Label(setup_win, text="New Password:", font=("calibri", 11)).grid(row=row_idx, column=0, sticky="w", padx=15, pady=(10, 0))
    row_idx += 1
    Entry(setup_win, textvariable=new_pass_var, show="*", font=("arial", 12)).grid(row=row_idx, column=0, sticky="ew", padx=15, pady=2)
    row_idx += 1

    Label(setup_win, text="Confirm New Password:", font=("calibri", 11)).grid(row=row_idx, column=0, sticky="w", padx=15, pady=(10, 0))
    row_idx += 1
    Entry(setup_win, textvariable=confirm_pass_var, show="*", font=("arial", 12)).grid(row=row_idx, column=0, sticky="ew", padx=15, pady=2)
    row_idx += 1

    setup_win.columnconfigure(0, weight=1)

    def save_password():
        if is_change and not verify_password(old_pass_var.get()):
            messagebox.showerror("Error", "Current password is incorrect", parent=setup_win)
            return

        new_pw = new_pass_var.get()
        confirm_pw = confirm_pass_var.get()

        if not new_pw:
            messagebox.showerror("Error", "Password cannot be empty", parent=setup_win)
            return

        if new_pw != confirm_pw:
            messagebox.showerror("Error", "Passwords do not match", parent=setup_win)
            return

        with open(PASSWORD_FILE, "w") as f:
            f.write(hash_password(new_pw))

        messagebox.showinfo("Success", "Password saved successfully", parent=setup_win)
        setup_win.destroy()

    Button(setup_win, text="SAVE PASSWORD", bg="#1089ff", fg="white", bd=0, height=2, command=save_password).grid(row=row_idx, column=0, sticky="ew", padx=15, pady=15)

def open_result_window(title, bg_color, label_text, result_text):
    popup = Toplevel(screen)
    popup.title(title)
    popup.geometry("400x200")
    popup.minsize(250, 150)
    popup.configure(bg=bg_color)

    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(1, weight=1)

    Label(popup, text=label_text, font=("arial", 12, "bold"), fg="white", bg=bg_color).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

    text_out = Text(popup, font=("Roboto", 10), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text_out.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
    text_out.insert(END, result_text)

def decrypt():
    password = code.get()

    if password == "":
        messagebox.showerror("Decryption", "Input Password")
    elif verify_password(password):
        message = text1.get("1.0", "end-1c")
        try:
            decode_message = message.encode("utf-8")
            base64_bytes = base64.b64decode(decode_message)
            decrypted_msg = base64_bytes.decode("utf-8")
            open_result_window("Decryption", "#00bd56", "DECRYPT", decrypted_msg)
        except Exception:
            messagebox.showerror("Decryption", "Invalid Base64 text")
    else:
        messagebox.showerror("Decryption", "Invalid Password")

def encrypt():
    password = code.get()

    if password == "":
        messagebox.showerror("Encryption", "Input Password")
    elif verify_password(password):
        message = text1.get("1.0", "end-1c")
        encode_message = message.encode("utf-8")
        base64_bytes = base64.b64encode(encode_message)
        encrypted_msg = base64_bytes.decode("utf-8")
        open_result_window("Encryption", "#ed3833", "ENCRYPT", encrypted_msg)
    else:
        messagebox.showerror("Encryption", "Invalid Password")

def main_screen():
    global screen
    global code
    global text1

    screen = Tk()
    screen.geometry("375x445")
    screen.minsize(320, 360)
    screen.title("EncApp")

    screen.columnconfigure(0, weight=1)
    screen.columnconfigure(1, weight=1)
    screen.rowconfigure(1, weight=1)

    def reset():
        code.set("")
        text1.delete(1.0, END)

    Label(screen, text="Enter text for encryption and decryption", fg="black", font=("calibri", 13)).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

    text1 = Text(screen, font=("Roboto", 14), bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text1.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

    Label(screen, text="Enter password for encryption and decryption", fg="black", font=("calibri", 13)).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

    code = StringVar()
    Entry(screen, textvariable=code, width=19, bd=0, font=("arial", 25), show="*").grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    Button(screen, text="ENCRYPT", height=2, bg="#ed3833", fg="white", bd=0, command=encrypt).grid(row=4, column=0, sticky="ew", padx=(10, 5), pady=(10, 5))
    Button(screen, text="DECRYPT", height=2, bg="#00bd56", fg="white", bd=0, command=decrypt).grid(row=4, column=1, sticky="ew", padx=(5, 10), pady=(10, 5))
    Button(screen, text="RESET", height=2, bg="#1089ff", fg="white", bd=0, command=reset).grid(row=5, column=0, sticky="ew", padx=(10, 5), pady=(5, 10))
    Button(screen, text="CHANGE PASSWORD", height=2, bg="#555555", fg="white", bd=0, command=lambda: open_password_setup(is_change=True)).grid(row=5, column=1, sticky="ew", padx=(5, 10), pady=(5, 10))

    if not password_exists():
        screen.after(100, lambda: open_password_setup(is_change=False))

    screen.mainloop()

main_screen()

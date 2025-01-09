import tkinter as tk
from tkinter import messagebox

# Global variables
user_balance = 2000
transaction_history = []
current_action = None  # Stores the current action (withdraw/deposit)


def enter_card():
    start_button.pack_forget()
    image_label.pack_forget()  # Hide the image when entering the next screen
    atm_interface()

def atm_interface():
    screen_label.config(text="Welcome! Users")
    screen_frame.pack(pady=5)

    left_frame.pack(side=tk.LEFT, padx=5, pady=5)
    right_frame.pack(side=tk.RIGHT, padx=5, pady=5)

    check_balance_button.pack(pady=5)
    print_statement_button.pack(pady=5)

    withdraw_button.pack(pady=5)
    deposit_button.pack(pady=5)
    keypad_frame.pack(pady=10, fill=tk.X)
    deactivate_keypad()  # Deactivate keypad initially


def check_balance():
    screen_label.config(text=f"Your current balance is ₹{user_balance}")


def print_statement():
    if transaction_history:
        statement = "\n".join(transaction_history)
    else:
        statement = "No transactions made yet."
    screen_label.config(text=f"Statement:\n{statement}")


def withdraw_cash():
    screen_label.config(text="Enter amount to withdraw:")
    activate_keypad("withdraw")


def deposit_cash():
    screen_label.config(text="Enter amount to deposit:")
    activate_keypad("deposit")

def activate_keypad(action):
    global current_action
    current_action = action  # Save current action (withdraw/deposit)
    entry.delete(0, tk.END)  # Clear the entry field
    keypad_status_label.grid_forget()
    for button in keypad_buttons:
        button.config(state=tk.NORMAL)  # Enable all number buttons
    clear_button.config(state=tk.NORMAL)  # Enable clear button
    confirm_button.config(state=tk.NORMAL)  # Enable confirm button
    zero_button.config(state=tk.NORMAL)  # Enable 0 button

def deactivate_keypad():
    keypad_status_label.grid(row=0, column=0, columnspan=3, pady=10)  # Show the label
    for button in keypad_buttons:
        button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)
    confirm_button.config(state=tk.DISABLED)
    zero_button.config(state=tk.DISABLED)

def confirm_action():
    global user_balance
    try:
        amount = int(entry.get())
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        if current_action == "withdraw":
            if amount > user_balance:
                raise ValueError("Insufficient balance. Please add cash to your amount")
            user_balance -= amount
            transaction_history.append(f"Withdrawn: ₹{amount}")
            screen_label.config(text=f"₹{amount} withdrawn successfully!")
        elif current_action == "deposit":
            user_balance += amount
            transaction_history.append(f"Deposited: ₹{amount}")
            screen_label.config(text=f"₹{amount} deposited successfully!")

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")
    finally:
        entry.delete(0, tk.END)
        deactivate_keypad()


def clear_entry():
    entry.delete(0, tk.END)


root = tk.Tk()
root.title("ATM Interface")
root.geometry("600x400")
root.resizable(False, False)

start_button = tk.Button(root, text="Click here to Insert card", font=("Arial", 16), command=enter_card)
# start_button.pack(expand=True)
start_button.pack(pady=(100, 0))  # No padding above or below the button

# First Screen Image
image = tk.PhotoImage(file="C:\\Users\\Admin\\Downloads\\BrainWave_Matrix_Internship\\Card.png")
image_label = tk.Label(root, image=image)
image_label.pack(pady=30)

screen_frame = tk.Frame(root)
screen_label = tk.Label(screen_frame, text="", font=("Arial", 14), wraplength=400)
screen_label.pack()

left_frame = tk.Frame(root)
right_frame = tk.Frame(root)
check_balance_button = tk.Button(left_frame, text="Check Balance", font=("Arial", 14), width=15, command=check_balance)
print_statement_button = tk.Button(left_frame, text="Print Statement", font=("Arial", 14), width=15, command=print_statement)
withdraw_button = tk.Button(right_frame, text="Cash Withdraw", font=("Arial", 14), width=15, command=withdraw_cash)
deposit_button = tk.Button(right_frame, text="Cash Deposit", font=("Arial", 14), width=15, command=deposit_cash)

# Keypad
keypad_frame = tk.Frame(root)
keypad_status_label = tk.Label(keypad_frame, text="Select Any Given Option ", font=("Arial", 14), fg="black")
entry = tk.Entry(keypad_frame, font=("Arial", 16), width=10)
entry.grid(row=1, column=0, columnspan=3, pady=5)

# Keypad buttons in the specified layout
keypad_layout = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
]

keypad_buttons = []
for row_index, row in enumerate(keypad_layout):
    for col_index, num in enumerate(row):
        button = tk.Button(
            keypad_frame, text=str(num), font=("Arial", 14), width=5,
            command=lambda num=num: entry.insert(tk.END, str(num))
        )
        button.grid(row=row_index + 2, column=col_index, padx=2, pady=5)
        keypad_buttons.append(button)

confirm_button = tk.Button(keypad_frame, text="Confirm", font=("Arial", 14), bg="green", fg="white", disabledforeground="white", command=confirm_action)
confirm_button.grid(row=5, column=0, padx=2, pady=5)

zero_button = tk.Button(keypad_frame, text="0", font=("Arial", 14), width=5, command=lambda: entry.insert(tk.END, "0"))
zero_button.grid(row=5, column=1, padx=2, pady=5)

clear_button = tk.Button(keypad_frame, text="Clear", font=("Arial", 14), bg="red", fg="white",disabledforeground="white",command=clear_entry)
clear_button.grid(row=5, column=2, padx=2, pady=5)

# Run the application
root.mainloop()

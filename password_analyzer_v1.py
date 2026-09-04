import tkinter as tk
from tkinter import messagebox


# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title("SecurePass Analyzer")
root.geometry("650x700")
root.resizable(False, False)
root.configure(bg="#101820")


# ==============================
# TITLE
# ==============================

title = tk.Label(
    root,
    text="SECUREPASS ANALYZER",
    font=("Arial", 24, "bold"),
    bg="#101820",
    fg="white"
)

title.pack(pady=(30, 5))


subtitle = tk.Label(
    root,
    text="Password Security Assessment Tool",
    font=("Arial", 11),
    bg="#101820",
    fg="#aaaaaa"
)

subtitle.pack(pady=(0, 25))


# ==============================
# PASSWORD INPUT
# ==============================

password_label = tk.Label(
    root,
    text="Enter Password",
    font=("Arial", 12, "bold"),
    bg="#101820",
    fg="white"
)

password_label.pack(anchor="w", padx=60)


password_entry = tk.Entry(
    root,
    width=45,
    font=("Arial", 14),
    show="*"
)

password_entry.pack(pady=10)


# ==============================
# SECURITY CHECKS TITLE
# ==============================

result_title = tk.Label(
    root,
    text="Security Checks",
    font=("Arial", 14, "bold"),
    bg="#101820",
    fg="white"
)

result_title.pack(pady=(30, 10))


# ==============================
# CHECK LABELS
# ==============================

length_result = tk.Label(
    root,
    text="○  At least 8 characters",
    font=("Arial", 11),
    bg="#101820",
    fg="white"
)

length_result.pack(anchor="w", padx=100)


uppercase_result = tk.Label(
    root,
    text="○  Contains uppercase letter",
    font=("Arial", 11),
    bg="#101820",
    fg="white"
)

uppercase_result.pack(anchor="w", padx=100)


lowercase_result = tk.Label(
    root,
    text="○  Contains lowercase letter",
    font=("Arial", 11),
    bg="#101820",
    fg="white"
)

lowercase_result.pack(anchor="w", padx=100)


number_result = tk.Label(
    root,
    text="○  Contains number",
    font=("Arial", 11),
    bg="#101820",
    fg="white"
)

number_result.pack(anchor="w", padx=100)


special_result = tk.Label(
    root,
    text="○  Contains special character",
    font=("Arial", 11),
    bg="#101820",
    fg="white"
)

special_result.pack(anchor="w", padx=100)


# ==============================
# SCORE
# ==============================

score_result = tk.Label(
    root,
    text="Score: 0 / 5",
    font=("Arial", 13, "bold"),
    bg="#101820",
    fg="white"
)

score_result.pack(pady=20)


# ==============================
# STRENGTH
# ==============================

strength_result = tk.Label(
    root,
    text="Strength: --",
    font=("Arial", 18, "bold"),
    bg="#101820",
    fg="white"
)

strength_result.pack(pady=10)


# ==============================
# ANALYZE FUNCTION
# ==============================

def analyze_password():

    password = password_entry.get()

    if password == "":
        messagebox.showwarning(
            "Empty Password",
            "Please enter a password."
        )
        return

    score = 0

    # Length
    if len(password) >= 8:
        score += 1
        length_result.config(
            text="✓  At least 8 characters"
        )
    else:
        length_result.config(
            text="✗  At least 8 characters"
        )

    # Uppercase
    if any(char.isupper() for char in password):
        score += 1
        uppercase_result.config(
            text="✓  Contains uppercase letter"
        )
    else:
        uppercase_result.config(
            text="✗  Contains uppercase letter"
        )

    # Lowercase
    if any(char.islower() for char in password):
        score += 1
        lowercase_result.config(
            text="✓  Contains lowercase letter"
        )
    else:
        lowercase_result.config(
            text="✗  Contains lowercase letter"
        )

    # Number
    if any(char.isdigit() for char in password):
        score += 1
        number_result.config(
            text="✓  Contains number"
        )
    else:
        number_result.config(
            text="✗  Contains number"
        )

    # Special character
    if any(not char.isalnum() for char in password):
        score += 1
        special_result.config(
            text="✓  Contains special character"
        )
    else:
        special_result.config(
            text="✗  Contains special character"
        )

    # Strength
    if score <= 2:
        strength = "WEAK"
    elif score == 3:
        strength = "MEDIUM"
    else:
        strength = "STRONG"

    score_result.config(
        text=f"Score: {score} / 5"
    )

    strength_result.config(
        text=f"Strength: {strength}"
    )


# ==============================
# CLEAR FUNCTION
# ==============================

def clear_password():

    password_entry.delete(0, tk.END)

    length_result.config(
        text="○  At least 8 characters"
    )

    uppercase_result.config(
        text="○  Contains uppercase letter"
    )

    lowercase_result.config(
        text="○  Contains lowercase letter"
    )

    number_result.config(
        text="○  Contains number"
    )

    special_result.config(
        text="○  Contains special character"
    )

    score_result.config(
        text="Score: 0 / 5"
    )

    strength_result.config(
        text="Strength: --"
    )


# ==============================
# BUTTONS
# ==============================

analyze_button = tk.Button(
    root,
    text="ANALYZE PASSWORD",
    font=("Arial", 12, "bold"),
    command=analyze_password,
    width=25
)

analyze_button.pack(pady=15)


clear_button = tk.Button(
    root,
    text="CLEAR",
    font=("Arial", 10, "bold"),
    command=clear_password,
    width=15
)

clear_button.pack()


# ==============================
# START APPLICATION
# ==============================

root.mainloop()
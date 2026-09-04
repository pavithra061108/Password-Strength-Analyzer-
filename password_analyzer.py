import tkinter as tk
from tkinter import ttk


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("SecurePass Analyzer")
root.geometry("650x720")
root.resizable(False, False)

# Dark background
root.configure(bg="#101820")

# Bring window to front
root.lift()
root.attributes("-topmost", True)
root.after(1000, lambda: root.attributes("-topmost", False))


# ============================================================
# COLORS
# ============================================================

BACKGROUND = "#101820"
CARD = "#1B2833"
WHITE = "#FFFFFF"
GRAY = "#AAB4BE"
CYAN = "#00D4FF"
GREEN = "#00FF88"
RED = "#FF5555"
YELLOW = "#FFD166"


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="SECUREPASS ANALYZER",
    font=("Arial", 24, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

title.pack(pady=(30, 5))


# ============================================================
# SUBTITLE
# ============================================================

subtitle = tk.Label(
    root,
    text="Password Security Assessment Tool",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

subtitle.pack(pady=(0, 25))


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = tk.Label(
    root,
    text="ENTER PASSWORD",
    font=("Arial", 11, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

password_label.pack(anchor="w", padx=70)


# ============================================================
# PASSWORD VARIABLE
# ============================================================

password_var = tk.StringVar()


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = tk.Entry(
    root,
    textvariable=password_var,
    font=("Arial", 14),
    show="*",
    bg=CARD,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    width=42
)

password_entry.pack(
    pady=10,
    ipady=8
)


# ============================================================
# SECURITY CHECKS TITLE
# ============================================================

checks_title = tk.Label(
    root,
    text="SECURITY CHECKS",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

checks_title.pack(pady=(25, 10))


# ============================================================
# SECURITY CHECK LABELS
# ============================================================

length_result = tk.Label(
    root,
    text="○  At least 8 characters",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

length_result.pack(anchor="w", padx=110, pady=3)


uppercase_result = tk.Label(
    root,
    text="○  Uppercase letter",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

uppercase_result.pack(anchor="w", padx=110, pady=3)


lowercase_result = tk.Label(
    root,
    text="○  Lowercase letter",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

lowercase_result.pack(anchor="w", padx=110, pady=3)


number_result = tk.Label(
    root,
    text="○  Number",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

number_result.pack(anchor="w", padx=110, pady=3)


special_result = tk.Label(
    root,
    text="○  Special character",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

special_result.pack(anchor="w", padx=110, pady=3)


# ============================================================
# SCORE
# ============================================================

score_result = tk.Label(
    root,
    text="Score: 0 / 5",
    font=("Arial", 13, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

score_result.pack(pady=(20, 5))


# ============================================================
# STRENGTH
# ============================================================

strength_result = tk.Label(
    root,
    text="Strength: --",
    font=("Arial", 18, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

strength_result.pack(pady=5)


# ============================================================
# PROGRESS BAR
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Cyber.Horizontal.TProgressbar",
    troughcolor="#2A3742",
    background=CYAN,
    thickness=15
)

strength_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate",
    maximum=5,
    style="Cyber.Horizontal.TProgressbar"
)

strength_bar.pack(pady=10)


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(show="")

        show_button.config(text="HIDE")

    else:

        password_entry.config(show="*")

        show_button.config(text="SHOW")


# ============================================================
# RESET RESULTS
# ============================================================

def reset_results():

    length_result.config(
        text="○  At least 8 characters",
        fg=GRAY
    )

    uppercase_result.config(
        text="○  Uppercase letter",
        fg=GRAY
    )

    lowercase_result.config(
        text="○  Lowercase letter",
        fg=GRAY
    )

    number_result.config(
        text="○  Number",
        fg=GRAY
    )

    special_result.config(
        text="○  Special character",
        fg=GRAY
    )

    score_result.config(
        text="Score: 0 / 5"
    )

    strength_result.config(
        text="Strength: --",
        fg=WHITE
    )

    strength_bar["value"] = 0


# ============================================================
# ANALYZE PASSWORD
# ============================================================

def analyze_password(*args):

    password = password_var.get()

    # Empty password
    if password == "":

        reset_results()

        return


    # Start score
    score = 0


    # --------------------------------------------------------
    # LENGTH
    # --------------------------------------------------------

    if len(password) >= 8:

        score += 1

        length_result.config(
            text="✓  At least 8 characters",
            fg=GREEN
        )

    else:

        length_result.config(
            text="✗  At least 8 characters",
            fg=RED
        )


    # --------------------------------------------------------
    # UPPERCASE
    # --------------------------------------------------------

    if any(char.isupper() for char in password):

        score += 1

        uppercase_result.config(
            text="✓  Uppercase letter",
            fg=GREEN
        )

    else:

        uppercase_result.config(
            text="✗  Uppercase letter",
            fg=RED
        )


    # --------------------------------------------------------
    # LOWERCASE
    # --------------------------------------------------------

    if any(char.islower() for char in password):

        score += 1

        lowercase_result.config(
            text="✓  Lowercase letter",
            fg=GREEN
        )

    else:

        lowercase_result.config(
            text="✗  Lowercase letter",
            fg=RED
        )


    # --------------------------------------------------------
    # NUMBER
    # --------------------------------------------------------

    if any(char.isdigit() for char in password):

        score += 1

        number_result.config(
            text="✓  Number",
            fg=GREEN
        )

    else:

        number_result.config(
            text="✗  Number",
            fg=RED
        )


    # --------------------------------------------------------
    # SPECIAL CHARACTER
    # --------------------------------------------------------

    if any(not char.isalnum() for char in password):

        score += 1

        special_result.config(
            text="✓  Special character",
            fg=GREEN
        )

    else:

        special_result.config(
            text="✗  Special character",
            fg=RED
        )


    # --------------------------------------------------------
    # STRENGTH
    # --------------------------------------------------------

    if score <= 2:

        strength = "WEAK"

        strength_result.config(
            text="Strength: WEAK",
            fg=RED
        )

    elif score == 3:

        strength = "MEDIUM"

        strength_result.config(
            text="Strength: MEDIUM",
            fg=YELLOW
        )

    else:

        strength = "STRONG"

        strength_result.config(
            text="Strength: STRONG",
            fg=GREEN
        )


    # --------------------------------------------------------
    # UPDATE SCORE
    # --------------------------------------------------------

    score_result.config(
        text=f"Score: {score} / 5"
    )


    # --------------------------------------------------------
    # UPDATE PROGRESS BAR
    # --------------------------------------------------------

    strength_bar["value"] = score


# ============================================================
# CLEAR PASSWORD
# ============================================================

def clear_password():

    password_var.set("")

    password_entry.config(show="*")

    show_button.config(text="SHOW")

    reset_results()


# ============================================================
# SHOW BUTTON
# ============================================================

show_button = tk.Button(
    root,
    text="SHOW",
    command=toggle_password,
    font=("Arial", 9, "bold"),
    bg="#2A3742",
    fg=WHITE,
    activebackground="#354653",
    activeforeground=WHITE,
    relief="flat",
    width=10
)

show_button.pack(pady=5)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = tk.Button(
    root,
    text="ANALYZE PASSWORD",
    command=analyze_password,
    font=("Arial", 11, "bold"),
    bg=CYAN,
    fg=BACKGROUND,
    activebackground="#00AACC",
    activeforeground=BACKGROUND,
    relief="flat",
    width=25,
    height=2
)

analyze_button.pack(pady=12)


# ============================================================
# CLEAR BUTTON
# ============================================================

clear_button = tk.Button(
    root,
    text="CLEAR",
    command=clear_password,
    font=("Arial", 10, "bold"),
    bg="#2A3742",
    fg=WHITE,
    activebackground="#354653",
    activeforeground=WHITE,
    relief="flat",
    width=15
)

clear_button.pack()


# ============================================================
# LIVE ANALYSIS
# ============================================================

password_var.trace_add(
    "write",
    analyze_password
)


# ============================================================
# START GUI
# ============================================================

root.mainloop()
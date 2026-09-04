import tkinter as tk
from tkinter import ttk


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("SecurePass Analyzer")
root.geometry("700x750")
root.resizable(False, False)

root.configure(bg="#101820")


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
    font=("Arial", 25, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

title.pack(pady=(25, 5))


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

subtitle.pack(pady=(0, 20))


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

password_label.pack(anchor="w", padx=80)


# ============================================================
# PASSWORD VARIABLE
# ============================================================

password_var = tk.StringVar()


# ============================================================
# PASSWORD FRAME
# ============================================================

password_frame = tk.Frame(
    root,
    bg=CARD
)

password_frame.pack(
    padx=80,
    pady=8,
    fill="x"
)


# ============================================================
# PASSWORD ENTRY
# ============================================================

password_entry = tk.Entry(
    password_frame,
    textvariable=password_var,
    font=("Arial", 14),
    show="*",
    bg=CARD,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=8,
    padx=10
)


# ============================================================
# SHOW / HIDE FUNCTION
# ============================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(show="")

        show_button.config(text="HIDE")

    else:

        password_entry.config(show="*")

        show_button.config(text="SHOW")


# ============================================================
# SHOW / HIDE BUTTON
# ============================================================

show_button = tk.Button(
    password_frame,
    text="SHOW",
    command=toggle_password,
    font=("Arial", 9, "bold"),
    bg="#2A3742",
    fg=WHITE,
    activebackground="#354653",
    activeforeground=WHITE,
    relief="flat",
    width=8
)

show_button.pack(
    side="right",
    padx=5
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

checks_title.pack(pady=(20, 8))


# ============================================================
# CHECK LABELS
# ============================================================

length_result = tk.Label(
    root,
    text="○  At least 8 characters",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

length_result.pack(anchor="w", padx=120, pady=2)


uppercase_result = tk.Label(
    root,
    text="○  Uppercase letter",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

uppercase_result.pack(anchor="w", padx=120, pady=2)


lowercase_result = tk.Label(
    root,
    text="○  Lowercase letter",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

lowercase_result.pack(anchor="w", padx=120, pady=2)


number_result = tk.Label(
    root,
    text="○  Number",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

number_result.pack(anchor="w", padx=120, pady=2)


special_result = tk.Label(
    root,
    text="○  Special character",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

special_result.pack(anchor="w", padx=120, pady=2)


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

score_result.pack(pady=(15, 3))


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

strength_result.pack(pady=3)


# ============================================================
# PROGRESS BAR STYLE
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Cyber.Horizontal.TProgressbar",
    troughcolor="#2A3742",
    background=CYAN,
    thickness=18
)


# ============================================================
# PROGRESS BAR
# ============================================================

strength_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=450,
    mode="determinate",
    maximum=5,
    style="Cyber.Horizontal.TProgressbar"
)

strength_bar.pack(pady=10)


# ============================================================
# RESET FUNCTION
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


    # --------------------------------------------------------
    # EMPTY PASSWORD
    # --------------------------------------------------------

    if password == "":

        reset_results()

        return


    score = 0


    # --------------------------------------------------------
    # LENGTH CHECK
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
    # UPPERCASE CHECK
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
    # LOWERCASE CHECK
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
    # NUMBER CHECK
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
    # SPECIAL CHARACTER CHECK
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
    # DETERMINE STRENGTH
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

    password_entry.config(
        show="*"
    )

    show_button.config(
        text="SHOW"
    )

    reset_results()


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

analyze_button.pack(pady=8)


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

clear_button.pack(pady=3)


# ============================================================
# LIVE ANALYSIS
# ============================================================

password_var.trace_add(
    "write",
    analyze_password
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
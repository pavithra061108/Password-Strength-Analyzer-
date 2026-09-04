import tkinter as tk
from tkinter import ttk


# ============================================================
# SECUREPASS ANALYZER - VERSION 3
# ============================================================


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("SecurePass Analyzer - V3")
root.geometry("760x850")
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
    font=("Arial", 26, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

title.pack(pady=(25, 5))


# ============================================================
# SUBTITLE
# ============================================================

subtitle = tk.Label(
    root,
    text="Intelligent Password Security Assessment",
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
# SHOW / HIDE PASSWORD
# ============================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(show="")

        show_button.config(text="HIDE")

    else:

        password_entry.config(show="*")

        show_button.config(text="SHOW")


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
# SCORE TITLE
# ============================================================

score_title = tk.Label(
    root,
    text="SECURITY SCORE",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

score_title.pack(pady=(20, 5))


# ============================================================
# SCORE
# ============================================================

score_result = tk.Label(
    root,
    text="0 / 100",
    font=("Arial", 28, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

score_result.pack()


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
# PROGRESS BAR
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Cyber.Horizontal.TProgressbar",
    troughcolor="#2A3742",
    background=CYAN,
    thickness=18
)


strength_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=500,
    mode="determinate",
    maximum=100,
    style="Cyber.Horizontal.TProgressbar"
)

strength_bar.pack(pady=10)


# ============================================================
# ANALYSIS TITLE
# ============================================================

analysis_title = tk.Label(
    root,
    text="SECURITY ANALYSIS",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

analysis_title.pack(pady=(15, 5))


# ============================================================
# ANALYSIS LABELS
# ============================================================

length_result = tk.Label(
    root,
    text="○  Password length",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

length_result.pack(anchor="w", padx=100, pady=2)


character_result = tk.Label(
    root,
    text="○  Character diversity",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

character_result.pack(anchor="w", padx=100, pady=2)


common_result = tk.Label(
    root,
    text="○  Common password check",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

common_result.pack(anchor="w", padx=100, pady=2)


repeat_result = tk.Label(
    root,
    text="○  Repeated character check",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

repeat_result.pack(anchor="w", padx=100, pady=2)


sequence_result = tk.Label(
    root,
    text="○  Sequential pattern check",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

sequence_result.pack(anchor="w", padx=100, pady=2)


# ============================================================
# RECOMMENDATIONS TITLE
# ============================================================

recommendation_title = tk.Label(
    root,
    text="RECOMMENDATIONS",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

recommendation_title.pack(pady=(15, 5))


# ============================================================
# RECOMMENDATIONS
# ============================================================

recommendation_result = tk.Label(
    root,
    text="Enter a password to receive security recommendations.",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY,
    justify="left",
    wraplength=550
)

recommendation_result.pack(
    padx=80,
    pady=5
)


# ============================================================
# COMMON PASSWORDS
# ============================================================

common_passwords = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "welcome",
    "letmein",
    "iloveyou",
    "abc123",
    "000000",
    "111111"
}


# ============================================================
# RESET RESULTS
# ============================================================

def reset_results():

    score_result.config(
        text="0 / 100",
        fg=WHITE
    )

    strength_result.config(
        text="Strength: --",
        fg=WHITE
    )

    strength_bar["value"] = 0

    length_result.config(
        text="○  Password length",
        fg=GRAY
    )

    character_result.config(
        text="○  Character diversity",
        fg=GRAY
    )

    common_result.config(
        text="○  Common password check",
        fg=GRAY
    )

    repeat_result.config(
        text="○  Repeated character check",
        fg=GRAY
    )

    sequence_result.config(
        text="○  Sequential pattern check",
        fg=GRAY
    )

    recommendation_result.config(
        text="Enter a password to receive security recommendations.",
        fg=GRAY
    )


# ============================================================
# CHECK SEQUENTIAL PATTERN
# ============================================================

def has_sequence(password):

    password = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "9876543210",
        "zyxwvutsrqponmlkjihgfedcba"
    ]

    for sequence in sequences:

        for i in range(len(sequence) - 2):

            part = sequence[i:i + 3]

            if part in password:

                return True

    return False


# ============================================================
# CHECK REPEATED CHARACTERS
# ============================================================

def has_repeated_characters(password):

    if len(password) < 3:

        return False

    for i in range(len(password) - 2):

        if (
            password[i]
            == password[i + 1]
            == password[i + 2]
        ):

            return True

    return False


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


    # ========================================================
    # START SCORE
    # ========================================================

    score = 0

    recommendations = []


    # ========================================================
    # LENGTH ANALYSIS
    # ========================================================

    length = len(password)

    if length >= 16:

        score += 35

        length_result.config(
            text="✓  Password length is excellent",
            fg=GREEN
        )

    elif length >= 12:

        score += 28

        length_result.config(
            text="✓  Password length is good",
            fg=GREEN
        )

    elif length >= 8:

        score += 18

        length_result.config(
            text="⚠  Password length is acceptable",
            fg=YELLOW
        )

        recommendations.append(
            "Use a longer password (12+ characters)."
        )

    else:

        score += 5

        length_result.config(
            text="✗  Password is too short",
            fg=RED
        )

        recommendations.append(
            "Use at least 12 characters."
        )


    # ========================================================
    # CHARACTER DIVERSITY
    # ========================================================

    diversity = 0

    if any(char.islower() for char in password):

        diversity += 1

    if any(char.isupper() for char in password):

        diversity += 1

    if any(char.isdigit() for char in password):

        diversity += 1

    if any(not char.isalnum() for char in password):

        diversity += 1


    if diversity == 4:

        score += 25

        character_result.config(
            text="✓  Excellent character diversity",
            fg=GREEN
        )

    elif diversity == 3:

        score += 19

        character_result.config(
            text="✓  Good character diversity",
            fg=GREEN
        )

    elif diversity == 2:

        score += 12

        character_result.config(
            text="⚠  Moderate character diversity",
            fg=YELLOW
        )

        recommendations.append(
            "Use a mix of uppercase, lowercase, numbers and symbols."
        )

    else:

        score += 5

        character_result.config(
            text="✗  Low character diversity",
            fg=RED
        )

        recommendations.append(
            "Add different types of characters."
        )


    # ========================================================
    # COMMON PASSWORD CHECK
    # ========================================================

    if password.lower() in common_passwords:

        score -= 35

        common_result.config(
            text="✗  Common password detected",
            fg=RED
        )

        recommendations.append(
            "Avoid commonly used passwords."
        )

    else:

        score += 15

        common_result.config(
            text="✓  Not in basic common-password list",
            fg=GREEN
        )


    # ========================================================
    # REPEATED CHARACTER CHECK
    # ========================================================

    if has_repeated_characters(password):

        score -= 10

        repeat_result.config(
            text="⚠  Repeated character pattern detected",
            fg=YELLOW
        )

        recommendations.append(
            "Avoid repeated character patterns."
        )

    else:

        score += 10

        repeat_result.config(
            text="✓  No obvious repeated pattern",
            fg=GREEN
        )


    # ========================================================
    # SEQUENTIAL PATTERN CHECK
    # ========================================================

    if has_sequence(password):

        score -= 15

        sequence_result.config(
            text="⚠  Sequential pattern detected",
            fg=YELLOW
        )

        recommendations.append(
            "Avoid predictable sequences such as abc or 123."
        )

    else:

        score += 15

        sequence_result.config(
            text="✓  No obvious sequential pattern",
            fg=GREEN
        )


    # ========================================================
    # CAP SCORE
    # ========================================================

    if score < 0:

        score = 0

    if score > 100:

        score = 100


    # ========================================================
    # ADD GENERAL RECOMMENDATION
    # ========================================================

    if length >= 16:

        pass

    elif length < 12:

        if "Use a longer password (12+ characters)." not in recommendations:

            recommendations.append(
                "Consider using a long passphrase."
            )


    # ========================================================
    # DETERMINE STRENGTH
    # ========================================================

    if score < 40:

        strength = "WEAK"

        strength_color = RED

    elif score < 70:

        strength = "MEDIUM"

        strength_color = YELLOW

    else:

        strength = "STRONG"

        strength_color = GREEN


    # ========================================================
    # UPDATE SCORE
    # ========================================================

    score_result.config(
        text=f"{score} / 100",
        fg=strength_color
    )


    # ========================================================
    # UPDATE STRENGTH
    # ========================================================

    strength_result.config(
        text=f"Strength: {strength}",
        fg=strength_color
    )


    # ========================================================
    # UPDATE PROGRESS BAR
    # ========================================================

    strength_bar["value"] = score


    # ========================================================
    # UPDATE RECOMMENDATIONS
    # ========================================================

    if len(recommendations) == 0:

        recommendation_result.config(
            text="✓ No major weaknesses detected by this local analyzer.",
            fg=GREEN
        )

    else:

        recommendation_text = ""

        for recommendation in recommendations:

            recommendation_text += (
                "• " + recommendation + "\n"
            )

        recommendation_result.config(
            text=recommendation_text,
            fg=YELLOW
        )


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
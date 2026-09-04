import tkinter as tk
from tkinter import ttk
import math


# ============================================================
# SECUREPASS ANALYZER - VERSION 4
# Entropy & Search-Space Analysis
# ============================================================


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("SecurePass Analyzer - V4")
root.geometry("780x920")
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

title.pack(pady=(20, 5))


# ============================================================
# SUBTITLE
# ============================================================

subtitle = tk.Label(
    root,
    text="Advanced Password Security Assessment",
    font=("Arial", 11),
    bg=BACKGROUND,
    fg=GRAY
)

subtitle.pack(pady=(0, 15))


# ============================================================
# PASSWORD LABEL
# ============================================================

password_label = tk.Label(
    root,
    text="ENTER TEST PASSWORD",
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
# SCORE TITLE
# ============================================================

score_title = tk.Label(
    root,
    text="SECURITY SCORE",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

score_title.pack(pady=(12, 3))


# ============================================================
# SCORE
# ============================================================

score_result = tk.Label(
    root,
    text="0 / 100",
    font=("Arial", 27, "bold"),
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
    font=("Arial", 17, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

strength_result.pack(pady=2)


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

strength_bar.pack(pady=8)


# ============================================================
# SECURITY ANALYSIS TITLE
# ============================================================

analysis_title = tk.Label(
    root,
    text="SECURITY ANALYSIS",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

analysis_title.pack(pady=(8, 5))


# ============================================================
# SECURITY ANALYSIS LABELS
# ============================================================

length_result = tk.Label(
    root,
    text="○  Password length",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

length_result.pack(anchor="w", padx=100, pady=1)


character_result = tk.Label(
    root,
    text="○  Character diversity",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

character_result.pack(anchor="w", padx=100, pady=1)


common_result = tk.Label(
    root,
    text="○  Common password check",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

common_result.pack(anchor="w", padx=100, pady=1)


repeat_result = tk.Label(
    root,
    text="○  Repeated character check",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

repeat_result.pack(anchor="w", padx=100, pady=1)


sequence_result = tk.Label(
    root,
    text="○  Sequential pattern check",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

sequence_result.pack(anchor="w", padx=100, pady=1)


# ============================================================
# ENTROPY TITLE
# ============================================================

entropy_title = tk.Label(
    root,
    text="ENTROPY ANALYSIS",
    font=("Arial", 14, "bold"),
    bg=BACKGROUND,
    fg=WHITE
)

entropy_title.pack(pady=(12, 5))


# ============================================================
# ENTROPY LABELS
# ============================================================

pool_result = tk.Label(
    root,
    text="Character Pool: --",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

pool_result.pack(pady=1)


entropy_result = tk.Label(
    root,
    text="Estimated Entropy: -- bits",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

entropy_result.pack(pady=1)


search_result = tk.Label(
    root,
    text="Theoretical Search Space: --",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY
)

search_result.pack(pady=1)


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

recommendation_title.pack(pady=(10, 3))


# ============================================================
# RECOMMENDATIONS
# ============================================================

recommendation_result = tk.Label(
    root,
    text="Enter a test password to receive recommendations.",
    font=("Arial", 10),
    bg=BACKGROUND,
    fg=GRAY,
    justify="left",
    wraplength=600
)

recommendation_result.pack(
    padx=70,
    pady=3
)


# ============================================================
# COMMON PASSWORD LIST
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
    "111111",
    "monkey",
    "dragon",
    "football",
    "master"
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

    pool_result.config(
        text="Character Pool: --",
        fg=GRAY
    )

    entropy_result.config(
        text="Estimated Entropy: -- bits",
        fg=GRAY
    )

    search_result.config(
        text="Theoretical Search Space: --",
        fg=GRAY
    )

    recommendation_result.config(
        text="Enter a test password to receive recommendations.",
        fg=GRAY
    )


# ============================================================
# SEQUENTIAL PATTERN CHECK
# ============================================================

def has_sequence(password):

    password = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "zyxwvutsrqponmlkjihgfedcba",
        "0123456789",
        "9876543210"
    ]

    for sequence in sequences:

        for i in range(len(sequence) - 2):

            pattern = sequence[i:i + 3]

            if pattern in password:

                return True

    return False


# ============================================================
# REPEATED CHARACTER CHECK
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
# CALCULATE CHARACTER POOL
# ============================================================

def calculate_character_pool(password):

    pool = 0

    has_lowercase = any(
        char.islower()
        for char in password
    )

    has_uppercase = any(
        char.isupper()
        for char in password
    )

    has_digit = any(
        char.isdigit()
        for char in password
    )

    has_special = any(
        not char.isalnum()
        for char in password
    )


    # Lowercase English letters
    if has_lowercase:

        pool += 26


    # Uppercase English letters
    if has_uppercase:

        pool += 26


    # Digits
    if has_digit:

        pool += 10


    # Common printable ASCII symbols
    if has_special:

        pool += 32


    return pool


# ============================================================
# CALCULATE ENTROPY
# ============================================================

def calculate_entropy(password, character_pool):

    if character_pool <= 0:

        return 0

    length = len(password)

    entropy = length * math.log2(character_pool)

    return entropy


# ============================================================
# FORMAT SEARCH SPACE
# ============================================================

def format_search_space(character_pool, length):

    if character_pool <= 0 or length <= 0:

        return "--"

    logarithm = length * math.log10(character_pool)

    if logarithm < 12:

        value = character_pool ** length

        return f"{value:,}"

    else:

        exponent = int(logarithm)

        return f"~10^{exponent}"


# ============================================================
# ANALYZE PASSWORD
# ============================================================

def analyze_password(*args):

    password = password_var.get()


    # ========================================================
    # EMPTY PASSWORD
    # ========================================================

    if password == "":

        reset_results()

        return


    # ========================================================
    # VARIABLES
    # ========================================================

    score = 0

    recommendations = []


    # ========================================================
    # LENGTH ANALYSIS
    # ========================================================

    length = len(password)


    if length >= 16:

        score += 30

        length_result.config(
            text="✓  Excellent password length",
            fg=GREEN
        )

    elif length >= 12:

        score += 25

        length_result.config(
            text="✓  Good password length",
            fg=GREEN
        )

    elif length >= 8:

        score += 15

        length_result.config(
            text="⚠  Acceptable password length",
            fg=YELLOW
        )

        recommendations.append(
            "Use 12 or more characters when possible."
        )

    else:

        score += 5

        length_result.config(
            text="✗  Password is too short",
            fg=RED
        )

        recommendations.append(
            "Use a longer password or passphrase."
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

        score += 20

        character_result.config(
            text="✓  Excellent character diversity",
            fg=GREEN
        )

    elif diversity == 3:

        score += 16

        character_result.config(
            text="✓  Good character diversity",
            fg=GREEN
        )

    elif diversity == 2:

        score += 10

        character_result.config(
            text="⚠  Moderate character diversity",
            fg=YELLOW
        )

        recommendations.append(
            "Consider using more character categories."
        )

    else:

        score += 5

        character_result.config(
            text="✗  Low character diversity",
            fg=RED
        )

        recommendations.append(
            "Use a wider variety of characters."
        )


    # ========================================================
    # COMMON PASSWORD CHECK
    # ========================================================

    if password.lower() in common_passwords:

        score -= 30

        common_result.config(
            text="✗  Common password detected",
            fg=RED
        )

        recommendations.append(
            "Avoid passwords that are commonly used."
        )

    else:

        score += 15

        common_result.config(
            text="✓  Not found in basic common-password list",
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
            "Avoid obvious repeated-character patterns."
        )

    else:

        score += 10

        repeat_result.config(
            text="✓  No obvious repeated characters",
            fg=GREEN
        )


    # ========================================================
    # SEQUENCE CHECK
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

        score += 10

        sequence_result.config(
            text="✓  No obvious sequential pattern",
            fg=GREEN
        )


    # ========================================================
    # CHARACTER POOL
    # ========================================================

    character_pool = calculate_character_pool(password)


    pool_result.config(
        text=f"Character Pool: {character_pool} possible characters",
        fg=CYAN
    )


    # ========================================================
    # ENTROPY
    # ========================================================

    entropy = calculate_entropy(
        password,
        character_pool
    )


    entropy_result.config(
        text=f"Estimated Entropy: {entropy:.2f} bits",
        fg=CYAN
    )


    # ========================================================
    # SEARCH SPACE
    # ========================================================

    search_space = format_search_space(
        character_pool,
        length
    )


    search_result.config(
        text=f"Theoretical Search Space: {search_space}",
        fg=CYAN
    )


    # ========================================================
    # ENTROPY RECOMMENDATIONS
    # ========================================================

    if entropy < 40:

        recommendations.append(
            "The theoretical entropy is relatively low."
        )

    elif entropy < 60:

        recommendations.append(
            "A longer password could increase the theoretical search space."
        )

    else:

        recommendations.append(
            "The theoretical entropy is relatively high."
        )


    # ========================================================
    # FINAL SCORE LIMIT
    # ========================================================

    if score < 0:

        score = 0


    if score > 100:

        score = 100


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
    # DISPLAY RECOMMENDATIONS
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

analyze_button.pack(pady=7)


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

clear_button.pack(pady=2)


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
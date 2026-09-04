import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

import math
import secrets
import string
from datetime import datetime


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "SECUREPASS ANALYZER V7"

BG = "#0d1117"
CARD = "#161b22"
CARD2 = "#21262d"

TEXT = "#ffffff"
MUTED = "#8b949e"

ACCENT = "#58a6ff"
PASS_COLOR = "#3fb950"
WARNING_COLOR = "#d29922"
FAIL_COLOR = "#f85149"
PURPLE = "#bc8cff"


# ============================================================
# COMMON PASSWORDS
# ============================================================

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "letmein",
    "welcome",
    "abc123",
    "iloveyou",
    "monkey",
    "dragon",
    "football"
}


# ============================================================
# CREATE MAIN WINDOW FIRST
# ============================================================

root = tk.Tk()

root.title(APP_NAME)

root.geometry("1100x1000")

root.configure(bg=BG)

root.resizable(False, False)


# ============================================================
# VARIABLES
# ============================================================

password_var = tk.StringVar()

length_var = tk.StringVar(value="16")

lowercase_var = tk.BooleanVar(value=True)

uppercase_var = tk.BooleanVar(value=True)

numbers_var = tk.BooleanVar(value=True)

symbols_var = tk.BooleanVar(value=True)

report_data = None

history = []

show_password = False


# ============================================================
# PASSWORD ANALYSIS FUNCTIONS
# ============================================================

def calculate_character_pool(password):

    pool = 0

    if any(c.islower() for c in password):
        pool += 26

    if any(c.isupper() for c in password):
        pool += 26

    if any(c.isdigit() for c in password):
        pool += 10

    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)

    return pool


def calculate_entropy(password, pool):

    if not password or pool == 0:
        return 0

    return len(password) * math.log2(pool)


def calculate_search_space(pool, length):

    if pool == 0 or length == 0:
        return 0

    return pool ** length


def format_search_space(number):

    if number == 0:
        return "0"

    if number < 1_000_000:
        return f"{number:,}"

    exponent = math.log10(number)

    return f"~10^{exponent:.1f}"


# ============================================================
# SECURITY CHECK 1 - LENGTH
# ============================================================

def check_length(password):

    length = len(password)

    if length >= 16:

        return {
            "status": "PASS",
            "details": f"Excellent length ({length} characters)",
            "points": 20
        }

    elif length >= 12:

        return {
            "status": "PASS",
            "details": f"Good length ({length} characters)",
            "points": 17
        }

    elif length >= 8:

        return {
            "status": "WARNING",
            "details": f"Acceptable length ({length} characters)",
            "points": 10
        }

    else:

        return {
            "status": "FAIL",
            "details": f"Too short ({length} characters)",
            "points": 0
        }


# ============================================================
# SECURITY CHECK 2 - CHARACTER DIVERSITY
# ============================================================

def check_diversity(password):

    lower = any(c.islower() for c in password)

    upper = any(c.isupper() for c in password)

    digit = any(c.isdigit() for c in password)

    special = any(not c.isalnum() for c in password)

    types = sum([
        lower,
        upper,
        digit,
        special
    ])

    if types == 4:

        return {
            "status": "PASS",
            "details": "All four major character types detected",
            "points": 20
        }

    elif types == 3:

        return {
            "status": "PASS",
            "details": "Three character types detected",
            "points": 15
        }

    elif types == 2:

        return {
            "status": "WARNING",
            "details": "Only two character types detected",
            "points": 10
        }

    else:

        return {
            "status": "FAIL",
            "details": "Only one character type detected",
            "points": 5
        }


# ============================================================
# SECURITY CHECK 3 - COMMON PASSWORD
# ============================================================

def check_common(password):

    if password.lower() in COMMON_PASSWORDS:

        return {
            "status": "FAIL",
            "details": "Found in built-in common-password list",
            "points": 0
        }

    return {
        "status": "PASS",
        "details": "Not found in built-in common-password list",
        "points": 15
    }


# ============================================================
# SECURITY CHECK 4 - REPEATED CHARACTERS
# ============================================================

def check_repeated(password):

    for i in range(len(password) - 2):

        if (
            password[i] == password[i + 1]
            and password[i] == password[i + 2]
        ):

            return {
                "status": "WARNING",
                "details": "Three or more repeated characters detected",
                "points": 0
            }

    return {
        "status": "PASS",
        "details": "No obvious repeated-character pattern",
        "points": 10
    }


# ============================================================
# SECURITY CHECK 5 - SEQUENCES
# ============================================================

def check_sequence(password):

    value = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "zyxwvutsrqponmlkjihgfedcba",
        "0123456789",
        "9876543210"
    ]

    for sequence in sequences:

        for i in range(len(sequence) - 2):

            pattern = sequence[i:i + 3]

            if pattern in value:

                return {
                    "status": "WARNING",
                    "details": f"Sequential pattern detected: {pattern}",
                    "points": 0
                }

    return {
        "status": "PASS",
        "details": "No obvious sequential pattern",
        "points": 10
    }


# ============================================================
# SECURITY CHECK 6 - PREDICTABLE WORDS
# ============================================================

def check_predictable_words(password):

    value = password.lower()

    words = [
        "password",
        "admin",
        "welcome",
        "login",
        "user",
        "qwerty"
    ]

    for word in words:

        if word in value:

            return {
                "status": "WARNING",
                "details": f"Predictable word detected: {word}",
                "points": 0
            }

    return {
        "status": "PASS",
        "details": "No obvious predictable security word",
        "points": 5
    }


# ============================================================
# SECURITY CHECK 7 - UNIQUE CHARACTERS
# ============================================================

def check_unique_characters(password):

    if not password:

        return {
            "status": "FAIL",
            "details": "No characters available",
            "points": 0
        }

    unique = len(set(password))

    total = len(password)

    ratio = unique / total

    if ratio >= 0.75:

        return {
            "status": "PASS",
            "details": f"Good character variety ({unique}/{total} unique)",
            "points": 10
        }

    elif ratio >= 0.50:

        return {
            "status": "WARNING",
            "details": f"Moderate character variety ({unique}/{total} unique)",
            "points": 5
        }

    else:

        return {
            "status": "WARNING",
            "details": f"Low character variety ({unique}/{total} unique)",
            "points": 0
        }


# ============================================================
# COMPLETE PASSWORD ANALYSIS
# ============================================================

def analyze_password(password):

    if not password:
        return None

    results = {

        "length": check_length(password),

        "diversity": check_diversity(password),

        "common": check_common(password),

        "repeated": check_repeated(password),

        "sequence": check_sequence(password),

        "predictable": check_predictable_words(password),

        "unique": check_unique_characters(password)
    }

    score = sum(
        item["points"]
        for item in results.values()
    )

    score = min(round(score), 100)

    # --------------------------------------------------------
    # STRENGTH AND GRADE
    # --------------------------------------------------------

    if score >= 90:

        strength = "VERY STRONG"
        grade = "A+"

    elif score >= 80:

        strength = "STRONG"
        grade = "A"

    elif score >= 70:

        strength = "GOOD"
        grade = "B"

    elif score >= 55:

        strength = "MODERATE"
        grade = "C"

    elif score >= 40:

        strength = "WEAK"
        grade = "D"

    else:

        strength = "VERY WEAK"
        grade = "F"

    # --------------------------------------------------------
    # ENTROPY
    # --------------------------------------------------------

    pool = calculate_character_pool(password)

    entropy = calculate_entropy(
        password,
        pool
    )

    search_space = calculate_search_space(
        pool,
        len(password)
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = []

    if results["length"]["status"] != "PASS":

        recommendations.append(
            "Use at least 12–16 characters."
        )

    if results["diversity"]["status"] != "PASS":

        recommendations.append(
            "Use uppercase, lowercase, numbers and symbols."
        )

    if results["common"]["status"] == "FAIL":

        recommendations.append(
            "Avoid commonly used passwords."
        )

    if results["repeated"]["status"] != "PASS":

        recommendations.append(
            "Avoid long repeated-character patterns."
        )

    if results["sequence"]["status"] != "PASS":

        recommendations.append(
            "Avoid predictable sequences such as abc or 123."
        )

    if results["predictable"]["status"] != "PASS":

        recommendations.append(
            "Avoid predictable words such as admin or password."
        )

    if results["unique"]["status"] != "PASS":

        recommendations.append(
            "Increase character variety."
        )

    if not recommendations:

        recommendations.append(
            "Excellent! No major weaknesses were detected."
        )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {

        "score": score,

        "strength": strength,

        "grade": grade,

        "results": results,

        "pool": pool,

        "entropy": entropy,

        "search_space": search_space,

        "recommendations": recommendations,

        "timestamp": timestamp
    }


# ============================================================
# UPDATE HISTORY
# ============================================================

def update_history():

    history_list.delete(
        0,
        tk.END
    )

    for item in reversed(history):

        history_list.insert(

            tk.END,

            f"{item['time']}\n"
            f"Score: {item['score']} | "
            f"Grade: {item['grade']} | "
            f"{item['strength']}\n"
        )


# ============================================================
# UPDATE DASHBOARD
# ============================================================

def update_dashboard(report):

    score_value.config(
        text=f"{report['score']} / 100"
    )

    grade_value.config(
        text=report["grade"]
    )

    strength_value.config(
        text=report["strength"]
    )

    meter["value"] = report["score"]

    pool_value.config(
        text=str(report["pool"])
    )

    entropy_value.config(
        text=f"{report['entropy']:.2f} bits"
    )

    search_value.config(
        text=format_search_space(
            report["search_space"]
        )
    )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    report_text.config(
        state="normal"
    )

    report_text.delete(
        "1.0",
        tk.END
    )

    report_text.insert(
        tk.END,
        "SECURITY CHECKS\n\n",
        "heading"
    )

    names = {

        "length": "Password Length",

        "diversity": "Character Diversity",

        "common": "Common Password",

        "repeated": "Repeated Patterns",

        "sequence": "Sequential Patterns",

        "predictable": "Predictable Words",

        "unique": "Character Variety"
    }

    for key, result in report["results"].items():

        status = result["status"]

        if status == "PASS":

            tag = "pass"

        elif status == "WARNING":

            tag = "warning"

        else:

            tag = "fail"

        report_text.insert(
            tk.END,
            f"{names[key]:25} "
        )

        report_text.insert(
            tk.END,
            f"{status:10}",
            tag
        )

        report_text.insert(
            tk.END,
            f"{result['details']}\n"
        )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    report_text.insert(
        tk.END,
        "\nRECOMMENDATIONS\n\n",
        "heading"
    )

    for recommendation in report["recommendations"]:

        report_text.insert(
            tk.END,
            f"• {recommendation}\n"
        )

    report_text.insert(
        tk.END,
        f"\nAnalysis Time: {report['timestamp']}\n",
        "details"
    )

    report_text.insert(
        tk.END,
        "\nPrivacy: Password is not stored in history or report.",
        "details"
    )

    report_text.config(
        state="disabled"
    )

    update_history()


# ============================================================
# ANALYZE BUTTON FUNCTION
# ============================================================

def analyze():

    global report_data

    password = password_var.get()

    if not password:

        messagebox.showwarning(
            "No Password",
            "Enter or generate a test password."
        )

        return

    report_data = analyze_password(
        password
    )

    # IMPORTANT:
    # Only analysis information is stored.
    # The actual password is NOT stored.

    history.append({

        "time": report_data["timestamp"],

        "score": report_data["score"],

        "grade": report_data["grade"],

        "strength": report_data["strength"]
    })

    update_dashboard(
        report_data
    )


# ============================================================
# PASSWORD GENERATOR
# ============================================================

def generate_password():

    try:

        length = int(
            length_var.get()
        )

    except ValueError:

        messagebox.showwarning(
            "Invalid Length",
            "Enter a number between 8 and 64."
        )

        return

    if length < 8 or length > 64:

        messagebox.showwarning(
            "Invalid Length",
            "Password length must be between 8 and 64."
        )

        return

    characters = ""

    required = []

    # --------------------------------------------------------
    # LOWERCASE
    # --------------------------------------------------------

    if lowercase_var.get():

        characters += string.ascii_lowercase

        required.append(
            secrets.choice(
                string.ascii_lowercase
            )
        )

    # --------------------------------------------------------
    # UPPERCASE
    # --------------------------------------------------------

    if uppercase_var.get():

        characters += string.ascii_uppercase

        required.append(
            secrets.choice(
                string.ascii_uppercase
            )
        )

    # --------------------------------------------------------
    # NUMBERS
    # --------------------------------------------------------

    if numbers_var.get():

        characters += string.digits

        required.append(
            secrets.choice(
                string.digits
            )
        )

    # --------------------------------------------------------
    # SYMBOLS
    # --------------------------------------------------------

    if symbols_var.get():

        characters += string.punctuation

        required.append(
            secrets.choice(
                string.punctuation
            )
        )

    if not characters:

        messagebox.showwarning(
            "Character Types",
            "Select at least one character type."
        )

        return

    if len(required) > length:

        messagebox.showwarning(
            "Length Error",
            "Increase the password length."
        )

        return

    generated = required.copy()

    # Fill remaining characters

    for _ in range(
        length - len(required)
    ):

        generated.append(
            secrets.choice(
                characters
            )
        )

    # Secure shuffle

    shuffled = []

    while generated:

        index = secrets.randbelow(
            len(generated)
        )

        shuffled.append(
            generated.pop(index)
        )

    final_password = "".join(
        shuffled
    )

    password_var.set(
        final_password
    )

    analyze()


# ============================================================
# COPY PASSWORD
# ============================================================

def copy_password():

    password = password_var.get()

    if not password:

        messagebox.showwarning(
            "Nothing to Copy",
            "Generate or enter a test password first."
        )

        return

    root.clipboard_clear()

    root.clipboard_append(
        password
    )

    root.update()

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

def toggle_password():

    global show_password

    show_password = not show_password

    if show_password:

        password_entry.config(
            show=""
        )

        show_button.config(
            text="HIDE"
        )

    else:

        password_entry.config(
            show="•"
        )

        show_button.config(
            text="SHOW"
        )


# ============================================================
# CLEAR / NEW ANALYSIS
# ============================================================

def clear_analysis():

    global report_data

    report_data = None

    password_var.set("")

    score_value.config(
        text="--"
    )

    grade_value.config(
        text="--"
    )

    strength_value.config(
        text="WAITING"
    )

    meter["value"] = 0

    pool_value.config(
        text="--"
    )

    entropy_value.config(
        text="--"
    )

    search_value.config(
        text="--"
    )

    report_text.config(
        state="normal"
    )

    report_text.delete(
        "1.0",
        tk.END
    )

    report_text.insert(
        tk.END,
        "Enter or generate a test password and click ANALYZE."
    )

    report_text.config(
        state="disabled"
    )


# ============================================================
# EXPORT REPORT
# ============================================================

def export_report():

    if report_data is None:

        messagebox.showwarning(
            "No Report",
            "Analyze a password before exporting."
        )

        return

    path = filedialog.asksaveasfilename(

        defaultextension=".txt",

        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ],

        title="Export Security Report"
    )

    if not path:

        return

    report = report_data

    names = {

        "length": "Password Length",

        "diversity": "Character Diversity",

        "common": "Common Password",

        "repeated": "Repeated Patterns",

        "sequence": "Sequential Patterns",

        "predictable": "Predictable Words",

        "unique": "Character Variety"
    }

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "========================================\n"
        )

        file.write(
            "       SECUREPASS ANALYZER V7\n"
        )

        file.write(
            "       SECURITY ASSESSMENT REPORT\n"
        )

        file.write(
            "========================================\n\n"
        )

        file.write(
            "PRIVACY NOTICE\n"
        )

        file.write(
            "The analyzed password is NOT included "
            "in this report.\n\n"
        )

        file.write(
            f"Score    : {report['score']} / 100\n"
        )

        file.write(
            f"Grade    : {report['grade']}\n"
        )

        file.write(
            f"Strength : {report['strength']}\n"
        )

        file.write(
            f"Time     : {report['timestamp']}\n\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        file.write(
            "SECURITY CHECKS\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        for key, result in report["results"].items():

            file.write(
                f"{names[key]}: "
                f"{result['status']} - "
                f"{result['details']}\n"
            )

        file.write("\n")

        file.write(
            "----------------------------------------\n"
        )

        file.write(
            "ENTROPY INFORMATION\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        file.write(
            f"Character Pool : {report['pool']}\n"
        )

        file.write(
            f"Entropy        : "
            f"{report['entropy']:.2f} bits\n"
        )

        file.write(
            f"Search Space   : "
            f"{format_search_space(report['search_space'])}\n"
        )

        file.write("\n")

        file.write(
            "----------------------------------------\n"
        )

        file.write(
            "RECOMMENDATIONS\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        for recommendation in report["recommendations"]:

            file.write(
                f"- {recommendation}\n"
            )

        file.write("\n")

        file.write(
            "This application performs a local "
            "heuristic security assessment.\n"
        )

        file.write(
            "Entropy and search-space values are "
            "theoretical estimates.\n"
        )

    messagebox.showinfo(
        "Export Complete",
        "Security report exported successfully."
    )


# ============================================================
# BUILD GUI
# ============================================================

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

title = tk.Label(

    root,

    text="🔐 SECUREPASS ANALYZER",

    font=("Segoe UI", 27, "bold"),

    fg=TEXT,

    bg=BG
)

title.pack(
    pady=(15, 0)
)


subtitle = tk.Label(

    root,

    text="V7  •  ADVANCED PASSWORD SECURITY DASHBOARD",

    font=("Segoe UI", 10),

    fg=MUTED,

    bg=BG
)

subtitle.pack(
    pady=(0, 8)
)


privacy_label = tk.Label(

    root,

    text="🔒 LOCAL ANALYSIS  •  PASSWORDS ARE NOT SAVED",

    font=("Segoe UI", 9, "bold"),

    fg=PASS_COLOR,

    bg=BG
)

privacy_label.pack(
    pady=(0, 8)
)


# ============================================================
# PASSWORD INPUT CARD
# ============================================================

input_card = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=12
)

input_card.pack(

    padx=25,

    fill="x"
)


tk.Label(

    input_card,

    text="PASSWORD TO ANALYZE",

    font=("Segoe UI", 10, "bold"),

    fg=MUTED,

    bg=CARD

).pack(
    anchor="w"
)


password_entry = tk.Entry(

    input_card,

    textvariable=password_var,

    show="•",

    font=("Segoe UI", 14),

    bg=CARD2,

    fg=TEXT,

    insertbackground=TEXT,

    relief="flat"
)

password_entry.pack(

    side="left",

    fill="x",

    expand=True,

    ipady=8,

    pady=(5, 0)
)


show_button = tk.Button(

    input_card,

    text="SHOW",

    command=toggle_password,

    bg=ACCENT,

    fg="white",

    relief="flat",

    font=("Segoe UI", 9, "bold"),

    padx=15,

    pady=7,

    cursor="hand2"
)

show_button.pack(

    side="right",

    padx=(10, 0),

    pady=(5, 0)
)


# ============================================================
# GENERATOR CARD
# ============================================================

generator_card = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=10
)

generator_card.pack(

    padx=25,

    pady=8,

    fill="x"
)


tk.Label(

    generator_card,

    text="⚡ SECURE PASSWORD GENERATOR",

    font=("Segoe UI", 11, "bold"),

    fg=TEXT,

    bg=CARD

).grid(

    row=0,

    column=0,

    columnspan=8,

    sticky="w",

    pady=(0, 7)
)


tk.Label(

    generator_card,

    text="Length:",

    font=("Segoe UI", 9, "bold"),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=0,

    padx=(0, 5)
)


length_entry = tk.Entry(

    generator_card,

    textvariable=length_var,

    width=5,

    justify="center",

    font=("Segoe UI", 10),

    bg=CARD2,

    fg=TEXT,

    insertbackground=TEXT,

    relief="flat"
)

length_entry.grid(

    row=1,

    column=1,

    padx=5
)


tk.Checkbutton(

    generator_card,

    text="Lowercase",

    variable=lowercase_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT

).grid(

    row=1,

    column=2,

    padx=4
)


tk.Checkbutton(

    generator_card,

    text="Uppercase",

    variable=uppercase_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT

).grid(

    row=1,

    column=3,

    padx=4
)


tk.Checkbutton(

    generator_card,

    text="Numbers",

    variable=numbers_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT

).grid(

    row=1,

    column=4,

    padx=4
)


tk.Checkbutton(

    generator_card,

    text="Symbols",

    variable=symbols_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT

).grid(

    row=1,

    column=5,

    padx=4
)


tk.Button(

    generator_card,

    text="⚡ GENERATE",

    command=generate_password,

    bg=ACCENT,

    fg="white",

    relief="flat",

    font=("Segoe UI", 9, "bold"),

    padx=15,

    pady=7,

    cursor="hand2"

).grid(

    row=1,

    column=6,

    padx=8
)


tk.Button(

    generator_card,

    text="📋 COPY",

    command=copy_password,

    bg=CARD2,

    fg=TEXT,

    relief="flat",

    font=("Segoe UI", 9, "bold"),

    padx=15,

    pady=7,

    cursor="hand2"

).grid(

    row=1,

    column=7,

    padx=4
)


# ============================================================
# ACTION BUTTONS
# ============================================================

actions = tk.Frame(

    root,

    bg=BG
)

actions.pack(
    pady=7
)


tk.Button(

    actions,

    text="🔍 ANALYZE",

    command=analyze,

    bg=ACCENT,

    fg="white",

    relief="flat",

    font=("Segoe UI", 10, "bold"),

    padx=25,

    pady=8,

    cursor="hand2"

).pack(

    side="left",

    padx=5
)


tk.Button(

    actions,

    text="📄 EXPORT REPORT",

    command=export_report,

    bg=CARD2,

    fg=TEXT,

    relief="flat",

    font=("Segoe UI", 10, "bold"),

    padx=25,

    pady=8,

    cursor="hand2"

).pack(

    side="left",

    padx=5
)


tk.Button(

    actions,

    text="↻ NEW ANALYSIS",

    command=clear_analysis,

    bg=CARD2,

    fg=TEXT,

    relief="flat",

    font=("Segoe UI", 10, "bold"),

    padx=25,

    pady=8,

    cursor="hand2"

).pack(

    side="left",

    padx=5
)


# ============================================================
# SCORE DASHBOARD
# ============================================================

dashboard = tk.Frame(

    root,

    bg=BG
)

dashboard.pack(

    padx=25,

    fill="x"
)


# SCORE CARD

score_card = tk.Frame(

    dashboard,

    bg=CARD,

    padx=30,

    pady=8
)

score_card.grid(

    row=0,

    column=0,

    sticky="nsew",

    padx=(0, 5)
)


tk.Label(

    score_card,

    text="SECURITY SCORE",

    font=("Segoe UI", 9, "bold"),

    fg=MUTED,

    bg=CARD

).pack()


score_value = tk.Label(

    score_card,

    text="--",

    font=("Segoe UI", 24, "bold"),

    fg=TEXT,

    bg=CARD
)

score_value.pack()


# GRADE CARD

grade_card = tk.Frame(

    dashboard,

    bg=CARD,

    padx=45,

    pady=8
)

grade_card.grid(

    row=0,

    column=1,

    sticky="nsew",

    padx=5
)


tk.Label(

    grade_card,

    text="GRADE",

    font=("Segoe UI", 9, "bold"),

    fg=MUTED,

    bg=CARD

).pack()


grade_value = tk.Label(

    grade_card,

    text="--",

    font=("Segoe UI", 24, "bold"),

    fg=PURPLE,

    bg=CARD
)

grade_value.pack()


# STRENGTH CARD

strength_card = tk.Frame(

    dashboard,

    bg=CARD,

    padx=25,

    pady=8
)

strength_card.grid(

    row=0,

    column=2,

    sticky="nsew",

    padx=(5, 0)
)


tk.Label(

    strength_card,

    text="STRENGTH",

    font=("Segoe UI", 9, "bold"),

    fg=MUTED,

    bg=CARD

).pack()


strength_value = tk.Label(

    strength_card,

    text="WAITING",

    font=("Segoe UI", 14, "bold"),

    fg=ACCENT,

    bg=CARD
)

strength_value.pack()


# ============================================================
# PROGRESS BAR
# ============================================================

meter = ttk.Progressbar(

    root,

    orient="horizontal",

    length=800,

    maximum=100,

    mode="determinate"
)

meter.pack(
    pady=7
)


# ============================================================
# REPORT + HISTORY
# ============================================================

content_frame = tk.Frame(

    root,

    bg=BG
)

content_frame.pack(

    padx=25,

    fill="both",

    expand=True
)


# ------------------------------------------------------------
# REPORT CARD
# ------------------------------------------------------------

report_card = tk.Frame(

    content_frame,

    bg=CARD
)

report_card.grid(

    row=0,

    column=0,

    sticky="nsew",

    padx=(0, 5)
)


tk.Label(

    report_card,

    text="🛡 SECURITY REPORT",

    font=("Segoe UI", 10, "bold"),

    fg=TEXT,

    bg=CARD

).pack(

    anchor="w",

    padx=12,

    pady=7
)


report_text = ScrolledText(

    report_card,

    width=67,

    height=13,

    font=("Consolas", 9),

    bg=CARD2,

    fg=TEXT,

    insertbackground=TEXT,

    relief="flat",

    wrap="word"
)

report_text.pack(

    padx=12,

    pady=(0, 10),

    fill="both",

    expand=True
)


# REPORT COLORS

report_text.tag_config(

    "heading",

    foreground=ACCENT,

    font=("Consolas", 10, "bold")
)


report_text.tag_config(

    "pass",

    foreground=PASS_COLOR,

    font=("Consolas", 9, "bold")
)


report_text.tag_config(

    "warning",

    foreground=WARNING_COLOR,

    font=("Consolas", 9, "bold")
)


report_text.tag_config(

    "fail",

    foreground=FAIL_COLOR,

    font=("Consolas", 9, "bold")
)


report_text.tag_config(

    "details",

    foreground=MUTED
)


# ------------------------------------------------------------
# HISTORY CARD
# ------------------------------------------------------------

history_card = tk.Frame(

    content_frame,

    bg=CARD,

    width=300
)

history_card.grid(

    row=0,

    column=1,

    sticky="nsew",

    padx=(5, 0)
)


tk.Label(

    history_card,

    text="🕒 ANALYSIS HISTORY",

    font=("Segoe UI", 10, "bold"),

    fg=TEXT,

    bg=CARD

).pack(

    anchor="w",

    padx=12,

    pady=7
)


history_list = tk.Listbox(

    history_card,

    height=13,

    bg=CARD2,

    fg=TEXT,

    selectbackground=ACCENT,

    relief="flat",

    font=("Consolas", 8)
)

history_list.pack(

    padx=12,

    pady=(0, 10),

    fill="both",

    expand=True
)


# ============================================================
# ENTROPY CARD
# ============================================================

entropy_card = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=8
)

entropy_card.pack(

    padx=25,

    pady=8,

    fill="x"
)


tk.Label(

    entropy_card,

    text="📊 ENTROPY & SEARCH SPACE",

    font=("Segoe UI", 10, "bold"),

    fg=TEXT,

    bg=CARD

).pack(
    anchor="w"
)


stats = tk.Frame(

    entropy_card,

    bg=CARD
)

stats.pack(
    pady=4
)


# CHARACTER POOL

pool_value = tk.Label(

    stats,

    text="--",

    font=("Segoe UI", 12, "bold"),

    fg=ACCENT,

    bg=CARD
)

pool_value.grid(

    row=0,

    column=0,

    padx=65
)


tk.Label(

    stats,

    text="Character Pool",

    font=("Segoe UI", 8),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=0,

    padx=65
)


# ENTROPY

entropy_value = tk.Label(

    stats,

    text="--",

    font=("Segoe UI", 12, "bold"),

    fg=ACCENT,

    bg=CARD
)

entropy_value.grid(

    row=0,

    column=1,

    padx=65
)


tk.Label(

    stats,

    text="Entropy",

    font=("Segoe UI", 8),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=1,

    padx=65
)


# SEARCH SPACE

search_value = tk.Label(

    stats,

    text="--",

    font=("Segoe UI", 12, "bold"),

    fg=ACCENT,

    bg=CARD
)

search_value.grid(

    row=0,

    column=2,

    padx=65
)


tk.Label(

    stats,

    text="Theoretical Search Space",

    font=("Segoe UI", 8),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=2,

    padx=65
)


# ============================================================
# SECURITY TIP
# ============================================================

tk.Label(

    root,

    text=(
        "💡 TIP: Use long, unique passwords or passphrases "
        "and avoid reusing passwords."
    ),

    font=("Segoe UI", 9),

    fg=MUTED,

    bg=BG

).pack(

    pady=(0, 8)
)


# ============================================================
# INITIAL REPORT
# ============================================================

report_text.insert(

    tk.END,

    "Enter or generate a test password and click ANALYZE."
)

report_text.config(
    state="disabled"
)


# ============================================================
# ENTER KEY
# ============================================================

password_entry.bind(

    "<Return>",

    lambda event: analyze()
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

import math
import secrets
import string
from datetime import datetime


# ============================================================
# SECUREPASS ANALYZER V6
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

    special_characters = string.punctuation

    if any(c in special_characters for c in password):
        pool += len(special_characters)

    return pool


def calculate_entropy(password, character_pool):

    if not password or character_pool == 0:
        return 0

    return len(password) * math.log2(character_pool)


def calculate_search_space(character_pool, length):

    if character_pool == 0 or length == 0:
        return 0

    return character_pool ** length


def format_search_space(number):

    if number == 0:
        return "0"

    if number < 1_000_000:
        return f"{number:,}"

    exponent = math.log10(number)

    return f"~10^{exponent:.1f}"


# ============================================================
# INDIVIDUAL SECURITY CHECKS
# ============================================================

def check_length(password):

    length = len(password)

    if length >= 16:

        return {
            "status": "PASS",
            "details": f"Excellent length ({length} characters)",
            "points": 25
        }

    elif length >= 12:

        return {
            "status": "PASS",
            "details": f"Good length ({length} characters)",
            "points": 20
        }

    elif length >= 8:

        return {
            "status": "WARNING",
            "details": f"Acceptable length ({length} characters)",
            "points": 12
        }

    else:

        return {
            "status": "FAIL",
            "details": f"Too short ({length} characters)",
            "points": 0
        }


def check_diversity(password):

    lower = any(c.islower() for c in password)

    upper = any(c.isupper() for c in password)

    digit = any(c.isdigit() for c in password)

    special = any(not c.isalnum() for c in password)

    types = sum([lower, upper, digit, special])

    if types == 4:

        return {
            "status": "PASS",
            "details": "Uses lowercase, uppercase, numbers and symbols",
            "points": 25
        }

    elif types == 3:

        return {
            "status": "PASS",
            "details": "Uses three different character types",
            "points": 19
        }

    elif types == 2:

        return {
            "status": "WARNING",
            "details": "Uses only two character types",
            "points": 12
        }

    else:

        return {
            "status": "FAIL",
            "details": "Uses only one character type",
            "points": 5
        }


def check_common_password(password):

    if password.lower() in COMMON_PASSWORDS:

        return {
            "status": "FAIL",
            "details": "Password appears in common-password list",
            "points": 0
        }

    return {
        "status": "PASS",
        "details": "Not found in built-in common-password list",
        "points": 15
    }


def check_repeated(password):

    for i in range(len(password) - 2):

        if (
            password[i] == password[i + 1]
            and password[i] == password[i + 2]
        ):

            return {
                "status": "WARNING",
                "details": "Repeated characters detected",
                "points": 0
            }

    return {
        "status": "PASS",
        "details": "No obvious repeated-character pattern",
        "points": 10
    }


def check_sequence(password):

    password_lower = password.lower()

    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "zyxwvutsrqponmlkjihgfedcba",
        "0123456789",
        "9876543210"
    ]

    for sequence in sequences:

        for i in range(len(sequence) - 2):

            pattern = sequence[i:i + 3]

            if pattern in password_lower:

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


def check_personal_patterns(password):

    lower_password = password.lower()

    suspicious_words = [
        "admin",
        "user",
        "login",
        "welcome",
        "password"
    ]

    for word in suspicious_words:

        if word in lower_password:

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
# SCORE
# ============================================================

def calculate_score(results):

    total_points = sum(
        result["points"]
        for result in results.values()
    )

    maximum_points = 100

    score = round(
        (total_points / maximum_points) * 100
    )

    return min(score, 100)


def get_strength(score):

    if score >= 85:
        return "VERY STRONG"

    elif score >= 70:
        return "STRONG"

    elif score >= 50:
        return "MODERATE"

    elif score >= 30:
        return "WEAK"

    else:
        return "VERY WEAK"


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(results, password):

    recommendations = []

    if results["length"]["status"] != "PASS":

        recommendations.append(
            "Use a longer password or passphrase."
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
            "Avoid repeating the same character multiple times."
        )

    if results["sequence"]["status"] != "PASS":

        recommendations.append(
            "Avoid predictable sequences such as abc or 123."
        )

    if results["personal"]["status"] != "PASS":

        recommendations.append(
            "Avoid predictable words such as admin or password."
        )

    if len(password) < 16:

        recommendations.append(
            "Consider using a longer passphrase."
        )

    if not recommendations:

        recommendations.append(
            "Excellent! No major weaknesses were detected."
        )

    return recommendations


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def analyze_password(password):

    if not password:

        return None

    results = {

        "length": check_length(password),

        "diversity": check_diversity(password),

        "common": check_common_password(password),

        "repeated": check_repeated(password),

        "sequence": check_sequence(password),

        "personal": check_personal_patterns(password)
    }

    score = calculate_score(results)

    strength = get_strength(score)

    character_pool = calculate_character_pool(password)

    entropy = calculate_entropy(
        password,
        character_pool
    )

    search_space = calculate_search_space(
        character_pool,
        len(password)
    )

    recommendations = generate_recommendations(
        results,
        password
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {

        "score": score,

        "strength": strength,

        "results": results,

        "character_pool": character_pool,

        "entropy": entropy,

        "search_space": search_space,

        "recommendations": recommendations,

        "timestamp": timestamp
    }


# ============================================================
# SECURE PASSWORD GENERATOR
# ============================================================

def generate_password():

    try:

        length = int(length_var.get())

    except ValueError:

        messagebox.showwarning(
            "Invalid Length",
            "Please enter a valid password length."
        )

        return

    if length < 8 or length > 64:

        messagebox.showwarning(
            "Invalid Length",
            "Password length must be between 8 and 64."
        )

        return

    characters = ""

    required_characters = []

    if lowercase_var.get():

        characters += string.ascii_lowercase

        required_characters.append(
            secrets.choice(string.ascii_lowercase)
        )

    if uppercase_var.get():

        characters += string.ascii_uppercase

        required_characters.append(
            secrets.choice(string.ascii_uppercase)
        )

    if numbers_var.get():

        characters += string.digits

        required_characters.append(
            secrets.choice(string.digits)
        )

    if symbols_var.get():

        characters += string.punctuation

        required_characters.append(
            secrets.choice(string.punctuation)
        )

    if not characters:

        messagebox.showwarning(
            "No Character Types",
            "Select at least one character type."
        )

        return

    if len(required_characters) > length:

        messagebox.showwarning(
            "Length Too Small",
            "Increase the password length."
        )

        return

    remaining_length = length - len(required_characters)

    password_characters = required_characters.copy()

    for _ in range(remaining_length):

        password_characters.append(
            secrets.choice(characters)
        )

    # Secure shuffle using secrets
    shuffled = []

    while password_characters:

        index = secrets.randbelow(
            len(password_characters)
        )

        shuffled.append(
            password_characters.pop(index)
        )

    generated = "".join(shuffled)

    password_var.set(generated)

    analyze()


def copy_password():

    password = password_var.get()

    if not password:

        messagebox.showwarning(
            "Nothing to Copy",
            "Generate or enter a test password first."
        )

        return

    root.clipboard_clear()

    root.clipboard_append(password)

    root.update()

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title(
    "SECUREPASS ANALYZER V6"
)

root.geometry(
    "1000x950"
)

root.configure(
    bg="#10141c"
)

root.resizable(
    False,
    False
)


# ============================================================
# COLORS
# ============================================================

BG = "#10141c"

CARD = "#181e28"

CARD2 = "#202734"

TEXT = "#ffffff"

MUTED = "#aab2c0"

ACCENT = "#5dade2"

PASS_COLOR = "#58d68d"

WARNING_COLOR = "#f5b041"

FAIL_COLOR = "#ec7063"


# ============================================================
# VARIABLES
# ============================================================

password_var = tk.StringVar()

length_var = tk.StringVar(
    value="16"
)

lowercase_var = tk.BooleanVar(
    value=True
)

uppercase_var = tk.BooleanVar(
    value=True
)

numbers_var = tk.BooleanVar(
    value=True
)

symbols_var = tk.BooleanVar(
    value=True
)

report_data = None

show_password = False


# ============================================================
# TITLE
# ============================================================

title = tk.Label(

    root,

    text="🔐 SECUREPASS ANALYZER V6",

    font=("Segoe UI", 25, "bold"),

    fg=TEXT,

    bg=BG
)

title.pack(
    pady=(18, 2)
)


subtitle = tk.Label(

    root,

    text="ADVANCED PASSWORD SECURITY & GENERATOR",

    font=("Segoe UI", 11),

    fg=MUTED,

    bg=BG
)

subtitle.pack(
    pady=(0, 12)
)


# ============================================================
# PASSWORD INPUT CARD
# ============================================================

input_frame = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=15
)

input_frame.pack(

    padx=25,

    fill="x"
)


input_label = tk.Label(

    input_frame,

    text="Password for analysis",

    font=("Segoe UI", 11, "bold"),

    fg=TEXT,

    bg=CARD
)

input_label.pack(

    anchor="w",

    pady=(0, 8)
)


password_entry = tk.Entry(

    input_frame,

    textvariable=password_var,

    font=("Segoe UI", 14),

    show="•",

    bg=CARD2,

    fg=TEXT,

    insertbackground=TEXT,

    relief="flat"
)

password_entry.pack(

    side="left",

    fill="x",

    expand=True,

    ipady=9
)


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


show_button = tk.Button(

    input_frame,

    text="SHOW",

    command=toggle_password,

    font=("Segoe UI", 9, "bold"),

    bg=ACCENT,

    fg="white",

    relief="flat",

    padx=15,

    pady=7,

    cursor="hand2"
)

show_button.pack(

    side="right",

    padx=(10, 0)
)


# ============================================================
# GENERATOR CARD
# ============================================================

generator_frame = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=12
)

generator_frame.pack(

    padx=25,

    pady=10,

    fill="x"
)


generator_title = tk.Label(

    generator_frame,

    text="🔑 SECURE PASSWORD GENERATOR",

    font=("Segoe UI", 12, "bold"),

    fg=TEXT,

    bg=CARD
)

generator_title.grid(

    row=0,

    column=0,

    columnspan=6,

    sticky="w",

    pady=(0, 10)
)


length_label = tk.Label(

    generator_frame,

    text="Length:",

    font=("Segoe UI", 10, "bold"),

    fg=MUTED,

    bg=CARD
)

length_label.grid(

    row=1,

    column=0,

    padx=(0, 5)
)


length_entry = tk.Entry(

    generator_frame,

    textvariable=length_var,

    width=5,

    font=("Segoe UI", 10),

    bg=CARD2,

    fg=TEXT,

    insertbackground=TEXT,

    relief="flat",

    justify="center"
)

length_entry.grid(

    row=1,

    column=1,

    padx=5
)


lowercase_check = tk.Checkbutton(

    generator_frame,

    text="Lowercase",

    variable=lowercase_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT
)

lowercase_check.grid(

    row=1,

    column=2,

    padx=5
)


uppercase_check = tk.Checkbutton(

    generator_frame,

    text="Uppercase",

    variable=uppercase_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT
)

uppercase_check.grid(

    row=1,

    column=3,

    padx=5
)


numbers_check = tk.Checkbutton(

    generator_frame,

    text="Numbers",

    variable=numbers_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT
)

numbers_check.grid(

    row=1,

    column=4,

    padx=5
)


symbols_check = tk.Checkbutton(

    generator_frame,

    text="Symbols",

    variable=symbols_var,

    bg=CARD,

    fg=TEXT,

    selectcolor=CARD2,

    activebackground=CARD,

    activeforeground=TEXT
)

symbols_check.grid(

    row=1,

    column=5,

    padx=5
)


generate_button = tk.Button(

    generator_frame,

    text="⚡ GENERATE PASSWORD",

    command=generate_password,

    font=("Segoe UI", 10, "bold"),

    bg=ACCENT,

    fg="white",

    relief="flat",

    padx=20,

    pady=8,

    cursor="hand2"
)

generate_button.grid(

    row=2,

    column=0,

    columnspan=3,

    pady=(12, 0),

    sticky="w"
)


copy_button = tk.Button(

    generator_frame,

    text="📋 COPY",

    command=copy_password,

    font=("Segoe UI", 10, "bold"),

    bg=CARD2,

    fg=TEXT,

    relief="flat",

    padx=20,

    pady=8,

    cursor="hand2"
)

copy_button.grid(

    row=2,

    column=3,

    columnspan=3,

    pady=(12, 0),

    sticky="e"
)


# ============================================================
# ACTION BUTTONS
# ============================================================

button_frame = tk.Frame(

    root,

    bg=BG
)

button_frame.pack(
    pady=10
)


def analyze():

    global report_data

    password = password_var.get()

    if not password:

        messagebox.showwarning(

            "No Password",

            "Please enter or generate a test password."
        )

        return

    report_data = analyze_password(
        password
    )

    update_gui(
        report_data
    )


def clear_analysis():

    global report_data

    report_data = None

    password_var.set("")

    score_value.config(
        text="--"
    )

    strength_value.config(
        text="WAITING FOR ANALYSIS"
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

        "Enter or generate a test password and click ANALYZE.\n"
    )

    report_text.config(
        state="disabled"
    )


analyze_button = tk.Button(

    button_frame,

    text="🔍 ANALYZE",

    command=analyze,

    font=("Segoe UI", 10, "bold"),

    bg=ACCENT,

    fg="white",

    relief="flat",

    padx=25,

    pady=9,

    cursor="hand2"
)

analyze_button.pack(

    side="left",

    padx=5
)


export_button = tk.Button(

    button_frame,

    text="📄 EXPORT REPORT",

    command=lambda: export_report(),

    font=("Segoe UI", 10, "bold"),

    bg=CARD2,

    fg=TEXT,

    relief="flat",

    padx=25,

    pady=9,

    cursor="hand2"
)

export_button.pack(

    side="left",

    padx=5
)


new_button = tk.Button(

    button_frame,

    text="↻ NEW ANALYSIS",

    command=clear_analysis,

    font=("Segoe UI", 10, "bold"),

    bg=CARD2,

    fg=TEXT,

    relief="flat",

    padx=25,

    pady=9,

    cursor="hand2"
)

new_button.pack(

    side="left",

    padx=5
)


# ============================================================
# SCORE CARD
# ============================================================

score_frame = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=10
)

score_frame.pack(

    padx=25,

    fill="x"
)


score_title = tk.Label(

    score_frame,

    text="SECURITY SCORE",

    font=("Segoe UI", 10, "bold"),

    fg=MUTED,

    bg=CARD
)

score_title.pack()


score_value = tk.Label(

    score_frame,

    text="--",

    font=("Segoe UI", 28, "bold"),

    fg=TEXT,

    bg=CARD
)

score_value.pack()


meter = ttk.Progressbar(

    score_frame,

    orient="horizontal",

    length=700,

    mode="determinate",

    maximum=100
)

meter.pack(
    pady=3
)


strength_value = tk.Label(

    score_frame,

    text="WAITING FOR ANALYSIS",

    font=("Segoe UI", 11, "bold"),

    fg=ACCENT,

    bg=CARD
)

strength_value.pack()


# ============================================================
# SECURITY REPORT
# ============================================================

report_frame = tk.Frame(

    root,

    bg=CARD
)

report_frame.pack(

    padx=25,

    pady=10,

    fill="both",

    expand=True
)


report_label = tk.Label(

    report_frame,

    text="🛡 SECURITY REPORT",

    font=("Segoe UI", 11, "bold"),

    fg=TEXT,

    bg=CARD
)

report_label.pack(

    anchor="w",

    padx=15,

    pady=(10, 5)
)


report_text = ScrolledText(

    report_frame,

    height=10,

    font=("Consolas", 9),

    bg=CARD2,

    fg=TEXT,

    insertbackground=TEXT,

    relief="flat",

    wrap="word"
)

report_text.pack(

    padx=15,

    pady=(0, 12),

    fill="both",

    expand=True
)


# ============================================================
# REPORT TEXT TAGS
# ============================================================

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


report_text.tag_config(

    "recommendation",

    foreground=TEXT
)


# ============================================================
# ENTROPY INFORMATION
# ============================================================

entropy_frame = tk.Frame(

    root,

    bg=CARD,

    padx=20,

    pady=10
)

entropy_frame.pack(

    padx=25,

    pady=(0, 15),

    fill="x"
)


entropy_title = tk.Label(

    entropy_frame,

    text="📊 ENTROPY & SEARCH SPACE",

    font=("Segoe UI", 10, "bold"),

    fg=TEXT,

    bg=CARD
)

entropy_title.pack(
    anchor="w"
)


stats_frame = tk.Frame(

    entropy_frame,

    bg=CARD
)

stats_frame.pack(
    pady=5
)


pool_value = tk.Label(

    stats_frame,

    text="--",

    font=("Segoe UI", 12, "bold"),

    fg=ACCENT,

    bg=CARD
)

pool_value.grid(

    row=0,

    column=0,

    padx=50
)


tk.Label(

    stats_frame,

    text="Character Pool",

    font=("Segoe UI", 8),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=0,

    padx=50
)


entropy_value = tk.Label(

    stats_frame,

    text="--",

    font=("Segoe UI", 12, "bold"),

    fg=ACCENT,

    bg=CARD
)

entropy_value.grid(

    row=0,

    column=1,

    padx=50
)


tk.Label(

    stats_frame,

    text="Entropy",

    font=("Segoe UI", 8),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=1,

    padx=50
)


search_value = tk.Label(

    stats_frame,

    text="--",

    font=("Segoe UI", 12, "bold"),

    fg=ACCENT,

    bg=CARD
)

search_value.grid(

    row=0,

    column=2,

    padx=50
)


tk.Label(

    stats_frame,

    text="Theoretical Search Space",

    font=("Segoe UI", 8),

    fg=MUTED,

    bg=CARD

).grid(

    row=1,

    column=2,

    padx=50
)


# ============================================================
# UPDATE GUI
# ============================================================

def update_gui(report):

    score = report["score"]

    strength = report["strength"]

    score_value.config(

        text=f"{score} / 100"
    )

    strength_value.config(

        text=strength
    )

    meter["value"] = score

    pool_value.config(

        text=str(
            report["character_pool"]
        )
    )

    entropy_value.config(

        text=f"{report['entropy']:.2f} bits"
    )

    search_value.config(

        text=format_search_space(
            report["search_space"]
        )
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

        "SECURITY CHECKS\n",

        "heading"
    )

    report_text.insert(
        tk.END,
        "\n"
    )

    check_names = {

        "length": "Password Length",

        "diversity": "Character Diversity",

        "common": "Common Password Check",

        "repeated": "Repeated Patterns",

        "sequence": "Sequential Patterns",

        "personal": "Predictable Words"
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

            f"{check_names[key]:30}",

            "details"
        )

        report_text.insert(

            tk.END,

            f"{status:10}",

            tag
        )

        report_text.insert(

            tk.END,

            f" {result['details']}\n"
        )

    report_text.insert(

        tk.END,

        "\nRECOMMENDATIONS\n\n",

        "heading"
    )

    for recommendation in report["recommendations"]:

        report_text.insert(

            tk.END,

            f"• {recommendation}\n",

            "recommendation"
        )

    report_text.insert(

        tk.END,

        f"\nAnalysis Time: {report['timestamp']}",

        "details"
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

    file_path = filedialog.asksaveasfilename(

        defaultextension=".txt",

        filetypes=[

            ("Text Files", "*.txt"),

            ("All Files", "*.*")
        ],

        title="Save Security Report"
    )

    if not file_path:

        return

    report = report_data

    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(
            "========================================\n"
        )

        file.write(
            "       SECUREPASS ANALYZER V6\n"
        )

        file.write(
            "       PASSWORD SECURITY REPORT\n"
        )

        file.write(
            "========================================\n\n"
        )

        file.write(
            "PRIVACY NOTICE:\n"
        )

        file.write(
            "The password itself is NOT stored in this report.\n\n"
        )

        file.write(
            f"Security Score : {report['score']} / 100\n"
        )

        file.write(
            f"Strength       : {report['strength']}\n"
        )

        file.write(
            f"Analysis Time  : {report['timestamp']}\n\n"
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

        check_names = {

            "length": "Password Length",

            "diversity": "Character Diversity",

            "common": "Common Password Check",

            "repeated": "Repeated Patterns",

            "sequence": "Sequential Patterns",

            "personal": "Predictable Words"
        }

        for key, result in report["results"].items():

            file.write(

                f"{check_names[key]}: "

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

            f"Character Pool : "
            f"{report['character_pool']}\n"
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

            "This report provides a heuristic and theoretical "
            "security assessment.\n"
        )

        file.write(

            "It does not guarantee that a password cannot be "
            "guessed or compromised.\n"
        )

    messagebox.showinfo(

        "Report Exported",

        "Security report saved successfully!"
    )


# ============================================================
# INITIAL REPORT
# ============================================================

report_text.insert(

    tk.END,

    "Enter or generate a test password and click ANALYZE.\n"
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
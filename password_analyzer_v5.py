import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import math
from datetime import datetime


# ============================================================
# PASSWORD SECURITY ANALYSIS
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


def calculate_character_pool(password):
    """Calculate the possible character pool based on characters used."""

    pool = 0

    if any(c.islower() for c in password):
        pool += 26

    if any(c.isupper() for c in password):
        pool += 26

    if any(c.isdigit() for c in password):
        pool += 10

    special_characters = set(
        "!@#$%^&*()-_=+[]{}|;:',.<>?/`~\\\""
    )

    if any(c in special_characters for c in password):
        pool += len(special_characters)

    return pool


def calculate_entropy(password, character_pool):
    """Calculate theoretical entropy."""

    if not password or character_pool == 0:
        return 0

    return len(password) * math.log2(character_pool)


def calculate_search_space(character_pool, length):
    """Calculate theoretical number of possible passwords."""

    if character_pool == 0 or length == 0:
        return 0

    return character_pool ** length


def format_search_space(number):
    """Display very large numbers in readable form."""

    if number == 0:
        return "0"

    if number < 1_000_000:
        return f"{number:,}"

    exponent = math.log10(number)

    return f"~10^{exponent:.1f}"


def check_length(password):
    """Check password length."""

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
    """Check character diversity."""

    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digit = any(c.isdigit() for c in password)

    special = any(
        not c.isalnum()
        for c in password
    )

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
    """Check against a small demonstration common-password list."""

    if password.lower() in COMMON_PASSWORDS:
        return {
            "status": "FAIL",
            "details": "Password appears in a common-password list",
            "points": 0
        }

    return {
        "status": "PASS",
        "details": "Not found in the built-in common-password list",
        "points": 15
    }


def check_repeated(password):
    """Detect three or more identical characters in a row."""

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
    """Detect simple ascending or descending sequences."""

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


def calculate_score(results):
    """Calculate final security score."""

    score = sum(item["points"] for item in results.values())

    # Maximum theoretical score = 95 from the checks above.
    # Convert it to a 100-point scale.
    score = round((score / 95) * 100)

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


def generate_recommendations(results, password):

    recommendations = []

    if results["length"]["status"] != "PASS":
        recommendations.append(
            "Use a longer password or passphrase."
        )

    if results["diversity"]["status"] != "PASS":
        recommendations.append(
            "Mix uppercase, lowercase, numbers and symbols."
        )

    if results["common"]["status"] == "FAIL":
        recommendations.append(
            "Avoid commonly used passwords."
        )

    if results["repeated"]["status"] != "PASS":
        recommendations.append(
            "Avoid repeating the same character several times."
        )

    if results["sequence"]["status"] != "PASS":
        recommendations.append(
            "Avoid predictable sequences such as abc or 123."
        )

    if len(password) < 16:
        recommendations.append(
            "Consider using a longer passphrase."
        )

    if not recommendations:
        recommendations.append(
            "Good job! No major issues were detected."
        )

    return recommendations


def analyze_password(password):

    if not password:
        return None

    results = {

        "length": check_length(password),

        "diversity": check_diversity(password),

        "common": check_common_password(password),

        "repeated": check_repeated(password),

        "sequence": check_sequence(password)
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
# GUI
# ============================================================

root = tk.Tk()

root.title("SECUREPASS ANALYZER V5")

root.geometry("950x900")

root.configure(bg="#10141c")

root.resizable(False, False)


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
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="🔐 SECUREPASS ANALYZER V5",
    font=("Segoe UI", 24, "bold"),
    fg=TEXT,
    bg=BG
)

title.pack(pady=(20, 3))


subtitle = tk.Label(
    root,
    text="PASSWORD SECURITY ASSESSMENT",
    font=("Segoe UI", 11),
    fg=MUTED,
    bg=BG
)

subtitle.pack(pady=(0, 15))


# ============================================================
# PASSWORD INPUT
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
    text="Enter a test password:",
    font=("Segoe UI", 11, "bold"),
    fg=TEXT,
    bg=CARD
)

input_label.pack(
    anchor="w",
    pady=(0, 8)
)


password_var = tk.StringVar()

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


show_password = False


def toggle_password():

    global show_password

    show_password = not show_password

    if show_password:
        password_entry.config(show="")
        show_button.config(text="HIDE")
    else:
        password_entry.config(show="•")
        show_button.config(text="SHOW")


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
# BUTTONS
# ============================================================

button_frame = tk.Frame(
    root,
    bg=BG
)

button_frame.pack(pady=15)


report_data = None


def clear_analysis():

    global report_data

    password_var.set("")

    report_data = None

    score_value.config(
        text="--"
    )

    strength_value.config(
        text="WAITING FOR ANALYSIS"
    )

    meter["value"] = 0

    report_text.config(
        state="normal"
    )

    report_text.delete(
        "1.0",
        tk.END
    )

    report_text.insert(
        tk.END,
        "Enter a test password above and click ANALYZE.\n"
    )

    report_text.config(
        state="disabled"
    )

    entropy_value.config(
        text="--"
    )

    pool_value.config(
        text="--"
    )

    search_value.config(
        text="--"
    )


def analyze():

    global report_data

    password = password_var.get()

    if not password:

        messagebox.showwarning(
            "No Password",
            "Please enter a test password."
        )

        return

    report_data = analyze_password(
        password
    )

    update_gui(
        report_data
    )


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

    # --------------------------------------------------------
    # ENTROPY
    # --------------------------------------------------------

    entropy_value.config(
        text=f"{report['entropy']:.2f} bits"
    )

    pool_value.config(
        text=str(report["character_pool"])
    )

    search_value.config(
        text=format_search_space(
            report["search_space"]
        )
    )

    # --------------------------------------------------------
    # SECURITY REPORT
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
        "sequence": "Sequential Patterns"
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
            f"✓ {check_names[key]:30}",
            "normal_text"
        )

        report_text.insert(
            tk.END,
            f"{status:10}",
            tag
        )

        report_text.insert(
            tk.END,
            f"  {result['details']}\n",
            "details"
        )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    report_text.insert(
        tk.END,
        "\nRECOMMENDATIONS\n",
        "heading"
    )

    report_text.insert(
        tk.END,
        "\n"
    )

    for recommendation in report["recommendations"]:

        report_text.insert(
            tk.END,
            f"• {recommendation}\n",
            "recommendation"
        )

    report_text.insert(
        tk.END,
        "\n"
    )

    report_text.insert(
        tk.END,
        f"Analysis Time: {report['timestamp']}\n",
        "details"
    )

    report_text.config(
        state="disabled"
    )


def export_report():

    if report_data is None:

        messagebox.showwarning(
            "No Report",
            "Please analyze a password before exporting."
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
            "       SECUREPASS ANALYZER V5\n"
        )

        file.write(
            "       PASSWORD SECURITY REPORT\n"
        )

        file.write(
            "========================================\n\n"
        )

        file.write(
            "IMPORTANT: The password itself is NOT stored "
            "in this report.\n\n"
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
            "sequence": "Sequential Patterns"
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
            "This analyzer provides a theoretical and "
            "heuristic assessment.\n"
        )

        file.write(
            "It does not guarantee that a password is "
            "impossible to guess or crack.\n"
        )

    messagebox.showinfo(
        "Report Exported",
        "Security report successfully exported!"
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
    pady=10,
    cursor="hand2"
)

analyze_button.pack(
    side="left",
    padx=5
)


export_button = tk.Button(
    button_frame,
    text="📄 EXPORT REPORT",
    command=export_report,
    font=("Segoe UI", 10, "bold"),
    bg=CARD2,
    fg=TEXT,
    relief="flat",
    padx=25,
    pady=10,
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
    pady=10,
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
    pady=15
)

score_frame.pack(
    padx=25,
    fill="x"
)


score_title = tk.Label(
    score_frame,
    text="SECURITY SCORE",
    font=("Segoe UI", 11, "bold"),
    fg=MUTED,
    bg=CARD
)

score_title.pack()


score_value = tk.Label(
    score_frame,
    text="--",
    font=("Segoe UI", 30, "bold"),
    fg=TEXT,
    bg=CARD
)

score_value.pack()


meter = ttk.Progressbar(
    score_frame,
    orient="horizontal",
    length=650,
    mode="determinate",
    maximum=100
)

meter.pack(
    pady=5
)


strength_value = tk.Label(
    score_frame,
    text="WAITING FOR ANALYSIS",
    font=("Segoe UI", 12, "bold"),
    fg=ACCENT,
    bg=CARD
)

strength_value.pack()


# ============================================================
# REPORT AREA
# ============================================================

report_frame = tk.Frame(
    root,
    bg=CARD
)

report_frame.pack(
    padx=25,
    pady=12,
    fill="both",
    expand=True
)


report_label = tk.Label(
    report_frame,
    text="SECURITY REPORT",
    font=("Segoe UI", 12, "bold"),
    fg=TEXT,
    bg=CARD
)

report_label.pack(
    anchor="w",
    padx=15,
    pady=(12, 5)
)


report_text = ScrolledText(
    report_frame,
    height=12,
    font=("Consolas", 10),
    bg=CARD2,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    wrap="word"
)

report_text.pack(
    padx=15,
    pady=(0, 15),
    fill="both",
    expand=True
)


# ============================================================
# REPORT TEXT COLORS
# ============================================================

report_text.tag_config(
    "heading",
    foreground=ACCENT,
    font=("Consolas", 11, "bold")
)

report_text.tag_config(
    "pass",
    foreground=PASS_COLOR,
    font=("Consolas", 10, "bold")
)

report_text.tag_config(
    "warning",
    foreground=WARNING_COLOR,
    font=("Consolas", 10, "bold")
)

report_text.tag_config(
    "fail",
    foreground=FAIL_COLOR,
    font=("Consolas", 10, "bold")
)

report_text.tag_config(
    "normal_text",
    foreground=TEXT
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
# ENTROPY CARD
# ============================================================

entropy_frame = tk.Frame(
    root,
    bg=CARD,
    padx=20,
    pady=12
)

entropy_frame.pack(
    padx=25,
    pady=(0, 20),
    fill="x"
)


entropy_title = tk.Label(
    entropy_frame,
    text="ENTROPY & SEARCH SPACE",
    font=("Segoe UI", 11, "bold"),
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
    pady=8
)


pool_value = tk.Label(
    stats_frame,
    text="--",
    font=("Segoe UI", 13, "bold"),
    fg=ACCENT,
    bg=CARD
)

pool_value.grid(
    row=0,
    column=0,
    padx=45
)


pool_label = tk.Label(
    stats_frame,
    text="Character Pool",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD
)

pool_label.grid(
    row=1,
    column=0,
    padx=45
)


entropy_value = tk.Label(
    stats_frame,
    text="--",
    font=("Segoe UI", 13, "bold"),
    fg=ACCENT,
    bg=CARD
)

entropy_value.grid(
    row=0,
    column=1,
    padx=45
)


entropy_label = tk.Label(
    stats_frame,
    text="Entropy",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD
)

entropy_label.grid(
    row=1,
    column=1,
    padx=45
)


search_value = tk.Label(
    stats_frame,
    text="--",
    font=("Segoe UI", 13, "bold"),
    fg=ACCENT,
    bg=CARD
)

search_value.grid(
    row=0,
    column=2,
    padx=45
)


search_label = tk.Label(
    stats_frame,
    text="Theoretical Search Space",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD
)

search_label.grid(
    row=1,
    column=2,
    padx=45
)


# ============================================================
# INITIAL MESSAGE
# ============================================================

report_text.insert(
    tk.END,
    "Enter a test password above and click ANALYZE.\n"
)

report_text.config(
    state="disabled"
)


# ============================================================
# LIVE ENTER KEY
# ============================================================

password_entry.bind(
    "<Return>",
    lambda event: analyze()
)


# ============================================================
# START PROGRAM
# ============================================================

root.mainloop()
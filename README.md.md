# 🔐 SecurePass Analyzer V8

SecurePass Analyzer is a local desktop application built with Python and Tkinter for analyzing password strength and generating strong test passwords.

> **Privacy:** Password analysis is performed locally. The application does not send passwords to a server, and the actual password is not stored in analysis history or exported reports.

## ✨ Features

- 🔐 Password strength analysis
- 📊 Security score from 0–100
- 🏆 Grade and strength classification
- 🔎 Multiple security checks
- 📈 Entropy calculation
- 🔢 Theoretical search-space estimation
- ⚡ Secure password generator using Python `secrets`
- 👁 Show / hide password
- 📋 Copy generated password
- 📜 Password-free analysis history
- 📊 Session statistics
- 💡 Security recommendations
- 📄 Exportable security report
- 🖥️ Dark cybersecurity-themed Tkinter GUI
- 🔒 Local-only processing

## 🛡️ Security Checks

The analyzer checks for:

- Password length
- Character diversity
- Common passwords
- Repeated characters
- Sequential patterns
- Predictable words
- Repeated blocks
- Character variety

## 🧰 Technologies

- Python 3
- Tkinter
- `secrets`
- `string`
- `math`
- `datetime`

No external Python packages are required.

## 📁 Project Structure

```text
Password-Strength-Analyzer/
│
├── password_analyzer.py
├── password_analyzer_v1.py
├── password_analyzer_v2.py
├── password_analyzer_v3.py
├── password_analyzer_v4.py
├── password_analyzer_v5.py
├── password_analyzer_v6.py
├── password_analyzer_v7.py
├── password_analyzer_v8.py
├── README.md
├── requirements.txt
└── .gitignore
```

**V8 is the final feature-complete version of the application.**

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Password-Strength-Analyzer-.git
```

### 2. Open the project

```bash
cd Password-Strength-Analyzer-
```

### 3. Run V8

```bash
python password_analyzer_v8.py
```

On Windows, you can also use:

```powershell
py password_analyzer_v8.py
```

## 🖥️ How to Use

1. Open the application.
2. Enter a **dummy/test password** or generate one.
3. Click **ANALYZE**.
4. Review the security score and grade.
5. Check the detailed security breakdown.
6. Review entropy and theoretical search-space information.
7. Use **GENERATE** to create a strong test password.
8. Use **EXPORT REPORT** to save the analysis as a text report.

## 📊 Score Interpretation

| Score | Grade | Strength |
|---:|:---:|---|
| 90–100 | A+ | Very Strong |
| 80–89 | A | Strong |
| 70–79 | B | Good |
| 55–69 | C | Moderate |
| 40–54 | D | Weak |
| 0–39 | F | Very Weak |

## 🔒 Privacy Design

This project is designed as a local educational cybersecurity tool.

- No network requests are required.
- Passwords are not written to analysis history.
- Exported reports do not contain the analyzed password.
- The secure generator uses Python's `secrets` module.
- Entropy and search-space values are theoretical estimates and should not be interpreted as exact real-world cracking times.

## ⚠️ Educational Project

This project is intended for learning about password security, Python GUI development, defensive cybersecurity concepts, and secure random password generation.

For testing, use dummy passwords rather than passwords used for real accounts.

## 🚀 Future Scope

Possible future improvements include:

- More comprehensive password dictionaries
- More advanced password-risk heuristics
- Improved accessibility
- Automated testing
- Packaged desktop executable
- Additional report formats

## 👩‍💻 Author

**Pavithra**

Built as a Python cybersecurity project.

import tkinter as tk

root = tk.Tk()

root.title("Tkinter Test")

root.geometry("500x300")

root.configure(bg="black")

label = tk.Label(
    root,
    text="TKINTER IS WORKING!",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="black"
)

label.pack(expand=True)

root.mainloop()
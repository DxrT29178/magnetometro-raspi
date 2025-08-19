def run_gui():
    import tkinter as tk
    root = tk.Tk()
    root.title("Magnetómetro GUI")
    label = tk.Label(root, text="Interfaz gráfica del magnetómetro")
    label.pack(padx=20, pady=20)
    root.mainloop()
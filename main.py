import tkinter as tk
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Layout with Tabs Example")
        self.geometry("600x400")

        # Creating and placing the top entry with a search button
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.search_button = tk.Button(self, text="Search")
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        # Creating and placing the image placeholder (using a Label here)
        self.image_frame = tk.Frame(self, bg='lightblue', width=200, height=100)
        self.image_frame.grid(row=1, column=1, rowspan=2, padx=5, pady=5, sticky='nsew')

        # Sun (yellow circle) and additional shapes inside the image frame
        self.sun = tk.Canvas(self.image_frame, width=50, height=50, bg='lightblue', highlightthickness=0)
        self.sun.create_oval(10, 10, 50, 50, fill='yellow')
        self.sun.pack()

        # Creating notebook with tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, rowspan=2, padx=5, pady=5, sticky='nsew')

        self.tab1 = tk.Frame(self.notebook, bg='white')
        self.tab2 = tk.Frame(self.notebook, bg='white')
        self.tab3 = tk.Frame(self.notebook, bg='white')

        self.notebook.add(self.tab1, text="Tab 1")
        self.notebook.add(self.tab2, text="Tab 2")
        self.notebook.add(self.tab3, text="Tab 3")

        # Adding content to tabs (example content for demonstration)
        tk.Label(self.tab1, text="Content of Tab 1").pack(padx=10, pady=10)
        tk.Label(self.tab2, text="Content of Tab 2").pack(padx=10, pady=10)
        tk.Label(self.tab3, text="Content of Tab 3").pack(padx=10, pady=10)

        # Creating and placing the bottom right large placeholder (for any content)
        self.large_placeholder = tk.Frame(self, bg='lightgreen', width=200, height=200)
        self.large_placeholder.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Configuring grid weights to ensure proper resizing behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

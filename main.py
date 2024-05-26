import tkinter as tk
from tkinter import ttk

""" asda """
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Layout with Tabs Example")
        self.geometry("800x600")

        # Creating and placing the top entry with a search button
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.search_button = tk.Button(self, text="Search")
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        # Creating notebook with tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Creating tabs
        self.tab1 = tk.Frame(self.notebook, bg='white')
        self.tab2 = tk.Frame(self.notebook, bg='white')
        self.tab3 = tk.Frame(self.notebook, bg='white')

        self.notebook.add(self.tab1, text="Tab 1")
        self.notebook.add(self.tab2, text="Tab 2")
        self.notebook.add(self.tab3, text="Tab 3")

        # Adding listbox and text areas to each tab
        self.create_tab_content(self.tab1)
        self.create_tab_content(self.tab2)
        self.create_tab_content(self.tab3)

        # Creating and placing the top right image placeholder
        self.image_frame_top = tk.Frame(self, bg='lightblue', width=200, height=100)
        self.image_frame_top.grid(row=0, column=2, rowspan=2, padx=5, pady=5, sticky='nsew')

        # Creating and placing the bottom right image placeholder
        self.image_frame_bottom = tk.Frame(self, bg='lightgreen', width=200, height=200)
        self.image_frame_bottom.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Configuring grid weights to ensure proper resizing behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def create_tab_content(self, tab):
        # Listbox on the left side of the tab
        listbox_frame = tk.Frame(tab, bg='white')
        listbox_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        listbox = tk.Listbox(listbox_frame)
        listbox.pack(fill='both', expand=True)

        # Text area on the right side of the tab
        text_frame = tk.Frame(tab, bg='white')
        text_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        text_area = tk.Text(text_frame)
        text_area.pack(fill='both', expand=True)


# if __name__ == "__main__":
#     app = Application()
#     app.mainloop()

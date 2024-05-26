import tkinter as tk
from tkinter import ttk

""" asda """
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("등산돌이")
        self.geometry("800x700")

        # Creating and placing the top entry with a search button
        self.entry = tk.Entry(self, width=20, font=('Helvetica', 16))
        #self.entry = tk.Text(self, height=2)
        self.entry.grid(row=0, column=0, padx=(20,0), pady=40, ipady=8, sticky='ew')

        self.search_button = tk.Button(self, text="검색", font=('Helvetica', 16))
        self.search_button.grid(row=0, column=1, padx=(0,20), pady=40, sticky='w')

        # Apply custom style for Notebook tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[40, 8], font=('Helvetica', 12))

        # Creating notebook with tabs
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.notebook.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

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

        # # Creating and placing the top right image placeholder
        self.image_weather = tk.Frame(self, bg='lightblue', width=260, height=120)
        self.image_weather.grid(row=0, column=2, padx=50, pady=30, sticky='n')
        #
        # # Creating and placing the bottom right image placeholder
        # self.image_frame_bottom = tk.Frame(self, bg='lightgreen', width=200, height=200)
        # self.image_frame_bottom.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Configuring grid weights to ensure proper resizing behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def create_tab_content(self, tab):
        # Listbox 설정
        listbox_frame = tk.Frame(tab, bg='white')
        listbox_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=50)

        listbox = tk.Listbox(listbox_frame)
        listbox.pack(side=tk.LEFT, fill='both', expand=True)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=listbox.yview)  # listbox와 scrollbar 연결
        listbox.config(yscrollcommand=scrollbar.set)  # scrollbar와 listbox 연결

        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")
        listbox.insert(tk.END, "Item 1")


        # 텍스트 출력 프레임 설정
        text_frame = tk.Frame(tab, bg='white')
        text_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)

        text_area = tk.Text(text_frame)
        text_area.pack(fill='both', expand=True)

        # 이미지 프레임 설정
        image_frame = tk.Frame(tab, bg='lightgreen', width=600)
        image_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=20, pady=20)

        # 그리드 레이아웃 설정
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

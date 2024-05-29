import tkinter as tk
from tkinter import ttk
import xml_read
import Gmap_Test
from PIL import Image, ImageTk

MT_data = []

class Application:
    def __init__(self):
        self.window = tk.Tk()  # Tk 인스턴스 생성
        self.window.title("등산돌이")
        self.window.geometry("800x700")

        # Creating and placing the top entry with a search button
        self.entry = tk.Entry(self.window, width=20, font=('Helvetica', 16))
        self.entry.grid(row=0, column=0, padx=(20,0), pady=40, ipady=8, sticky='ew')

        self.search_button = tk.Button(self.window, text="검색", font=('Helvetica', 16), command=self.SIGUN_search)
        self.search_button.grid(row=0, column=1, padx=(0,20), pady=40, sticky='w')

        # Apply custom style for Notebook tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[40, 8], font=('Helvetica', 12), bg='black')

        # Creating custom styles for each tab
        style.map('TNotebook.Tab', background=[('selected', 'lightblue')], foreground=[('selected', 'blue')])

        # Creating notebook with tabs
        self.notebook = ttk.Notebook(self.window, style='TNotebook')
        self.notebook.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Creating tabs
        self.tab1 = tk.Frame(self.notebook, bg='white')
        self.tab2 = tk.Frame(self.notebook, bg='white')
        self.tab3 = tk.Frame(self.notebook, bg='white')

        self.notebook.add(self.tab1, text="해당 지역의 산")
        self.notebook.add(self.tab2, text="Tab 2")
        self.notebook.add(self.tab3, text="Tab 3")

        # Adding listbox and text areas to each tab
        self.listbox1 = self.create_tab_content(self.tab1)
        self.listbox2 = self.create_tab_content(self.tab2)
        self.listbox3 = self.create_tab_content(self.tab3)

        # Creating and placing the top right image placeholder
        self.image_weather = tk.Frame(self.window, bg='lightblue', width=260, height=120)
        self.image_weather.grid(row=0, column=2, padx=50, pady=30, sticky='n')

        # Creating a label to display the map image
        self.map_label = tk.Label(self.window)
        self.map_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky='n')

        # Configuring grid weights to ensure proper resizing behavior
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

    def create_tab_content(self, tab):
        def on_item_select(event):
            # 현재 선택된 항목의 인덱스 가져오기
            selected_index = event.widget.curselection()

            # 선택된 항목의 텍스트 가져오기
            selected_item = event.widget.get(selected_index)
            data = xml_read.MT_deap_data(selected_item)
            text_area.delete('1.0', tk.END)  # 텍스트 영역 초기화

            # data = {
            #     "MT_NAME": MT_NAME,
            #     "MT_CODE": MT_CODE,
            #     "MT_LOCATION": MT_LOCATION,
            #     "MT_HIGH": MT_HIGH,
            #     "MT_ADMIN": MT_ADMIN,
            #     "MT_ADMIN_NUM": MT_ADMIN_NUM,
            #     "MT_INFO": MT_INFO
            # }
            if data == -1:
                text_area.insert(tk.END, "산 정보 없음" + '\n')
            elif data and "MT_ADMIN_NUM" in data:
                text_area.insert(tk.END, "산 이름 : " + data["MT_NAME"] + '\n')
                text_area.insert(tk.END, "산 코드 : " + data["MT_CODE"] + '\n')
                text_area.insert(tk.END, "산 위치 : " + data["MT_LOCATION"] + '\n')
                text_area.insert(tk.END, "산 높이 : " + data["MT_HIGH"] + '\n')
                text_area.insert(tk.END, "산 관리 주체 : " + data["MT_ADMIN"] + '\n')
                text_area.insert(tk.END, "산 관리 주체 연락처 : " + data["MT_ADMIN_NUM"] + '\n')

                # Show the map
                img = Gmap_Test.print_map(data["MT_NAME"])
                self.show_map_image(img)

        # Label 위젯을 추가하여 특정 텍스트 출력
        labelText = " "
        if tab == self.tab1:
            labelText = "Tab 1에 표시할 특정 텍스트"
        elif tab == self.tab2:
            labelText = "Tab 2에 표시할 다른 특정 텍스트"
        elif tab == self.tab3:
            labelText = "Tab 3에 표시할 다른 특정 텍스트"

        label = tk.Label(tab, text=labelText, font=('Helvetica', 12), bg='white', fg='black')
        label.grid(row=0, column=0, padx=20, pady=20, sticky='n')

        # Listbox 설정
        listbox_frame = tk.Frame(tab, bg='white')
        listbox_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

        listbox = tk.Listbox(listbox_frame)
        listbox.pack(side=tk.LEFT, fill='both', expand=True)
        listbox.bind('<<ListboxSelect>>', on_item_select)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        # 텍스트 출력 프레임 설정
        text_frame = tk.Frame(tab, bg='white', height=100)
        text_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=20)

        text_area = tk.Text(text_frame)
        text_area.pack(fill='both', expand=True)

        # graph_frame = tk.Frame(tab, bg='white', height=50)
        # graph_frame.grid(row=3, column=0, sticky='sew', padx=20, pady=20)
        #
        # graph_area = tk.Canvas(graph_frame)
        # graph_area.pack()

        # 이미지 프레임 설정
        self.image_frame = tk.Frame(tab, bg='white', width=600, height=100)
        self.image_frame.grid(row=0, column=1, rowspan=4, sticky='nsew', padx=20, pady=20)

        # 그리드 레이아웃 설정
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        tab.grid_rowconfigure(3, weight=1)

        return listbox

    def show_map_image(self, img):
        tk_img = ImageTk.PhotoImage(img)
        self.map_label.configure(image=tk_img)
        self.map_label.image = tk_img  # Keep a reference to avoid garbage collection
        self.map_label.place(x=375, y=260)
    def SIGUN_search(self):
        global MT_data
        self.listbox1.delete(0, tk.END)
        search_text = self.entry.get()
        print("검색어:", search_text)
        MT_data = []
        mountain_data = xml_read.MT_data_read(search_text)
        if mountain_data is not None:
            MT_data.append(mountain_data)
            for mountain_data in MT_data:
                for mountain_name in mountain_data["mntn_info"]:
                    self.listbox1.insert(tk.END, mountain_name)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()

=======
# if __name__ == "__main__":
#     app = Application()
#     app.mainloop()


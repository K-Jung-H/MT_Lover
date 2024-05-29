import tkinter as tk
from tkinter import ttk
import xml_read

MT_data = []

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("등산돌이")
        self.geometry("800x700")

        # Creating and placing the top entry with a search button
        self.entry = tk.Entry(self, width=20, font=('Helvetica', 16))
        self.entry.grid(row=0, column=0, padx=(20,0), pady=40, ipady=8, sticky='ew')

        self.search_button = tk.Button(self, text="검색", font=('Helvetica', 16), command=self.SIGUN_search)
        self.search_button.grid(row=0, column=1, padx=(0,20), pady=40, sticky='w')

        # Apply custom style for Notebook tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[40, 8], font=('Helvetica', 12), bg='black')

        # Creating custom styles for each tab
        style.map('TNotebook.Tab', background=[('selected', 'lightblue')], foreground=[('selected', 'blue')])

        # Creating notebook with tabs
        self.notebook = ttk.Notebook(self, style='TNotebook')
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

        # # Creating and placing the top right image placeholder
        self.image_weather = tk.Frame(self, bg='lightblue', width=260, height=120)
        self.image_weather.grid(row=0, column=2, padx=50, pady=30, sticky='n')

        # Configuring grid weights to ensure proper resizing behavior
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

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

            # 선택된 항목에 대한 처리
            # print("선택된 항목:", selected_item)
            #
            # xml_read.MT_data_read()

        # Label 위젯을 추가하여 특정 텍스트 출력
        labelText = " "
        if tab == self.tab1:
            labelText = "Tab 1에 표시할 특정 텍스트"
        elif tab == self.tab2:
            labelText = "Tab 2에 표시할 다른 특정 텍스트"
        elif tab == self.tab3:
            labelText = "Tab 3에 표시할 다른 특정 텍스트"

        label = tk.Label(tab, text=labelText, font=('Helvetica', 12), bg='white', fg='black')  # fg를 추가하여 텍스트 색상 설정
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
        scrollbar.config(command=listbox.yview)  # listbox와 scrollbar 연결
        listbox.config(yscrollcommand=scrollbar.set)  # scrollbar와 listbox 연결

        # 텍스트 출력 프레임 설정
        text_frame = tk.Frame(tab, bg='white', height=100)
        text_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=20)

        text_area = tk.Text(text_frame)
        text_area.pack(fill='both', expand=True)

        graph_frame = tk.Canvas(tab, bg='white', height=200)
        graph_frame.grid(row=3, column=0, sticky='sew', padx=20, pady=20)

        # 이미지 프레임 설정
        image_frame = tk.Frame(tab, bg='lightgreen', width=600)
        image_frame.grid(row=0, column=1, rowspan=4, sticky='nsew', padx=20, pady=20)

        # 그리드 레이아웃 설정
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        tab.grid_rowconfigure(3, weight=1)

        return listbox  # 수정된 부분: listbox를 반환합니다.

    def SIGUN_search(self):
        global MT_data
        self.listbox1.delete(0, tk.END)  # 탭 1 리스트 상자 초기화
        search_text = self.entry.get()
        print("검색어:", search_text)
        MT_data = []  # MT_data 초기화
        mountain_data = xml_read.MT_data_read(search_text)
        if mountain_data is not None:
            MT_data.append(mountain_data)
            for mountain_data in MT_data:
                for mountain_name in mountain_data["mntn_info"]:
                    self.listbox1.insert(tk.END, mountain_name)




if __name__ == "__main__":
    app = Application()
    app.mainloop()
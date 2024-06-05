import tkinter as tk
from tkinter import ttk
from tkinter import *

import urllib3

import xml_read
import Gmap_Test
from PIL import Image, ImageTk
import Weather_Test
import image_search
# import noti
import teller
# import telepot

MT_data = []

class Application:
    def __init__(self):
        self.window = tk.Tk()  # Tk 인스턴스 생성
        self.window.title("등산돌이")
        self.window.geometry("800x700")

        self.Mt_list = {}
        self.local_mt_list = []

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
        self.notebook.add(self.tab2, text="산의 높이 막대 그래프")
        self.notebook.add(self.tab3, text="Tab 3")

        # Adding listbox and text areas to each tab
        self.listbox1 = self.create_tab_content(self.tab1)
        #self.listbox2 = self.create_tab_content(self.tab2)
        self.listbox3 = self.create_tab_content(self.tab3)

        # Creating and placing the top right image placeholder
        self.image_weather = tk.Frame(self.window, bg='lightblue', width=260, height=120)
        self.image_weather.grid(row=0, column=2, padx=50, pady=30, sticky='n')

        # Creating a label to display the map image
        self.map_label = tk.Label(self.window)
        self.map_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky='n')

        self.canvas = tk.Canvas(self.tab2, bg='white', width=600, height=400)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, sticky='n')

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # Create bar chart initially
        self.create_bar_chart()

        self.now_g_image = ""

        self.B_Tele = Button(self.window, text="텔레그렘", width=10, height=1, command=self.pressedTele)
        self.B_Tele.place(x=50, y=50)

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
                print(data["MT_LOCATION"][0:7] + ' ' + data["MT_NAME"])
                # Show the map
                img = Gmap_Test.print_map(data["MT_NAME"])
                self.now_g_image = Gmap_Test.print_map(data["MT_NAME"])
                self.show_map_image(img)

                mt_dx,mt_dy = Gmap_Test.find_XY(data["MT_NAME"])
                print(mt_dx,mt_dy)
                W_data = Weather_Test.get_weather_data(mt_dx,mt_dy)
                print(W_data)

                time_str = W_data[4].split()[1]  # 문자열을 공백을 기준으로 분리하고 두 번째 요소 선택
                # 시간 부분을 정수로 변환하여 비교
                hour = int(time_str.split(':')[0])
                time_of_day = ""
                if 6 <= hour < 18:
                    time_of_day = "낮"
                else:
                    time_of_day = "밤"

                image_path = ""  # 이미지 파일 경로
                # 강수량과 날씨 정보를 확인하여 이미지 프레임에 글자 입력
                if W_data[1] == "강수 없음":
                    if W_data[0] == "맑음":
                        if time_of_day == "낮":
                            image_path = "weather_image/맑음(낮).png"
                        else:
                            image_path = "weather_image/맑음(밤).png"
                    elif W_data[0] == "구름많음":
                        if time_of_day == "낮":
                            image_path = "weather_image/구름많음(낮).png"
                        else:
                            image_path = "weather_image/구름많음(밤).png"
                    elif W_data[0] == "흐림":
                        image_path = "weather_image/흐림.png"
                else:
                    # 강수가 있는 경우에 대한 처리
                    if W_data[1] == "비":
                        image_path = "weather_image/비.png"
                    elif W_data[1] == "비/눈":
                        image_path = "weather_image/비또는눈.png"
                    elif W_data[1] == "눈":
                        image_path = "weather_image/눈.png"
                    elif W_data[1] == "빗방울":
                        image_path = "weather_image/빗방울.png"
                    elif W_data[1] == "눈날림":
                        image_path = "weather_image/눈날림.png"

                # 이미지 프레임에 글자 입력
                # weather_label = tk.Label(self.image_weather, text=weather_text, font=('Helvetica', 16), bg='lightblue',
                #                          fg='black')
                # weather_label.pack(fill='both', expand=True)
                # weather_label = tk.Label(self.image_weather, text=weather_text, font=('Helvetica', 16), bg='lightblue',
                #                          fg='black')
                # # weather_label.place(relx=0.5, rely=0.5, anchor='center')  # 중앙에 배치
                # weather_label.place(relx=0.0, rely=0.5, anchor='w')  # 중앙에 배치
                self.image_weather.configure(bg='white')


                image = Image.open(image_path)
                tk_image = ImageTk.PhotoImage(image)
                # 이미지 레이블 생성 및 이미지 삽입
                image_label = tk.Label(self.image_weather, image=tk_image, bg='white')
                image_label.image = tk_image  # Tkinter에서 이미지가 가비지 컬렉션되는 것을 방지하기 위해 참조 유지
                image_label.place(relx=0.05, rely=0.45, anchor='w')  # 이미지 레이블 배치

                rain_text = W_data[1]
                weather_label = tk.Label(self.image_weather, text=rain_text, font=('Helvetica', 12), bg='white',
                                         fg='black')
                weather_label.place(relx=0.55, rely=0.15, anchor='w')  # 중앙에 배치

                do_text = "기온 " + W_data[2] + "℃"
                weather_label = tk.Label(self.image_weather, text=do_text, font=('Helvetica', 12), bg='white',
                                         fg='black')
                weather_label.place(relx=0.55, rely=0.45, anchor='w')  # 중앙에 배치

                sp_text = "습도 " + W_data[2] + "%"
                weather_label = tk.Label(self.image_weather, text=sp_text, font=('Helvetica', 12), bg='white',
                                         fg='black')
                weather_label.place(relx=0.55, rely=0.7, anchor='w')  # 중앙에 배치

                now_time_text = W_data[4]
                weather_label = tk.Label(self.image_weather, text=now_time_text, font=('Helvetica', 8), bg='white',
                                         fg='black')
                weather_label.place(relx=0.5, rely=0.9, anchor='w')  # 중앙에 배치


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

    def close_map_image(self):
        # self.map_label.configure(image=None)
        # self.map_label.image = None
        self.map_label.place_forget()

    def SIGUN_search(self):
        global MT_data
        self.local_mt_list.clear()
        self.listbox1.delete(0, tk.END)
        search_text = self.entry.get()
        print("검색어:", search_text)

        mountain_data = xml_read.MT_data_read(search_text)
        if mountain_data is not None:
            for mt_name in mountain_data["mntn_info"]:
                self.listbox1.insert(tk.END, mt_name)


                if mt_name not in self.Mt_list.keys():
                    deep_data = xml_read.MT_deap_data(mt_name)
                    if deep_data is not None:
                        self.local_mt_list.append(mt_name)
                        self.Mt_list[mt_name] = deep_data['MT_HIGH']
                else:
                    self.local_mt_list.append(mt_name)

            print('산 리스트 테스트: ', self.local_mt_list)
            print('Mt_list 테스트: ', self.Mt_list)

    def create_bar_chart(self):
        # Clear canvas before drawing
        self.canvas.delete("all")
        self.canvas.place_forget()

        # Drawing parameters
        bar_width = 20
        max_height = 0
        mt_info = []  # 막대 그래프를 그릴 산의 정보 리스트
        mt_info.clear()
        for mt_n in self.local_mt_list:
            mt_info.append((mt_n, self.Mt_list[mt_n]))
            max_height = max(max_height, float(self.Mt_list[mt_n]))  # 최대 높이 갱신

        canvas_height = 400
        canvas_width = 600
        x_offset = 50
        y_offset = 50

        print(mt_info)
        # Draw bars
        for i, (mt_name, mt_height) in enumerate(mt_info):
            x0 = x_offset + i * 50
            y0 = canvas_height - y_offset
            x1 = x0 + bar_width
            y1 = y0 - (float(mt_height) / max_height) * (canvas_height - 2 * y_offset)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='skyblue')

            # Add mountain names
            self.canvas.create_text((x0 + x1) / 2, y0 + 10, text=mt_name, anchor='n',
                                    font=('Helvetica', 10))

        # Draw axes
        self.canvas.create_line(x_offset, canvas_height - y_offset, canvas_width - x_offset,
                                canvas_height - y_offset, width=2)
        self.canvas.create_line(x_offset, canvas_height - y_offset, x_offset, y_offset, width=2)
        self.canvas.create_text(canvas_width / 2, canvas_height - y_offset + 40, text="산 이름", font=('Helvetica', 12))
        self.canvas.create_text(x_offset - 20, canvas_height / 2, text="높이", font=('Helvetica', 12), anchor='e',
                                angle=90)

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "해당 지역의 산":
            if self.now_g_image:
                self.show_map_image(self.now_g_image)
        elif tab_text == "산의 높이 막대 그래프":

            self.close_map_image()
            self.create_bar_chart()

    def run(self):
        self.window.mainloop()

    def pressedTele(self):
        teller.run()
        pass

if __name__ == "__main__":
    app = Application()
    app.run()


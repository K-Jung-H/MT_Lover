import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import xml_read
import Gmap_Test

class Application:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("등산돌이")
        self.window.geometry("800x700")
        self.local_mt_list = []
        self.mt_info = []
        self.create_widgets()
        self.configure_grid()

    def create_widgets(self):
        # Entry and search button
        self.entry = tk.Entry(self.window, width=20, font=('Helvetica', 16))
        self.entry.grid(row=0, column=0, padx=(20,0), pady=40, ipady=8, sticky='ew')

        self.search_button = tk.Button(self.window, text="검색", font=('Helvetica', 16), command=self.SIGUN_search)
        self.search_button.grid(row=0, column=1, padx=(0,20), pady=40, sticky='w')

        # Notebook with tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[40, 8], font=('Helvetica', 12), bg='black')
        style.map('TNotebook.Tab', background=[('selected', 'lightblue')], foreground=[('selected', 'blue')])

        self.notebook = ttk.Notebook(self.window, style='TNotebook')
        self.notebook.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        self.tab1 = tk.Frame(self.notebook, bg='white')
        self.tab2 = tk.Frame(self.notebook, bg='white')
        self.tab3 = tk.Frame(self.notebook, bg='white')

        self.notebook.add(self.tab1, text="해당 지역의 산")
        self.notebook.add(self.tab2, text="산의 높이 막대 그래프")
        self.notebook.add(self.tab3, text="Tab 3")

        self.listbox1 = self.create_tab_content(self.tab1)
        self.listbox3 = self.create_tab_content(self.tab3)

        # Image placeholder
        self.image_weather = tk.Frame(self.window, bg='lightblue', width=260, height=120)
        self.image_weather.grid(row=0, column=2, padx=50, pady=30, sticky='n')

        self.map_label = tk.Label(self.window)

        # Canvas for bar chart
        self.canvas = tk.Canvas(self.tab2, bg='white', width=600, height=400)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, sticky='n')

        # Bind event to tab2 selection
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        # Create bar chart initially
        self.create_bar_chart()

    def configure_grid(self):
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
    def create_tab_content(self, tab):
        def on_item_select(event):
            selected_index = event.widget.curselection()
            if selected_index:
                selected_item = event.widget.get(selected_index)
                data = xml_read.MT_deap_data(selected_item)
                text_area.delete('1.0', tk.END)

                if data == -1:
                    text_area.insert(tk.END, "산 정보 없음\n")
                elif data and "MT_ADMIN_NUM" in data:
                    text_area.insert(tk.END, f"산 이름 : {data['MT_NAME']}\n")
                    text_area.insert(tk.END, f"산 코드 : {data['MT_CODE']}\n")
                    text_area.insert(tk.END, f"산 위치 : {data['MT_LOCATION']}\n")
                    text_area.insert(tk.END, f"산 높이 : {data['MT_HIGH']}\n")
                    text_area.insert(tk.END, f"산 관리 주체 : {data['MT_ADMIN']}\n")
                    text_area.insert(tk.END, f"산 관리 주체 연락처 : {data['MT_ADMIN_NUM']}\n")

                    img = Gmap_Test.print_map(data["MT_NAME"])
                    self.show_map_image(img)

        label_texts = {
            self.tab1: "Tab 1에 표시할 특정 텍스트",
            self.tab2: "Tab 2에 표시할 다른 특정 텍스트",
            self.tab3: "Tab 3에 표시할 다른 특정 텍스트"
        }
        label = tk.Label(tab, text=label_texts.get(tab, " "), font=('Helvetica', 12), bg='white', fg='black')
        label.grid(row=0, column=0, padx=20, pady=20, sticky='n')

        listbox_frame = tk.Frame(tab, bg='white')
        listbox_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

        listbox = tk.Listbox(listbox_frame)
        listbox.pack(side=tk.LEFT, fill='both', expand=True)
        listbox.bind('<<ListboxSelect>>', on_item_select)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        text_frame = tk.Frame(tab, bg='white', height=100)
        text_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=20)

        text_area = tk.Text(text_frame)
        text_area.pack(fill='both', expand=True)

        self.image_frame = tk.Frame(tab, bg='white', width=600, height=100)
        self.image_frame.grid(row=0, column=1, rowspan=4, sticky='nsew', padx=20, pady=20)

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
        self.map_label.image = tk_img
        self.map_label.place(x=375, y=260)

    def SIGUN_search(self):
        global MT_data
        self.listbox1.delete(0, tk.END)
        search_text = self.entry.get()
        print("검색어:", search_text)
        MT_data = []
        mountain_data = xml_read.MT_data_read(search_text)
        if mountain_data:
            MT_data.append(mountain_data)
            for mountain in MT_data:
                for mountain_name in mountain["mntn_info"]:
                    self.listbox1.insert(tk.END, mountain_name)
                    self.local_mt_list.append(mountain_name)
        print('산 리스트 테스트: ', self.local_mt_list)

    def create_bar_chart(self):
        # Clear canvas before drawing
        self.canvas.delete("all")

        # Drawing parameters
        bar_width = 20
        max_height = 0
        mt_info = []  # 막대 그래프를 그릴 산의 정보 리스트

        for mt in self.local_mt_list:
            data = xml_read.MT_deap_data(mt)
            if data == -1:
                continue
            elif data and "MT_ADMIN_NUM" in data:
                mt_info.append((mt, data['MT_HIGH']))
                max_height = max(max_height, float(data['MT_HIGH']))  # 최대 높이 갱신

        canvas_height = 400
        canvas_width = 600
        x_offset = 50
        y_offset = 50

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
        self.canvas.create_text(canvas_width / 2, canvas_height - y_offset + 40, text="산 이름",  font=('Helvetica', 12))
        self.canvas.create_text(x_offset - 20, canvas_height / 2, text="높이", font=('Helvetica', 12), anchor='e', angle=90)

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "산의 높이 막대 그래프":
            self.create_bar_chart()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
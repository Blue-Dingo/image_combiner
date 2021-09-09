from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox as msgbox
from PIL import Image
import os

root = Tk()
root.title("이미지 합치기")
root.resizable(width=False, height=False)
# root.geometry("480x640")

############################################


class ComboBoxFrame():
    def __init__(self, parent, text, values):
        self.frame = Frame(parent)
        self.label = Label(self.frame, text=text)
        self.label.pack(side="left", anchor="e")
        self.cb = ttk.Combobox(
            self.frame, state="readonly", values=values, width=11)
        self.cb.pack(side="right")
        self.cb.current(0)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


def add_btn_click():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요",
                                        filetypes=(("jpg 파일", "*.jpg"),
                                                   ("모든 파일", "*.*")),
                                        initialdir="C:/")
    for file in files:
        listbox.insert(END, file)


def del_btn_click():
    for index in reversed(listbox.curselection()):
        listbox.delete(index)


def dest_btn_click():
    dir = filedialog.askdirectory(title="저장할 폴더를 선택하세요")
    if not dir:
        return
    dest_entry.delete(0, END)
    dest_entry.insert(END, dir)


def run_btn_clcik():
    if listbox.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return

    if len(dest_entry.get()) == 0:
        msgbox.showwarning("경고", "저장 경로를 선택하세요")
        return
    try:
        combine()
    except Exception as err:
        msgbox.showerror("에러", err)


def get_options():
    opt_width = opt_width_cbf.cb.get()
    opt_space = opt_space_cbf.cb.get()
    opt_format = opt_format_cbf.cb.get()

    opt_width = -1 if opt_width == OPTS[0][1][0] else int(opt_width)
    opt_space = OPTS[1][1].index(opt_space) * OPT_SPACE
    opt_format = "." + opt_format.lower()
    return opt_width, opt_space, opt_format


def combine():
    files = list(listbox.get(0, END))
    images = [Image.open(file) for file in files]
    opt_width, opt_space, opt_format = get_options()

    if opt_width < 0:  # 원본 사이즈 유지
        sizes = [image.size for image in images]
    else:
        sizes = [(opt_width, int(opt_width*image.size[1]/image.size[0]))
                 for image in images]

    widths, heights = zip(*sizes)
    total_height = sum(heights) + opt_space * (len(images)-1)
    max_width = max(widths)

    new = Image.new("RGB", (max_width, total_height), (255, 255, 255))

    offsety = 0
    for index, image in enumerate(images):
        if opt_width > 0:
            image = image.resize(sizes[index])

        new.paste(image, (0, offsety))

        offsety += opt_space+image.size[1]

        pbar_value.set((index+1)/len(images)*100)
        pbar.update()

    dest_folder = dest_entry.get()
    filename = SAVE_NAME + opt_format

    new.save(os.path.join(dest_folder, filename))
    msgbox.showinfo("알림", "작업이 완료되었습니다")


OPTS = [
    ("가로넓이", ["원본유지", "1024", "800", "640"]),
    ("간격", ["없음", "좁게", "보통", "넓게"]),
    ("포맷", ["JPG", "PNG", "BMP"])]

OPT_SPACE = 30
SAVE_NAME = "merged_image"

############################################
# file_frame
file_frame = Frame(root)
file_frame.pack(fill="x", padx=10, pady=10)

add_btn = Button(file_frame, text="파일추가", pady=5,
                 width=20, command=add_btn_click)
add_btn.pack(side="left")
del_btn = Button(file_frame, text="선택삭제", pady=5,
                 width=20, command=del_btn_click)
del_btn.pack(side="right")
############################################
# list frame
list_frame = Frame(root)
list_frame.pack(fill="x", padx=10, pady=10)

listbox = Listbox(list_frame, height=10, selectmode=EXTENDED)
listbox.pack(side="left", fill="x", expand="yes")
sbar = Scrollbar(list_frame, command=listbox.yview)
sbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=sbar.set)

############################################
# dest_frame
dest_frame = LabelFrame(root, text="저장경로")
dest_frame.pack(fill="x", padx=10, pady=5, ipady=10)

dest_entry = Entry(dest_frame)
dest_entry.pack(side="left", fill="x", expand="yes", padx=5, ipady=2)

dest_btn = Button(dest_frame, text="찾아보기", command=dest_btn_click)
dest_btn.pack(side="right", padx=5, ipadx=10)

############################################
# option_frame
option_frame = LabelFrame(root, text="옵션")
option_frame.pack(fill="x", padx=10, pady=5, ipady=10)

opt_width_cbf = ComboBoxFrame(option_frame, *OPTS[0])
opt_width_cbf.pack(side="left", padx=5)

opt_space_cbf = ComboBoxFrame(option_frame, *OPTS[1])
opt_space_cbf.pack(side="left", padx=5)

opt_format_cbf = ComboBoxFrame(option_frame, *OPTS[2])
opt_format_cbf.pack(side="left", padx=5)


# progress_frame
progress_frame = LabelFrame(root, text="진행상황")
progress_frame.pack(fill="x", padx=10, pady=5)

pbar_value = DoubleVar()
pbar = ttk.Progressbar(progress_frame, maximum=100, variable=pbar_value)
pbar.pack(fill="x", padx=10, pady=10)
############################################
quit_btn = Button(root, text="닫기", command=root.quit, width=20)
quit_btn.pack(side="right", anchor="n", padx=10, pady=20)
run_btn = Button(root, text="시작", command=run_btn_clcik, width=20)
run_btn.pack(side="right", anchor="n", pady=20)


############################################
root.mainloop()

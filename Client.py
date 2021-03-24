import tkinter as tk
from tkinter import filedialog
from Main import main


window = tk.Tk()

window.title('Xmind用例生成器')

form_width = [10, 30, 10]
form_height = 2

# 获取屏幕分辨率
def get_screen_size(win):
    return win.winfo_screenwidth(), win.winfo_screenheight()


# 窗口居中
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


center_window(window, 750, 550)
# window.geometry('600x500+600+200')

# 用例生成器标题
big_title = tk.Label(window, text='Xmind用例生成器', bg='green', font=('Arial', 22), width=40, height=3)
big_title.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Xmind文件路径标题
xmind_path_title = tk.Label(window, text='Xmind文件路径：', font=('Arial', 12), width=20, height=2)
xmind_path_title.grid(row=1, column=0, padx=10, pady=10, sticky='E')

# Xmind文件路径输入框
xmind_path_input = tk.Entry(window, show=None, font=('Arial', 14))
xmind_path_input.grid(row=1, column=1, padx=10, pady=10, sticky='E')


# 获取xmind文件路径方法
def get_xmind_file_path():
    xmind_path_input.delete(0, 'end')
    xmind_path = filedialog.askopenfilename()
    xmind_path_input.insert(0, xmind_path)


# Xmind选择按钮
xmind_path_button = tk.Button(window, text='请选择文件路径', width=20, height=1, command=get_xmind_file_path)
xmind_path_button.grid(row=1, column=2, padx=10, pady=10, sticky='E')

# 模块标题
module_title = tk.Label(window, text='模块： ', font=('Arial', 12), width=20, height=2)
module_title.grid(row=2, column=0, padx=10, pady=10, sticky='E')

# 模块输入框
module_input = tk.Entry(window, show=None, font=('Arial', 14))
module_input.grid(row=2, column=1, padx=10, pady=10, sticky='E')

# 用例类型标题
case_type_title = tk.Label(window, text='用例类型： ', font=('Arial', 12), width=20, height=2)
case_type_title.grid(row=3, column=0, padx=10, pady=10, sticky='E')

# 用例类型输入框
case_type_input = tk.Entry(window, show=None, font=('Arial', 14))
case_type_input.grid(row=3, column=1, padx=10, pady=10, sticky='E')

# 适用阶段标题
phase_title = tk.Label(window, text='适用阶段： ', font=('Arial', 12), width=20, height=2)
phase_title.grid(row=4, column=0, padx=10, pady=10, sticky='E')

# 适用阶段输入框
phase_input = tk.Entry(window, show=None, font=('Arial', 14))
phase_input.grid(row=4, column=1, padx=10, pady=10, sticky='E')

# 用例文件路径标题
save_path_title = tk.Label(window, text='用例保存位置： ', font=('Arial', 12), width=20, height=2)
save_path_title.grid(row=5, column=0, padx=10, pady=10, sticky='E')

# 用例文件路径输入框
save_path_input = tk.Entry(window, show=None, font=('Arial', 14))
save_path_input.grid(row=5, column=1, padx=10, pady=10, sticky='E')


def get_save_path():
    save_path_input.delete(0, 'end')
    save_path = filedialog.askdirectory()
    save_path_input.insert(0, save_path)


# 用例文件夹路径选择按钮
save_path_button = tk.Button(window, text='请选择文件夹路径', width=20, height=1, command=get_save_path)
save_path_button.grid(row=5, column=2, padx=10, pady=10, sticky='E')


# 生成Excel方法
def generate_excel():
    xmind_path = xmind_path_input.get()
    module_value = module_input.get()
    case_type_value = case_type_input.get()
    phase_value = phase_input.get()
    save_path_value = save_path_input.get()
    main(xmind_path, save_path_value, module_value, case_type_value, phase_value)


# 生成用例按钮
confirm = tk.Button(window, text='确定生成用例', font=('Arial', 14), width=20, height=1, command=generate_excel)
confirm.grid(row=6, column=1, padx=0, pady=30)

# Main
window.mainloop()

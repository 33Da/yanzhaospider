import tkinter
from tkinter import ttk  # 导入内部包
from spider import SpiderYanZhao



data = None  # 列表的数据

def go():
    """搜索按钮点击事件"""

    #  获取学位代号
    type = typevalue.get()[0:2]


    # 获取学校
    s = school.get()



    global data

    data = spider.major_spider(s,type)


    # 先执行清空之前的item
    x = tree.get_children()
    for item in x:
        tree.delete(item)

    # 下标
    index = 1


    for d in data:
        # 插入数据
        tree.insert("", index, values=(index, d['院系所'], d['专业'],d['研究方向']))
        index = index + 1



def get_detail(event):
    """列表点击事件"""

    # 从('I006',)获取点的是第几个
    item = tree.selection()[0]


    # item 返回这一列的值，取第一个是序号
    index = tree.item(item, "values")[0]


    # 通过序号拿到该列链接
    href = data[int(index)-1]['详情链接']

    # 爬取该页详细信息
    detail_data = spider.deatil_spider(url=href)


    # 新建一个窗口
    win1 = tkinter.Tk()
    # 标题
    win1.title('2020考研加油！！')

    # 学校
    peoplelabel = ttk.Label(win1, text="报考院校: ")
    peoplelabel.grid(row=0, column=0)

    # 学校 数据
    schooldlabel = ttk.Label(win1, text=detail_data["学校"])
    schooldlabel.grid(row=0, column=1)

    # 拟招人数
    peoplelabel = ttk.Label(win1, text="拟招人数: ")
    peoplelabel.grid(row=1, column=0)

    # 拟招人数 数据
    peopledlabel = ttk.Label(win1, text=detail_data["拟招人数"])
    peopledlabel.grid(row=1, column=1)



    # 考试方式
    examlabel = ttk.Label(win1, text="考试方式: ")
    examlabel.grid(row=2, column=0)

    # 考试方式 数据
    peopledlabel = ttk.Label(win1, text=detail_data["考试方式"])
    peopledlabel.grid(row=2, column=1)

    # 考试科目
    exam_sub_label = ttk.Label(win1, text="考试科目: ")
    exam_sub_label.grid(row=3, column=0)

    # 考试科目 数据
    exam_subdlabel = ttk.Label(win1, text=" ".join(detail_data["考试科目"]))
    exam_subdlabel.grid(row=3, column=1)



    win1.mainloop()













def get_types(data):
    """获取到种类"""
    types = []

    for key,value in data.items():
        types.append(key)

    return types



if __name__ == '__main__':
    # 窗口
    win = tkinter.Tk()
    # 标题
    win.title('2020考研加油！！')

    # 实例化爬虫类
    spider = SpiderYanZhao()

    # 种类框
    timelabel = ttk.Label(win, text="专业学位: ")
    timelabel.grid(row=0, column=0)

    # 学位列表框
    typevalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
    comboxlist2 = ttk.Combobox(win, textvariable=typevalue)  # 初始化
    comboxlist2["values"] = ["01哲学类", "02经济类", "03法学类", "04教育学类", "05文学类", "06历史学类", "07理学类", "08工学类", "09农学类", "10医学类",
                             "11军事学", "12管理学", "13艺术类"]
    comboxlist2.current(0)  # 选择第一个
    comboxlist2.grid(row=0, column=1)

    # 学校框
    timelabel = ttk.Label(win, text="学校: ")
    timelabel.grid(row=0, column=2)

    # 学校输入框
    school = ttk.Entry(win)
    school.grid(row=0, column=3)

    # 按钮
    button = ttk.Button(win, text="查询", command=go)
    button.grid(row=0, column=4)

    # 表格
    tree = ttk.Treeview(win, show="headings")  # 表格

    tree["columns"] = ("序号", "院系所", "专业", "研究方向")
    tree.column('序号', width=50, anchor="center")
    tree.column("院系所", width=200, anchor="center")  # 表示列,不显示
    tree.column("专业", width=200, anchor="center")
    tree.column("研究方向", width=300, anchor="center")

    tree.heading('序号', text='序号')
    tree.heading("院系所", text="院系所")  # 显示表头
    tree.heading("专业", text="专业")  # 显示表头
    tree.heading("研究方向", text="研究方向")

    # 绑定列表点击事件
    tree.bind("<Double-Button-1>", get_detail)
    tree.grid(row=2, columnspan=8)

    win.mainloop()
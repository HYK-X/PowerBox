import flet
import json
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
    ListView,
)


class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete, tasklist, completed = False):
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.tasklist = tasklist

    def build(self):
        self.display_task = Checkbox(
            value=self.completed, label=self.task_name, on_change=self.status_changed,
        )#复选框控件
        self.edit_name = TextField(expand=1)#文本框控件
        #基础 控件
        self.display_view = Row(
            #对齐调整
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="更改",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="删除",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        #更改时显示
        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="更新",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Column(controls=[self.display_view, self.edit_view])
    # 定义更改按钮点击事件
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        #可视处理
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()
    # 定义保存按钮点击事件
    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value#向复选框传值 更改任务名称
        self.tasklist[hash(self)][0] = self.edit_name.value#更改存储文件中任务名称
        # 可视处理
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
    #定义状态改变事件
    def status_changed(self, e):
        self.completed = self.display_task.value
        self.tasklist[hash(self)][1] = self.display_task.value#将任务完成状态储存
        self.task_status_change(self)#任务更新
    # 定义删除按钮点击事件
    def delete_clicked(self, e):
        self.tasklist.pop(hash(self))#删除存储中该任务
        self.task_delete(self)#删除


class TodoApp(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.tasklist = {}#创建字典

    def build(self):
        self.new_task = TextField(hint_text="你需要做什么", expand=True,)#定义文本框 #todo字符数超过35导致按钮暴毙
        self.tasks = Column()#定义列

        self.filter = Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=self.tabs_changed,
            tabs=[Tab(text="全部"), Tab(text="未完成"), Tab(text="已完成")],
        )#定义选择框

        self.items_left = Text("你已经完成所有任务了")#左下角文本
        #返回打包好的页面
        return Column(
            width=600,
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="清除已完成", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    #添加按钮点击事件
    def add_clicked(self, e):
        if self.new_task.value:#判断任务名是否为空
            task = Task(self.new_task.value, self.task_status_change, self.task_delete, self.tasklist)
            self.tasklist[hash(task)] = [self.new_task.value, False]#将task的哈希作为键 task的任务名和状态作为值
            self.tasks.controls.append(task)#向页面的tasks列加入任务
            self.new_task.value = ""#清空文本框内字符
            self.update()
    #task状态改变事件
    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.tasklist.pop(hash(task))#删除存储中该任务
                self.task_delete(task)#删除任务
    #自写更新模块 添加计数和选择器功能
    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "全部"
                or (status == "未完成" and task.completed == False)
                or (status == "已完成" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"还剩{count}未完成 "
        super().update()
    #存储任务保存控件
    def save(self):
        file = open("./data/todo.json",mode = "w")
        file.write(json.dumps(self.tasklist))
        file.close()
    #文件加载控件
    def load(self):
        file = open("./data/todo.json",mode = "r")
        self.tasklist=json.loads(file.read())
        file.close()
        temp = []
        #遍历存储内容 task任务名和状态
        for item in self.tasklist.values():
            temp.append(item)
        self.tasklist.clear()#清除列表中所有内容
        #遍历缓存中所有存储内容
        for item in temp:
            task = Task(item[0], self.task_status_change, self.task_delete, self.tasklist, item[1])
            #重新赋值并更新页面
            self.tasklist[hash(task)] = [item[0], item[1]]
            self.tasks.controls.append(task)
            self.update()
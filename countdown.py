import flet as ft
import datePicker
import datetime
import json

#打包Task部分
class Task(ft.UserControl):
    def __init__(self, name, date, sup):
        super().__init__()
        self.name = name
        self.date = date
        self.sup = sup
        self.tasklist = sup.tasklist

    def modify(self,e):
        self.sup.task_modify(self)

    def delete(self,e):
        self.sup.task_del(self)

    def build(self):
        modifyButton = ft.PopupMenuItem(icon=ft.icons.CREATE_OUTLINED,text="编辑",on_click=self.modify)
        self.list = ft.ListTile(
                            leading=ft.Icon(name=ft.icons.SNOOZE,color="red" if (self.date.__ge__(datetime.date.today())) else "green"),
                            title=ft.Text(self.name),
                            subtitle=ft.Text(f"{self.date} | {'还剩下' if((self.date-datetime.date.today()).days>=0) else '已过去'}{abs((self.date-datetime.date.today()).days)}天"),
                            trailing=ft.PopupMenuButton(
                                tooltip = "菜单",
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    modifyButton,
                                    ft.PopupMenuItem(icon=ft.icons.DELETE_OUTLINE,text="删除",on_click=self.delete),
                                ],
                            ),
                        )
        return self.list

class Countdown(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.modifyTask = None
        self.tasklist = {}  # 创建字典
    #task更改事件
    def task_modify(self,task):
        self.page.dialog = self.dlg
        self.page.update()
        self.modifyTask = task
        self.modiText.value = task.name
        self.tasklist[hash(task)][0] = self.modiText.value
        self.modiDate.set(task.date)
        self.dlg.open = True
        self.page.update()
    #task删除事件
    def task_del(self,task):
        self.list.controls.remove(task)
        self.tasklist.pop(hash(task))
        self.update()
    #task添加事件
    def add(self, e):
        date = self.adddate.content.get_date()
        d_data = [date.year,date.month,date.day]
        name = self.new_countdownday.value
        if(date != None and name != ""):
            task=Task(name,date,self,)
            self.list.controls.append(task)
            self.tasklist[hash(task)] = [name, d_data]
            self.adddate.content.clear()
            self.new_countdownday.value=""
        elif(name == ""):
            self.warning.content.value = "请输入内容!"
            self.warning.open = True
            self.page.update()
        else:
            self.warning.content.value = "请输入时间!"
            self.warning.open = True
            self.page.update()
        self.update()
    #标签更改事件
    def tabs_changed(self, e):
        self.update()
    #dlg关闭事件
    def close_dlg(self,e):
        self.dlg.open = False
        self.modiText.value = ""
        self.modiDate.clear()
        self.modifyTask.update()
        self.page.update()
        self.update()
        self.modifyTask = None
    #更改信息事件
    def change_info(self,e):
        name = self.modiText.value
        date = self.modiDate.get_date()
        if (date != None and name != ""):
            self.update()
            self.modifyTask.name = name
            self.modifyTask.date = date
            d_data = [date.year, date.month, date.day]
            self.tasklist[hash(self.modifyTask)] = [name, d_data]
            self.modifyTask.controls[0].leading = ft.Icon(name=ft.icons.SNOOZE, color="red" if (
                self.modifyTask.date.__ge__(datetime.date.today())) else "green")
            self.modifyTask.controls[0].title = ft.Text(self.modifyTask.name)
            self.modifyTask.controls[0].subtitle = ft.Text(
                f"{self.modifyTask.date} | {'还剩下' if ((self.modifyTask.date - datetime.date.today()).days >= 0) else '已过去'}{abs((self.modifyTask.date - datetime.date.today()).days)}天")
            self.dlg.open = False
            self.modiText.value = ""
            self.modiDate.clear()
            self.modifyTask.update()
            self.page.update()
            self.update()
            self.modifyTask = None

        elif (name == ""):
            self.warning.content.value = "请输入内容!"
            self.warning.open = True
            self.page.update()
        else:
            self.warning.content.value = "请输入时间!"
            self.warning.open = True
            self.page.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.list.controls:
            task.visible = (
                status == "全部"
                or (status == "倒数日" and (task.date-datetime.date.today()).days >=0)
                or (status == "正数日" and (task.date-datetime.date.today()).days < 0)
            )
        super().update()
    #保存
    def save(self):
        file = open("./data/countdown.json",mode = "w")
        file.write(json.dumps(self.tasklist))
        file.close()

    def load(self):
        file = open("./data/countdown.json",mode = "r")
        self.tasklist=json.loads(file.read())
        file.close()
        temp = []
        for item in self.tasklist.values():
            temp.append(item)
        self.tasklist.clear()#清除列表中所有内容
        #遍历缓存中所有存储内容
        for item in temp:
            date = datetime.date(item[1][0],item[1][1],item[1][2])
            task = Task(item[0],date,self)
            #重新赋值并更新页面
            self.tasklist[hash(task)] = [item[0], item[1]]
            self.list.controls.append(task)
            self.update()

    def build(self):
        self.new_countdownday =  ft.TextField(hint_text="倒数日名", expand=True,content_padding=28,text_size=20)
        self.addButton = ft.FloatingActionButton(icon=ft.icons.ADD,width = 82,height = 82,on_click = self.add)
        self.adddate = ft.Container(content = datePicker.DateSelector(),)

        self.filter = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="全部"), ft.Tab(text="正数日"), ft.Tab(text="倒数日")],
        )

        self.modiText = ft.TextField()
        self.modiDate = datePicker.DateSelector()

        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("编辑"),
            content=ft.Column(
                height = 200,
                #alignment=ft.MainAxisAlignment.BEGIN,
                controls=[
                    ft.Text("新名称"),
                    self.modiText,
                    ft.Text("新日期"),
                    self.modiDate,
                    ft.Text("                                                                       "),
                ]
            ),
            actions=[
                ft.TextButton("确定", on_click=self.change_info),
                ft.TextButton("取消", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dlg

        self.adddate.border_radius = ft.border_radius.all(10)
        self.adddate.border=ft.border.all(1, ft.colors.BLACK)
        self.warning = ft.SnackBar(content=ft.Text(" "),
                                   action="好的",
                                   action_color = "blue400"
                                      )
        self.page.snack_bar = self.warning
        self.dayaddRow=ft.Container(
            # padding = ft.padding.symmetric(horizontal = 280),
            content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.new_countdownday,
                self.adddate,
                self.addButton
                ],
            )
        )
        self.list=ft.Column()
        self.view=ft.Column(
            width=700,
            controls=[
                self.dayaddRow,
                self.filter,
                self.list
                      ],
        )
        return [self.view]


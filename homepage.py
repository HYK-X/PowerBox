import todo#导入todos模块
import pomo#导入番茄钟模块
import countdown#导入导数日模块
import flet as ft#导入ft模块
import os
import easywebdav
#创建专有的主页按钮类方便按钮创建
class HomepageButton(ft.UserControl):
    def __init__(self,icon,text,click_func):
        super().__init__()#使其可调用父类全部方法
        #参数获取
        self.icon = icon
        self.text = text
        self.click_func = click_func
    #构建函数
    def build(self):
        self.expand = True#可扩展
        return ft.ElevatedButton(
                on_click=self.click_func,
                #建立一个列模块
                content = ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,#主轴中心对齐

                    controls=[
                        #图标模块
                        ft.Container(
                            content=ft.Icon(name = self.icon, color = "blue400", size = 50),
                            alignment = ft.alignment.center
                        ),
                        # 文字模块
                        ft.Container(
                            content=ft.Text(value = self.text),
                            alignment=ft.alignment.center
                        ),
                    ]
                ),
                #创建主题
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius=20),#设置圆角
                    padding = ft.padding.symmetric(vertical = 200),#设置垂直方向按钮内部 上下空隙200px
                )
        )

atMainpage = True

def Homepage(page:ft.Page):
    isClosing = [False,False] #主页面传递关闭信号 用于关闭番茄钟线程

    #按钮更新模块
    def updateButton(button):
        buttonSize = 200 + (page.window_height - default_height)/2 #自适应按钮纵坐标
        button.controls[0].style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius=20),#设置圆角
                    padding = ft.padding.symmetric(vertical = buttonSize),#设置垂直方向按钮内部 上下空隙200px
                )
        button.update()#按钮更新
    #检测是否需要更新按钮
    def onWindowEvent(e):
        global atMainpage
        if(e.data != "close" and atMainpage):
            updateButton(todoButton)
            updateButton(pomodoroButton)
            updateButton(countdownButton)
        if(e.data == "close"):
            if(not atMainpage):
                animation.content.save()
            page.window_destroy()

    #页面切换模块
    def changePage(e):
        global atMainpage
        atMainpage = False#是否在主页状态调为否
        returnButton.visible = True#返回按钮可视
        #主页面按键监听
        if e.control == todoButton.controls[0]:
            animation.content = todo.TodoApp(page)
            mainTitle.value = "ToDo"
            page.update()
        elif e.control == pomodoroButton.controls[0]:
            animation.content = pomo.tmclock(page, isClosing)
            mainTitle.value = "番茄钟"
            page.update()
        elif e.control == countdownButton.controls[0]:
            animation.content = countdown.Countdown(page)
            mainTitle.value = "倒数日"
            page.update()
        animation.content.load()
    #返回主页面事件
    def returnPage(e):
        global atMainpage
        atMainpage = True#是否在主页状态调为是
        returnButton.visible = False#返回按钮不可视
        if(isClosing[1]):
            isClosing[0] = True
            while(isClosing[0]):
                pass
        isClosing[1]=False
        animation.content.save()
        animation.content = home#切换回主页面
        mainTitle.value = "效率盒"
        page.update()

    def showSetting(e):
        page.dialog = settingdlg
        settingdlg.open = True
        page.update()

    def change_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if(e.control.value==False) else ft.ThemeMode.DARK
        page.update()

    def close_dlg(e):
        settingdlg.open = False
        page.update()

    def change_setting(e):

        close_dlg(e)
    #设置页面
    # settingslist=[False,0,0]
    loginStatusText=ft.Text("  链接状态：未连接")
    # loginTextField=ft.TextField(label="坚果云同步账号")
    # passwordTextField=ft.TextField(label="坚果云应用密码")
    # loginButton=ft.ElevatedButton("登录")
    # cloudButton=ft.ElevatedButton("从云端同步本地", disabled=True)
    themeSwich=ft.Switch(label="深色主题", value=False,on_change=change_theme)
    settingdlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("设置"),
        content=ft.Column(
            height=30,#单机高度
            # height=280,#云同步高度
            controls=[
                themeSwich,
                # loginTextField,
                # passwordTextField,
                # loginStatusText,
                # ft.Row(
                #     controls=[
                #         loginButton,
                #         cloudButton,
                #     ]
                # ),
            ]
        ),
        actions=[
            ft.TextButton("确定", on_click=change_setting),
            ft.TextButton("取消", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.horizontal_alignment = "center"#页面对齐设置
    page.scroll = "adaptive"#滚动条设置
    page.update()#更新页面
    default_height = page.window_height#页面高度获取
    returnButton = ft.FloatingActionButton(
        icon = ft.icons.KEYBOARD_RETURN,
        on_click = returnPage,
        visible = False
    )
    page.on_window_event = onWindowEvent
    page.window_prevent_close = True
    page.client_storage.clear()


    #字体设置
    #按钮定义
    page.title = "效率盒"
    page.fonts = {"HarmonyOS": "/fonts/HarmonyOS_Sans_SC_Regular.ttf"}
    page.theme = ft.Theme(font_family="HarmonyOS")
    page.dark_theme = ft.Theme(font_family="HarmonyOS")
    page.floating_action_button = returnButton#返回按钮
    mainTitle = ft.Text(value="效率盒",style="headlineMedium",size=45)#左上标题
    #三个主页面按钮定义
    todoButton = HomepageButton(ft.icons.PENDING_ACTIONS_ROUNDED,"ToDo",changePage)
    pomodoroButton = HomepageButton(ft.icons.TIMER_SHARP,"番茄钟",changePage)
    countdownButton = HomepageButton(ft.icons.CALENDAR_MONTH_ROUNDED, "倒数日",changePage)
    #主页下方 三个按钮打包
    home = ft.Container(
            padding=ft.padding.symmetric(horizontal=40, vertical=20),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    todoButton,
                    pomodoroButton,
                    countdownButton,
                ]
            )
        )
    #切换 动画控件  负责下方动画打包
    animation = ft.AnimatedSwitcher(
        reverse_duration = 0,
        content = home
    )
    #程序整个节目控件打包
    mainColumn = ft.Column(
        controls=[
            ft.Container(#上方标题和设置按钮打包
                padding = ft.padding.symmetric(horizontal = 40,vertical = 20),
                content = ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        mainTitle,
                        ft.IconButton(#设置按钮
                            icon=ft.icons.SETTINGS_ROUNDED,
                            icon_color="blue400",
                            icon_size=30,
                            tooltip="设置",
                            on_click = showSetting
                        )
                    ]
                )
            ),
            ft.Container(
                content = animation,
                alignment=ft.alignment.center,
            )

        ]
    )

    page.add(mainColumn)


#文件创建
if(not os.path.exists("./data")):
    os.mkdir("./data")
if(not os.path.isfile("./data/todo.json")):
    f = open("./data/todo.json", mode = "w")
    f.write("{}")
    f.close()
if (not os.path.isfile("./data/pomo.json")):
    f = open("./data/pomo.json", mode = "w")
    f.write("{}")
    f.close()
if (not os.path.isfile("./data/countdown.json")):
    f = open("./data/countdown.json", mode = "w")
    f.write("{}")
    f.close()
# if (not os.path.isfile("./data/settings.json")):
#     f = open("./data/settings.json", mode = "w")
#     f.write("{}")
#     f.close()


ft.app(target=Homepage,assets_dir="assets")

#导入库
import flet as ft
import threading as th
import time as t
import math
import json

class tmclock(ft.UserControl):
    def __init__(self,page,isClosing):
        super().__init__()
        self.page = page
        self.isClosing = isClosing
    #定义分秒按钮和文本框转换
    def setMin(self,e):
        self.text_min.value = self.time_min.content.value
        self.time_min.visible = False
        self.text_min.visible = True
        self.text_min.focus()
        self.update()

    def setSec(self,e):
        self.text_sec.value = self.time_sec.content.value
        self.time_sec.visible = False
        self.text_sec.visible = True
        self.text_sec.focus()
        self.update()

    # 定义分秒按钮和文本框转换
    def finishMin(self,e):
        value = self.text_min.value
        if(value==""):
            value = "00"
        self.time_min.content.value = value.zfill(2)
        self.time_min.visible = True
        self.text_min.visible = False
        self.update()

    def finishSec(self,e):
        value = self.text_sec.value
        if(value==""):
            value = "00"
        self.time_sec.content.value = value.zfill(2)
        self.time_sec.visible = True
        self.text_sec.visible = False
        self.update()
    #数字检测
    def numberCheck(self,e):
        if((not e.data.isdigit())and(e.data!="")):
            e.control.value = ""
            self.warning.content.value = "请输入数字!"
            self.warning.open = True
            self.update()
            self.page.update()
    #读秒
    def cutTime(self,event):
        while(self.start and not self.isClosing[0]):
            self.work = True
            self.status.value = "番茄时间"
            self.clock.content.color = "#f0c9cf"
            self.clock.content.bgcolor = "#ee3f4d"
            self.update()

            secCount = self.workCount

            while(secCount > 1 and self.start and not self.isClosing[0]):
                if(self.pause):
                    event.wait()
                    event.clear()
                secCount -= 0.1
                self.pomo_time += 0.1
                min, sec = divmod(secCount, 60)
                self.time_min.content.value = str(math.floor(min)).zfill(2)
                self.time_sec.content.value = str(math.floor(sec)).zfill(2)
                self.clock.content.value = 1-(secCount-1)/(self.workCount-1)
                self.update()
                t.sleep(0.1)



            if (not self.start):
                return

            self.update()
            self.Pause(None)
            self.clockaudio.play()

            self.work = False
            self.status.value = "休息时间"
            self.clock.content.bgcolor = "#2b73af"
            self.clock.content.color = "#baccd9"
            self.update()

            secCount = self.restCount
            while(secCount > 1 and self.start and not self.isClosing[0]):
                if(self.pause):
                    event.wait()
                    event.clear()
                secCount -= 0.1
                self.rest_time+=0.1
                min, sec = divmod(secCount, 60)
                self.time_min.content.value = str(math.floor(min)).zfill(2)
                self.time_sec.content.value = str(math.floor(sec)).zfill(2)
                self.clock.content.value = 1-(secCount-1)/(self.restCount-1)
                self.update()
                t.sleep(0.1)
            self.update()
            self.Pause(None)
            self.clockaudio.play()

        self.isClosing[0] = False
        self.time_sec.content.value = "00"
        self.time_min.content.value = "00"
        self.text_sec.value = "00"
        self.text_min.value = "00"
    #继续控件
    def Continue(self,e):
        self.workCount = int(self.time_sec.content.value) + int(self.time_min.content.value) * 60 + 1
        if(self.workCount == 1):
            self.warning.content.value = "你输入的时间太短了，请重新输入!"
            self.warning.open = True
            self.page.update()
            return
        self.buttonData.visible = False
        self.buttonContinue.visible = False
        self.buttonStart.visible = True
        self.time_sec.content.value = "00"
        self.time_min.content.value = "00"
        self.text_sec.value = "00"
        self.text_min.value = "00"
        self.status.value = "休息时间"
        self.clock.content.bgcolor = "#2b73af"
        self.clock.content.color = "#baccd9"
        self.update()

    def showData(self,e):
        self.page.dialog = self.dlg
        pomo_min,pomo_sec = divmod(self.pomo_time,60)
        rest_min, rest_sec = divmod(self.rest_time, 60)
        self.dlg.content.value = f"您的番茄时间为：{int(pomo_min)}分{int(pomo_sec)}秒，" \
                                 f"您的休息时间为：{int(rest_min)}分{int(rest_sec)}秒。"
        self.dlg.open = True
        self.page.update()

    def Start(self,e):
        if(self.work):
            self.status.value = "番茄时间"
            self.clock.content.color = "#f0c9cf"
            self.clock.content.bgcolor = "#ee3f4d"
        else:
            self.status.value = "休息时间"
            self.clock.content.bgcolor = "#2b73af"
            self.clock.content.color = "#baccd9"
        if(not self.start):
            self.restCount = int(self.time_sec.content.value) + int(self.time_min.content.value) * 60 + 1
            if (self.restCount == 1):
                self.warning.content.value = "你输入的时间太短了，请重新输入!"
                self.warning.open = True
                self.page.update()
                return
            self.start = True
            self.timer = th.Thread(target=self.cutTime,daemon=True,args=(self.event,))
            self.timer.start()
            self.isClosing[1]=True
        else:
            self.pause = False
            self.event.set()
        self.buttonStart.visible = False
        self.buttonPause.visible = True
        self.buttonStop.visible = True
        self.time_min.disabled = True
        self.time_sec.disabled = True
        self.update()

    def Pause(self,e):
        self.buttonStart.visible = True
        self.buttonPause.visible = False
        self.buttonStop.visible = True
        self.pause = True
        self.update()

    def Stop(self,e):
        self.Start(None)
        self.buttonContinue.visible = True
        self.buttonData.visible = True
        self.buttonStart.visible = False
        self.buttonPause.visible = False
        self.buttonStop.visible = False
        self.start = False
        self.isClosing[1] = False
        self.status.value = "番茄时间"
        self.clock.content.color = "#f0c9cf"
        self.clock.content.bgcolor = "#ee3f4d"
        self.clock.content.value = None
        self.time_min.disabled = False
        self.time_sec.disabled = False
        self.work = True
        self.time_sec.content.value = "00"
        self.time_min.content.value = "00"
        self.text_sec.value = "00"
        self.text_min.value = "00"
        self.update()

    def close_dlg(self,e):
        self.dlg.open = False
        self.page.update()

    def save(self):
        self.pomodata=[self.pomo_time,self.rest_time]
        file = open("./data/pomo.json",mode = "w")
        file.write(json.dumps(self.pomodata))
        file.close()

    def load(self):
        file = open("./data/pomo.json", mode="r")
        self.pomodata=json.loads(file.read())
        self.pomo_time = self.pomodata[0]
        self.rest_time = self.pomodata[1]
        file.close()
        self.pomodata = [0,0]

    def build(self):
        self.pomo_time=0
        self.rest_time=0
        self.event = th.Event()
        self.pause = False
        self.start = False
        self.work = True
        self.clockaudio = ft.Audio(
            src="./assets/audio/clock.mp3",
        )
        self.clock = ft.Container(
            alignment=ft.alignment.center,
            content = ft.ProgressRing(width=500, height=500, stroke_width=25,bgcolor="#f0c9cf",color="#ee3f4d")
        )
        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("记录"),
            content=ft.Text(f"您的番茄时间为：{self.pomo_time}，您的休息时间为：{self.rest_time}。"),
            actions=[
                ft.TextButton("好的", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.status = ft.Text(value="番茄时间",size=50)
        self.time_min = ft.TextButton(content=ft.Text(value="00",size=100),on_click = self.setMin)
        self.time_sec = ft.TextButton(content=ft.Text(value="00",size=100),on_click = self.setSec)
        self.text_min = ft.TextField(
            hint_text="分钟",
            max_length=2,
            width=150,
            counter_text=" ",
            text_size=60,
            visible=False,
            on_blur=self.finishMin,
            on_change=self.numberCheck,
            keyboard_type="number",
        )
        self.text_sec = ft.TextField(
            hint_text="秒数",
            max_length=2,
            width=150,
            counter_text=" ",
            text_size=60,
            visible=False,
            on_blur=self.finishSec,
            on_change=self.numberCheck,
            keyboard_type="number",
        )
        self.buttonContinue = ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS_ROUNDED,
                                         visible=True,
                                         icon_size = 50,
                                         on_click=self.Continue
                                         )
        self.buttonData = ft.IconButton(icon=ft.icons.NOTES_ROUNDED,
                                         visible=True,
                                         icon_size = 50,
                                         on_click=self.showData
                                         )
        self.buttonStart = ft.IconButton(icon=ft.icons.PLAY_ARROW_ROUNDED,
                                         visible=False,
                                         icon_size = 50,
                                         on_click=self.Start
                                         )
        self.buttonPause = ft.IconButton(icon=ft.icons.PAUSE_ROUNDED,
                                         visible=False,
                                         icon_size = 50,
                                         on_click = self.Pause
                                         )
        self.buttonStop = ft.IconButton(icon=ft.icons.STOP_ROUNDED,
                                        visible=False,
                                        icon_size = 50,
                                        on_click = self.Stop
                                        )
        self.warning = ft.SnackBar(content=ft.Text(" "),
                                   action="好的",
                                   action_color = "blue400"
                                      )
        self.page.snack_bar = self.warning
        col = ft.Container(
            padding = 100,
            content = ft.Column(
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 20,
            controls = [
                    self.status,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls = [
                        self.time_min,
                        self.text_min,
                        ft.Text(":",size=100),
                        self.time_sec,
                        self.text_sec
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls = [
                        self.buttonContinue,
                        self.buttonData,
                        self.buttonStart,
                        self.buttonPause,
                        self.buttonStop,
                        ]
                    )
                ]
            )
        )
        return [self.clock,col,self.clockaudio]
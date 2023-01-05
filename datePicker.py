import flet
import datetime
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
    Dropdown,
    dropdown,
    Container,
    Icon
)
class DateSelector(UserControl):
    """Date selector."""
#修复 月份日期bug
    def __init__(self):
        super().__init__()
        self.months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
        self.year_dropdown = Dropdown(
            label="年",
            options=[
                dropdown.Option(year) for year in range (2022, datetime.date.today().year + 50)
            ],
            width=100,
            on_change = self.set_year
        )

        self.month_dropdown = Dropdown(
            label="月",
            options=[
                dropdown.Option(month) for month in range (1, 13)
            ],
            width=50,
            on_change= self.set_month,
            visible= False
        )

        self.day_dropdown = Dropdown(
            label="日",

            width=50,
            visible = False
        )


        self.view = Container(
            content=Row(
                [
                    Icon(
                        icons.CALENDAR_MONTH,
                    ),
                    self.year_dropdown,
                    self.month_dropdown,
                    self.day_dropdown,
                ],
                alignment="center",
            ),
            padding=10,
        )
    def set_year(self,e):
        self.month_dropdown.visible = True

        if (int(self.year_dropdown.value) % 4 == 0 and int(self.year_dropdown.value) % 100 != 0):
            self.months[2] = 29
        else:
            self.months[2] = 28
        self.update()

    def set_month(self,e):
        self.day_dropdown.visible = True
        self.day_dropdown.options.clear()
        self.day_dropdown.options = [
              dropdown.Option(day) for day in range(1, self.months[int(self.month_dropdown.value)]+1)
          ]
        self.update()

    def build(self):
        return self.view

    def clear(self):
        self.year_dropdown.value = None
        self.month_dropdown.value = None
        self.day_dropdown.value = None
        self.update()

    def set(self,date):
        self.year_dropdown.value = date.year
        self.month_dropdown.value = date.month
        self.day_dropdown.value = date.day
        self.update()

    def get_date(self):
        """Return the selected timeframe."""
        if(self.year_dropdown.value == None or self.month_dropdown.value == None or self.day_dropdown.value ==None):
            return None
        else:
            date = datetime.date(
                year=int(self.year_dropdown.value),
                month=int(self.month_dropdown.value),
                day=int(self.day_dropdown.value),
            )
            return date
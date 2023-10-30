import json
from time import sleep

from kivymd.uix.snackbar import BaseSnackbar
from kvdroid.jclass.android.graphics import Color
from kvdroid.tools.notification import create_notification
from kvdroid.tools import get_resource
from kvdroid.tools import share_text
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.button import MDFlatButton

from main import Tasksivate
from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)


class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")


while True:
    try:
        with open('tasks-file.json') as json_file:
            data = json.load(json_file)

        for task_data in data['task_body']:
            category = task_data['category']
            title = task_data['title']
            description = task_data['description']
            completed_tasks_count = task_data['completed_tasks_count']
            total_tasks_count = task_data['total_tasks_count']
            end_date = task_data['end_date']
            task_time = task_data["time"]

            from datetime import datetime, date

            # ... (continue with the remaining code to display the task data)
            # Convert the string to a datetime object
            date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            given_date = date_obj.date()
            todays_date = date.today()

            # Get the weekday name
            weekday = date_obj.strftime("%a")
            # Get the month, date, and day
            month = date_obj.strftime("%b")  # Full month name
            day = date_obj.strftime("%a")  # Full weekday name
            date = date_obj.strftime("%d")  # Day of the month (with leading zero)
            # Get the formatted date
            formatted_date = date_obj.strftime("%A, %d")
            current_time = datetime.now().time()
            if given_date == todays_date and task_time == current_time:
                create_notification(
                    small_icon=get_resource("drawable").ico_nocenstore,  # app icon
                    channel_id="1", title="Task Reminder",
                    text=f"It's time for {title} \n {description}",
                    ids=1, channel_name=f"ch1",
                    large_icon="store/mylogo",
                    expandable=False,
                    small_icon_color=Color().rgb(0x00, 0xC8, 0x53),  # 0x00 0xC8 0x53 is same as 00C853
                    big_picture="store/mylogo"
                )
                # plyer.notification.notify(title='Task Reminder!', message=f"It's time for {title} \n {description}",
                #                           app_name='Tasksivate', app_icon='store/app-icon.ico', timeout=10)
                snackbar = CustomSnackbar(
                    text=f"It's time for {title}",
                    icon="information",
                    pos_hint={"center_y": .95},
                    buttons=[MDFlatButton(text="ACTION", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
                )
                snackbar.open()
    except:
        pass
    print("service running.....")
    sleep(5)

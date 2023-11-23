import json
from datetime import datetime, date
from kvdroid.jclass.android.graphics import Color
from kvdroid.tools.notification import create_notification
from kvdroid.tools import get_resource


def send_notification(title, text, extras=None):
    # Create a notification using the code from the first snippet
    try:
        ids = 1
        ids += 1
        create_notification(
            small_icon=get_resource("mipmap").icon,
            channel_id="ch1",
            title=title,
            text=text,
            ids=ids,
            channel_name=f"It's Important! to perform this task",
            large_icon="store/myicon.png",
            small_icon_color=Color().rgb(0x00, 0xC8, 0x53),
            big_picture="store/myicon.png",
            action_title1="action1",
            reply_title="reply",
            key_text_reply="TEST_KEY",
            extras=extras,
        )

    except:
        pass


def get_notification():
    try:
        notified_tasks2 = []
        notification_id = 1
        with open('tasks-file.json') as json_file:
            data = json.load(json_file)
        current_time = datetime.now().strftime("%I:%M %p")
        for task_data in data['task_body']:
            task_id = task_data['id']
            if task_id not in notified_tasks2:
                todays_date = date.today()
                title = task_data['title']
                tasks = task_data['tasks']
                description = task_data['description']
                start_date = task_data['start_date']
                end_date = task_data['end_date']
                task_time = task_data["time"]
                if start_date == str(todays_date):
                    notification_id += 1
                    send_notification(title=f"Reminder! {title} starts Today!", text=f"{description}")

    except:
        pass

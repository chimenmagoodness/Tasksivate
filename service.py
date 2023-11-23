from time import sleep
from jnius import autoclass
from edit_notifier import edit_task_notification
from notification1 import get_notification
from notification2 import get_notification2
from current_notification import get_current_notification


# Get the current service instance
PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

while True:
    # Call the functions from the service class, or schedule them with Clock
    print("service running.....")
    get_notification()
    get_notification2()
    get_current_notification()
    edit_task_notification()
    sleep(8)

from time import sleep
from main import Tasksivate
from jnius import autoclass

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)


while True:
    Tasksivate.get_current_notification()
    print("service running.....")
    sleep(5)
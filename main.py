import json
import os
import tempfile

import plyer as plyer
from kivmob import KivMob
from kivymd.uix.label import MDLabel, MDIcon
from matplotlib import pyplot as plt
from kivy.uix.image import Image, AsyncImage
from datetime import datetime
from random import randrange
import random
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty, ColorProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.utils import QueryDict, rgba
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import FakeRectangularElevationBehavior, CircularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.list import OneLineIconListItem, MDList, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.textfield import MDTextField
from kivy.utils import get_color_from_hex as hex_to_rgba
from kivy import platform
# from kivy.properties import NumericProperty, ObjectProperty, StringProperty, ListProperty, ColorProperty
# Window.size = (310, 620)


class Tasksivate(MDApp):
    main_primary_color = ColorProperty(hex_to_rgba("#7057BB"))
    main_theme_color = ColorProperty(hex_to_rgba("#FFFFFF"))
    main_accent_color = ColorProperty([1, 170/255, 23/255, 1])
    main_texture = ColorProperty(hex_to_rgba("#EBEBEB"))
    ads = KivMob('ca-app-pub-4268254501946298~4518366608')
    theme_color = ""
    tasks = ""
    notes = ""
    nav_icon_color = ColorProperty(hex_to_rgba("#DFD7F3"))
    weight = NumericProperty(12)
    age = NumericProperty(18)
    note_image_list = []
    accent_colors = ""
    primary_colors = ""
    dark_themes = ""
    textures = ""
    category = ""
    total_task = 0
    ErrorNetwork = False
    enter = ""
    category_text = ""
    error_dialog = None
    confirmation_dialog = None
    show_cate_dialog = None
    cate_dialog = None
    fonts = QueryDict()
    value = ""
    cat_mgn_dialog = None
    todo_dialog = None
    task_dialog = None
    todo_count = 0
    progress_count = 0
    completed_count = 0
    completed_tasks = []
    completed_tasks_count = 0
    uncompleted_tasks_count = 0
    uncompleted_tasks = []
    fonts.size = QueryDict()
    fonts.size.extra = dp(20)
    fonts.size.hello = dp(40)
    fonts.size.h1 = dp(24)
    fonts.size.h2 = dp(22)
    fonts.size.h3 = dp(18)
    fonts.size.h4 = dp(16)
    fonts.size.h5 = dp(14)
    fonts.size.h6 = dp(12)
    range = []
    todo_list = []
    todo_time = ""
    min_date = None
    max_date = None
    loading_dialog = None
    user_store = JsonStore('user_details.json')
    fonts.heading = 'fonts/Inter/Inter-Bold.otf'
    fonts.subheading = 'fonts/Roboto/Roboto-Medium.ttf'
    fonts.body = 'fonts/Roboto/Roboto-Regular.ttf'
    fonts.styled = 'fonts/Lobster/Lobster-Regular.ttf'

    fonts.poppinsbold = "Poppins/Poppins-Bold.ttf"
    fonts.poppinslight = "Poppins/Poppins-Light.ttf"
    fonts.poppinsmedium = "Poppins/Poppins-Medium.ttf"
    fonts.poppinsregular = "Poppins/Poppins-Regular.ttf"
    fonts.poppinssemibold = "Poppins/Poppins-SemiBold.ttf"
    fonts.BelieveIt = "Poppins/BelieveIt-DvLE.ttf"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)
        user_store = JsonStore('user_details.json')
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        self.note_file_manager = MDFileManager(
            exit_manager=self.exit_note_manager,
            select_path=self.select_note_path,
            preview=True
        )
        self.edit_note_file_manager = MDFileManager(
            exit_manager=self.exit_edit_note_manager,
            select_path=self.select_edit_note_path,
            preview=True
        )
        self.cover_manager = MDFileManager(
            exit_manager=self.exit_cover_manager,
            select_path=self.select_cover_path,
            preview=True
        )

    def render(self, _):
        pass
        # t1 = Thread(target=self.change_main_primary, daemon=True)
        # t1.start()

    def open_edit_popup(self, image):
        root_img = image.ids.edit_note_image.source
        viewer = ImageViewer()
        carousel = viewer.ids.image_viewer

        for img_source in self.note_image_list:
            carousel.add_widget(
                AsyncImage(source=img_source, pos_hint={"center_x": .5, "center_y": .5},
                           allow_stretch=True, keep_data=False))

            if img_source == root_img:
                carousel.index = self.note_image_list.index(img_source)

        viewer.open()

    def open_popup(self, image):
        root_img = image.ids.note_image.source
        viewer = ImageViewer()
        carousel = viewer.ids.image_viewer

        for img_source in self.note_image_list:
            carousel.add_widget(
                AsyncImage(source=img_source, pos_hint={"center_x": .5, "center_y": .5},
                           allow_stretch=True, keep_data=False))

            if img_source == root_img:
                carousel.index = self.note_image_list.index(img_source)

        viewer.open()

    def start_breathing(self, *args):
        Clock.schedule_interval(self.increase_btn_size, 4)
        Clock.schedule_interval(self.decrease_btn_size, 4)

    def increase_btn_size(self, *args):
        button = self.root.get_screen("main").ids.add_task_btn
        button.twist()
        button.icon_size = 35
        button.shrink()
        # anim = Animation(opacity=0.7, duration=2) + Animation(opacity=1, duration=1)
        # anim.repeat = True
        # anim.start(button)

    def decrease_btn_size(self, *args):
        button = self.root.get_screen("main").ids.add_task_btn
        button.twist()
        button.icon_size = 35
        # button.opacity = 0.5
        button.grow()

    def next_slide(self):
        Image = ImageViewer()
        images = Image.ids.image
        Image_viewer = Image.ids.image_viewer
        for img in range(len(self.note_image_list)):
            images.source = self.note_image_list[img]
            Image_viewer.load_next(images)

    def search_note(self, instance):
        search_input = instance.text
        self.root.get_screen("main").ids.note_manager.clear_widgets()
        matching_notes = []
        for note in self.notes:
            note_body = note["note_body"]
            note_title = note_body["title"]
            note_description = note_body["description"]
            if search_input in note_title.lower() or search_input in note_description.lower():
                matching_notes.append(note)

        if matching_notes:
            for note in matching_notes:
                Note_Card = NoteCard()
                Note_Card.ids.title.text = note["note_body"]["title"]
                Note_Card.ids.description_text.text = note["note_body"]["description"]
                Note_Card.ids.date_text.text = note["note_body"]["date"]
                if len(note["note_body"]["images"]) > 1:
                    Note_Card.ids.note_img.source = note["note_body"]["images"][0]
                else:
                    pass
                self.root.get_screen("main").ids.note_manager.add_widget(Note_Card)
                # list_item = OneLineListItem(text=task["title"])
                # self.results_list.add_widget(list_item)
            self.root.get_screen("main").ids.note_search_text.text = ''
        else:
            self.root.get_screen("main").ids.note_search_text.text = 'No results'

    def on_search(self, instance):
        search_input = instance.text
        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
        self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
        self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
        # results = [item for item in self.data if search_input.lower() in item.lower()]

        label = MDLabel(text='No results', halign='center', size_hint_x=None, width="250dp")
        matching_tasks = []
        for task in self.tasks:
            if search_input in task["title"].lower() or search_input in task["description"].lower():
                matching_tasks.append(task)

        if matching_tasks:
            for task in matching_tasks:
                title = task["title"]
                description = task["description"]
                end_date = task["end_date"]
                category = task["category"]
                completed_tasks = task["completed_tasks"]
                completed_tasks_count = ["completed_tasks_count"]
                uncompleted_tasks = task["uncompleted_tasks"]
                uncompleted_tasks_count = task["total_tasks_count"]
                total_tasks_count = task["total_tasks_count"]
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
                if len(completed_tasks) == 0:
                    Task_card = TaskCard()
                    Task_card.ids.title.text = title
                    Task_card.ids.description.text = description
                    Task_card.ids.end_date.text = end_date
                    Task_card.ids.category.text = category
                    if given_date < todays_date:
                        Task_card.ids.end_date.text = f"Expired"
                    else:
                        Task_card.ids.end_date.text = f"till {day}, {date} {month}"
                    self.root.get_screen("main").ids.task_card_layout.add_widget(Task_card)

                elif len(completed_tasks) > 0 and len(completed_tasks) != total_tasks_count:
                    completeness = len(completed_tasks) / total_tasks_count
                    task_percent = round(completeness * 100)
                    Progress_Card = ProgressCard()
                    Progress_Card.ids.title.text = title
                    Progress_Card.ids.description.text = description
                    Progress_Card.ids.category.text = category
                    Progress_Card.ids.percent.text = f"{task_percent}%"
                    Progress_Card.ids.date_range.text = end_date
                    Progress_Card.ids.progress.value = task_percent
                    if given_date < todays_date:
                        Progress_Card.ids.date_range.text = f"Expired"
                    else:
                        Progress_Card.ids.date_range.text = f"till {day}, {date} {month}"
                    self.root.get_screen("main").ids.progress_card_layout.add_widget(Progress_Card)

                elif len(completed_tasks) == total_tasks_count:
                    completeness = len(completed_tasks) / total_tasks_count
                    task_percent = round(completeness * 100)
                    Completed_Card = CompletedCard()
                    Completed_Card.ids.title.text = title
                    Completed_Card.ids.category.text = category
                    Completed_Card.ids.description.text = description
                    Completed_Card.ids.progress.value = task_percent
                    Completed_Card.ids.percent.text = f"{task_percent}%"
                    self.root.get_screen("main").ids.completed_card_layout.add_widget(Completed_Card)

            label.text = ''
            self.root.get_screen("main").ids.task_card_layout.add_widget(label)
        else:
            label.text = 'No results'
            self.root.get_screen("main").ids.task_card_layout.add_widget(label)

    def show_cate_edit_dialog(self, catego_text):
        if not self.cate_dialog:
            self.cate_dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=MDBoxLayout(
                    MDTextField(
                        id="text_field_id",
                        text=catego_text.strip(),
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="35dp",
                ),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_cate_dialog
                    ),
                    MDFlatButton(
                        text="SAVE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.save_edited_cate(catego_text.strip()),
                    ),
                ],
            )
        else:
            self.cate_dialog.content_cls.ids.text_field_id.text = catego_text.strip()  # Update text_field_id text

        self.cate_dialog.open()

    def load_home_cate(self):
        try:
            with open("categories-file.json", "r") as cate_data:
                data = json.load(cate_data)

            categories = data["categories"]
            for value in categories:
                cate_value = value['categories']
                cat = TaskCategories()
                cat.ids.title.text = cate_value
                self.root.get_screen('main').ids.cat_layout.add_widget(cat)
        except:
            pass

    def save_edited_cate(self, text):
        new_text = self.cate_dialog.content_cls.ids.text_field_id.text
        try:
            with open('categories-file.json') as json_file:
                data = json.load(json_file)

            modified_categories = []
            category_found = False

            for category in data['categories']:
                if category['categories'] == text:
                    updated_category = category.copy()
                    updated_category['categories'] = new_text
                    modified_categories.append(updated_category)
                    category_found = True
                else:
                    modified_categories.append(category)

            if not category_found:
                print("Can't be changed because it doesn't exist")

            updated_data = {'categories': modified_categories}

            with open('categories-file.json', 'w') as json_file:
                json.dump(updated_data, json_file, indent=4)
        except:
            pass

        self.root.get_screen("main").ids.category_manager.clear_widgets()
        self.show_all_categories()
        self.cate_dialog.dismiss()

    def show_categories_dialog(self):
        dialog = CategoriesDialog()
        try:
            cate_file_path = "categories-file.json"
            if os.path.exists(cate_file_path) and os.path.getsize(cate_file_path) > 0:
                with open(cate_file_path, "r") as cate_file:
                        data = json.load(cate_file)

                items_layout = dialog.ids.layout_manager
                items = []
                for category in data['categories']:
                    category_text = category['categories']
                    item = ItemConfirm(text=str(category_text))
                    item.bind(on_release=self.print_selected_item_text)  # Bind on_release event
                    items_layout.add_widget(item)
            dialog.open()
        except:
            pass
        
    def print_selected_item_text(self, item):
        self.close_all_cate_dialog()
        self.category_text = item.text
        # print(f"Selected item text: {item.text}")

    def close_all_cate_dialog(self, *args):
        dialog = CategoriesDialog()
        dialog.dismiss()

    def menu_callback(self, text_item):
        print(text_item)

    def file_manager_open(self):
        #if platform == 'android':
            #from android.permissions import request_permissions, Permission
            #request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        self.file_manager.show('/')  # for computer
        # self.file_manager.show(primary_ext_storage)  # for mobile phone
        self.manager_open = True

    def open_note_file_manger(self):
        # if platform == 'android':
        # from android.permissions import request_permissions, Permission
        # request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        self.note_file_manager.show('/')  # output manager to the screen
        # self.file_manager.show(primary_ext_storage)  # for mobile phone
        self.manager_open = True

    def open_edit_note_file_manger(self):
        # if platform == 'android':
        # from android.permissions import request_permissions, Permission
        # request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        self.edit_note_file_manager.show('/')  # output manager to the screen
        # self.file_manager.show(primary_ext_storage)  # for mobile phone
        self.manager_open = True

    def open_cover_manger(self):
        # if platform == 'android':
        # from android.permissions import request_permissions, Permission
        # request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        self.cover_manager.show('/')  # output manager to the screen
        # self.file_manager.show(primary_ext_storage)  # for mobile phone
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        snackbar = CustomSnackbar(
            text="Profile Successfully Updated",
            icon="check",
            snackbar_x="5dp",
            snackbar_y="10dp",
            buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
        )
        snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
        snackbar.open()
        App.get_running_app().change_profile_source(path)

    def select_cover_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_cover_manager()
        snackbar = CustomSnackbar(
            text="Cover Successfully Updated",
            icon="check",
            snackbar_x="5dp",
            snackbar_y="10dp",
            buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
        )
        snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
        snackbar.open()
        App.get_running_app().change_cover_source(path)

    def select_note_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_note_manager()
        NI = NoteImage()
        NI.ids.note_image.source = path
        self.note_image_list.append(path)
        # noteimage.source = path
        self.root.get_screen("main").ids.note_image_layout.add_widget(NI)
        # toast(path)
        # App.get_running_app().change_profile_source(path)

    def select_edit_note_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_edit_note_manager()
        NI = EditNoteImage()
        NI.ids.edit_note_image.source = path
        self.note_image_list.append(path)
        # noteimage.source = path
        self.root.get_screen("main").ids.edit_note_image_layout.add_widget(NI)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def exit_cover_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.cover_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def exit_note_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.note_file_manager.close()

    def exit_edit_note_manager(self):
        self.note_file_manager = False
        self.edit_note_file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.note_file_manager.back()
        return True

    def load_notes(self):
        try:
            note_file_path = "notes-file.json"

            if os.path.exists(note_file_path) and os.path.getsize(note_file_path) > 0:
                with open(note_file_path, "r") as note_file:
                    data = json.load(note_file)

                # Access the list of notes
                notes = data["notes"]

                # Print all the data from the file
                for note in notes:
                    NC = NoteCard()  # Create a new instance of NoteCard for each note
                    note_body = note["note_body"]
                    title = note_body["title"]
                    description = note_body["description"]
                    images = note_body["images"]
                    note_date = note_body["date"]
                    bg_color = note_body["bg_color"]
                    note_layout = self.root.get_screen("main").ids.note_manager
                    NC.ids.title.text = title
                    NC.ids.description_text.text = description
                    NC.md_bg_color = bg_color
                    if len(images) > 0:
                        NC.ids.note_img.source = images[0]
                    else:
                        NC.ids.note_img.source = ""
                    NC.ids.date_text.text = note_date
                    note_layout.add_widget(NC)

                self.root.get_screen("main").ids.note_search_text.text = ""

        except json.decoder.JSONDecodeError:
            pass

    def add_note(self):
        bg_colors = ["#FAF4E3", "#e4f0fb", "#e6e6e6", "#DFD7F3", "#F3EAF6", "#F6ECEE", "#E1F5EC", "#E3F0FF", "#FFDDE4", "#FFE9EE", "#FBFAF0", "#FFE5D9"]
        random_bg_color = random.choice(bg_colors)
        NC = NoteCard()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
        note_layout = self.root.get_screen("main").ids.note_manager
        NC.ids.title.text = self.root.get_screen("main").ids.note_title.text
        NC.ids.description_text.text = self.root.get_screen("main").ids.note_description.text
        NC.md_bg_color = random_bg_color
        if len(self.note_image_list) > 0:
            NC.ids.note_img.source = self.note_image_list[0]
        else:
            NC.ids.note_img.source = ""
        NC.ids.date_text.text = formatted_datetime
        note_layout.add_widget(NC)
        categories = {
            "note_body": {
                "title": NC.ids.title.text.strip(),
                "description": NC.ids.description_text.text.strip(),
                "images": self.note_image_list,
                "date": NC.ids.date_text.text.strip(),
                "bg_color": random_bg_color
            }
        }

        note_file_path = "notes-file.json"

        if os.path.exists(note_file_path) and os.path.getsize(note_file_path) > 0:
            with open(note_file_path, "r") as note_file:
                note_data = json.load(note_file)

                if "notes" in note_data:
                    note_data["notes"].append(categories)
                else:
                    note_data["notes"] = [categories]
        else:
            note_data = {"notes": [categories]}

        with open(note_file_path, "w") as note_file:
            json.dump(note_data, note_file, indent=4)

        self.root.get_screen("main").ids.note_title.text = ""
        self.root.get_screen("main").ids.note_description.text = ""
        self.root.get_screen("main").ids.note_image_layout.clear_widgets()
        self.note_image_list = []

        #description_text
        #note_img
        #date_text

    def edit_note(self, note_card):
        # Access the data from the clicked NoteCard
        title = note_card.ids.title.text
        description = note_card.ids.description_text.text

        # Open the JSON file and retrieve the corresponding note data
        with open("notes-file.json", "r") as note_file:
            data = json.load(note_file)
        notes = data["notes"]
        for note in notes:
            note_body = note["note_body"]
            if note_body["title"] == title and note_body["description"] == description:
                # Print the data corresponding to the clicked NoteCard
                self.root.get_screen("main").ids.edit_note_title.text = note_body["title"]
                self.root.get_screen("main").ids.edit_note_description.text = note_body["description"]
                images = note_body["images"]
                self.note_image_list = images
                # print("Title:", note_body["title"])
                # print("Description:", note_body["description"])
                # ... print/process other properties as needed
                if len(images) > 0:
                    for img in images:
                        NI = EditNoteImage()
                        NI.ids.edit_note_image.source = img
                        self.root.get_screen("main").ids.edit_note_image_layout.add_widget(NI)
                else:
                    self.root.get_screen("main").ids.edit_note_image_layout.clear_widgets()

    def save_edit_note(self, note_card):
        # Access the data from the clicked NoteCard
        title = self.root.get_screen("main").ids.edit_note_title.text
        description = self.root.get_screen("main").ids.edit_note_description.text

        # Open the JSON file and retrieve the corresponding note data
        with open("notes-file.json", "r") as note_file:
            data = json.load(note_file)
        notes = data["notes"]

        # Find the index of the edited note within the notes list
        for index, note in enumerate(notes):
            note_body = note["note_body"]
            if note_body["title"] == title and note_body["description"] == description:
                # Update the note data with the new values
                note_body["title"] = self.root.get_screen("main").ids.edit_note_title.text
                note_body["description"] = self.root.get_screen("main").ids.edit_note_description.text

                # Clear the image list before adding the edited images
                self.note_image_list.clear()

                # Retrieve the edited images
                for image_layout in self.root.get_screen("main").ids.edit_note_image_layout.children:
                    self.note_image_list.append(image_layout.ids.edit_note_image.source)

                note_body["images"] = self.note_image_list

                # Write the modified data back to the JSON file
                with open("notes-file.json", "w") as note_file:
                    json.dump(data, note_file, indent=4)

        # Clear the image layout before adding the edited images
        self.root.get_screen("main").ids.edit_note_image_layout.clear_widgets()

        # Clear the note layout before reloading the notes
        note_layout = self.root.get_screen("main").ids.note_manager
        note_layout.clear_widgets()
        self.load_notes()

    def delete_note(self, title, description):
        # Access the data from the clicked NoteCard
        # title = self.ids.title.text
        # description = self.ids.description_text.text

        # Open the JSON file and retrieve the corresponding note data
        with open("notes-file.json", "r") as note_file:
            data = json.load(note_file)
        notes = data["notes"]

        # Find the index of the note within the notes list
        for index, note in enumerate(notes):
            note_body = note["note_body"]
            if note_body["title"] == title and note_body["description"] == description:
                # Remove the note from the notes list
                del notes[index]

                # Write the modified data back to the JSON file
                with open("notes-file.json", "w") as note_file:
                    json.dump(data, note_file, indent=4)

                # Remove the note card from the UI
                note_layout = self.root.get_screen("main").ids.note_manager
                note_layout.remove_widget(self)
                toast("Note deleted Successfully", background=[1, 0, 0, 1])
                break
        self.root.get_screen("main").ids.note_manager.clear_widgets()
        self.load_notes()

    def delete_full_task(self, title, description):
        self.todo_count = self.todo_count
        self.progress_count = self.progress_count
        self.completed_count = self.completed_count
        self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
        self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
        self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)

        with open("tasks-file.json", "r") as task_file:
            data = json.load(task_file)

        for task_index, task_body in enumerate(data["task_body"]):
            if task_body['title'] == title and task_body['description'] == description:
                completed_tasks_count = task_body['completed_tasks_count']
                total_tasks_count = task_body['total_tasks_count']

                if completed_tasks_count == 0:
                    self.todo_count -= 1
                    self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
                    data["task_body"].pop(task_index)
                    try:
                        self.root.get_screen("main").ids.task_card_layout.remove_widget(
                            self.root.get_screen("main").ids.task_card_layout.children[task_index]
                        )
                        self.root.get_screen("main").ids.all_tasks_layout.remove_widget(
                            self.root.get_screen("main").ids.all_tasks_layout.children[task_index]
                        )
                    except:
                        self.root.get_screen("main").ids.task_card_layout.remove_widget(
                            self.root.get_screen("main").ids.task_card_layout.children[task_index]
                        )
                        self.root.get_screen("main").ids.all_tasks_layout.remove_widget(
                            self.root.get_screen("main").ids.all_tasks_layout.children[task_index]
                        )
                else:
                    completeness = completed_tasks_count / total_tasks_count
                    task_percent = round(completeness * 100)

                    if task_percent == 100:
                        self.completed_count -= 1
                        self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
                        data["task_body"].pop(task_index)
                        try:
                            self.root.get_screen("main").ids.completed_card_layout.remove_widget(
                                self.root.get_screen("main").ids.completed_card_layout.children[task_index]
                            )
                            self.root.get_screen("main").ids.all_completed_layout.remove_widget(
                                self.root.get_screen("main").ids.all_completed_layout.children[task_index]
                            )
                        except:
                            self.root.get_screen("main").ids.completed_card_layout.remove_widget(
                                self.root.get_screen("main").ids.task_card_layout.children[task_index]
                            )
                            self.root.get_screen("main").ids.completed_card_layout.remove_widget(
                                self.root.get_screen("main").ids.all_completed_layout.children[task_index]
                            )
                    else:
                        self.progress_count -= 1
                        self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
                        data["task_body"].pop(task_index)
                        try:
                            self.root.get_screen("main").ids.progress_card_layout.remove_widget(
                                self.root.get_screen("main").ids.progress_card_layout.children[task_index]
                            )
                            self.root.get_screen("main").ids.all_progress_layout.remove_widget(
                                self.root.get_screen("main").ids.all_progress_layout.children[task_index]
                            )
                        except:
                            self.root.get_screen("main").ids.progress_card_layout.remove_widget(
                                self.root.get_screen("main").ids.progress_card_layout.children[task_index]
                            )
                            self.root.get_screen("main").ids.all_progress_layout.remove_widget(
                                self.root.get_screen("main").ids.all_progress_layout.children[task_index]
                            )

                break

        with open("tasks-file.json", "w") as task_file:
            json.dump(data, task_file, indent=4)

        self.close_task_dialog()
        self.load_home_tasks()

    def get_categories_task(self, cate):
            self.todo_count = 0
            self.progress_count = 0
            self.completed_count = 0
            self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
            self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
            self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
            self.root.get_screen("main").ids.task_card_layout.clear_widgets()
            self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
            self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
            cate_title = cate.text
            from datetime import datetime, date
            with open("tasks-file.json", "r") as task_file:
                data = json.load(task_file)

            # tasks = data["task_body"]
            # Iterate over each task in the "task_body" list
            for task in data["task_body"]:
                if task['category'] == cate_title:
                    category = task['category']
                    title = task['title']
                    description = task['description']
                    start_date = task['start_date']
                    end_date = task['end_date']
                    tasks = task['tasks']
                    completed_tasks = task['completed_tasks']
                    uncompleted_tasks = task['uncompleted_tasks']
                    completed_tasks_count = task['completed_tasks_count']
                    uncompleted_tasks_count = task['uncompleted_tasks_count']
                    total_tasks_count = task['total_tasks_count']
                    self.uncompleted_tasks = uncompleted_tasks
                    self.completed_tasks = completed_tasks
                    self.root.get_screen("main").ids.edit_task_title.text = title
                    self.root.get_screen("main").ids.edit_task_description.text = description
                    date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                    weekday = date_obj.strftime("%a")
                    month = date_obj.strftime("%b")
                    card_date = date_obj.strftime("%d")
                    day = date_obj.strftime("%a")
                    date_str = end_date
                    given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    todays_date = date.today()

                    if completed_tasks_count == 0:
                        TC = TaskCard()
                        TC.ids.category.text = category
                        TC.ids.title.text = title
                        TC.ids.description.text = description
                        self.todo_count += 1
                        self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
                        self.root.get_screen("main").ids.task_card_layout.add_widget(TC)
                        if given_date < todays_date:
                            TC.ids.end_date.text = "Expired"
                        else:
                            TC.ids.end_date.text = f"till {day}, {card_date} {month}"
                    else:
                        completeness = completed_tasks_count / total_tasks_count
                        taskPecent = round(completeness * 100)
                        if taskPecent == 100:
                            completeCard = CompletedCard()
                            completeCard.ids.title.text = title
                            completeCard.ids.description.text = description
                            completeCard.ids.percent.text = f"{str(taskPecent)}%"
                            completeCard.ids.progress.value = taskPecent
                            self.completed_count += 1
                            self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
                            self.root.get_screen("main").ids.completed_card_layout.add_widget(completeCard)
                        else:
                            Pro_card = ProgressCard()
                            Pro_card.ids.title.text = title
                            Pro_card.ids.description = description
                            Pro_card.ids.date_range = f"till {day}, {card_date} {month}"
                            Pro_card.ids.category = category
                            Pro_card.ids.percent.text = f"{str(taskPecent)}%"
                            Pro_card.ids.progress.value = taskPecent
                            self.progress_count += 1
                            self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
                            self.root.get_screen("main").ids.progress_card_layout.add_widget(Pro_card)
                            if given_date < todays_date:
                                Pro_card.ids.date_range = f"Expired"
                            else:
                                Pro_card.ids.date_range = f"till {day}, {card_date} {month}"

                        # Print or process the extracted information as needed
                        break
                else:
                    # If the task does not have nested "task_body", access the keys directly
                    if task['category'] == cate_title:
                        category = task['category']
                        title = task['title']
                        description = task['description']
                        start_date = task['start_date']
                        end_date = task['end_date']
                        tasks = task['tasks']
                        completed_tasks = task['completed_tasks']
                        uncompleted_tasks = task['uncompleted_tasks']
                        completed_tasks_count = task['completed_tasks_count']
                        uncompleted_tasks_count = task['uncompleted_tasks_count']
                        total_tasks_count = task['total_tasks_count']
                        self.uncompleted_tasks = uncompleted_tasks
                        self.completed_tasks = completed_tasks
                        self.root.get_screen("main").ids.edit_task_title.text = title
                        self.root.get_screen("main").ids.edit_task_description.text = description
                        from datetime import datetime, date
                        date_obj = datetime.strptime(end_date, "%Y-%m-%d")

                        # Get the weekday name
                        weekday = date_obj.strftime("%a")
                        # Get the month, date, and day
                        month = date_obj.strftime("%b")  # Full month name
                        card_date = date_obj.strftime("%d")  # Day of the month (with leading zero)
                        day = date_obj.strftime("%a")  # Full weekday name
                        date_str = end_date
                        given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        todays_date = date.today()

                        # Get the formatted date
                        formatted_date = date_obj.strftime("%A, %d")
                        # Print or process the extracted information as needed
                        # for card in task:
                        if completed_tasks_count == 0:
                            TC = TaskCard()
                            TC.ids.category.text = category
                            TC.ids.title.text = title
                            TC.ids.description.text = description
                            self.todo_count += 1
                            self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
                            self.root.get_screen("main").ids.task_card_layout.add_widget(TC)
                            if given_date < todays_date:
                                TC.ids.end_date.text = f"Expired"
                            else:
                                TC.ids.end_date.text = f"till {day}, {card_date} {month}"

                        else:
                            completeness = completed_tasks_count / total_tasks_count
                            taskPecent = round(completeness * 100)
                            if taskPecent == 100:
                                completeCard = CompletedCard()
                                completeCard.ids.title.text = title
                                completeCard.ids.description.text = description
                                completeCard.ids.percent.text = f"{str(taskPecent)}%"
                                completeCard.ids.progress.value = taskPecent
                                self.completed_count += 1
                                self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
                                self.root.get_screen("main").ids.completed_card_layout.add_widget(completeCard)
                            else:
                                Todocard = ProgressCard()
                                Todocard.ids.title.text = title
                                Todocard.ids.description.text = description
                                Todocard.ids.category.text = category
                                Todocard.ids.percent.text = f"{str(taskPecent)}%"
                                Todocard.ids.progress.value = taskPecent
                                self.progress_count += 1
                                self.root.get_screen("main").ids.total_task_progress_count.text = self.progress_count
                                self.root.get_screen("main").ids.progress_card_layout.add_widget(Todocard)
                                if given_date < todays_date:
                                    Todocard.ids.date_range.text = f"Expired"
                                else:
                                    Todocard.ids.date_range.text = f"till {day}, {card_date} {month}"

                        break

            # else:
            if cate.text == "all":
                self.load_home_tasks()
            else:
                toast("No available Task!")

    def search_for_quotes_for_the_day(self, *args):
        # getting search for the quotes_for_the_day
        search_input = self.root.get_screen("main").ids.home_search.text
        try:
            motivation_bg_images = ["motivation_images/accessories.jpg", "motivation_images/motivation_image4.jpg",
                 "motivation_images/motivation_image5.jpg", "motivation_images/motiv3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image7.jpg", "motivation_images/motivation_image8.jpg",
                 "motivation_images/motivation_image9.jpg", "motivation_images/motivation_image10.jpg",
                 "motivation_images/motivation_image11.jpg",
                 "motivation_images/motivation_image13.jpg", "motivation_images/motivation_image14.jpg",
                 "motivation_images/motivation_image15.jpg", "motivation_images/motivation_image16.jpg",
                 "motivation_images/motivation_image17.jpg", "motivation_images/motivation_image18.jpg",
                 "motivation_images/motivation_image19.jpg", "motivation_images/motivation_image21.jpg",
                 "motivation_images/motivation_image22.jpg", "motivation_images/motivation_image23.jpg",
                 "motivation_images/motivation_image24.jpg", "motivation_images/motivation_image25.jpg",
                 "motivation_images/motivation_image29.jpg", ]
            url = f"https://api.api-ninjas.com/v1/quotes?category={search_input}"
            reqest2 = requests.get(url,
                                   headers={'X-Api-Key': 'PKdyDYuaaEZ2vwwPogR8WA==8LPK2F0HaIMSXkP4'})  # requests.get(url)
            quotes_respond = reqest2.json()
            quotes_for_the_day_quote = quotes_respond[0]['quote']
            quotes_for_the_day_author = quotes_respond[0]['author']
            self.root.get_screen("main").ids.quotes_for_the_day_layout.add_widget(
                QuotesForTheDayImageCard(quotes_for_the_day_text=quotes_for_the_day_quote,
                                         quotes_for_the_day_author=quotes_for_the_day_author,
                                         quote_bg_image=random.choice(motivation_bg_images)))

        except IndexError:
            toast(f"no Data on {search_input} for search_for_quotes_for_the_day")
        except requests.ConnectionError:
            self.ErrorNetwork = True
        except requests.RequestException:
            pass

    def search_most_popular_quote(self, *args):
        search_input = self.root.get_screen("main").ids.home_search.text
        try:
            motivation_bg_images = ["motivation_images/accessories.jpg", "motivation_images/motivation_image4.jpg",
                 "motivation_images/motivation_image5.jpg", "motivation_images/motiv3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image7.jpg", "motivation_images/motivation_image8.jpg",
                 "motivation_images/motivation_image9.jpg", "motivation_images/motivation_image10.jpg",
                 "motivation_images/motivation_image11.jpg",
                 "motivation_images/motivation_image13.jpg", "motivation_images/motivation_image14.jpg",
                 "motivation_images/motivation_image15.jpg", "motivation_images/motivation_image16.jpg",
                 "motivation_images/motivation_image17.jpg", "motivation_images/motivation_image18.jpg",
                 "motivation_images/motivation_image19.jpg", "motivation_images/motivation_image21.jpg",
                 "motivation_images/motivation_image22.jpg", "motivation_images/motivation_image23.jpg",
                 "motivation_images/motivation_image24.jpg", "motivation_images/motivation_image25.jpg",
                 "motivation_images/motivation_image29.jpg", ]

            # getting search for the most_popular_quote
            url = f"http://api.quotable.io/search/quotes?query={search_input}"
            request = requests.get(url)
            most_popular_response = request.json()
            print(most_popular_response)
            most_popular_quote = most_popular_response['results'][0]['content']
            most_popular_author = most_popular_response['results'][0]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.clear_widgets()
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author, most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][1]['content']
            most_popular_author = most_popular_response['results'][1]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][2]['content']
            most_popular_author = most_popular_response['results'][2]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][3]['content']
            most_popular_author = most_popular_response['results'][3]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][4]['content']
            most_popular_author = most_popular_response['results'][4]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][5]['content']
            most_popular_author = most_popular_response['results'][5]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][6]['content']
            most_popular_author = most_popular_response['results'][6]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][7]['content']
            most_popular_author = most_popular_response['results'][7]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][7]['content']
            most_popular_author = most_popular_response['results'][7]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][8]['content']
            most_popular_author = most_popular_response['results'][8]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][9]['content']
            most_popular_author = most_popular_response['results'][9]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

            most_popular_quote = most_popular_response['results'][10]['content']
            most_popular_author = most_popular_response['results'][10]['author']
            self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(
                MostPopularMotivation(most_popular_quotes_text=most_popular_quote,
                                      most_popular_quotes_author=most_popular_author,
                                      most_popular_quote_bg_image=random.choice(motivation_bg_images)))

        except IndexError:
            toast(f"no Data on {search_input} for search_for_quotes_for_the_day")
        except requests.ConnectionError:
            self.ErrorNetwork = True
        except requests.RequestException:
            pass

    def search_of_get_quotes_of_the_day(self):
        # getting search for get_quotes_of_the_day
        search_input = self.root.get_screen("main").ids.home_search.text
        try:
            url = f"https://free-quotes-api.herokuapp.com/{search_input}"
            req = requests.get(url)
            respond = req.json()
            if len(respond) == 0:
                toast(f"no quotes_of_the_day on '{search_input}'")
                url = f"https://free-quotes-api.herokuapp.com/"
                req = requests.get(url)
                respond = req.json()
                quotes = respond['quote']  # [x]
                author = respond['author']  # [x]
                self.root.ids.quotes_of_the_day_layout.clear_widgets()
                for i in range(5):
                    self.root.get_screen("main").ids.quotes_of_the_day_layout.add_widget(
                        QuotesOfTheDaycard(qoute_of_the_day_text=quotes, quote_of_the_day_author=author,
                                           md_bg_color=rgba(randrange(180), randrange(180), randrange(180), 255)))
            else:
                quotes = respond['quote']  # [x]
                author = respond['author']  # [x]
                self.root.get_screen("main").ids.quotes_of_the_day_layout.clear_widgets()
                for i in range(1):
                    self.root.get_screen("main").ids.quotes_of_the_day_layout.add_widget(
                        QuotesOfTheDaycard(qoute_of_the_day_text=quotes, quote_of_the_day_author=author,
                                           md_bg_color=rgba(randrange(180), randrange(180), randrange(180), 255)))
        except IndexError:
            toast(f"no Data on {search_input} for search_for_quotes_for_the_day")
        except requests.ConnectionError:
            self.ErrorNetwork = True

        except requests.RequestException:
            pass

    def search(self):
        if self.ErrorNetwork == True:
            self.show_loading_dialog()
            Clock.schedule_once(self.close_loading_dialog, 5)
            Clock.schedule_once(self.show_error_dialog, 5)
        else:
            self.show_loading_dialog()
            for i in range(5):
                self.search_of_get_quotes_of_the_day()
            for i in range(5):
                Clock.schedule_once(self.search_for_quotes_for_the_day, 5)
            self.search_most_popular_quote()
            Clock.schedule_once(self.close_loading_dialog, 7)

    def show_reset_dialog(self):
        dialog = ResetThemesDialog()
        dialog.open()

    def reset_themes(self):
        self.main_primary_color = "#7057BB"
        self.main_theme_color = "#FFFFFF"
        self.main_accent_color = (1, 170 / 255, 23 / 255, 1)
        self.main_texture = "#EBEBEB"
        self.theme_color = ""

        cate_file_path = "main_theme.json"

        if os.path.exists(cate_file_path) and os.path.getsize(cate_file_path) > 0:
            with open(cate_file_path, "r") as cate_file:
                data = json.load(cate_file)

            data["main_primary_color"] = self.main_primary_color
            data["main_accent_color"] = self.main_accent_color
            data["theme_color"] = self.theme_color
            data["main_texture"] = self.main_texture

        with open("main_theme.json", "w") as reset_files:
            json.dump(data, reset_files, indent=4)

    def change_primary_color(self, inst):
        themes_file_path = "main_theme.json"

        if os.path.exists(themes_file_path) and os.path.getsize(themes_file_path) > 0:
            with open(themes_file_path, "r") as cate_file:
                data = json.load(cate_file)

        if inst in self.root.get_screen('main').ids.values():
            current_id = list(self.root.get_screen('main').ids.keys())[
                list(self.root.get_screen('main').ids.values()).index(inst)]
            for i in range(5):
                if f"box{i + 1}" == current_id:
                    self.root.get_screen('main').ids[f"box{i + 1}"].state = "down"
                    self.primary_colors = self.root.get_screen("main").ids[f"box{i + 1}"].color_active
                    color = self.primary_colors
                    self.main_primary_color = color
                    data["main_primary_color"] = color

                else:
                    self.root.get_screen('main').ids[f"box{i + 1}"].state = "normal"
                    color = self.root.get_screen("main").ids[f"box{i + 1}"].color_inactive
                    self.root.get_screen("main").ids[f"box{i + 1}"].active = False  # Uncheck other checkboxes

        with open("main_theme.json", "w") as theme_file:
            json.dump(data, theme_file, indent=4)

    def change_accent_color(self, inst):
        themes_file_path = "main_theme.json"

        if os.path.exists(themes_file_path) and os.path.getsize(themes_file_path) > 0:
            with open(themes_file_path, "r") as cate_file:
                data = json.load(cate_file)

        if inst in self.root.get_screen('main').ids.values():
            current_id = list(self.root.get_screen('main').ids.keys())[
                list(self.root.get_screen('main').ids.values()).index(inst)]
            for i in range(5):
                if f"mbox{i + 1}" == current_id:
                    self.root.get_screen('main').ids[f"mbox{i + 1}"].state = "down"
                    self.accent_colors = self.root.get_screen("main").ids[f"mbox{i + 1}"].color_active
                    color = self.accent_colors
                    self.main_accent_color = color
                    data["main_accent_color"] = color

                else:
                    self.root.get_screen('main').ids[f"mbox{i + 1}"].state = "normal"
                    color = self.root.get_screen("main").ids[f"mbox{i + 1}"].color_inactive
                    self.root.get_screen("main").ids[f"mbox{i + 1}"].active = False  # Uncheck other checkboxes
        else:
            pass

        with open("main_theme.json", "w") as theme_file:
            json.dump(data, theme_file, indent=4)

    def change_theme_color(self, inst):
        themes_file_path = "main_theme.json"

        if os.path.exists(themes_file_path) and os.path.getsize(themes_file_path) > 0:
            with open(themes_file_path, "r") as cate_file:
                data = json.load(cate_file)

            # self.main_primary_color = data["main_primary_color"]
            # self.main_accent_color = data["main_accent_color"]
            # self.theme_color = data["theme_color"]
            # self.main_texture = data["main_texture"]

        # data["themes"] = self.theme_color
        # data["texture"] = self.textures
        if inst in self.root.get_screen('main').ids.values():
            current_id = list(self.root.get_screen('main').ids.keys())[
                list(self.root.get_screen('main').ids.values()).index(inst)]
            for i in range(10):
                if f"check{i + 1}" == current_id:
                    if self.root.get_screen('main').ids[f"check{i + 1}"].state == "down" and i + 1 <= 5:
                        self.theme_color = self.root.get_screen("main").ids[f"check{i + 1}"].color_active
                        color = self.theme_color
                        self.main_texture = color
                        self.nav_icon_color = self.root.get_screen("main").ids.check6.color_active
                        data["theme_color"] = color
                        data["main_texture"] = color
                    else:
                        self.textures = self.root.get_screen("main").ids[f"check{i + 1}"].color_active
                        color = self.textures
                        self.main_texture = color
                        data["main_texture"] = color
                        if self.root.get_screen('main').ids[f"check{i + 1}"].state == "down" and i + 1 == 10:
                            self.nav_icon_color = "#FFFFFF"
                        else:
                            self.nav_icon_color = "#DFD7F3"
                else:
                    self.root.get_screen('main').ids[f"check{i + 1}"].state = "normal"
                    color = self.root.get_screen("main").ids[f"check{i + 1}"].color_inactive
                    self.root.get_screen("main").ids[f"check{i + 1}"].active = False  # Uncheck other checkboxes
            else:
                pass

        with open("main_theme.json", "w") as theme_file:
            json.dump(data, theme_file, indent=4)

    # def change_texture_color(self, inst):
    #     with open("themes.json", "r") as theme_file:
    #         data = json.load(theme_file)
    #     data["themes"] = self.theme_color
    #     if inst in self.root.get_screen('main').ids.values():
    #         current_id = list(self.root.get_screen('main').ids.keys())[
    #             list(self.root.get_screen('main').ids.values()).index(inst)]
    #         for i in range(5):
    #             if f"check{i + 1}" == current_id:
    #                 self.root.get_screen('main').ids[f"check{i + 1}"].state = "down"
    #                 self.theme_color = self.root.get_screen("main").ids[f"check{i + 1}"].color_active
    #             else:
    #                 self.root.get_screen('main').ids[f"check{i + 1}"].state = "normal"
    #                 color = self.root.get_screen("main").ids[f"check{i + 1}"].color_inactive
    #                 self.root.get_screen("main").ids[f"check{i + 1}"].active = False  # Uncheck other checkboxes
    #         else:
    #             pass
    #
    #     with open("themes.json", "w") as theme_file:
    #         json.dump(data, theme_file, indent=4)

    def get_todo_dates(self):
        try:
            from datetime import datetime, timedelta

            # Get the current date
            current_date = datetime.now()

            # Calculate the date for yesterday
            yesterday = current_date - timedelta(days=1)
            yesterday_str = yesterday.strftime("%a")
            yesterday_day_str = yesterday.strftime("%d")

            # Calculate the date for the day before yesterday
            day_before_yesterday = current_date - timedelta(days=2)
            day_before_yesterday_str = day_before_yesterday.strftime("%a")
            day_before_yesterday_day_str = day_before_yesterday.strftime("%d")

            # Print or use the date values as needed
            # print("Yesterday:", yesterday_str, yesterday_day_str)
            # print("Day before yesterday:", day_before_yesterday_str, day_before_yesterday_day_str)
            with open("tasks-file.json", "r") as file:
                data = json.load(file)

            end_dates = []

            for task in data["task_body"]:
                if "task_body" in task:
                    end_date = task["task_body"]["end_date"]
                    date_str = end_date
                    # Convert the string to a datetime object
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                    # Get the weekday name
                    weekday = date_obj.strftime("%a")
                    # Get the month, date, and day
                    month = date_obj.strftime("%b")  # Full month name
                    date = date_obj.strftime("%d")  # Day of the month (with leading zero)
                    day = date_obj.strftime("%a")  # Full weekday name
                    dates = Dates()
                    # dates.ids.dates_text.text = date
                    dates.ids.day_text.text = f"{date}\n{day}"
                    dates.ids.main_date.text = end_date
                    if end_date == current_date:
                        dates.md_bg_color = "#7057BB"
                        dates.ids.date.text.color = "#FFFFFF"
                    else:
                        # dates.ids.dates_text.theme_text_color = "Custom"
                        # dates.ids.dates_text.text_color = "#7057BB"
                        dates.ids.day_text.theme_text_color = "Custom"
                        dates.ids.day_text.text_color = "#7057BB"
                        # dates.ids.date.text.text_color = "#7057BB"
                    self.root.get_screen("main").ids.dates_layout.add_widget(dates)
                else:
                    end_date = task["end_date"]
                    date_str = end_date
                    # Convert the string to a datetime object
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                    # Get the weekday name
                    weekday = date_obj.strftime("%a")
                    # Get the month, date, and day
                    month = date_obj.strftime("%b")  # Full month name
                    date = date_obj.strftime("%d")  # Day of the month (with leading zero)
                    day = date_obj.strftime("%a")  # Full weekday name
                    dates = Dates()
                    # dates.ids.dates_text.text = date
                    dates.ids.day_text.text = f"{date}\n{day}"
                    dates.ids.main_date.text = end_date
                    if end_date == current_date:
                        dates.md_bg_color = "#7057BB"
                        dates.ids.main_date.text.color = "#FFFFFF"
                    else:
                        # dates.ids.dates_text.theme_text_color = "Custom"
                        # dates.ids.dates_text.text_color = "#7057BB"
                        dates.ids.day_text.theme_text_color = "Custom"
                        dates.ids.day_text.text_color = "#7057BB"
                        # dates.ids.date.text.color = "#7057BB"
                    self.root.get_screen("main").ids.dates_layout.add_widget(dates)
                end_dates.append(end_date)

            return end_dates
        except:
            pass

    import json

    def show_date_task(self, dates_):
        dates = dates_.ids.main_date.text.strip()
        self.todo_count = 0
        self.progress_count = 0
        self.completed_count = 0
        self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
        self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
        self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
        self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
        self.root.get_screen("main").ids.completed_card_layout.clear_widgets()

        with open("tasks-file.json", "r") as file:
            data = json.load(file)

        for task_item in data['task_body']:
            end_date = task_item['end_date']
            date_str = end_date
            # Convert the string to a datetime object
            from datetime import datetime, date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            given_date = date_obj
            todays_date = date.today()
            # Get the weekday name
            weekday = date_obj.strftime("%a")
            # Get the month, date, and day
            month = date_obj.strftime("%b")  # Full month name
            _date = date_obj.strftime("%d")  # Day of the month (with leading zero)
            day = date_obj.strftime("%a")  # Full weekday name

            # Get the formatted date
            formatted_date = date_obj.strftime("%A, %d")

            if end_date == dates:
                title = task_item['title']
                description = task_item['description']
                tasks = task_item['tasks']
                category = task_item['category']
                completed_tasks = task_item['completed_tasks']
                uncompleted_tasks = task_item['uncompleted_tasks']
                completed_tasks_count = task_item['completed_tasks_count']
                total_tasks_count = task_item["total_tasks_count"]
                # Get the formatted date
                if completed_tasks_count == 0:
                    TC = TaskCard()
                    TC.ids.category.text = category
                    TC.ids.title.text = title
                    TC.ids.description.text = description
                    self.todo_count += 1
                    self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
                    self.root.get_screen("main").ids.task_card_layout.add_widget(TC)
                    self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
                    self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
                    if given_date < todays_date:
                        TC.ids.end_date.text = f"Expired"
                    else:
                        TC.ids.end_date.text = f"till {day}, {_date} {month}"
                else:
                    completeness = completed_tasks_count / total_tasks_count
                    taskPecent = round(completeness * 100)
                    if taskPecent == 100:
                        completeCard = CompletedCard()
                        completeCard.ids.title.text = title
                        completeCard.ids.description.text = description
                        completeCard.ids.percent.text = f"{str(taskPecent)}%"
                        completeCard.ids.progress.value = taskPecent
                        self.completed_count += 1
                        self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
                        self.root.get_screen("main").ids.completed_card_layout.add_widget(completeCard)
                        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
                        self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
                    else:
                        Todocard = ProgressCard()
                        Todocard.ids.title.text = title
                        Todocard.ids.description.text = description
                        Todocard.ids.category.text = category
                        Todocard.ids.percent.text = f"{str(taskPecent)}%"
                        Todocard.ids.progress.value = taskPecent
                        self.progress_count += 1
                        self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
                        self.root.get_screen("main").ids.progress_card_layout.add_widget(Todocard)
                        self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
                        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
                        if given_date < todays_date:
                            Todocard.ids.date_range.text = f"Expired"
                        else:
                            Todocard.ids.date_range.text = f"till {day}, {_date} {month}"

                break
            else:
                category = task_item['category']
                title = task_item['title']
                description = task_item['description']
                completed_tasks_count = task_item["completed_tasks_count"]
                total_tasks_count = task_item['total_tasks_count']
                end_date = task_item['end_date']
                date_str = end_date
                # Convert the string to a datetime object
                from datetime import datetime, date
                # ... (continue with the remaining code to display the task data)
                # Convert the string to a datetime object
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                given_date = date_obj

                date_str = end_date
                given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                todays_date = date.today()
                # Get the weekday name
                weekday = date_obj.strftime("%a")
                # Get the month, date, and day
                month = date_obj.strftime("%b")  # Full month name
                _date = date_obj.strftime("%d")  # Day of the month (with leading zero)
                day = date_obj.strftime("%a")  # Full weekday name

                # Get the formatted date
                formatted_date = date_obj.strftime("%A, %d")
                if completed_tasks_count == 0:
                    TC = TaskCard()
                    TC.ids.category.text = category
                    TC.ids.title.text = title
                    TC.ids.description.text = description
                    TC.ids.end_date.text = f"till {day}, {date} {month}"
                    self.todo_count += 1
                    self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
                    self.root.get_screen("main").ids.task_card_layout.add_widget(TC)
                    self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
                    self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
                    if given_date < todays_date:
                        TC.ids.end_date.text = f"Expired"
                    else:
                        TC.ids.end_date.text = f"till {day}, {_date} {month}"
                else:
                    completeness = completed_tasks_count / int(total_tasks_count)
                    taskPecent = round(completeness * 100)
                    if taskPecent == 100:
                        completeCard = CompletedCard()
                        completeCard.ids.title.text = title
                        completeCard.ids.description.text = description
                        completeCard.ids.percent.text = f"{str(taskPecent)}%"
                        completeCard.ids.progress.value = taskPecent
                        self.completed_count += 1
                        self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
                        self.root.get_screen("main").ids.completed_card_layout.add_widget(completeCard)
                        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
                        self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
                    else:
                        Todocard = ProgressCard()
                        Todocard.ids.title.text = title
                        Todocard.ids.description.text = description
                        Todocard.ids.date_range.text = f"till {day}, {_date} {month}"
                        Todocard.ids.category.text = category
                        Todocard.ids.percent.text = f"{str(taskPecent)}%"
                        Todocard.ids.progress.value = taskPecent
                        self.progress_count += 1
                        self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
                        self.root.get_screen("main").ids.progress_card_layout.add_widget(Todocard)
                        self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
                        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
                        if given_date < todays_date:
                            Todocard.ids.date_range.text = f"Expired"
                        else:
                            Todocard.ids.date_range.text = f"till {day}, {date} {month}"

    def change_cover_source(self, path):
        self.root.get_screen("main").ids.profile.source = path
        with open("cover_source.txt", "w") as f:
            f.write(path)  # For mobile phone
            # f.write("C:" + path)  # For computer

        if os.path.isfile("cover_source.txt"):
            with open("cover_source.txt", "r") as f:
                some_path = f.read()
                if len(some_path) > 0:
                    self.root.get_screen("main").ids.profile.source = path  # For mobile phone
                else:
                    self.root.get_screen("main").ids.profile.source = "store/profile_pics.png"  # For mobile phone

        else:
            self.root.get_screen("main").ids.profile.source = "store/profile_pics.png"

    def change_profile_source(self, path):
        #self.root.ids.profile.source = "C:" + path  # For computer
        self.root.get_screen("main").ids.edit_profile_pics.source = path # For mobile phone
        self.root.get_screen("main").ids.insight_pics.source = path
        self.root.get_screen("main").ids.home_image.source = path
        with open("profile_source.txt", "w") as f:
            f.write(path) # For mobile phone
            #f.write("C:" + path)  # For computer

        if os.path.isfile("profile_source.txt"):
            with open("profile_source.txt", "r") as f:
                some_path = f.read()
                if len(some_path) > 0:
                    self.root.get_screen("main").ids.edit_profile_pics.source = path  # For mobile phone
                    self.root.get_screen("main").ids.insight_pics.source = path
                    self.root.get_screen("main").ids.home_image.source = path
                else:
                    self.root.get_screen("main").ids.edit_profile_pics.source = "store/profile_pics.png"  # For mobile phone
                    self.root.get_screen("main").ids.insight_pics.source = "store/profile_pics.png"

        else:
            self.root.get_screen("main").ids.insight_pics.source = "store/profile_pics.png"

    def edit_complete(self, box, todo_text):
        # print(box.ids.todo_text.text)
        task_text = todo_text.text
        todo_text = box.ids.todo_text
        bar = box.ids.bar
        uncompleted_tasks = self.uncompleted_tasks
        if box.ids.md_check_box.state == "down":
            todo_text.text = f"[s]{task_text}[/s]"
            bar.md_bg_color = "#5D3AB7"  # 0, 175 / 255, 0, 1

            if f"[s]{task_text}[/s]" in self.completed_tasks:
                pass
                # print(f"This task is already in the completed list: {task_text}")
            else:
                self.completed_tasks.append(f"[s]{task_text}[/s]")  # Add task to completed tasks
                self.completed_tasks_count = len(self.completed_tasks)
                # print(f"This is the new completed list: {self.completed_tasks}")

                if task_text in self.uncompleted_tasks:
                    self.uncompleted_tasks.remove(task_text)  # Remove task from uncompleted tasks
                elif f"[s]{task_text}[/s]" in self.uncompleted_tasks:
                    self.uncompleted_tasks.remove(f"[s]{task_text}[/s]")  # Remove formatted task from uncompleted tasks
                self.uncompleted_tasks_count = len(self.uncompleted_tasks)
                # print(f"This is the new uncompleted list: {self.uncompleted_tasks}")
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                todo_text.text = todo_text.text.replace(i, "")
            bar.md_bg_color = 1, 170 / 255, 23 / 255, 1

            if task_text in self.completed_tasks:
                self.completed_tasks.remove(task_text)  # Remove task from completed tasks
                self.completed_tasks_count = len(self.completed_tasks)
                # print(f"This is the new completed list: {self.completed_tasks}")

            if task_text not in self.uncompleted_tasks and f"[s]{task_text}[/s]" not in self.uncompleted_tasks:
                self.uncompleted_tasks.append(task_text)  # Add task to uncompleted tasks
                self.uncompleted_tasks_count = len(self.uncompleted_tasks)
                # print(f"This is the new uncompleted list: {self.uncompleted_tasks}")

    def complete(self, checkbox, value, todo_text, bar):
        task_text = todo_text.text
        if value:
            todo_text.text = f"[s]{task_text}[/s]"
            bar.md_bg_color = "#5D3AB7"  # 0, 175 / 255, 0, 1

            if f"[s]{task_text}[/s]" in self.completed_tasks:
                pass
                # print(f"This task is already in the completed list: {task_text}")
            else:
                self.completed_tasks.append(f"[s]{task_text}[/s]")  # Add task to completed tasks
                self.completed_tasks_count = len(self.completed_tasks)
                # print(f"This is the new completed list: {self.completed_tasks}")

                if task_text in self.uncompleted_tasks:
                    self.uncompleted_tasks.remove(task_text)  # Remove task from uncompleted tasks
                elif f"[s]{task_text}[/s]" in self.uncompleted_tasks:
                    self.uncompleted_tasks.remove(f"[s]{task_text}[/s]")  # Remove formatted task from uncompleted tasks
                self.uncompleted_tasks_count = len(self.uncompleted_tasks)
                # print(f"This is the new uncompleted list: {self.uncompleted_tasks}")
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                todo_text.text = todo_text.text.replace(i, "")
            bar.md_bg_color = 1, 170 / 255, 23 / 255, 1

            if task_text in self.completed_tasks:
                self.completed_tasks.remove(task_text)  # Remove task from completed tasks
                self.completed_tasks_count = len(self.completed_tasks)
                # print(f"This is the new completed list: {self.completed_tasks}")

            if task_text not in self.uncompleted_tasks and f"[s]{task_text}[/s]" not in self.uncompleted_tasks:
                self.uncompleted_tasks.append(task_text)  # Add task to uncompleted tasks
                self.uncompleted_tasks_count = len(self.uncompleted_tasks)

    def build(self):
        global screen_manager
        # app ID 'ca-app-pub-4268254501946298~4518366608'
        # banner ID 'ca-app-pub-4268254501946298/4026879184'
        # interstitial ID 'ca-app-pub-4268254501946298/8317477982'

        self.ads.new_banner('ca-app-pub-4268254501946298/4026879184', top_pos=False)
        self.ads.new_interstitial('ca-app-pub-4268254501946298/8317477982')
        self.ads.request_banner()
        self.ads.request_interstitial()
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("splash.kv"))
        screen_manager.add_widget(Builder.load_file("menu.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("page.kv"))
        # self.items = [f"Item {i}" for i in range(50)]
        return screen_manager

    def get_my_quotes(self):
        bg_colors = ["#FAF4E3", "#e6e6e6", "#F3EAF6", "#F6ECEE", "#E1F5EC", "#E3F0FF", "#FFDDE4", "#FFE9EE", "#FBFAF0",
                     "#FFE5D9"]
        my_quotes = ['"Life" is hard, but you got to show her that you are "though"',
                     "life is this, life is that, hey! that's when you let her decide, i know you are smarter than this.",
                     "you want to quit now cause it's ain't easy? it's fine but ask your self why didn't mom stop during birth?",
                     'take a nap when you are tired, but hey! "KEEP PUSHING"',
                     "Never Second Guess your Self Cause You are a god",
                     "One Day You will be heard it's a must",
                     "what ever you are doing keep doing cause most people out there doing samething are shy & scared to show it up. so keep pushing...",
                     "keep the dream big!",
                     "think twice before you act. it's important",
                     "hustle hard but not dirty",
                     "your vision is real so don't give up"
                     "value your ideas and work towards them cause you are not the only one with those same ideas.",
                     "giving without reward expectations gives you the ability to forgive easily",
                     "always put family first.  don't do it if they won't gain from it",
                     "don't wait till you're perfect cause you will  never be. we learn in the process",
                     "make that move today! tomorrow isn't promised",
                     "it's okay not to forget, but try to forgive. it's essential",
                     "the earlier you realize that nobody owes you the strong you become. every man for him self.",
                     "gifting is the act of giving with your heart without expecting a reward. ",
                     "giving is not meant to be reciprocated. if you give and get something back then is now transactional. it's no more giving but bussiness",
                     "is there no heaven? so stupid to think there is devil and no God or heaven and no hell.",
                     "your carrier doesn't change you, you chose to change."
                     ]
        author = ["Switnex xtra", "Eze .C. Goodness"]
        for i in range(1):
            self.root.get_screen("main").ids.quotes_of_the_day_layout.add_widget(
                QuotesOfTheDaycard(qoute_of_the_day_text=random.choice(my_quotes), quote_of_the_day_author=random.choice
                (author), bg_color=random.choice(bg_colors)))

    def quotes_for_the_day(self):
        try:
            motivation_bg_images = random.choice(
                ["motivation_images/motivation_image4.jpg", "motivation_images/motiv1.jpeg", "motivation_images/motiv3.jpg",
                 "motivation_images/accessories.jpg", "motivation_images/motivation_image4.jpg",
                 "motivation_images/motivation_image5.jpg", "motivation_images/motiv3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image7.jpg", "motivation_images/motivation_image8.jpg",
                 "motivation_images/motivation_image9.jpg", "motivation_images/motivation_image10.jpg",
                 "motivation_images/motivation_image11.jpg",
                 "motivation_images/motivation_image13.jpg", "motivation_images/motivation_image14.jpg",
                 "motivation_images/motivation_image15.jpg", "motivation_images/motivation_image16.jpg",
                 "motivation_images/motivation_image17.jpg", "motivation_images/motivation_image18.jpg",
                 "motivation_images/motivation_image19.jpg", "motivation_images/motivation_image21.jpg",
                 "motivation_images/motivation_image22.jpg", "motivation_images/motivation_image23.jpg",
                 "motivation_images/motivation_image24.jpg", "motivation_images/motivation_image25.jpg",
                 "motivation_images/motivation_image29.jpg",
                 "motivation_images/motiv2.jpg", "motivation_images/motivation_image3.jpg", "motivation_images/motiv2.jpg",
                 "motivation_images/motivation_image7.jpg", "motivation_images/motivation_image10.jpg"])
            api_url = 'https://api.api-ninjas.com/v1/quotes?'
            request = requests.get(api_url, headers={'X-Api-Key': 'PKdyDYuaaEZ2vwwPogR8WA==8LPK2F0HaIMSXkP4'})
            res = request.json()
            quotes = res[0]['quote']
            author = res[0]['author']
            for i in range(1):
                self.root.ids.quotes_for_the_day_layout.add_widget(
                    QuotesForTheDayImageCard(quotes_for_the_day_text=quotes, quotes_for_the_day_author=author,
                                         quote_bg_image=motivation_bg_images))  # quote_bg_image=motivation_bg_images[1]

        except requests.exceptions.ConnectionError:
            self.ErrorNetwork = True

    def load(self, *args):
        try:
            # self.show_banner_ads()
            for i in range(13):
                self.quotes_for_the_day()

            for i in range(13):
                self.most_popular_quote()

            for i in range(13):
                self.get_quotes_of_the_day()

            for i in range(12):
                self.get_my_quotes()

        except requests.exceptions.ConnectionError:
            self.show_error_dialog()

    def signup(self):
        self.show_loading_dialog()
        Clock.schedule_once(self.close_loading_dialog, 9)
        Clock.schedule_once(self.send_signup_data, 10)

    def send_signup_data(self, *args):
        fullname = self.root.get_screen("page").ids.signup_fullname.text
        email = self.root.get_screen("page").ids.signup_email.text
        skills = self.root.get_screen("page").ids.signup_skills.text
        password = self.root.get_screen("page").ids.signup_password.text
        user_name = self.root.get_screen("page").ids.signup_username.text
        user_details = {
            "user_details": {
                "username": user_name,
                "email": email,
                "fullname": fullname,
                "password": password,
                "skills": skills
            }
        }
        if user_name == "" or email == "" or fullname == "" or password == "" or skills == "":
            snackbar = CustomSnackbar(
                text="please all complete fields",
                icon="information",
                snackbar_x="5dp",
                snackbar_y="10dp",
                buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
            )
            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
            snackbar.open()
        else:
            with open("user-details.json", "w") as user_file:
                json.dump(user_details, user_file, indent=4)
            snackbar = CustomSnackbar(
                text="Signup Successful",
                icon="check",
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
            )
            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
            snackbar.open()
            screen_manager.current = "main"
            self.load_full_details()
        # # self.change_screen("home")

    def validate(self):
        self.show_loading_dialog()
        Clock.schedule_once(self.close_loading_dialog, 6)
        Clock.schedule_once(self.retrieve_and_validate, 7)

    def remember_user(self):
        login_email = self.root.get_screen("page").ids.login_email.text
        login_password = self.root.get_screen("page").ids.login_password.text
        remember_state = self.root.get_screen("page").ids.remember_user.state
        if login_email == "" or login_password == "":
            snackbar = CustomSnackbar(
                text="Fill in all blanks",
                icon="information",
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
            )
            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
            snackbar.open()
        else:
            remember = "no"
            if remember_state == "down":
                remember = "yes"

            details = {
                "user_name": login_email,
                "password": login_password,
                "remember": remember
            }
            with open("login-details.json", "w") as login_details:
                json.dump(details, login_details, indent=4)

    def retrieve_and_validate(self, *args):
        try:
            with open("user-details.json", "r") as user_file:
                data = json.load(user_file)
            details = data["user_details"]
            email = details["email"]
            password = details["password"]
            login_email = self.root.get_screen("page").ids.login_email.text
            login_password = self.root.get_screen("page").ids.login_password.text
            if login_email == email and login_password == password:
                snackbar = CustomSnackbar(
                    text="Login Successful",
                    icon="check",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
                )
                snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
                snackbar.open()
                screen_manager.current = "main"
                self.load_full_details()
            else:
                snackbar = CustomSnackbar(
                    text="Login Failed, wrong email or password",
                    icon="information",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    buttons=[MDFlatButton(text="OK", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
                )
                snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
                snackbar.open()
        except:
            snackbar = CustomSnackbar(
                text="No data found!",
                icon="archive-cancel",
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[MDFlatButton(text="Try Again", theme_text_color="Custom", text_color=(1, 1, 1, 1))]
            )
            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
            snackbar.open()

    def refresh(self):
        self.close_error_dialog()
        self.call_refresh()

    def get_quotes_of_the_day(self):
        #self.text()
        bg_colors = ["#FAF4E3", "#e6e6e6", "#F3EAF6", "#F6ECEE", "#E1F5EC", "#E3F0FF", "#FFDDE4", "#FFE9EE", "#FBFAF0",
                     "#FFE5D9"]
        try:
            url = "https://zenquotes.io/api/quotes" #"https://type.fit/api/quotes"
            response = requests.get(url)
            passed = response.json()
            #print(passed)
            quotes = passed[0]["q"]
            author = passed[1]["a"]
            for i in range(1):
                self.root.get_screen("main").ids.quotes_of_the_day_layout.add_widget(
                    QuotesOfTheDaycard(qoute_of_the_day_text=quotes, quote_of_the_day_author=author,md_bg_color=random.choice(bg_colors)))
        except requests.exceptions.ConnectionError:
            self.ErrorNetwork = True

        except IndexError:
            snackbar = CustomSnackbar(
                text=f"error on quotes_of_the_day try again!",
                icon="information",
                snackbar_x="10dp",
                snackbar_y="10dp",
                buttons=[MDFlatButton(text="ACTION", text_color=(1, 1, 1, 1))]
            )
            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
            snackbar.open()

    def show_error_dialog(self, *args):
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                title="Error Network",
                type="custom",
                # radius=[30],
                auto_dismiss=False,
                content_cls=ErrorDialogContent(),
            )

        self.error_dialog.open()

    def close_error_dialog(self):
        self.error_dialog.dismiss()

    def call_refresh(self):
        self.show_loading_dialog()
        Clock.schedule_once(self.close_loading_dialog, 8)
        Clock.schedule_once(self.home_refresh, 10)

    def home_refresh(self, *args):
        try:
            for i in range(2):
                self.get_my_quotes()
            for i in range(15):
                self.most_popular_quote()
            for i in range(15):
                self.get_quotes_of_the_day()
            for i in range(15):
                self.quotes_for_the_day()
            if self.ErrorNetwork == True:
                self.show_error_dialog()
        except requests.ConnectionError:
            self.show_error_dialog()

    def show_loading_dialog(self, *args):
        bg_colors = ["#FAF4E3", "#e6e6e6", "#F3EAF6", "#F6ECEE", "#E1F5EC", "#E3F0FF", "#FFDDE4", "#FFE9EE", "#FBFAF0",
                     "#FFE5D9"]
        if not self.loading_dialog:
            self.loading_dialog = MDDialog(
                type="custom",
                auto_dismiss=False,
                content_cls=LoadingDialog(),
                md_bg_color=random.choice(bg_colors)

            )
        self.loading_dialog.open()

    def close_loading_dialog(self, *args):
        self.loading_dialog.dismiss()

    def greet(self, *args):
        """Return part of day depending on time_now and the user's timzone
        offset value.

        user_tz_offset - integer of user's time zone offset in hours
        time_now - UTC time in seconds

        From  -  To  => part of day
        ---------------------------
        00:00 - 04:59 => midnight
        05:00 - 06:59 => dawn
        07:00 - 10:59 => morning
        11:00 - 12:59 => noon
        13:00 - 16:59 => afternoon
        17:00 - 18:59 => dusk
        19:00 - 20:59 => evening 21:00 - 23:59 => night
        """
        #user_time = time_now + (user_tz_offset * 60 * 60)
        # gmtime[3] is tm_hour
        now = datetime.now()
        user_hour = now.hour
        user_name = self.root.get_screen("main").ids.insight_username.text
        if 0 <= user_hour < 5:
            # self.root.ids.greeting.text = "It's MidNight"
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} It's MidNight"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} It's MidNight"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} It's MidNight"
            self.root.get_screen("menu").ids.welcome_text.text = "Still Awake? Get Affirmed & Motivated Tonight before You Sleep. and Perhaps set your Schedule for Tomorrow"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/image3.jpg"
        elif 5 <= user_hour < 7:
            # self.root.ids.greeting.text = "It's Dawn"
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} It's Dawn"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} It's Dawn"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} It's Dawn"
            self.root.get_screen("menu").ids.welcome_text.text = "IT's Dawn!. Get Affirmed & Motivated Before its morning. and Perhaps set your Schedule for This Night & Tomorrow"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/morning_menu.png"
        elif 7 <= user_hour < 11:
            # self.root.ids.greeting.text = 'Good Morning'
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} Good Morning"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} Good Morning"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} Good Morning"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/morning_menu.png"
            self.root.get_screen("menu").ids.welcome_text.text = "Good Morning. This is the Best Time To Get Affirmed & Motivated during the day to keep you going. Then Perhaps set your Schedule for This Night & Tomorrow"
        elif 11 <= user_hour < 13:
            # self.root.ids.greeting.text = "It's Noon"
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} It's Noon"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} It's Noon"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} It's Noon"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/morning_menu.png"
            self.root.get_screen("menu").ids.welcome_text.text = "Hey It's noon. Get Affirmed & Motivated to keep you going. and Perhaps set your Schedule for This Night & Tomorrow"
        elif 13 <= user_hour < 17:
            # self.root.ids.greeting.text = 'Good Afternoon'
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} Good Afternoon"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} Good Afternoon"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} Good Afternoon"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/morning_menu.png"
            self.root.get_screen("menu").ids.welcome_text.text = "Good Afternoon We know You are Tied. So Get Affirmed & Motivated this AfterNoon to keep you going. and Perhaps set your Schedule for This Night & Tomorrow"
        elif 19 <= user_hour < 21:
            # self.root.ids.greeting.text = "Good Evening"
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} Good Evening"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} Good Evening"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} Good Evening"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/image3.jpg"
            self.root.get_screen("menu").ids.welcome_text.text = "Good Evening, How are Feeling? Get Affirmed & Motivated This Evening before going to Bed. and Perhaps set your Schedule for Tomorrow"
        else:
            # self.root.ids.greeting.text = "Good Night"
            self.root.get_screen("main").ids.all_completed_greeting.text = f"{user_name} Good Night"
            self.root.get_screen("main").ids.all_tasks_greeting.text = f"{user_name} Good Night"
            self.root.get_screen("main").ids.all_progress_greeting.text = f"{user_name} Good Night"
            self.root.get_screen("menu").ids.suggest_txt.text = "Last Thing"
            self.root.get_screen("menu").ids.menu_image.source = "menuimages/image3.jpg"
            self.root.get_screen("menu").ids.welcome_text.text = "How Is The Night Going?. Get Affirmed & Motivated Tonight before going to Bed. and Perhaps set your Schedule for Tomorrow"

    def go_home(self, *args):
        screen_manager.current = "menu"

    def on_resume(self):
        self.ads.request_interstitial()

    def show_inter_ads(self, *args):
        self.ads.show_interstitial()

    def on_start(self):
        Clock.schedule_once(self.go_home, 12)
        Clock.schedule_interval(self.show_inter_ads, 180)
        self.ads.show_banner()
        self.ads.show_interstitial()
        try:
            self.greet()
            self.tasks_notification()
            self.load_home_cate()
            self.load_home_tasks()
            self.get_todo_dates()
            self.load_notes()
            self.show_all_categories()
            Clock.schedule_interval(self.get_current_notification, 250)
            self.start_breathing()
        except:
            pass
        # self.plot_graph()
        today_ = datetime.today()
        wd = datetime.weekday(today_)
        days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        year = str(datetime.now().year)
        month = str(datetime.now().strftime("%b"))
        day = str(datetime.now().strftime("%d"))
        self.root.get_screen("main").ids.date.text = f"Get Motivated Today  {days[wd]}, {day}, {month}, {year}"
        themes_file_path = "main_theme.json"

        if os.path.exists(themes_file_path) and os.path.getsize(themes_file_path) > 0:
            with open(themes_file_path, "r") as theme_file:
                data = json.load(theme_file)

            self.main_primary_color = data["main_primary_color"]
            self.main_accent_color = data["main_accent_color"]
            self.theme_color = data["theme_color"]
            self.main_texture = data["main_texture"]

        else:
            themes = {
                "main_primary_color": "#7057BB",
                "main_theme_color": "#FFFFFF",
                "main_accent_color": (1, 170 / 255, 23 / 255, 1),
                "main_texture": "#EBEBEB",
                "theme_color": ""
            }
            with open("main_theme.json", "w") as theme_file:
                json.dump(themes, theme_file, indent=4)

            self.main_primary_color = "#7057BB"
            self.main_theme_color = "#FFFFFF"
            self.main_accent_color = (1, 170 / 255, 23 / 255, 1)
            self.main_texture = "#EBEBEB"
            self.theme_color = ""
        # self.load()
        self.check_remember()
        try:
            with open('tasks-file.json', 'r') as file:
                data = json.load(file)

            self.tasks = data["task_body"]

            with open('notes-file.json', 'r') as file:
                data = json.load(file)

            self.notes = data["notes"]
        except:
            pass
        try:
            if os.path.isfile("profile_source.txt"):
                with open("profile_source.txt", "r") as f:
                    path = f.read()
                    if len(path) > 0:
                        self.root.get_screen("main").ids.edit_profile_pics.source = path  # For mobile phone
                        self.root.get_screen("main").ids.insight_pics.source = path
                        self.root.get_screen("main").ids.home_image.source = path

                    else:
                        self.root.get_screen("main").ids.edit_profile_pics.source = "store/profile_pics.png"  # For mobile phone
                        self.root.get_screen("main").ids.insight_pics.source = "store/profile_pics.png"
            else:
                self.root.get_screen("main").ids.edit_profile_pics.source = "store/profile_pics.png"  # For mobile phone
                self.root.get_screen("main").ids.insight_pics.source = "store/profile_pics.png"

            if os.path.isfile("cover_source.txt"):
                with open("cover_source.txt", "r") as f:
                    some_path = f.read()
                    if len(some_path) > 0:
                        self.root.get_screen("main").ids.profile.source = some_path

                    else:
                        self.root.get_screen("main").ids.profile.source = "store/mylogo.png"
            else:
                self.root.get_screen("main").ids.profile.source = "store//mylogo.png"
            #self.save_users_details()
        except:
            # self.root.ids.menu_profile_image.source = some_path
            pass
        try:
            self.show_user_details()
            self.load_full_details()
            self.root.get_screen("main").ids.pass_word.text = "*" * len(str(self.root.ids.pass_word.text))
        except:
            pass

        if platform == "android":
            self.start_service()
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def get_date(self,instance, date_dialog, the_date):
        selected_date = date_dialog.date
        # print("Selected Date:", selected_date)
        # print("Minimum Date:", self.min_date)
        # print("Maximum Date:", self.max_date)

    @staticmethod
    def start_service():
        from jnius import autoclass
        service = autoclass("org.tasksivating.taskisvate.ServiceTasksivate")
        mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(mActivity, "")
        return service

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        print(value, date_range)
        self.range = date_range

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        '''
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        '''
        self.todo_time = time

    def save_user_full_details(self):
        fullname = self.root.get_screen("main").ids.fullname_text_field.text
        email = self.root.get_screen("main").ids.email_textfield.text
        skills = self.root.get_screen("main").ids.skills_textfield.text
        password = self.root.get_screen("main").ids.password_text_field.text
        user_name = self.root.get_screen("main").ids.username_textinput.text
        user_details = {
            "user_details": {
                "username": user_name,
                "email": email,
                "fullname": fullname,
                "password": password,
                "skills": skills
            }
        }
        with open("tails.json", "w") as user_file:
            json.dump(user_details, user_file, indent=4)
        self.load_full_details()

    def show_user_details(self):
        with open("user-details.json", "r") as user_file:
            data = json.load(user_file)
        details = data["user_details"]
        self.root.get_screen("page").ids.signup_fullname.text = details["fullname"].capitalize()
        self.root.get_screen("page").ids.signup_email.text = details["email"]
        self.root.get_screen("page").ids.signup_skills.text = details["skills"]
        self.root.get_screen("page").ids.signup_password.text = details["password"]
        self.root.get_screen("page").ids.signup_username.text = details["username"].capitalize()
        self.root.get_screen("main").ids.insight_username.text = self.root.get_screen("main").ids.user_name.text
        self.root.get_screen("main").ids.login_logout_text.text = self.root.get_screen("main").ids.login_logout_btn.text
        self.root.get_screen("main").ids.insight_pics.source = self.root.get_screen("main").ids.edit_profile_pics.source

    def hide_password(self):
        with open("user-details.json", "r") as user_file:
            data = json.load(user_file)
        details = data["user_details"]
        self.root.get_screen("main").ids.password_btn.icon = "eye-off" if self.root.get_screen("main").ids.password_btn.icon == "eye" else "eye"
        if self.root.get_screen("main").ids.password_btn.icon == "eye-off":
            self.root.get_screen("main").ids.pass_word.text = "*" * len(str(self.root.get_screen("main").ids.pass_word.text))
        else:
            self.root.get_screen("main").ids.pass_word.text = details['password']

    def load_full_details(self):
        with open("user-details.json", "r") as user_file:
            data = json.load(user_file)
        details = data["user_details"]
        self.root.get_screen("main").ids.user_name.text = details["username"].capitalize()
        self.root.get_screen("main").ids.fullname.text = details["fullname"]
        self.root.get_screen("main").ids.email.text = details["email"]
        self.root.get_screen("main").ids.pass_word.text = details["password"]
        self.root.get_screen("main").ids.skills.text = details["skills"]
        self.root.get_screen("main").ids.insight_username.text = self.root.get_screen("main").ids.user_name.text.capitalize()
        self.root.get_screen("main").ids.login_logout_text.text = self.root.get_screen("main").ids.login_logout_btn.text
        self.root.get_screen("main").ids.insight_pics.source = self.root.get_screen("main").ids.edit_profile_pics.source
        if self.root.get_screen("main").ids.pass_word.text != "PassWord":
            self.root.get_screen("main").ids.login_logout_btn.text = "Logout"
            self.root.get_screen("main").ids.login_logout_text.text = "Logout"
        else:
            self.root.get_screen("main").ids.login_logout_btn.text = "LogIn"

    def delete_note_image(self, note_image):
        layout = self.root.get_screen("main").ids.note_image_layout
        layout.remove_widget(note_image)

        if note_image.ids.note_image.source in self.note_image_list:
            self.note_image_list.remove(note_image.ids.note_image.source)

    def delete_edit_note_image(self, note_image):
        layout = self.root.get_screen("main").ids.edit_note_image_layout
        layout.remove_widget(note_image)

        if note_image.ids.edit_note_image.source in self.note_image_list:
            self.note_image_list.remove(note_image.ids.edit_note_image.source)

    def checkout(self):
        dc = ConfirmDialog()
        dc.title = "Checkout"
        dc.subtitle = "Are sure you want to Complete this Cart?"
        dc.textConfirm = "Yes Checkout"
        # dc.textCancel = "Cancel"
        # dc.confirmColor = App.get_running_app().color_primary
        # dc.cancelColor = App.get_running_app().color_primary
        # dc.confirmCallback = self.print_receipt()
        dc.open()

    def add_todo(self):
        TDC = TodoCard()
        task_text = self.root.get_screen("main").ids.task_text
        if len(task_text.text) < 5:
            toast("Please input a valid task")
        elif len(task_text.text) > 59:
            toast("Your task is too long. Shorten it.")

        else:
            TDC.ids.todo_text.text = task_text.text
            task_text.text = ""
            self.root.get_screen("main").ids.todo_card_manager.add_widget(TDC)
            self.todo_list.append(task_text.text)
            self.uncompleted_tasks.append(task_text.text)  # Add task to uncompleted tasks

    def edit_add_todo(self):
        TDC = TodoCard()
        task_text = self.root.get_screen("main").ids.edit_task_text
        if len(task_text.text) <= 5:
            toast("Please input a valid task")

        if len(task_text.text) >= 59:
            TDC.ids.todo_text.text = task_text.text
            self.root.get_screen("main").ids.edit_todo_card_manager.add_widget(TDC)
            self.todo_list.append(task_text.text)
            self.uncompleted_tasks.append(task_text.text)  # Add task to uncompleted tasks
            # print(self.todo_list)
        else:
            toast("Your task is too long. Shorten it.")

    def add_full_todo(self):
        task_text = self.root.get_screen("main").ids.edit_task_text
        # ...
        title = self.root.get_screen("main").ids.task_title.text
        description = self.root.get_screen("main").ids.task_description.text
        try:
            # ...
            start_date = self.range[0].strftime("%Y-%m-%d")  # Convert start date to string
            end_date = self.range[-1].strftime("%Y-%m-%d")  # Convert end date to string
            time_str = self.todo_time.strftime("%H:%M")  # Convert time to string
            if self.category_text == "":
                toast("make sure you choose a category")
            elif len(title) < 3:
                toast("title can not be less than 3 words")
            elif len(title) > 12:
                toast("make your title short not greater than 12 words")
            elif len(description) < 3:
                toast("description can not be less than 3 words")
            elif len(description) > 27:
                toast("make your description short not greater than 27 words")
            else:
                task_file = 'tasks-file.json'
                tasks = {
                    'category': self.category_text,
                    'title': title,
                    'description': description,
                    'start_date': start_date,
                    'end_date': end_date,
                    'time': time_str,
                    'tasks': self.todo_list,
                    'completed_tasks': self.completed_tasks,
                    'uncompleted_tasks': self.uncompleted_tasks,
                    'completed_tasks_count': len(self.completed_tasks),
                    'uncompleted_tasks_count': len(self.uncompleted_tasks),
                    'total_tasks_count': len(self.completed_tasks) + len(self.uncompleted_tasks)
                }

                if os.path.exists(task_file) and os.path.getsize(task_file) > 0:
                    # Load existing data from the JSON file
                    with open(task_file, "r") as note_file:
                        task_data = json.load(note_file)

                    if 'task_body' in task_data:
                        # Append new task data to existing data
                        task_data['task_body'].append(tasks)
                    else:
                        task_data['task_body'] = [tasks]
                else:
                    task_data = {'task_body': [tasks]}

                # Write the updated data back to the JSON file
                with open(task_file, "w") as note_file:
                    json.dump(task_data, note_file, indent=4)

        except IndexError:
            toast("pick a time, start and end date")
        self.root.get_screen("main").ids.task_title.text = ""
        self.root.get_screen("main").ids.task_description.text = ""
        task_text.text = ""
        self.root.get_screen("main").ids.todo_card_manager.clear_widgets()

        self.todo_list = []
        self.completed_tasks = []
        self.uncompleted_tasks = []
        self.load_home_tasks()
        self.change_screen("home")

    def edit_task(self, task_card):
        self.root.get_screen("main").ids.edit_todo_card_manager.clear_widgets()
        title = task_card.ids.title.text
        description = task_card.ids.description.text

        # Open the JSON file and retrieve the corresponding TASK data
        with open("tasks-file.json", "r") as task_file:
            data = json.load(task_file)

        tasks = data["task_body"]
        # Iterate over each task in the "task_body" list
        for task in tasks:
            if 'task_body' in task:
                # If the task has nested "task_body", access the nested key
                task_body = task['task_body']
                if task_body['title'] == title and task_body['description'] == description:
                    title = task_body['title']
                    description = task_body['description']
                    completed_tasks = task_body['completed_tasks']
                    uncompleted_tasks = task_body['uncompleted_tasks']
                    self.uncompleted_tasks = uncompleted_tasks
                    self.completed_tasks = completed_tasks
                    print(self.completed_tasks)
                    self.root.get_screen("main").ids.edit_task_title.text = title
                    self.root.get_screen("main").ids.edit_task_description.text = description
                    for card in self.uncompleted_tasks:
                        ToCa = EditTodoCard()
                        ToCa.ids.todo_text.text = card
                        self.root.get_screen("main").ids.edit_todo_card_manager.add_widget(ToCa)
                    for card in self.completed_tasks:
                        ToCa = EditTodoCard()
                        ToCa.ids.todo_text.text = card
                        print(f"this is the state before disabled {ToCa.ids.md_check_box.state}")
                        ToCa.ids.md_check_box.active = "down"
                        print(f"this is the state after disabled {ToCa.ids.md_check_box.state}")
                        self.root.get_screen("main").ids.edit_todo_card_manager.add_widget(ToCa)
                    task_text = "[s]create Virtual environment for the app[/s]"
                    if task_text in self.completed_tasks:
                        self.completed_tasks.remove(task_text)
                    # Print or process the extracted information as needed
                    break
            else:
                # If the task does not have nested "task_body", access the keys directly
                if task['title'] == title and task['description'] == description:
                    title = task['title']
                    description = task['description']
                    completed_tasks = task['completed_tasks']
                    uncompleted_tasks = task['uncompleted_tasks']
                    self.uncompleted_tasks = uncompleted_tasks
                    self.completed_tasks = completed_tasks
                    self.root.get_screen("main").ids.edit_task_title.text = title
                    self.root.get_screen("main").ids.edit_task_description.text = description
                    # Print or process the extracted information as needed
                    for card in self.uncompleted_tasks:
                        ToCa = EditTodoCard()
                        ToCa.ids.todo_text.text = card
                        self.root.get_screen("main").ids.edit_todo_card_manager.add_widget(ToCa)
                    for card in self.completed_tasks:
                        ToCa = EditTodoCard()
                        print(f"this is the state before disabled {ToCa.ids.md_check_box.state}")
                        ToCa.ids.md_check_box.active = "down"
                        print(f"this is the state after disabled {ToCa.ids.md_check_box.state}")
                        ToCa.ids.todo_text.text = card
                        self.root.get_screen("main").ids.edit_todo_card_manager.add_widget(ToCa)
                    task_text = "[s]create Virtual environment for the app[/s]"
                    if task_text in self.completed_tasks:
                        self.completed_tasks.remove(task_text)
                    break
        else:
            toast("No available Task!")

    def save_edit_task(self, task_card):
        # Access the data from the clicked NoteCard
        title = self.root.get_screen("main").ids.edit_task_title.text
        description = self.root.get_screen("main").ids.edit_task_description.text

        with open("tasks-file.json", "r") as task_file:
            data = json.load(task_file)
        tasks = data["task_body"]

        # Find the index of the edited note within the tasks list
        for index, task in enumerate(tasks):
            task_body = task
            if task_body["title"] == title and task_body["description"] == description:
                # Update the task data with the new values
                task_body["title"] = self.root.get_screen("main").ids.edit_task_title.text
                task_body["description"] = self.root.get_screen("main").ids.edit_task_description.text
                task_body["completed_tasks"] = self.completed_tasks
                task_body["uncompleted_tasks"] = self.uncompleted_tasks
                task_body["uncompleted_tasks_count"] = self.uncompleted_tasks_count
                task_body["completed_tasks_count"] = self.completed_tasks_count

                with open("tasks-file.json", "w") as task_file:
                    json.dump(data, task_file, indent=4)

        # Clear the image layout before adding the edited images
        self.root.get_screen("main").ids.edit_todo_card_manager.clear_widgets()

        # Clear the note layout before reloading the notes
        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
        self.load_home_tasks()

    def show_delete_cate_dialog(self, title):
        dialog = DeleteCateDialog(title=title)
        dialog.open()

    def close_delete_cate_dialog(self, *args):
        dialog = DeleteCateDialog()
        dialog.dismiss()

    def delete_category(self, title):
        # category = self.root.ids.title.text
        with open("categories-file.json", "r") as file:
            data = json.load(file)

        categories = data["categories"]

        for item in categories:
            if item["categories"] == title:
                if title == "all":
                    toast("You can't delete this!")
                    break
                else:
                    categories.remove(item)
                    self.root.get_screen("main").ids.category_manager.clear_widgets()
                break

        with open("categories-file.json", "w") as file:
            json.dump(data, file, indent=4)
        self.root.get_screen("main").ids.category_manager.clear_widgets()
        self.show_all_categories()
        self.close_delete_cate_dialog()

    def show_delete_todo_dialog(self, todo):
        # categories_manager = self.root.get_screen("main").ids.category_manager
        # cate = categories_manager.ids.title.text
        if not self.todo_dialog:
            self.todo_dialog = MDDialog(
                title="Delete Task?",
                text="This will delete this Task permanently are you sure you want to continue?.",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_todo_dialog
                    ),
                    MDFlatButton(
                        text="Delete",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.delete_todo(todo)

                    ),
                ],
            )
            self.todo_dialog.open()

    def close_todo_dialog(self, *args):
        self.todo_dialog.dismiss()

    def show_delete_task_dialog(self, title, description):
        dialog = DeleteTaskDialog(title=title, subtitle=description)
        dialog.open()

    def close_task_dialog(self, *args):
        dialog = DeleteTaskDialog()
        dialog.dismiss()

    def delete_todo(self, todo):
        with open("tasks-file.json", "r") as file:
            data = json.load(file)

        task_bodies = [item.get("task_body", item) for item in data["task_body"]]

        for task_body in task_bodies:
            tasks = task_body.get("tasks", [])
            completed_tasks = task_body.get("completed_tasks", [])
            uncompleted_tasks = task_body.get("uncompleted_tasks", [])

            if todo.ids.todo_text.text in tasks:
                tasks.remove(todo.ids.todo_text.text)
                if todo.ids.todo_text.text in completed_tasks:
                    completed_tasks.remove(todo.ids.todo_text.text)
                elif todo.ids.todo_text.text in uncompleted_tasks:
                    uncompleted_tasks.remove(todo.ids.todo_text.text)

                task_body["completed_tasks_count"] = len(completed_tasks)
                task_body["uncompleted_tasks_count"] = len(uncompleted_tasks)
                task_body["total_tasks_count"] = len(tasks)
                # Update the JSON file with the modified data
                with open("tasks-file.json", "w") as file:
                    json.dump(data, file, indent=4)
                self.root.get_screen("main").ids.edit_todo_card_manager.remove_widget(todo)
                self.todo_dialog.dismiss()

    def show_all_categories(self):
        try:
            with open("categories-file.json", "r") as categories_file:
                categories_data = json.load(categories_file)

            with open("tasks-file.json", "r") as task_body_file:
                task_body_data = json.load(task_body_file)

            categories = [category["categories"] for category in categories_data["categories"]]
            category_counts = {category: 0 for category in categories}

            for task in task_body_data["task_body"]:
                if "task_body" in task:
                    category = task["task_body"]["category"]
                    category_counts[category] += 1
                else:
                    category = task["category"]
                    category_counts[category] += 1

            # Calculate the total count of all categories
            total_count = sum(category_counts.values())

            # Add "all" category with the total count to the category_counts dictionary
            category_counts["all"] = total_count

            for category, count in category_counts.items():
                # print(f"{category}: {count}")
                cate = CategoriesManager()
                cate.ids.title.text = category
                cate.ids.task_counts.text = str(count)
                self.root.get_screen("main").ids.category_manager.add_widget(cate)
            return category_counts
        except:
            pass

    def get_all_progress(self):
        self.root.get_screen("main").ids.all_progress_layout.clear_widgets()
        self.total_task = 0
        self.completed_count = 0
        self.todo_count = 0

        with open('tasks-file.json') as json_file:
            data = json.load(json_file)

        for task_data in data['task_body']:
            category = task_data['category']
            title = task_data['title']
            description = task_data['description']
            completed_tasks_count = task_data['completed_tasks_count']
            total_tasks_count = task_data['total_tasks_count']
            end_date = task_data['end_date']

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
            if completed_tasks_count == 0:
                TC = TaskCard()
                TC.ids.category.text = category
                TC.ids.title.text = title
                TC.ids.description.text = description

            else:
                completeness = completed_tasks_count / total_tasks_count
                task_percent = round(completeness * 100)
                if task_percent == 100:
                    completeCard = CompletedCard()
                    completeCard.ids.title.text = title
                    completeCard.ids.description.text = description
                    completeCard.ids.percent.text = f"{str(task_percent)}%"
                else:
                    Todocard = AllProgressCard()
                    Todocard.ids.title.text = title
                    Todocard.ids.description.text = description
                    Todocard.ids.date_range.text = f"till {day}, {date} {month}"
                    Todocard.ids.category.text = category
                    Todocard.ids.percent.text = f"{str(task_percent)}%"
                    Todocard.ids.progress.value = task_percent
                    self.progress_count += 1
                    self.root.get_screen("main").ids.all_progress_layout.add_widget(Todocard)
                    if given_date < todays_date:
                        Todocard.ids.date_range.text = f"Expired"
                    else:
                        Todocard.ids.date_range.text = f"till {day}, {date} {month}"
        total_task_progress_count = self.root.get_screen("main").ids.total_task_progress_count.text
        self.root.get_screen(
            "main").ids.all_progress_text.text = f"You've got a total of [color=#FFAA17]{str(self.progress_count)}[/color] Tasks in Progress"

    def get_all_completed(self):
        self.root.get_screen("main").ids.all_completed_layout.clear_widgets()
        self.total_task = 0
        self.completed_count = 0
        self.todo_count = 0

        with open('tasks-file.json') as json_file:
            data = json.load(json_file)

        for task_data in data['task_body']:
            category = task_data['category']
            title = task_data['title']
            description = task_data['description']
            completed_tasks_count = task_data['completed_tasks_count']
            total_tasks_count = task_data['total_tasks_count']
            end_date = task_data['end_date']

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
            if completed_tasks_count == 0:
                TC = TaskCard()
                TC.ids.category.text = category
                TC.ids.title.text = title
                TC.ids.description.text = description

            else:
                completeness = completed_tasks_count / total_tasks_count
                task_percent = round(completeness * 100)
                if task_percent == 100:
                    completeCard = AllCompletedCard()
                    completeCard.ids.title.text = title
                    completeCard.ids.description.text = description
                    completeCard.ids.percent.text = f"{str(task_percent)}%"
                    completeCard.ids.progress.value = task_percent
                    self.completed_count += 1
                    self.root.get_screen("main").ids.all_completed_layout.add_widget(completeCard)
                    self.root.get_screen(
                        "main").ids.all_completed_text.text = f"You've got a total of [color=#FFAA17]{str(self.completed_count)}[/color] Completed Tasks"

    def get_all_tasks(self):
        self.root.get_screen("main").ids.all_tasks_layout.clear_widgets()
        self.total_task = 0
        self.completed_count = 0
        self.todo_count = 0

        with open('tasks-file.json') as json_file:
            data = json.load(json_file)

        for task_data in data['task_body']:
            category = task_data['category']
            title = task_data['title']
            description = task_data['description']
            completed_tasks_count = task_data['completed_tasks_count']
            total_tasks_count = task_data['total_tasks_count']
            end_date = task_data['end_date']

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
            if completed_tasks_count == 0:
                Todocard = AllTasksCard()
                Todocard.ids.title.text = title
                Todocard.ids.description.text = description
                Todocard.ids.date_range.text = f"till {day}, {date} {month}"
                Todocard.ids.category.text = category
                self.todo_count += 1
                self.root.get_screen("main").ids.all_tasks_layout.add_widget(Todocard)
                if given_date < todays_date:
                    Todocard.ids.date_range.text = f"Expired"
                else:
                    Todocard.ids.date_range.text = f"till {day}, {date} {month}"
                self.root.get_screen(
                    "main").ids.all_tasks_text.text = f"You've got a [color=#FFAA17]{str(self.todo_count)}[/color] pending Tasks"

    def get_current_notification(self, *args):
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
                    plyer.notification.notify(title='Task Reminder!', message=f"It's time for {title} \n {description}", app_name='Tasksivate', app_icon='store/app-icon.ico', timeout=10)
                    snackbar = CustomSnackbar(
                        text=f"It's time for {title}",
                        icon="information",
                        snackbar_x="550dp",
                        snackbar_y=.8,
                        buttons=[MDFlatButton(text="ACTION", text_color=(1, 1, 1, 1))]
                    )
                    snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
                    snackbar.open()
        except:
            pass

    def tasks_notification(self, *args):
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
                if completed_tasks_count == 0:
                    TC = TaskCard()
                    TC.ids.category.text = category
                    TC.ids.title.text = title
                    TC.ids.description.text = description
                    if given_date < todays_date:
                        plyer.notification.notify(title='Task Reminder',
                                                  message=f"you have some Expired undone Task.",
                                                  app_name='Taskivate', app_icon='store/app-icon.ico', timeout=10)
                        snackbar = CustomSnackbar(
                            text=f"you have some Expired undone Task.",
                            icon="information",
                            snackbar_x="550dp",
                            snackbar_y=.8,
                            buttons=[MDFlatButton(text="ACTION", text_color=(1, 1, 1, 1))]
                        )
                        snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
                        snackbar.open()
                    else:
                        plyer.notification.notify(title='Task Reminder',
                                                  message=f"you have some undone Task.",
                                                  app_name='Tasksivate', app_icon='store/app-icon.ico', timeout=10)
                        snackbar = CustomSnackbar(
                            text=f"you have some undone Task.",
                            icon="information",
                            snackbar_x="550dp",
                            snackbar_y=.8,
                            buttons=[MDFlatButton(text="ACTION", text_color=(1, 1, 1, 1))]
                        )
                        snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
                        snackbar.open()
                else:
                    completeness = completed_tasks_count / total_tasks_count
                    task_percent = round(completeness * 100)
                    if task_percent == 100:
                        completeCard = CompletedCard()

                    else:
                        if given_date < todays_date:
                            plyer.notification.notify(title='Task Reminder',
                                                      message=f"you have some Expired pending Task.",
                                                      app_name='Tasksivate', app_icon='store/app-icon.ico', timeout=10)
                            snackbar = CustomSnackbar(
                                text=f"you have some Expired pending Task.",
                                icon="information",
                                snackbar_x="550dp",
                                snackbar_y=.8,
                                buttons=[MDFlatButton(text="ACTION", text_color=(1, 1, 1, 1))]
                            )
                            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
                            snackbar.open()
                        else:
                            plyer.notification.notify(title='Task Reminder',
                                                      message=f"you have some pending Task.",
                                                      app_name='Tasksivate', app_icon='store/app-icon.ico', timeout=10)
                            snackbar = CustomSnackbar(
                                text=f"you have some pending Task.",
                                icon="information",
                                snackbar_x="550dp",
                                snackbar_y=.8,
                                buttons=[MDFlatButton(text="ACTION", text_color=(1, 1, 1, 1))]
                            )
                            snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 1)) / Window.width
                            snackbar.open()
        except:
            pass

    def load_home_tasks(self):
        self.root.get_screen("main").ids.task_card_layout.clear_widgets()
        self.root.get_screen("main").ids.progress_card_layout.clear_widgets()
        self.root.get_screen("main").ids.completed_card_layout.clear_widgets()
        self.total_task = 0
        self.completed_count = 0
        self.todo_count = 0
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

                if completed_tasks_count == 0:
                    TC = TaskCard()
                    TC.ids.category.text = category
                    TC.ids.title.text = title
                    TC.ids.description.text = description

                    self.todo_count += 1
                    self.root.get_screen("main").ids.total_task_count.text = str(self.todo_count)
                    self.root.get_screen("main").ids.task_card_layout.add_widget(TC)
                    if given_date < todays_date:
                        TC.ids.end_date.text = f"Expired"
                    else:
                        TC.ids.end_date.text = f"till {day}, {date} {month}"

                else:
                    completeness = completed_tasks_count / total_tasks_count
                    task_percent = round(completeness * 100)
                    if task_percent == 100:
                        completeCard = CompletedCard()
                        completeCard.ids.title.text = title
                        completeCard.ids.description.text = description
                        completeCard.ids.percent.text = f"{str(task_percent)}%"
                        completeCard.ids.progress.value = task_percent
                        self.completed_count += 1
                        self.root.get_screen("main").ids.total_completed_task_count.text = str(self.completed_count)
                        self.root.get_screen("main").ids.completed_card_layout.add_widget(completeCard)
                    else:
                        Todocard = ProgressCard()
                        Todocard.ids.title.text = title
                        Todocard.ids.description.text = description
                        Todocard.ids.date_range.text = f"till {day}, {date} {month}"
                        Todocard.ids.category.text = category
                        Todocard.ids.percent.text = f"{str(task_percent)}%"
                        Todocard.ids.progress.value = task_percent
                        self.progress_count += 1
                        self.root.get_screen("main").ids.total_task_progress_count.text = str(self.progress_count)
                        self.root.get_screen("main").ids.progress_card_layout.add_widget(Todocard)
                        if given_date < todays_date:
                            Todocard.ids.date_range.text = f"Expired"
                        else:
                            Todocard.ids.date_range.text = f"till {day}, {date} {month}"
        except:
            pass
        total_task_count = self.root.get_screen("main").ids.total_task_count.text
        total_task_progress_count = self.root.get_screen("main").ids.total_task_progress_count.text
        total_completed_task_count = self.root.get_screen("main").ids.total_completed_task_count.text
        self.total_task = int(total_task_count) + int(total_task_progress_count)
        self.root.get_screen("main").ids.pending_task.text = str(self.total_task)
        self.root.get_screen("main").ids.completed_task_text.text = total_completed_task_count
        self.root.get_screen("menu").ids.all_tasks.text = str(self.total_task)
        self.root.get_screen("menu").ids.pending_tasks.text = str(total_task_progress_count)
        self.root.get_screen("menu").ids.completed_tasks.text = str(total_completed_task_count)
        self.root.get_screen("main").ids.insight_pics.source = self.root.get_screen("main").ids.edit_profile_pics.source
        self.root.get_screen(
            "main").ids.notify_text1.text = f"You've got a total of [color=#FFAA17]{self.total_task}[/color] Tasks"
        # signal = [int(total_task_count), int(total_task_progress_count), self.total_task]
        self.get_pie_chart()
        self.get_area_graph()
        self.get_current_notification()

    def get_area_graph(self):
        total_task_count = self.root.get_screen("main").ids.total_task_count.text
        total_task_progress_count = self.root.get_screen("main").ids.total_task_progress_count.text
        total_completed_task_count = self.root.get_screen("main").ids.total_completed_task_count.text
        graph_image = self.root.get_screen("main").ids.graph_image

        # Generate the data for the graph based on task counts
        labels = ['Pending', 'In Progress', 'Completed']

        # Define custom colors for the labels
        colors = [self.main_primary_color, self.main_accent_color, self.main_texture]

        values = [int(total_task_count), int(total_task_progress_count), int(total_completed_task_count)]

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Plot the data as an area graph
        ax.stackplot(labels, values, labels=labels, colors=colors)

        # Set the font size for the labels on the x-axis
        ax.tick_params(axis='x', labelsize=13)

        # Set the font size for the labels on the y-axis
        ax.tick_params(axis='y', labelsize=13)

        # Set the font size for the legend
        ax.legend(fontsize=13)

        # Save the plot as a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            plt.savefig(temp_file, format='png')
            temp_file.close()
            file_path = temp_file.name

        # Assign the file path to the Image widget's source property
        graph_image.source = file_path

    def get_pie_chart(self):
        total_task_count = self.root.get_screen("main").ids.total_task_count.text
        total_task_progress_count = self.root.get_screen("main").ids.total_task_progress_count.text
        total_completed_task_count = self.root.get_screen("main").ids.total_completed_task_count.text
        pie_image = self.root.get_screen("main").ids.pie_image

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Generate the data for the graph based on task counts
        labels = ['Pending', 'In Progress', 'Completed']
        # Define custom colors for the labels
        colors = [self.main_primary_color, self.main_accent_color, self.main_texture]

        values = [int(total_task_count), int(total_task_progress_count), int(total_completed_task_count)]

        # # Plot the data as a bar graph
        # ax.bar(labels, values)

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Plot the data as a pie chart
        pie = ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'fontsize': 15})

        # Set the font size for the percentage labels
        for text in pie[2]:
            text.set_fontsize(13)

        # Save the plot as a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            plt.savefig(temp_file, format='png')
            temp_file.close()
            file_path = temp_file.name

        # Assign the file path to the Image widget's source property
        pie_image.source = file_path

    def check_logout(self):
        if self.root.get_screen("main").ids.login_logout_btn.text == "Logout" or self.root.get_screen("main").ids.login_logout_text.text == "Logout":
            # self.show_logout_dialog()
            dialog = LogoutDailog()
            dialog.open()
        else:
            screen_manager.current = "page"

    def logout(self):
        self.close_logout_dialog()

        self.show_loading_dialog()
        Clock.schedule_once(self.close_loading_dialog, 9)
        Clock.schedule_once(self.logout_page, 10)

    def check_remember(self):
        login_file_path = "login-details.json"
        if os.path.exists(login_file_path) and os.path.getsize(login_file_path) > 0:
            with open(login_file_path, "r") as login_file:
                data = json.load(login_file)

            if data["remember"] == "yes":
                self.root.get_screen("page").ids.login_email.text = data["user_name"]
                self.root.get_screen("page").ids.login_password.text = data['password']
                self.root.get_screen("page").ids.remember_user.state = "down"

    def logout_page(self, *args):
        screen_manager.current = "page"

    def close_logout_dialog(self, *args):
        logout_dialog = LogoutDailog()
        logout_dialog.dismiss()

    def show_confirmation_dialog(self, *args):
        content = MDTextField(
            hint_text="Enter your Category",
            helper_text="Required",
            helper_text_mode="on_error"
        )
        if not self.confirmation_dialog:
            self.confirmation_dialog = MDDialog(
                title="Category:",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_confirmation_dialog
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.process_input(content.text)
                    ),
                ],
            )
        self.confirmation_dialog.open()


    def close_cate_dialog(self, *args):
        self.cate_dialog.dismiss()

    def close_confirmation_dialog(self, *args):
        self.confirmation_dialog.dismiss()

    def close_dialog(self, *args):
        self.show_cate_dialog.dismiss()

    def process_input(self, label):
        # print("Entered text:", label)
        categories = {
                    "categories": label
                }
        cate_file_path = "categories-file.json"

        if os.path.exists(cate_file_path) and os.path.getsize(cate_file_path) > 0:
            with open(cate_file_path, "r") as cate_file:
                note_data = json.load(cate_file)

                if "categories" in note_data:
                    note_data["categories"].append(categories)
                else:
                    note_data["categories"] = [categories]
        else:
            note_data = {"categories": [categories]}

        with open(cate_file_path, "w") as cate_file:
            json.dump(note_data, cate_file, indent=4)

        self.root.get_screen("main").ids.category_manager.clear_widgets()
        self.show_all_categories()
        self.confirmation_dialog.dismiss()
        self.root.get_screen('main').ids.cat_layout.clear_widgets()
        self.load_home_cate()

    def most_popular_quote(self):
        try:
            motivation_bg_images = ["motivation_images/accessories.jpg", "motivation_images/motivation_image4.jpg",
                                    "motivation_images/motivation_image5.jpg", "motivation_images/motiv3.jpg",
                                    "motivation_images/motiv2.jpg",
                                    "motivation_images/motivation_image3.jpg", "motivation_images/motiv2.jpg",
                                    "motivation_images/motivation_image7.jpg", "motivation_images/motivation_image8.jpg",
                                    "motivation_images/motivation_image9.jpg", "motivation_images/motivation_image10.jpg",
                                    "motivation_images/motivation_image11.jpg",
                                    "motivation_images/motivation_image13.jpg", "motivation_images/motivation_image14.jpg",
                                    "motivation_images/motivation_image15.jpg", "motivation_images/motivation_image16.jpg",
                                    "motivation_images/motivation_image17.jpg", "motivation_images/motivation_image18.jpg",
                                    "motivation_images/motivation_image19.jpg", "motivation_images/motivation_image21.jpg",
                                    "motivation_images/motivation_image22.jpg", "motivation_images/motivation_image23.jpg",
                                    "motivation_images/motivation_image24.jpg", "motivation_images/motivation_image25.jpg",
                                    "motivation_images/motivation_image29.jpg", ]
            url ="http://api.quotable.io/random"
            request = requests.get(url)
            responsed = request.json()
            tags = responsed["tags"]
            quotes = responsed["content"]
            author = responsed["author"]
            for i in range(1):
                self.root.get_screen("main").ids.most_popular_quotes_layout.add_widget(MostPopularMotivation(most_popular_quotes_text=quotes,most_popular_quotes_author=author, most_popular_quote_bg_image=random.choice(motivation_bg_images)))

        except requests.exceptions.ConnectionError:
            self.ErrorNetwork = True

    # getting the Quotes for the day
    def quotes_for_the_day(self):
        try:
            motivation_bg_images = random.choice(["motivation_images/motivation_image4.jpg","motivation_images/motiv1.jpeg","motivation_images/motiv3.jpg",
                    "motivation_images/accessories.jpg", "motivation_images/motivation_image4.jpg",
                     "motivation_images/motivation_image5.jpg", "motivation_images/motiv3.jpg", "motivation_images/motiv2.jpg",
                     "motivation_images/motivation_image3.jpg", "motivation_images/motiv2.jpg",
                     "motivation_images/motivation_image7.jpg", "motivation_images/motivation_image8.jpg",
                     "motivation_images/motivation_image9.jpg", "motivation_images/motivation_image10.jpg",
                     "motivation_images/motivation_image11.jpg",
                     "motivation_images/motivation_image13.jpg", "motivation_images/motivation_image14.jpg",
                     "motivation_images/motivation_image15.jpg", "motivation_images/motivation_image16.jpg",
                     "motivation_images/motivation_image17.jpg", "motivation_images/motivation_image18.jpg",
                     "motivation_images/motivation_image19.jpg", "motivation_images/motivation_image21.jpg",
                     "motivation_images/motivation_image22.jpg", "motivation_images/motivation_image23.jpg",
                     "motivation_images/motivation_image24.jpg", "motivation_images/motivation_image25.jpg",
                     "motivation_images/motivation_image29.jpg",
                    "motivation_images/motiv2.jpg","motivation_images/motivation_image3.jpg","motivation_images/motiv2.jpg","motivation_images/motivation_image7.jpg", "motivation_images/motivation_image10.jpg"])
            api_url = 'https://api.api-ninjas.com/v1/quotes?'
            request = requests.get(api_url, headers={'X-Api-Key': 'PKdyDYuaaEZ2vwwPogR8WA==8LPK2F0HaIMSXkP4'})
            res = request.json()
            quotes = res[0]['quote']
            author = res[0]['author']
            for i in range(1):
                self.root.get_screen("main").ids.quotes_for_the_day_layout.add_widget(QuotesForTheDayImageCard(quotes_for_the_day_text=quotes, quotes_for_the_day_author=author, quote_bg_image=motivation_bg_images))# quote_bg_image=motivation_bg_images[1]

        except requests.exceptions.ConnectionError:
            self.ErrorNetwork = True

    def delete_confirm(self, title, description):
        dialog = DeleteDialog(title=title, subtitle=description)
        dialog.open()

    def nav_drawer_open(self, *args):
        nav_drawer = self.root.children[0].ids.nav_drawer
        nav_drawer.set_state("open")
        self.root.get_screen('main').ids["nav_icon1"].icon = "close"
        if nav_drawer.state == "open":
            nav_drawer.set_state("close")
            self.root.get_screen('main').ids["nav_icon1"].icon = "view-dashboard-outline"

    def nav_drawer_close(self, *args):
        nav_drawer = self.root.children[0].ids.nav_drawer
        nav_drawer.set_state("close")
        self.root.get_screen('main').ids["nav_icon1"].icon = "view-dashboard-outline"

    def on_complete2(self, checkbox, value, male_button, calculate_btn, calculate_bmi_bg):

        if value:
            calculate_btn.disabled = False
            calculate_bmi_bg.md_bg_color = self.theme_cls.accent_color
            calculate_btn.text_color = 1, 1, 1, 1 #self.theme_cls.primary_color
            male_button.theme_text_color = "Custom"
            male_button.text_color = self.theme_cls.primary_color

        else:
            male_button.text_color = rgba(180, 180, 180, 255)
            calculate_btn.disabled = True
            calculate_bmi_bg.md_bg_color = 0, 0, 0, .3
            #toast("please choose your gender by clicking on the checkbox of the gender that suits your gender ")

    def on_complete1(self, checkbox, value, female_button, calculate_btn, calculate_bmi_bg):
        if value:
            calculate_btn.disabled = False
            calculate_bmi_bg.md_bg_color = self.theme_cls.accent_color
            calculate_btn.text_color = self.theme_cls.primary_color
            female_button.theme_text_color = "Custom"
            female_button.text_color = self.theme_cls.primary_color
        else:
            female_button.text_color = rgba(180, 180, 180, 255)
            calculate_btn.disabled = True
            calculate_bmi_bg.md_bg_color = 0, 0, 0, .3

    def get_height_value(self):
        slider_value = self.root.get_screen("main").ids.height_value
        self.root.get_screen("main").ids.slider_text.text = str(int(slider_value.value))

    # function to control the weight selection of the user
    def increase_weight(self):
        self.weight = self.weight + 1

    def decrease_weight(self):
        self.weight = self.weight - 1

        # function to control the age  selection of the user

    def increase_age(self):
        self.age = self.age + 1

    def decrease_age(self):
        self.age = self.age - 1

        # function to calculate the BMI

    def calculate_bmi(self):
        height = (self.root.get_screen("main").ids.height_value.value) / 100
        height_squared = height * height
        bmi = self.weight / height_squared
        weight_range = 'normal'
        if bmi < 18.5:
            weight_range = 'UnderWeight'
        elif bmi >= 18.5 and bmi <= 24.9:
            weight_range = 'normal'
        elif bmi >= 25 and bmi <= 29.9:
            weight_range = 'Overweight'
        elif bmi > 30:
            weight_range = 'Obese'
        self.dailog = MDDialog(
            title='BMI Calculated', text=f'your BMI is {bmi} \nYour Category is {weight_range}',
               buttons=[
                   MDFlatButton(
                       text="CANCEL", on_release=self.close_bmi_dailog
                   ),

                   MDFlatButton(
                       text="watch weight?", theme_text_color="Custom",
                       text_color=self.theme_cls.accent_color
                   ),
               ],
               )
        self.dailog.open()

    def close_bmi_dailog(self, obj):
        self.dailog.dismiss()

    def change_screen(self, screen_name):
        self.nav_drawer_close()
        self.root.get_screen("main").ids.scrn_mgnr.current = screen_name

    def change_page(self, page_name):
        self.root.get_screen("page").ids.scrn_mgnr.current = page_name

    def change_menu_page(self, menu_name):
        screen_manager.current = menu_name
        try:
            self.change_screen(menu_name)
        except:
            pass

    def change_color(self, inst):
        color = "#DFD7F3"
        if inst in self.root.get_screen('main').ids.values():
            current_id = list(self.root.get_screen('main').ids.keys())[list(self.root.get_screen('main').ids.values()).index(inst)]
            for i in range(5):
                if f"nav_icon{i+1}" == current_id:
                    self.root.get_screen('main').ids[f"nav_icon{i + 1}"].theme_icon_color = "Custom"
                    self.root.get_screen('main').ids[f"nav_icon{i+1}"].icon_color = self.main_primary_color#"#5D3AB7"
                else:
                    self.root.get_screen('main').ids[f"nav_icon{i + 1}"].theme_icon_color = "Custom"
                    self.root.get_screen('main').ids[f"nav_icon{i+1}"].text_color = self.nav_icon_color#"#DFD7F3" #0, 0, 0, .3
                    self.root.get_screen('main').ids[f"nav_icon{i + 1}"].icon_color = self.nav_icon_color #"#DFD7F3" #0, 0, 0, .3


class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class RoundedCheck(MDCheckbox):
    pass


class Check(MDCheckbox):
    pass


class MostPopularMotivation(MDCard):
    most_popular_quotes_text = StringProperty()
    most_popular_quotes_author = StringProperty()
    most_popular_quote_bg_image = StringProperty()
    #most_popular_quotes_bg_color = StringProperty()

class Categories(OneLineAvatarIconListItem):
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class CategoriesLayout(MDBoxLayout):
    pass


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    completed = BooleanProperty(False)


class EditTodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


Builder.load_string("""
<Text>:
    text_size: self.size
    valign: "middle"
    font_name: app.fonts.poppinsmedium
    shorten_from: "right"
    shorten: True
    color: [0,0,0, 1]
    markup: True
""")


class Text(Label):
    def __init__(self, **kw):
        super().__init__(**kw)


class Dates(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class ImageViewer(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)
    image = ""
    # app = App.get_running_app()
    # note_image_list = app.note_image_list
    image_count = StringProperty()

    def current_slide(self, index):
        app = App.get_running_app()
        carousel_index = index + 1
        self.image_count = f"{carousel_index}/{len(app.note_image_list)}"
        # Viewer.ids.image_count.texture_update()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def get_current_image(self):
        app = App.get_running_app()
        current_index = self.ids.image_viewer.index
        for current_index in range(len(app.note_image_list)):
            self.image = app.note_image_list[current_index]
        # return ""  # Return an empty string as a fallback
    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def load_images_to_carousel(self):
        carousel = self.ids.image_viewer
        carousel.clear_widgets()  # Clear existing slides

        for image_source in self.note_image_list:
            image = Image(source=image_source, radius=[15])
            carousel.add_widget(image)

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)


Builder.load_string("""
<ImageViewer>:
    background: ""
    background_color: [0,0,0,0]
    # pos_hint: {"center_x":.65, "center_y":.85}
    radius: [self.height*.08]
    size_hint: [None, .9]
    width: "300dp" #self.height
    MDFloatLayout:
        orientation: "vertical"
        size_hint: 1, 1
        pos_hint: {"center_x":.5, "center_y":.5}
        radius: [15]
        MDCarousel:
            id: image_viewer
            pos_hint: {"center_x":.5, "center_y":.5}
            on_current_slide: root.current_slide(self.index)
            on_slide_progress: root.get_current_image() #app.next_slide()
            
            
        MDLabel:
            id: image_count
            text: root.image_count
            font_size: 18
            bold: True
            color: app.main_primary_color
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.95}  
        MDIconButton:
            icon: "close"
            theme_icon_color: "Custom"
            icon_color: app.main_primary_color
            pos_hint: {"center_x":.12,"center_y":.95}
            icon_size: 18
            on_release: root.cancel()
        


""")


class ErrorDialogContent(MDFloatLayout):
    pass


class QuotesForTheDayImageCard(MDCard):
    quotes_for_the_day_text = StringProperty()
    quotes_for_the_day_author = StringProperty()
    quote_bg_image = StringProperty()


class LoadingDialog(MDFloatLayout):
    pass


class QuotesOfTheDaycard(FakeRectangularElevationBehavior, MDFloatLayout):
    qoute_of_the_day_text = StringProperty()
    quote_of_the_day_author = StringProperty()
    bg_color = StringProperty()


class ConfirmDialog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)
    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)

Builder.load_string("""
<ConfirmDialog>:
    background: ""
    background_color: [0,0,0,0]
    pos_hint: {"center_x":.65, "center_y":.85}
    size_hint: [None, .1]
    width: "180dp"
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.72, "center_y":.8}
        md_bg_color: 1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.08]
        width: "180dp"
        MDIconButton:
            icon: "close"
            pos_hint: {"center_x":.95, "center_y":.9}
            icon_size: 14
            # md_bg_color: 0,0,0,1
            on_release:
                root.cancel()
        MDTextButton:
            text: "Categories Manager"
            # color: "red"
            halign: "center"
            pos_hint: {"center_x":.42, "center_y":.63}
            on_release:
                app.change_screen("category_screen")
                root.cancel()

""")


class CategoriesDialog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)
    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)

Builder.load_string("""
<CategoriesDialog>:
    background: ""
    background_color: [0,0,0,0]
    pos_hint: {"center_x":.5, "center_y":.5}
    size_hint: [None, .8]
    width: "280dp"
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.5, "center_y":.5}
        md_bg_color: app.main_texture #1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.03]
        width: "180dp"
        MDLabel:
            text: "Categories"
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.95}
        OneLineIconListItem:
            divider: None
            text: "Add New Category"
            pos_hint: {"center_x":.5, "center_y":.88}
            line_color: app.main_texture
            width: "50dp"
            theme_text_color: "Custom"
            text_color: app.main_accent_color
            on_release:
                root.cancel()
                app.show_confirmation_dialog()
            IconLeftWidget:
                icon: "plus"
                theme_icon_color: "Custom"
                icon_color: app.main_primary_color
                on_release:
                    root.cancel()
                    app.show_confirmation_dialog()
        
        ScrollView:
            do_scroll_y: True
            do_scroll_x: False
            size_hint: 1, .67
            pos_hint: {"center_x":.5, "center_y":.52}
            bar_width: 0
            GridLayout:
                id: layout_manager
                cols: 1
                # spacing: 8, 8
                # padding: 8, 8
                size_hint: None, None
                height: self.minimum_height
                width: dp(350)
                pos_hint:{"center_x":.5, "center_y":.1}
        
        MDTextButton:
            text: "Cancel"
            halign: "center"
            font_size: 16
            theme_text_color: "Custom"
            text_color: app.theme_cls.accent_color
            pos_hint: {"center_x":.6, "center_y":.08}
            on_release:
                root.cancel()
        MDTextButton:
            text: "Save"
            font_size: 16
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            pos_hint: {"center_x":.85, "center_y":.08}
            # color: rgba("ffffff")
            on_release:
                root.cancel()


""")


class CatPlus(ButtonBehavior, MDBoxLayout):
    pass


class NoteImage(ButtonBehavior, MDFloatLayout):
    source = StringProperty("")


class EditNoteImage(ButtonBehavior, MDFloatLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class ContentNavigationDrawer(MDBoxLayout):
    pass


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        app = App.get_running_app()
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
        if instance_check.active == True:
            app.print_selected_item_text(self)


class DeleteTaskDialog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)

    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)


Builder.load_string("""
<DeleteTaskDialog>:
    background: ""
    background_color: [0,0,0,0]
    # pos_hint: {"center_x":.65, "center_y":.85}
    radius: [self.height*.08]
    size_hint: [None, .4]
    width: "220dp" #self.height
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.72, "center_y":.8}
        md_bg_color: 1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.08]
        # width: "250dp"
        MDFloatLayout:
            size_hint: .3, .27
            pos_hint: {"center_x":.5, "center_y":.8}
            md_bg_color: "red"
            radius: [44]
            MDIconButton:
                icon: "trash-can-outline"
                pos_hint: {"center_x":.5, "center_y":.5}
                icon_size: "40dp"
                ripple_scale: 0
                md_bg_color: "#FFFFFF"
                theme_icon_color: "Custom"
                icon_color: "red"
                # on_release:
                #     root.cancel()
        MDLabel:
            text: "Delete ?"
            bold: True
            font_name: app.fonts.poppinsbold
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.53}
            
        MDLabel:
            text: "Note: If you delete this note, action cannot be undone. do you still want to delete?"
            size_hint_x: .85
            font_size: 13
            font_name: app.fonts.poppinsregular
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.36}
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: "red"
            radius: [5]
            pos_hint: {"center_x":.7, "center_y":.13}
            MDTextButton:
                text: "Delete"
                # color: "red"
                theme_text_color: "Custom"
                text_color: "#FFFFFF"
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release:
                    app.delete_full_task(title=root.title, description=root.subtitle)
                    root.cancel()
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: 0, 0, 0, .08
            radius: [5]
            pos_hint: {"center_x":.3, "center_y":.13}
            MDTextButton:
                text: "Cancel"
                # font_size: dp(30)
                # md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x":.5, "center_y":.5}
                # color: rgba("ffffff")
                on_release:
                    root.cancel()



    """)


class DeleteCateDialog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)

    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)


Builder.load_string("""
<DeleteCateDialog>:
    background: ""
    background_color: [0,0,0,0]
    # pos_hint: {"center_x":.65, "center_y":.85}
    radius: [self.height*.08]
    size_hint: [None, .4]
    width: "220dp" #self.height
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.72, "center_y":.8}
        md_bg_color: 1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.08]
        # width: "250dp"
        MDFloatLayout:
            size_hint: .3, .27
            pos_hint: {"center_x":.5, "center_y":.8}
            md_bg_color: "red"
            radius: [44]
            MDIconButton:
                icon: "trash-can-outline"
                pos_hint: {"center_x":.5, "center_y":.5}
                icon_size: "40dp"
                ripple_scale: 0
                md_bg_color: "#FFFFFF"
                theme_icon_color: "Custom"
                icon_color: "red"
                # on_release:
                #     root.cancel()
        MDLabel:
            text: "Delete ?"
            bold: True
            font_name: app.fonts.poppinsbold
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.56}

        MDLabel:
            text: "Note: If you delete this Category, action cannot be undone. do you still want to delete?"
            size_hint_x: .85
            font_size: 12
            font_name: app.fonts.poppinsregular
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.36}
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: "red"
            radius: [5]
            pos_hint: {"center_x":.7, "center_y":.13}
            MDTextButton:
                text: "Delete"
                # color: "red"
                theme_text_color: "Custom"
                text_color: "#FFFFFF"
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release:
                    app.delete_category(title=root.title)
                    root.cancel()
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: 0, 0, 0, .08
            radius: [5]
            pos_hint: {"center_x":.3, "center_y":.13}
            MDTextButton:
                text: "Cancel"
                # font_size: dp(30)
                # md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x":.5, "center_y":.5}
                # color: rgba("ffffff")
                on_release:
                    root.cancel()



    """)


class LogoutDailog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)

    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)


Builder.load_string("""
<LogoutDailog>:
    background: ""
    background_color: [0,0,0,0]
    # pos_hint: {"center_x":.65, "center_y":.85}
    radius: [self.height*.08]
    size_hint: [None, .4]
    width: "220dp" #self.height
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.72, "center_y":.8}
        md_bg_color: 1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.08]
        # width: "220dp"
        MDFloatLayout:
            size_hint: .5, .32
            pos_hint: {"center_x":.5, "center_y":.76}
            radius: [44]
            FitImage:
                source: "store/why_logout.png"
                pos_hint: {"center_x":.5, "center_y":.45}
                
        MDLabel:
            text: "Comeback Soon!"
            bold: True
            font_name: app.fonts.poppinsbold
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.5}
            
        MDLabel:
            text: "Are you sure you want to logout?"
            size_hint_x: .85
            font_size: 16
            font_name: app.fonts.poppinsregular
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.33}
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: "red"
            radius: [5]
            pos_hint: {"center_x":.7, "center_y":.13}
            MDTextButton:
                text: "Logout"
                # color: "red"
                theme_text_color: "Custom"
                text_color: "#FFFFFF"
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release:
                    app.logout()
                    root.cancel()
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: 0, 0, 0, .08
            radius: [5]
            pos_hint: {"center_x":.3, "center_y":.13}
            MDTextButton:
                text: "Cancel"
                # font_size: dp(30)
                # md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x":.5, "center_y":.5}
                # color: rgba("ffffff")
                on_release:
                    root.cancel()

    """)


class ResetThemesDialog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)

    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def delete(self):
        # Access the title and description from the DeleteDialog properties
        title = self.title
        description = self.subtitle

        # Call the delete_note method of the SkiddooApp class
        App.get_running_app().delete_note(title, description)

        # Dismiss the DeleteDialog
        self.dismiss()

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)


Builder.load_string("""
<ResetThemesDialog>:
    background: ""
    background_color: [0,0,0,0]
    # pos_hint: {"center_x":.65, "center_y":.85}
    radius: [self.height*.08]
    size_hint: [None, .4]
    width: "220dp" #self.height
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.72, "center_y":.8}
        md_bg_color: 1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.08]
        MDFloatLayout:
            size_hint: .33, .3
            pos_hint: {"center_x":.5, "center_y":.8}
            md_bg_color: "red"
            radius: [44]
            MDIconButton:
                icon: "frequently-asked-questions"
                pos_hint: {"center_x":.5, "center_y":.5}
                icon_size: "60dp"
                ripple_scale: 0
                md_bg_color: "#FFFFFF"
                theme_icon_color: "Custom"
                icon_color: "red"

        MDLabel:
            text: "Reset Themes ?"
            bold: True
            font_name: app.fonts.poppinsbold
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.6}

        MDLabel:
            text: "Reseting this themes will revert the colors back to the main app color, Are you sure you want to Reset?"
            size_hint_x: .85
            font_size: 13
            font_name: app.fonts.poppinsregular
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.38}
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: "red"
            radius: [5]
            pos_hint: {"center_x":.7, "center_y":.13}
            MDTextButton:
                text: "Reset"
                # color: "red"
                theme_text_color: "Custom"
                text_color: "#FFFFFF"
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release:
                    app.reset_themes()
                    root.cancel()
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: 0, 0, 0, .08
            radius: [5]
            pos_hint: {"center_x":.3, "center_y":.13}
            MDTextButton:
                text: "Cancel"
                # font_size: dp(30)
                # md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x":.5, "center_y":.5}
                # color: rgba("ffffff")
                on_release:
                    root.cancel()


""")


class DeleteDialog(ModalView):
    callback = ObjectProperty(allownone=True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone=True)
    cancelCallback = ObjectProperty(allownone=True)
    # confirmColor = ColorProperty([1, 1, 1, 1])
    # cancelColor = ColorProperty([1, 1, 1, 1])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def delete(self):
        # Access the title and description from the DeleteDialog properties
        title = self.title
        description = self.subtitle

        # Call the delete_note method of the SkiddooApp class
        App.get_running_app().delete_note(title, description)

        # Dismiss the DeleteDialog
        self.dismiss()

    def cancel(self):
        self.dismiss()

        if self.cancelCallback:
            self.cancelCallback()

    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            toast(f"Successfully Deleted", background=App.get_running_app().color_tertiary)

Builder.load_string("""
<DeleteDialog>:
    background: ""
    background_color: [0,0,0,0]
    # pos_hint: {"center_x":.65, "center_y":.85}
    radius: [self.height*.08]
    size_hint: [None, .4]
    width: "220dp" #self.height
    MDFloatLayout:
        orientation: "vertical"
        spacing: dp(12)
        # padding: dp(14)
        pos_hint: {"center_x":.72, "center_y":.8}
        md_bg_color: 1, 1, 1, 1 #app.color_primary_bg
        radius: [self.height*.08]
        MDFloatLayout:
            size_hint: .33, .3
            pos_hint: {"center_x":.5, "center_y":.8}
            md_bg_color: "red"
            radius: [44]
            MDIconButton:
                icon: "trash-can-outline"
                pos_hint: {"center_x":.5, "center_y":.5}
                icon_size: "60dp"
                ripple_scale: 0
                md_bg_color: "#FFFFFF"
                theme_icon_color: "Custom"
                icon_color: "red"
                # on_release:
                #     root.cancel()
        MDLabel:
            text: "Delete ?"
            bold: True
            font_name: app.fonts.poppinsbold
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.53}
            
        MDLabel:
            text: "Note: If you delete this note, action cannot be undone. do you still want to delete?"
            size_hint_x: .85
            font_size: 16
            font_name: app.fonts.poppinsregular
            halign: "center"
            pos_hint: {"center_x":.5, "center_y":.36}
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: "red"
            radius: [5]
            pos_hint: {"center_x":.7, "center_y":.13}
            MDTextButton:
                text: "Delete"
                # color: "red"
                theme_text_color: "Custom"
                text_color: "#FFFFFF"
                halign: "center"
                pos_hint: {"center_x":.5, "center_y":.5}
                on_release:
                    app.delete_note(title=root.title, description=root.subtitle)
                    # app.delete_note()
                    root.cancel()
        MDFloatLayout:
            size_hint: .3, .09
            md_bg_color: 0, 0, 0, .08
            radius: [5]
            pos_hint: {"center_x":.3, "center_y":.13}
            MDTextButton:
                text: "Cancel"
                # font_size: dp(30)
                # md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x":.5, "center_y":.5}
                # color: rgba("ffffff")
                on_release:
                    root.cancel()


""")


class NoteCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class TaskCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class ProgressCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class AllProgressCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class AllTasksCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class AllCompletedCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class CompletedCard(ButtonBehavior, FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class CategoriesManager(ButtonBehavior, MDFloatLayout):
    title = StringProperty("")
    task_count = NumericProperty(0)
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass

    def delete_product(self):
        if self.callback:
            self.callback(self)


class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")


class CircularRippleButton(CircularRippleBehavior, ButtonBehavior, MDIcon):
    def __init__(self, **kwargs):
        self.ripple_scale = 0.85
        super().__init__(**kwargs)


class TaskCategories(ButtonBehavior, MDBoxLayout):
    title = StringProperty("")
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 1)

    def render(self, _):
        pass


if __name__ == '__main__':
    Tasksivate().run()

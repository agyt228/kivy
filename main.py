from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from api import API
import config
session = None

class LoginScreen(Screen):
    def validate_user(self):
        global session
        api_request = API()
        response = api_request.request_post('auth', {'login': self.ids.username_input.text, 'password': self.ids.password_input.text})
        if response['status'] == 'ok':
            token = response['token']
            session = token


        if session == None:
            self.show_invalid_login_popup()
        else:
            if session != None:
                response = api_request.request_post('list_chats', {'token': session})
                if response['status'] == 'ok':

                    chat_screen = self.manager.get_screen('chats')
                    chat_screen.set_chat_list(response['chat'])
                    self.manager.current = 'chats'

    def show_invalid_login_popup(self):
        popup = Popup(title='Ошибка авторизации', content=Label(text='Логин и/или пароль введены не верно!'), size_hint=(0.6, 0.4))
        popup.open()
class ChatListScreen(Screen):
    def __init__(self, **kwargs):
        global session
        super(ChatListScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical')
        self.header = Label(text="Список чатов", font_size='54px', size_hint=(1, 0.1))
        self.layout.add_widget(self.header)



        self.create_chat_btn = Button(text='Создать чат', size_hint=(1, 0.1))
        self.create_chat_btn.bind(on_press=self.create_chat)
        self.layout.add_widget(self.create_chat_btn)

        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.chat_list_layout = GridLayout(cols=1, size_hint_y=None)
        self.chat_list_layout.bind(minimum_height=self.chat_list_layout.setter('height'))
        self.scroll_view.add_widget(self.chat_list_layout)
        self.layout.add_widget(self.scroll_view)

        self.add_widget(self.layout)




    def set_chat_list(self, chats):
        self.chat_list_layout.clear_widgets()

        for chat in chats:
            grid_chats_list = GridLayout(cols=2) #сетка состоит из 2-х колонок

            #1 добавляем аватарку
            avatar = AsyncImage(source = f'{config.url_site}{chat['avatar']}', size_hint_x=None, width=200)
            grid_chats_list.add_widget(avatar)

            #2 добавляем кнопку
            btn = Button(text=chat['title'], size_hint = (0.4, 1), height=60)
            btn.bind(on_press=partial(self.open_chat, chat['id']))
            grid_chats_list.add_widget(btn)

            #эту сетку добавляем в окно
            self.chat_list_layout.add_widget(grid_chats_list)
    def create_chat(self, instance):


        box1 = BoxLayout(orientation='vertical')
        label_title = Label(size_hint=(1, None), text='Введите название чата')
        box1.add_widget(label_title)
        self.input_title = TextInput(size_hint=(1, None), hint_text='Введите название чата', multiline=False)
        box1.add_widget(self.input_title)

        label_description = Label(size_hint=(1, None), text='Введите описание чата')
        box1.add_widget(label_description)
        self.input_description = TextInput(size_hint=(1, None), hint_text='Введите описание чата', multiline=False)
        box1.add_widget(self.input_description)

        create_chat_btn = Button(size_hint=(0.7, None), text='Создать чат')
        create_chat_btn.bind(on_press=self.create_chat_1)
        box1.add_widget(create_chat_btn)
        self.popup_create_chat = Popup(title='Создание чата', content=box1,
                      size_hint=(0.6, 0.4))
        self.popup_create_chat.open()
    def open_chat(self, chat_id, instance):
        title = self.input_title
        token = session

    def create_chat_1(self, instance):
        pass
        #запрос на создание чата
        #token находится в переменной session
        title = self.input_title.text
        description = self.input_description.text
        api = API()
        response = api.request_post('create_chat', {'token': session, 'title': title, 'description': description})
        if response['status'] == 'ok':
            self.refresh_chat_list()
        self.popup_create_chat.dismiss()
    def refresh_chat_list(self):
        api = API()
        response = api.request_post('list_chats', {'token': session})
        self.set_chat_list(response['chat'])
    def show_create_chat_popup(self):
        pass
class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ChatListScreen(name='chats'))
        return sm

LoginApp().run()





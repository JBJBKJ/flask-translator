from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
import requests

class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.filechooser = FileChooserIconView(filters=["*.mp3", "*.wav", "*.m4a"])
        self.add_widget(self.filechooser)

        self.send_button = Button(text="Отправить файл на сервер", size_hint=(1, 0.1))
        self.send_button.bind(on_press=self.send_file)
        self.add_widget(self.send_button)

        self.result_label = Label(text="Результат появится здесь", size_hint=(1, 0.2))
        self.add_widget(self.result_label)

    def send_file(self, instance):
        if not self.filechooser.selection:
            self.result_label.text = "Файл не выбран"
            return

        file_path = self.filechooser.selection[0]
        self.result_label.text = "Отправка..."

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                # ⚠️ ЗАМЕНИ IP на свой из Flask (если нужно)
                response = requests.post("http://127.0.0.1:5000/transcribe", files=files)

            if response.status_code == 200:
                result = response.json()
                self.result_label.text = f"Текст: {result['text']}\nПеревод: {result['translation']}"
            else:
                self.result_label.text = f"Ошибка: {response.text}"
        except Exception as e:
            self.result_label.text = f"Ошибка: {str(e)}"

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()

# # from tkinter import *  # importing the tkinter library

# # #creating tkinter window
# # root = Tk()

# # # title function change the tittle to calculator
# # root.title('Antivirus')

# # #setting the dimension of window
# # root.geometry('1031x553+100+125')

# # # disable window resizing
# # #root.resizable(False, False)

# # # changing background
# # root['bg']="grey"

# # # expression variable
# # expression_value = " "

# # def adjust_text_size(event):
# #     new_height = root.winfo_height()  # Get the new height of the window
# #     new_width = root.winfo_width()
# #     print(new_height, "   ",new_width)
# #     font_size = new_height // 12
# #     paddingx = new_height // 36
# #     paddingy = new_width // 36
# #     # Update the font size for the entry field and buttons
# #     # entry_field.config(font=("Arial", font_size))
# #     # input_frame.grid_configure(padx=paddingx,pady=paddingy)
# #     # button_frame.grid_configure(padx=paddingx,pady=paddingy)

# # root.bind("<Configure>", adjust_text_size)

# # root.mainloop()






# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.button import Button

# class MyApp(App):
#     def build(self):
#         # Create the main layout
#         layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
#         # Create a label and a button
#         self.label = Label(text="Hello, Kivy!")
#         button = Button(text="Click Me!")
        
#         # Bind the button click event to a custom function
#         button.bind(on_press=self.on_button_click)
        
#         # Add the label and button to the layout
#         layout.add_widget(self.label)
#         layout.add_widget(button)
        
#         return layout

#     def on_button_click(self, instance):
#         # Update the label text when the button is clicked
#         self.label.text = "Button Clicked!"

# if __name__ == '__main__':
#     MyApp().run()

# # import sys
# # from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# # class MyWindow(QWidget):
# #     def __init__(self):
# #         super().__init__()

# #         # Set up the main window
# #         self.setWindowTitle("PyQt5 Example")
# #         self.setGeometry(100, 100, 400, 200)

# #         # Create widgets
# #         self.label = QLabel("Hello, PyQt5!")
# #         self.button = QPushButton("Click Me!")

# #         # Create a vertical layout
# #         layout = QVBoxLayout()
# #         layout.addWidget(self.label)
# #         layout.addWidget(self.button)

# #         # Set the layout for the main window
# #         self.setLayout(layout)

# #         # Connect the button click event to a custom function
# #         self.button.clicked.connect(self.on_button_click)

# #     def on_button_click(self):
# #         # Update the label text when the button is clicked
# #         self.label.setText("Button Clicked!")

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = MyWindow()
# #     window.show()
# #     sys.exit(app.exec_())

# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.animation import Animation

# class LoginWindow(BoxLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.orientation = 'vertical'
#         self.spacing = 10
#         self.padding = [20, 20]

#         self.username_input = TextInput(hint_text='Username', multiline=False)
#         self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
#         self.login_button = Button(text='Login')
        
#         self.add_widget(Label(text='Login', font_size=30))
#         self.add_widget(self.username_input)
#         self.add_widget(self.password_input)
#         self.add_widget(self.login_button)

#     def animate_login(self):
#         # Create an animation to slide in the login window
#         slide_in = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=1)
#         slide_in.bind(on_complete=self.on_login_animation_complete)

#         # Start the slide-in animation
#         slide_in.start(self)

#     def on_login_animation_complete(self, widget, animation):
#         # Animation complete callback (you can perform login logic here)
#         pass

# class MyApp(App):
#     def build(self):
#         login_window = LoginWindow()
#         login_window.animate_login()  # Start the login window animation
#         return login_window

# if __name__ == '__main__':
#     MyApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation

class LoginWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [20, 20]

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.login_button = Button(text='Login')
        
        self.add_widget(Label(text='Login', font_size=30))
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)

    def animate_login(self):
        # Create an animation to scale in the login window
        scale_in = Animation(size_hint=(1, 1), duration=1)
        scale_in.bind(on_complete=self.on_login_animation_complete)

        # Start the scale-in animation
        scale_in.start(self)

    def on_login_animation_complete(self, widget, animation):
        # Animation complete callback (you can perform login logic here)
        pass

class MyApp(App):
    def build(self):
        login_window = LoginWindow()
        login_window.animate_login()  # Start the login window animation
        return login_window

if __name__ == '__main__':
    MyApp().run()

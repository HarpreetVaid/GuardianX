import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class PasswordManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)  # Remove frame and title bar
        self.setWindowTitle("Password Manager")
        self.setGeometry(330, 160, 1565, 565)  # Set the fixed window position
        
        self.initUI()
        
        # Create a database or connect to an existing one
        self.conn = sqlite3.connect('password_manager.db')
        
        # Create a table to store usernames, passwords, and website names
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                website TEXT,
                username TEXT,
                password TEXT
            )
        ''')
        self.conn.commit()
    
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        
        self.website_label = QtWidgets.QLabel("Website:")
        self.website_input = QtWidgets.QLineEdit()
        
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_input = QtWidgets.QLineEdit()
        
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_password)
        
        self.show_all_button = QtWidgets.QPushButton("Show All")
        self.show_all_button.clicked.connect(self.show_all_passwords)
        
        self.output_text = QtWidgets.QTextEdit()
        
        layout.addWidget(self.website_label)
        layout.addWidget(self.website_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.show_all_button)
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
    
    def save_password(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        
        if website and username and password:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)', (website, username, password))
            self.conn.commit()
            self.output_text.append(f'Password for {website} has been saved.')
            self.clear_inputs()
    
    def show_all_passwords(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT website, username, password FROM passwords')
        results = cursor.fetchall()
        
        if results:
            self.output_text.clear()
            for website, username, password in results:
                self.output_text.append(f'Website: {website}')
                self.output_text.append(f'Username: {username}')
                self.output_text.append(f'Password: {password}')
                self.output_text.append('-' * 20)
        else:
            self.output_text.append('No passwords saved.')

    def clear_inputs(self):
        self.website_input.clear()
        self.username_input.clear()
        self.password_input.clear()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = PasswordManager()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

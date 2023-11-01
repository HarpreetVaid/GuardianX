import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QIcon
import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import system_hardware_info
import system_live_info
import system_virus_check
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QThread, QObject, pyqtSignal, Qt
from junk_removers import JunkRemover
import subprocess
from password import PasswordManager  # Import the PasswordManager class
from system_virus_check import VirusScanner
import re


class LivePlotApp:
    def __init__(self, parent=None):
        self.data = 0
        # Initialize lists to store historical data for CPU frequency and RAM
        self.cpu_freq = []
        self.ram_usage = []
        self.partition = []

        # # Initialize lists to store historical data for CPU frequency and RAM
        self.cpu_freq = []
        self.ram_usage = []

        self.hardware_info = system_hardware_info.get_hardware_info()
        for keys in self.hardware_info['partition']:
            self.partition.append(keys)

        # Create two subplots (2 rows, 2 columns)
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)
                   ) = plt.subplots(2, 2, figsize=(12, 8))

        # Initialize empty lists for data
        self.x_data = []
        self.y_data1 = []
        self.y_data2 = []

        # Create an animation to update the plots
        # Update every 1 second
        self.ani = FuncAnimation(
            self.fig, self.update_data, interval=1000, save_count=10)

        # Hide x and y axis tick labels (showing none)
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_xticks([])  # Remove x-axis tick marks
            ax.set_yticks([])  # Remove y-axis tick marks

        # Adjust layout
        plt.tight_layout()

    def generate_random_data(self):
        return [random.randint(0, 100) for _ in range(2)]

    def update_data(self, i):
        # Replace with actual data retrieval
        live_info = system_live_info.get_live_info()
        if self.data > 15:
            self.cpu_freq.pop(0)
            self.ram_usage.pop(0)
        self.data += 1

        # Update CPU frequency and RAM data
        self.cpu_freq.append(live_info['cpu_info']['cpu_usage'])
        self.ram_usage.append(live_info['used_ram'])

        # Limit the data to show only the last N points
        max_points = 10
        if len(self.cpu_freq) > max_points:
            self.cpu_freq.pop(0)
            self.ram_usage.pop(0)

        # Append new data to x_data, y_data1, and y_data2
        # Use the 'data' variable as x-axis value
        self.x_data.append(self.data)
        # Update with the actual CPU data
        self.y_data1.append(float(live_info['cpu_info']['cpu_usage']))
        # Update with the actual RAM data
        self.y_data2.append(float(live_info['used_ram']))

        # Update the line plots
        self.ax1.clear()
        self.ax1.plot(self.x_data, self.y_data1, marker=None)
        self.ax1.set_title('CPU Usage')
        self.ax1.set_xlabel('X-axis')
        self.ax1.set_ylabel('Y-axis')

        self.ax2.clear()
        self.ax2.plot(self.x_data, self.y_data2, marker=None)
        self.ax2.set_title('RAM Usage')
        self.ax2.set_xlabel('X-axis')
        self.ax2.set_ylabel('Y-axis')

        # Generate random data for the pie charts (replace with actual data)
        data1 = [self.hardware_info['partition'][self.partition[0]],
                 live_info['partition'][self.partition[0]]]
        data2 = [self.hardware_info['partition'][self.partition[1]],
                 live_info['partition'][self.partition[1]]]

        # Update the pie charts with appropriate labels
        self.ax3.clear()
        self.ax3.pie(data1, labels=['Used', 'Unused'],
                     autopct='%1.1f%%', startangle=45)
        self.ax3.set_title(self.partition[0])

        self.ax4.clear()
        self.ax4.pie(data2, labels=['Used', 'Unused'],
                     autopct='%1.1f%%', startangle=45)
        self.ax4.set_title(self.partition[1])

    def start(self):

        self.ani = FuncAnimation(
            self.fig, self.update_data, interval=1000, save_count=10)
        plt.show()

    def stop(self):
        # Stop the animation and release any resources
        self.ani.event_source.stop()
        plt.close(self.fig)


class JunkRemovalWorker(QObject):
    progress_changed = pyqtSignal(str)
    results_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.junk_remover = JunkRemover()

    def run(self):
        # Perform the junk file removal
        result = self.junk_remover.remove_temp_files()
        if result:
            progress, results = result
            self.progress_changed.emit(progress)
            # Emit the details of the removed files
            for file_path, success in results.items():
                if success:
                    self.results_ready.emit(f"Removed: {file_path}")
                else:
                    self.results_ready.emit(f"Failed to remove: {file_path}")
        else:
            self.progress_changed.emit(f"{'PYTHON'}:{'junk_removers.py'}")
            self.results_ready.emit("Junk file removal failed")


# Update the SHAWorker class to emit progress and result signals
# class SHAWorker(QThread):
#     progress_changed = pyqtSignal(str)
#     results_ready = pyqtSignal(str)

#     def __init__(self):
#         super().__init__()

#     def run(self):
#         # Perform the SHA scan
#         virus_scanner = VirusScanner()

#         # Simulate progress updates (replace with actual progress)
#         for progress in range(0, 101, 10):
#             self.progress_changed.emit(f"Progress: {progress}%")

#         # Simulate scan results (replace with actual results)
#         scan_results = "Scan completed. No threats found."
#         self.results_ready.emit(scan_results)


class Ui_MainWindow(object):
    def __init__(self):
        self.current_content = None
        self.port_scan_button = None
        # self.sha_worker = SHAWorker()
        self.junk_worker = JunkRemovalWorker()
        self.dynamic_label = QLabel()
        self.output_textedit = QTextEdit()
        self.password_manager = None  # Initialize the PasswordManager instance to None

    def sha_scan_action(self):
        # Clear the terminal output
        self.terminal_output.clear()

    # Simulate the SHA scan progress and results
        progress = 0
        while progress <= 100:
            self.terminal_output.append(f"Progress: {progress}%")
            progress += 10
            QtCore.QCoreApplication.processEvents()  # Ensure the GUI remains responsive

    # Simulate scan results (replace with actual results)
        scan_results = "Scan completed. No threats found."

    # Display the final scan result
        self.terminal_output.append(scan_results)

    def show_SHA_SCAN_window(self):
        if self.sha_scan is None:
            # Create an instance of PasswordManager
            self.sha_scan = VirusScanner()
            self.sha_scan.show()  # Show the PasswordManager window

    def perform_port_scanning(self):
        # Full path to the nmap executable
        nmap_executable = "R:\\Nmap\\nmap.exe"  # Replace with the actual path to nmap

        scanner = subprocess.Popen(
            [nmap_executable, "-p", "1-65535", "--min-rate",
                "1000", "--max-retries", "1", "127.0.0.1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = scanner.communicate()
        port_pattern = r"(\d+)/tcp\s+(open|filtered)\s+(\w+)"
        stdout = re.findall(port_pattern, stdout)
        if scanner.returncode == 0:
            # nmap command executed successfully
            output = stdout
        else:
            # nmap command encountered an error
            output = f"Error:\n{stderr}"

    # Display the output in the QTextEdit
        self.terminal_output.clear()
        for port, state, service in output:
            self.terminal_output.append(
                f"Port {service} at {port} and state is {state} ")

    def show_password_manager_window(self):
        if self.password_manager is None:
            # Create an instance of PasswordManager
            self.password_manager = PasswordManager()
            self.password_manager.show()  # Show the PasswordManager window

    def close_password_manager_window(self):
        # Close the PasswordManager window if it exists
        if self.password_manager is not None:
            self.password_manager.close()
            self.password_manager = None

    def JUNK_REMOVE_action(self):
        # Clear the terminal output
        self.terminal_output.clear()

        # Run the junk removal command using subprocess and capture the output
        try:
            junk_output = subprocess.check_output(
                ["python", "junk_removers.py"], stderr=subprocess.STDOUT, text=True)

            # Display the output in the QTextEdit
            self.terminal_output.append(junk_output)
        except subprocess.CalledProcessError as e:
            # Display any errors or exceptions in the QTextEdit
            self.terminal_output.append(f"Error: {e.output}")

    def update_dynamic_label(self, text):
        self.dynamic_label.setText(text)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("HVR SOLUTIONS")
        MainWindow.resize(924, 911)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a horizontal layout for the central widget
        central_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        # Left Side Dashboard
        self.left_dashboard = QtWidgets.QWidget()
        self.left_dashboard.setObjectName("left_dashboard")
        self.left_dashboard.setStyleSheet(
            "background-color: #3A3D3B;"
        )

        # Set a fixed width for the left dashboard
        self.left_dashboard.setFixedWidth(300)

        # Create a vertical layout for the left dashboard
        self.left_dashboard_layout = QtWidgets.QVBoxLayout(self.left_dashboard)
        self.left_dashboard_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Add a label for "HVR SOLUTIONS" at the top
        self.label = QLabel("HVR SOLUTIONS")
        self.label.setStyleSheet(
            "color: white;"
            "font-size: 36px;"
            "font-weight: bold;"
            "padding: 50px 20px;"
            "border-radius: 25px;"
        )
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # Create a QGraphicsDropShadowEffect for the label
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
        shadow_effect.setOffset(7, 7)

        # Apply the shadow effect to the label
        self.label.setGraphicsEffect(shadow_effect)

        # Create a QLabel for displaying the image
        image_label = QLabel()
        pixmap = QPixmap("icon/logo-removebg-preview (1).png")
        pixmap = pixmap.scaled(350, 350)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create a spacer item for spacing between image and buttons
        spacer_item = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.left_dashboard_layout.addWidget(self.label)
        self.left_dashboard_layout.addWidget(image_label)
        self.left_dashboard_layout.addItem(spacer_item)
        self.left_dashboard_layout.setContentsMargins(10, 10, 10, 10)

        # Create buttons for the dashboard
        self.dashboard_buttons = []

        def button_clicked(index):
            def on_button_clicked():
                for i, button in enumerate(self.dashboard_buttons):
                    if i == index:
                        button.setStyleSheet("background-color: red;"
                                             "color: white;"
                                             "   border: ;"
                                             "   border-radius: 18px;"

                                             )
                    else:
                        button.setStyleSheet(
                            "QPushButton {"
                            "   background-color: #3465a4;"
                            "   color: white;"
                            "   border: ;"
                            "   border-radius: 25px;"
                            "   font-size: 21px;"
                            "   padding: 10px;"
                            "}"
                            "QPushButton:hover {"
                            "   background-color: #204a87;"
                            "}")

                self.show_right_option(index)

                if index == 1:  # "SCAN" button clicked
                    # ... previous code ...

                    button3 = QtWidgets.QPushButton("SHA SCAN")
                    # button3.setIcon(QIcon(SHA_image))  # Set the Full Scan image
                    # Adjust the size as needed
                    button3.setIconSize(QtCore.QSize(80, 80))
                    button3.clicked.connect(self.sha_scan_action)

                elif index == 2:  # "SCAN" button clicked
                    # ... previous code ...

                    button2 = QtWidgets.QPushButton("JUNK REMOVER")

                    button2.setIconSize(QtCore.QSize(80, 80))
                    button2.clicked.connect(self.JUNK_REMOVE_action)

                elif index == 0:  # "STATUS" button clicked
                    # Clear any existing widgets in the right_output layout
                    self.remove_plot()

    # Create an instance of the LivePlotApp class
                    live_plot = LivePlotApp(self.right_output)

    # Create a canvas for the live plot
                    canvas = FigureCanvasQTAgg(live_plot.fig)
                    canvas.show()

    # Update the current content to the LivePlotApp instance
                    self.current_content = live_plot

    # Add the canvas widget to the right side layout
                    self.right_output_layout.addWidget(canvas)

            return on_button_clicked

        button_data = [
            {"text": "STATUS", "image_path": "icon/status.png"},
            {"text": "SCAN", "image_path": "icon/search.png"},
            {"text": "MORE TOOLS", "image_path": "icon/folder.png"},
            {"text": "FIREWALL", "image_path": "icon/firewall.png"},
            {"text": "NETWORK-SECURITY", "image_path": "icon/network.png"},
            {"text": "ABOUT", "image_path": "icon/Information.png"},
        ]

        for idx, data in enumerate(button_data):
            button = QtWidgets.QPushButton()
            button.setObjectName(data["text"])
            button.setText(data["text"])

            # Load the image from the provided image_path
            button_image = QPixmap(data["image_path"])
            button.setIcon(QIcon(button_image))
            # Adjust the size as needed
            button.setIconSize(QtCore.QSize(60, 40))

            # Connect the button's clicked signal to a function
            button.clicked.connect(button_clicked(idx))

            # Create a shadow effect for the button
            button_shadow_effect = QGraphicsDropShadowEffect()
            button_shadow_effect.setBlurRadius(5)
            button_shadow_effect.setColor(QtGui.QColor(0, 0, 0, 160))
            button_shadow_effect.setOffset(2, 2)

            button.setGraphicsEffect(button_shadow_effect)

            # Set a fixed width for the buttons
            button.setFixedWidth(270)

            # Adjust the button styling
            button.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: green;"
                "   border-radius: 25px;"
                "   font-size: 21px;"
                "   padding: 10px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )

            self.dashboard_buttons.append(button)
            self.left_dashboard_layout.addWidget(button)

            if idx < len(button_data) - 1:
                spacer_item = QtWidgets.QSpacerItem(
                    20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                self.left_dashboard_layout.addItem(spacer_item)

        # Right Side Output Frame
        self.right_output = QtWidgets.QWidget()

        self.right_output.setObjectName("WE ARE THE SOLUTION OF OUR SIDE")
        self.right_output.setStyleSheet("background-color: #3A3D3B;")

        central_layout.addWidget(self.left_dashboard)
        central_layout.addWidget(self.right_output)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.right_output_layout = QtWidgets.QVBoxLayout(self.right_output)
        self.timer = QtCore.QTimer(MainWindow)
        self.timer.timeout.connect(self.change_label_color)
        self.timer.start(500)

        # Create a QLabel for displaying dynamic text at the top of the right side frame
        self.dynamic_label = QLabel()
        self.dynamic_label.setStyleSheet(
            "color: white;"
            "font-size: 50px;"
            "font-weight: bold;"
            "padding: 10px 10px 800px 200px;"
        )
        self.show_initial_text()  # Add this line to show the initial text

    def change_label_color(self):
        color_input = self.get_random_color()
        self.label.setStyleSheet(
            f"color: {color_input};"
            "font-size: 36px;"
            "padding: 10px 0;"
        )

    def update_dynamic_label(self, text):
        self.text_edit.clear()
        self.text_edit.append(text)

    def remove_plot(self):
        # Clear the right_output layout to remove any existing widgets
        for i in reversed(range(self.right_output_layout.count())):
            widget = self.right_output_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def change_label_color(self):
        color_input = self.get_random_color()
        self.label.setStyleSheet(
            f"color: {color_input};"
            "font-size: 36px;"
            "padding: 10px 0;"
        )

    def get_random_color(self):
        letters = '0123456789ABCDEF'
        color = '#'
        for _ in range(6):
            color += random.choice(letters)
        return color

    def show_initial_text(self):
        # Create a QLabel for displaying the initial text
        initial_text_label = QLabel("WE ARE THE SECURE NOW")
        initial_text_label.setStyleSheet(
            "color: green;"
            "font-size: 55px;"
            "font-weight: bold;"
            "padding: 20px 10px 800px 200px;"
        )
        # Add the initial text label to the right-side dashboard
        self.right_output_layout.addWidget(initial_text_label)

    def show_status_plot(self):
        # Clear any existing widgets in the right_output layout
        self.remove_plot()

        # Create an instance of the LivePlotApp class
        live_plot = LivePlotApp(self.right_output)

        # Create a canvas for the live plot
        canvas = FigureCanvasQTAgg(live_plot.fig)
        # canvas.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        canvas.show()

        # Update the current content to the LiavePlotApp instance
        self.current_content = live_plot

    def clear_current_content(self):
        if self.current_content:
            self.current_content.stop()
            self.current_content = None

    def show_right_option(self, index):
        self.clear_current_content()
        for i in reversed(range(self.right_output_layout.count())):
            widget = self.right_output_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.dynamic_label = QLabel("System Status")
        self.dynamic_label.setStyleSheet(
            "color: white;"
            "font-size: 50px;"
            "font-weight: bold;"
            "padding: 20px 10px;"
        )
        self.right_output_layout.addWidget(self.dynamic_label)

        self.terminal_output = QTextEdit(self.right_output)
        # Set the QTextEdit to read-only (disable editing)
        self.terminal_output.setReadOnly(True)

        self.terminal_output.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "font-size: 16px;"
            "border: 2px solid #3465a4;"
            "border-radius: 10px;"
        )
        self.terminal_output.setAlignment(QtCore.Qt.AlignLeft)
        self.right_output_layout.addWidget(self.terminal_output)

        if index == 1:  # scan TOOLS

            # Create QPixmap objects for the images
            MD5_image = QPixmap("icon/.png")
            YARA_image = QPixmap("icon/.png")
            SHA_image = QPixmap("icon/.webp")

            # Create buttons and set images as icons
            button1 = QtWidgets.QPushButton("MD5 SCAN")
            button1.setIcon(QIcon(MD5_image))  # Set the Quick Scan image
            # Adjust the size as needed
            button1.setIconSize(QtCore.QSize(80, 80))

            button2 = QtWidgets.QPushButton("YARA SCAN")
            # Set the Malicious Scan image
            button2.setIcon(QIcon(YARA_image))
            # Adjust the size as needed
            button2.setIconSize(QtCore.QSize(80, 80))

            button3 = QtWidgets.QPushButton("SHA SCAN")
            button3.setIcon(QIcon(SHA_image))  # Set the Full Scan image
            # Adjust the size as needed
            button3.setIconSize(QtCore.QSize(80, 80))
            button3.clicked.connect(self.sha_scan_action)

            button1.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 30px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )

            self.right_output_layout.addWidget(button1)

            button2.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 30px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            self.right_output_layout.addWidget(button2)

            button3.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 30px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )

            self.right_output_layout.addWidget(button3)

        elif index == 2:  # MORE TOOLS

            # Create QPixmap objects for the images
            PASSSWORD_image = QPixmap("icon/.png")
            junkremover_image = QPixmap("icon/.png")
            realtime_image = QPixmap("icon/.webp")

            # Create buttons and set images as icons
            button1 = QtWidgets.QPushButton("Password_Manager")
            button1.setIcon(QIcon(PASSSWORD_image))  # Set the Quick Scan image
            # Adjust the size as needed
            button1.setIconSize(QtCore.QSize(80, 80))

            button2 = QtWidgets.QPushButton("Junk Remover")
            # Set the Malicious Scan image
            button2.setIcon(QIcon(junkremover_image))
            # Adjust the size as needed
            button2.setIconSize(QtCore.QSize(80, 80))
            button2.clicked.connect(self.JUNK_REMOVE_action)

            button3 = QtWidgets.QPushButton("Real Time Protection")
            button3.setIcon(QIcon(realtime_image))  # Set the Full Scan image
            # Adjust the size as needed
            button3.setIconSize(QtCore.QSize(80, 80))

            button1.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 30px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            # Connect the "Password Manager" button click event to show_password_manager_window
            button1.clicked.connect(self.show_password_manager_window)

        # Add the "Password Manager" button to the layout

            self.right_output_layout.addWidget(button1)

            button2.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 30px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            self.right_output_layout.addWidget(button2)

            button3.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 30px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            self.right_output_layout.addWidget(button3)

        elif index == 3:  # Firewall

            button1 = QtWidgets.QPushButton("    ON")
            button2 = QtWidgets.QPushButton("    OFF")

            def gh():
                pass

            def rk():
                pass

            button1.clicked.connect(gh)
            button2.clicked.connect(rk)

            button1.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 100px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            self.right_output_layout.addWidget(button1)

            button2.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 10px;"
                "   font-size: 36px;"
                "   padding: 20px 100px ;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            self.right_output_layout.addWidget(button2)

        elif index == 4:  # Network Security
            port_scan_image = QPixmap("icon/port.png")
            self.port_scan_button = QtWidgets.QPushButton("Port Scanning")
            self.port_scan_button.setIcon(QIcon(port_scan_image))
            self.port_scan_button.setIconSize(QtCore.QSize(80, 80))
            self.port_scan_button.clicked.connect(self.perform_port_scanning)

            self.port_scan_button.setStyleSheet(
                "QPushButton {"
                "   background-color: #3465a4;"
                "   color: white;"
                "   border: none;"
                "   border-radius: 5px;"
                "   font-size: 30px;"
                "   padding: 20px 80px;"
                "}"
                "QPushButton:hover {"
                "   background-color: #204a87;"
                "}"
            )
            self.right_output_layout.addWidget(self.port_scan_button)

        # Connect the clicked signals of other buttons to close the PasswordManager window
        for i in range(4):  # Change the range as needed for your buttons
            if i != index:  # Skip the current button
                button = self.dashboard_buttons[i]
                button.clicked.connect(self.close_password_manager_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def update_dynamic_label(self, text):
        self.dynamic_label.setText(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # Set dynamic label text
    ui.update_dynamic_label("You are secure now")

    # Show the "Network Security" options
    ui.show_right_option(4)

    # Connect the button click to the port scanning function
    if ui.port_scan_button is not None:
        ui.port_scan_button.clicked.connect(ui.perform_port_scanning)

    sys.exit(app.exec_())

import json
import os
import re
import sys

import maya.OpenMayaUI as omui
import openai
import requests
from PySide2.QtCore import Qt, QThread, QMutex, QMutexLocker, Signal, QTimer
from PySide2.QtGui import QTransform, QPixmap
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QSplitter, QHBoxLayout, QComboBox
from maya import cmds
from shiboken2 import wrapInstance

from . import pythonedtor


def find_mayagpt_key():
    home_dir = os.path.expanduser("~")
    key_file_path = os.path.join(home_dir, "mayagpt.key")
    if os.path.exists(key_file_path):
        with open(key_file_path, "r") as f:
            return f.read()
    else:
        return None


# Get the environment information
def get_environment_info():
    maya_version = cmds.about(version=True)
    python_version = sys.version.split()[0]

    environment_info = f"Autodesk Maya {maya_version} using Python {python_version}."
    return environment_info


def maya_main_window():
    """
    # Get the main Maya window

    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class RotatingIcon(QLabel):
    """
    A QLabel subclass that displays a rotating icon. It handles the rotation and pausing of the icon.

    """

    def __init__(self, icon_path=":waitBusy.png", parent=None):
        super(RotatingIcon, self).__init__(parent)
        self.icon_path = icon_path
        self.rotation_angle = 0
        self.setPixmap(QPixmap(self.icon_path))

        self.rotate_timer = QTimer(self)
        self.rotate_timer.timeout.connect(self.rotate_icon)
        self.rotate_timer.setInterval(50)  # Rotate every 0.05 seconds

        self.pause_timer = QTimer(self)
        self.pause_timer.timeout.connect(self.start_rotation)
        self.pause_timer.setSingleShot(True)

    def start_rotation(self):
        self.rotate_timer.start()

    def stop_rotation(self):
        self.rotate_timer.stop()
        self.pause_timer.start(1000)  # Pause for 1 second

    def rotate_icon(self):
        self.rotation_angle = (self.rotation_angle + 10) % 360
        pixmap = QPixmap(self.icon_path)
        transform = QTransform().rotate(self.rotation_angle)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.setPixmap(rotated_pixmap)

        if self.rotation_angle % 180 == 0:
            self.stop_rotation()


class CodeBlock(QWidget):
    """
     A QWidget subclass that contains a code editor with syntax highlighting and an
        "Execute" button. It allows users to execute the code displayed in the editor.
    """

    def __init__(self, parent=None):
        super(CodeBlock, self).__init__(parent=parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.code_edit = pythonedtor.CodeEditor()

        highlight = pythonedtor.PythonHighlighter(self.code_edit.document())

        # self.code_edit.setReadOnly(True)
        self.execute_button = QPushButton("Run")
        self.execute_button.clicked.connect(self.execute_script)
        layout.addWidget(self.code_edit)
        layout.addWidget(self.execute_button)

    def setPlainText(self, content):
        self.code_edit.setPlainText(content)

    def execute_script(self):
        try:
            exec(self.code_edit.toPlainText(), globals())
        except Exception as e:
            print(f"{str(e.__traceback__)}Error executing script:\n{str(e)}")


class CodeSnippetWidget(QWidget):
    """
    A QWidget subclass that displays both text and code snippets in a single widget.
    It can parse input text and create appropriate widgets for displaying text and code blocks.
    """
    update_ui = Signal(str)  # Add this line

    def __init__(self, parent=None):
        super(CodeSnippetWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Connect the update_ui signal to the init_ui slot
        self.update_ui.connect(self.init_ui)  # Add this line

    def init_ui(self, text):
        layout = self.layout()
        self.clear_layout()
        for snippet_type, content in self.split_text_and_code(text):
            if snippet_type == "text":
                label = QLabel(content)
                label.setWordWrap(True)
                layout.addWidget(label)
            elif snippet_type == "code":
                # code_edit = QPlainTextEdit(content)
                code_edit = CodeBlock(self)
                code_edit.setPlainText(content)
                layout.addWidget(code_edit)

        self.setLayout(layout)

    def clear_layout(self):
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            widget = child.widget()
            if widget:
                widget.deleteLater()

    @staticmethod
    def split_text_and_code(text):
        pattern = r"(?s)(.*?)```python(.*?)```"
        matches = re.findall(pattern, text)
        result = []
        if not matches:
            result.append(("text", 'Script:'))
            result.append(("code", text))
            return result

        for normal_text, code_text in matches:
            result.append(("text", normal_text.strip()))
            result.append(("code", code_text.strip()))

        return result


class ExecuteScriptThread(QThread):
    """A QThread subclass that runs a script execution function in a separate thread.
    It emits a signal when the script execution is complete and handles stopping the thread when requested."""
    script_executed = Signal(str)  # Add this line

    def __init__(self, parent, execute_script_func):
        super(ExecuteScriptThread, self).__init__(parent)
        self.execute_script_func = execute_script_func
        self.mutex = QMutex()
        self.stop_requested = False

    def run(self):
        script = self.execute_script_func(self)
        self.script_executed.emit(script)  # Add this line

    def request_stop(self):
        with QMutexLocker(self.mutex):
            self.stop_requested = True

    def is_stop_requested(self):
        with QMutexLocker(self.mutex):
            return self.stop_requested


class ChatGPTMayaUI(QWidget):
    """
    The main QWidget subclass for the ChatGPT integration in Maya.
    It contains input and output widgets, as well as buttons to start and stop the script execution thread.
    It also displays a rotating icon while the script is being executed.
    """

    def __init__(self, parent=maya_main_window()):
        super(ChatGPTMayaUI, self).__init__(parent)
        self.setObjectName('femtomayachatgpt')
        self.setWindowTitle("MayaGPT")
        self.API_KEY = None
        self.setWindowFlags(Qt.Window)
        self.init_ui()
        self.thread = None
        self.setFindAndSetKey()

    def init_ui(self):
        top_layout = QVBoxLayout(self)

        self.main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        input_label = QLabel("Input:")
        self.input_edit = QTextEdit()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_edit)

        button_layout = QHBoxLayout()
        self.execute_button = QPushButton("Ask")
        self.stop_button = QPushButton("Stop")
        self.execute_button.clicked.connect(self.start_thread)
        self.stop_button.clicked.connect(self.stop_thread)
        button_layout.addWidget(self.execute_button)
        button_layout.addWidget(self.stop_button)
        input_layout.addLayout(button_layout)

        output_layout = QVBoxLayout()
        output_layout.setAlignment(Qt.AlignTop)
        self.model_ = QComboBox(self)
        self.model_.addItem('gpt-3.5-turbo')
        self.model_.addItem('text-davinci-003')
        self.output_label = QLabel("Output:")
        self.output_edit = CodeSnippetWidget(self)
        output_layout.addWidget(self.model_, alignment=Qt.AlignTop)
        output_layout.addWidget(self.output_label, alignment=Qt.AlignTop)
        output_layout.addWidget(self.output_edit, alignment=Qt.AlignTop)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        output_widget = QWidget()
        output_widget.setLayout(output_layout)

        splitter = QSplitter()
        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        self.main_layout.addWidget(splitter)

        # Add this code block to create a QLabel with a rotating icon
        self.rotating_icon = RotatingIcon()
        self.rotating_icon.hide()
        output_layout.addWidget(self.rotating_icon)

        self.key_layout = QHBoxLayout(self)
        key_label = QLabel('Enter you API key')
        self.key_lineEdit = QLineEdit()
        key_button = QPushButton('Save')
        key_button.clicked.connect(self.saveKey)
        self.key_layout.addWidget(key_label)
        self.key_layout.addWidget(self.key_lineEdit)
        self.key_layout.addWidget(key_button)

        top_layout.addLayout(self.key_layout)
        top_layout.addLayout(self.main_layout)
        self.toggle_layout(self.main_layout)
        self.setLayout(top_layout)

    @staticmethod
    def toggle_layout(layout, hide=True):
        for i in range(layout.count()):
            if hide:
                layout.itemAt(i).widget().hide()
            else:
                layout.itemAt(i).widget().show()

    def saveKey(self):
        self.API_KEY = self.key_lineEdit.text()
        home_dir = os.path.expanduser("~")
        key_file_path = os.path.join(home_dir, "mayagpt.key")
        with open(key_file_path, "w") as f:
            f.write(self.API_KEY)
        self.setFindAndSetKey()

    def setFindAndSetKey(self):
        self.API_KEY = find_mayagpt_key()
        if self.API_KEY is not None:
            openai.api_key = self.API_KEY
            self.toggle_layout(self.key_layout)
            self.toggle_layout(self.main_layout, False)
        else:
            self.toggle_layout(self.key_layout, False)
            self.toggle_layout(self.main_layout)

    def execute_script(self, thread):
        user_input = self.input_edit.toPlainText()
        response = self.get_chatgpt_response_debug(user_input)

        script = response['choices'][0]

        if 'message' in script:
            script = script['message']['content'].strip()
        elif 'text' in script:
            script = script['text']

        if thread.is_stop_requested():
            return ""
        return script

    def start_thread(self):
        self.rotating_icon.show()
        self.rotating_icon.start_rotation()
        self.thread = ExecuteScriptThread(self, self.execute_script)
        self.thread.finished.connect(self.stop_thread)
        self.thread.script_executed.connect(self.output_edit.update_ui)  # Add this line
        self.thread.start()

    def stop_thread(self):
        if self.thread and self.thread.isRunning():
            self.thread.request_stop()
            self.thread.wait()
        self.rotating_icon.hide()
        self.rotating_icon.stop_rotation()

    def get_chatgpt_response_debug(self, prompt):
        if self.model_.currentText() == "text-davinci-003":
            return self.get_chatgpt_davinci(prompt)

        return self.get_chatgpt_turbo(prompt)

    def get_chatgpt_davinci(self, prompt):
        model_engine = "text-davinci-003"
        prompt = f"Generate a Python script to be executed in {get_environment_info()}, you can utilize maya api2 and cmds and numpy:\n{prompt}\n\n---\n\n"

        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2048,  # Increase max_tokens to avoid truncation
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response

    def get_chatgpt_turbo(self, prompt):
        model = "gpt-3.5-turbo"  # Change model to gpt-3.5-turbo
        url = "https://api.openai.com/v1/chat/completions"

        messages = [
            {"role": "system",
             "content": f"Generate a Python script to be executed in {get_environment_info()}, you can utilize maya api2 and cmds and numpy"},
            {"role": "user", "content": prompt},
        ]

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.API_KEY}",
            },
            data=json.dumps({
                "model": model,
                "messages": messages,
                "max_tokens": 4000,
                "n": 1,
                "stop": None,
                "temperature": 0.5,
            })
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error in API request: {response.status_code}, {response.text}")

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.request_stop()
            self.thread.wait()
        super().closeEvent(event)


def run():
    mayaUI = maya_main_window()
    femto_ui = mayaUI.findChild(QWidget, 'femtomayachatgpt')

    try:
        femto_ui.close()  # pylint: disable=E0601
        femto_ui.deleteLater()
    except:
        pass

    femto_ui = ChatGPTMayaUI()
    femto_ui.show()
    return femto_ui


if __name__ == "__main__":
    ui = run()

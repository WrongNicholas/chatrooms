from typing import Callable, Optional
import sys
import asyncio
from asyncio import AbstractEventLoop
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QStackedWidget)
from PyQt6.QtCore import QThread, pyqtSignal

from chatrooms.client import ChatClient

class ClientThread(QThread):
    """Runs the chat client in a separate thread to avoid blocking the GUI"""
    message_received = pyqtSignal(str)

    def __init__(self, username: str, room_id: str) -> None:
        super().__init__()
        self.username: str = username
        self.room_id: str = room_id
        self.client: ChatClient = ChatClient()
        self.loop: Optional[AbstractEventLoop] = None
    
    def run(self) -> None:
        """Starts the asyncio loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_client_async())
        self.loop.close()
    
    async def start_client_async(self) -> None:
        """Connects and listens to the server VIA ChatClient"""
        try:
            await self.client.connect(self.room_id, self.username)
            await self.client.listen(self.message_received.emit)
        except Exception as e:
            self.message_received.emit(f"System: Error - {str(e)}")
        
    def send_message(self, message: str) -> None:
        """Sends a message to the server VIA ChatClient"""
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.client.send_message(message), self.loop)

    def stop(self) -> None:
        """Safely closes the connection"""
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.client.close(), self.loop)
            self.quit()
            self.wait()


class ChatRoomsGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatrooms GUI Beta")
        self.resize(400, 500)

        self.user: str = ""
        self.room_id: str = ""
        self.client_thread: Optional[ClientThread] = None

        self.stacked_widget: QStackedWidget= QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.init_username_page()
        self.init_room_selection_page()
        self.init_chat_page()

        self.stacked_widget.addWidget(self.room_selection_widget)
        self.stacked_widget.addWidget(self.username_widget)
        self.stacked_widget.addWidget(self.chat_widget)
    
    def init_room_selection_page(self):
        """Sets up the page where you enter what room to join"""
        self.room_selection_widget: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout()

        self.room_label: QLabel = QLabel("Enter room to join:")
        self.room_input: QLineEdit = QLineEdit()
        self.join_room_button: QPushButton = QPushButton("Join Room")

        layout.addStretch()
        layout.addWidget(self.room_label)
        layout.addWidget(self.room_input)
        layout.addWidget(self.join_room_button)
        layout.addStretch()
        self.room_selection_widget.setLayout(layout)

        self.room_input.returnPressed.connect(self.on_submit_room)
        self.join_room_button.clicked.connect(self.on_submit_room)

    def init_username_page(self):
        """Sets up the page where you enter your username"""
        self.username_widget: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout()

        self.username_label: QLabel = QLabel("Enter username:")
        self.username_input: QLineEdit = QLineEdit()
        self.submit_username_button: QPushButton = QPushButton("Submit")

        layout.addStretch()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.submit_username_button)
        layout.addStretch()
        self.username_widget.setLayout(layout)

        self.username_input.returnPressed.connect(self.on_submit_username)
        self.submit_username_button.clicked.connect(self.on_submit_username)

    
    def init_chat_page(self):
        """Sets up the main chat page"""
        self.chat_widget: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout()

        self.room_info_label: QLabel = QLabel()

        self.chat_display: QTextEdit = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.message_input: QLineEdit = QLineEdit()
        self.send_message_button: QPushButton = QPushButton("Send")

        input_layout: QHBoxLayout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_message_button)

        layout.addWidget(self.room_info_label)
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)

        self.chat_widget.setLayout(layout)

        self.message_input.returnPressed.connect(self.on_send_message)
        self.send_message_button.clicked.connect(self.on_send_message)
    

    """event handler functions"""
    def on_submit_room(self):
        room_id = self.room_input.text().strip()
        if room_id:
            self.room_id = room_id
            self.stacked_widget.setCurrentWidget(self.username_widget)
            self.username_input.setFocus()

    def on_submit_username(self):
        username = self.username_input.text().strip()
        if username:
            self.user = username
            self.room_info_label.setText(f"Room: {self.room_id} | User: {self.user}")
            self.stacked_widget.setCurrentWidget(self.chat_widget)
            self.message_input.setFocus() 

            self.start_client_thread()

    def start_client_thread(self):
        self.client_thread = ClientThread(self.user, self.room_id)
        self.client_thread.message_received.connect(self.display_message)
        self.client_thread.start()

    def on_send_message(self):
        message: str = self.message_input.text()
        if message:
            self.message_input.clear()
            if self.client_thread:
                self.client_thread.send_message(message)
                self.display_message(message)

    def display_message(self, message: str):
        self.chat_display.append(message)
    


    



if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: ChatRoomsGUI = ChatRoomsGUI()
    window.show()
    sys.exit(app.exec())
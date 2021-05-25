
from loft.util.file import open_
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from loft.util.net import get_ip_thru_gateway as get_ip


def create_main_window(title: str, gui) -> QWidget:
    '''
    Create the main application window layout.
    '''
    window = QWidget()
    window.setWindowTitle(title)
    window.setGeometry(0, 0, 400, 300)
    window.move(400, 400)
    # Keep the window on top so that user remembers to close when they're done
    window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
    layout = QGridLayout(window)

    start_button = QPushButton(text='Start Connection')
    start_button.setCheckable(True)
    start_button.toggled.connect(gui.server.run)
    start_button.toggled.connect(lambda: start_button.setDisabled(True))
    # start_button.toggled.connect(lambda: select_to_send.setDisabled(True))

    connect_msg = QLabel(text='''
Note: Send file cannot be modified after starting.<br />
Please Close Loft and restart to make changes.
<ol>
    <li>Select Send Files if sending.</li>
    <li>Start Connection.</li>
    <li>On your other device, open <font color="#0000ee">http://{}:{}</font>.</li>
    <li>Close Loft after transfering.</li>
</ol>
'''.format(get_ip(), gui.server.config.PORT))

    done_button = QPushButton(text='Done Transferring')
    done_button.clicked.connect(window.close)

    open_received = QPushButton(text='Open Downloads')
    open_received.clicked.connect(gui.server.open_downloads)

    display_selected_file = QLabel("Sending File: ")
    def select_to_send_func():
        file_name = gui.send_file_dialog(window)
        display_selected_file.clear()
        display_selected_file.setText("Sending File: \n" + file_name)

    select_to_send = QPushButton(text='Send File…')
    select_to_send.clicked.connect(select_to_send_func)

    def clear_file_func():
        gui.clear_api_call(window)
        display_selected_file.clear()
        display_selected_file.setText("Sending File: ")

    clear_file = QPushButton(text='Clear Selected Files')
    clear_file.clicked.connect(clear_file_func)

    full_instr = QLabel(
        '<a href=https://github.com/ucsb-cs148-s21/t7-local-network-file-transfer/blob/main/usage.md>Full Instructions</a>')
    full_instr.setTextInteractionFlags(
        QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
    full_instr.setOpenExternalLinks(True)


    layout.addWidget(connect_msg, 0, 0, 1, 2)
    layout.addWidget(start_button, 1, 0, 1, 2)
    layout.addWidget(select_to_send, 2, 0, 1, 1)
    layout.addWidget(open_received, 2, 1, 1, 1)
    layout.addWidget(display_selected_file, 3, 0, 1, 1)
    layout.addWidget(clear_file, 4, 0, 1, 2)
    layout.addWidget(done_button, 5, 0, 1, 2)
    layout.addWidget(full_instr)

    window.setTabOrder(start_button, select_to_send)
    window.setTabOrder(select_to_send, open_received)
    window.setTabOrder(open_received, done_button)
    window.setTabOrder(done_button, full_instr)

    return window

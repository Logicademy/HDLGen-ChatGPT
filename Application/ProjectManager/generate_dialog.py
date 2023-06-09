import sys
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox

class GenerationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Generation")
        layout = QVBoxLayout()
        self.cancelled = True
        self.file_checkboxes = []

        # Add "Select All" checkbox
        select_all_checkbox = QCheckBox("Select All")
        select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        layout.addWidget(select_all_checkbox)

        # Add checkboxes for each file
        #for i in range(10):
        checkbox = QCheckBox(f"HDL Model ")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"HDL Model Reference")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"HDL Testbench ")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"HDL Testbench Reference")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)

        checkbox = QCheckBox(f"ChatGPT Title Section Message")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"ChatGPT Title Section Message Reference")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"ChatGPT Model Message")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"ChatGPT Model Message Reference")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"ChatGPT Testbench Message")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"ChatGPT Testbench Message Reference")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)
        checkbox = QCheckBox(f"Waveform File")
        layout.addWidget(checkbox)
        self.file_checkboxes.append(checkbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.get_selected_files)
        button_box.rejected.connect(self.cancel_selected)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def cancel_selected(self):
        self.cancelled = True
        self.close()
    def toggle_select_all(self, state):
        for checkbox in self.file_checkboxes:
            checkbox.setChecked(state == 2)

    def get_selected_files(self):
        selected_files = []
        i=0
        for checkbox in self.file_checkboxes:
            if checkbox.isChecked():
                selected_files.append(str(i))#checkbox.text())
            i=i+1
        self.cancelled = False
        self.close()
        return selected_files


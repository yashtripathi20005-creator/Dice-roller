# ============================================
# File: dice_roller_gui.py
# ============================================
# Main GUI class for the Dice Roller application
# ============================================

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpinBox, QComboBox, QGroupBox,
    QTextEdit, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor
from dice_animation import DiceAnimationWidget
from dice_logic import DiceLogic
import random

class DiceRollerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dice_logic = DiceLogic()
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_rolling_display)
        self.roll_count = 0
        self.max_rolls = 20
        self.current_result = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('🎲 Dice Roller with Animation')
        self.setGeometry(100, 100, 700, 600)
        self.setMinimumSize(600, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel('🎲 Dice Roller')
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont('Arial', 24, QFont.Bold)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Animation display
        self.dice_display = DiceAnimationWidget()
        self.dice_display.setMinimumHeight(250)
        main_layout.addWidget(self.dice_display)
        
        # Controls area
        controls_group = QGroupBox("Roll Controls")
        controls_layout = QGridLayout()
        controls_group.setLayout(controls_layout)
        main_layout.addWidget(controls_group)
        
        # Dice type selector
        controls_layout.addWidget(QLabel('Dice Type:'), 0, 0)
        self.dice_type_combo = QComboBox()
        self.dice_type_combo.addItems(['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100'])
        self.dice_type_combo.setCurrentText('d20')
        controls_layout.addWidget(self.dice_type_combo, 0, 1)
        
        # Number of dice
        controls_layout.addWidget(QLabel('Number of Dice:'), 0, 2)
        self.num_dice_spin = QSpinBox()
        self.num_dice_spin.setRange(1, 10)
        self.num_dice_spin.setValue(1)
        controls_layout.addWidget(self.num_dice_spin, 0, 3)
        
        # Roll button
        self.roll_button = QPushButton('🎲 Roll Dice!')
        self.roll_button.setFont(QFont('Arial', 14, QFont.Bold))
        self.roll_button.clicked.connect(self.roll_dice)
        self.roll_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        controls_layout.addWidget(self.roll_button, 1, 0, 1, 4)
        
        # Result display
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout()
        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)
        
        self.result_label = QLabel('Roll the dice to see the result!')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 16))
        self.result_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        result_layout.addWidget(self.result_label)
        
        # Detailed results
        self.detail_label = QLabel('')
        self.detail_label.setAlignment(Qt.AlignCenter)
        self.detail_label.setFont(QFont('Arial', 12))
        self.detail_label.setWordWrap(True)
        result_layout.addWidget(self.detail_label)
        
        # History
        history_group = QGroupBox("History")
        history_layout = QVBoxLayout()
        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)
        
        self.history_text = QTextEdit()
        self.history_text.setMaximumHeight(120)
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont('Courier', 10))
        history_layout.addWidget(self.history_text)
        
        # Clear history button
        clear_button = QPushButton('Clear History')
        clear_button.clicked.connect(self.clear_history)
        history_layout.addWidget(clear_button)
        
        # Status bar
        self.statusBar().showMessage('Ready to roll!')
        
    def roll_dice(self):
        """Start the dice rolling animation"""
        if self.roll_button.isEnabled():
            self.roll_button.setEnabled(False)
            self.statusBar().showMessage('Rolling...')
            
            # Get dice parameters
            dice_type = self.dice_type_combo.currentText()
            num_dice = self.num_dice_spin.value()
            
            # Store the actual result for later
            self.current_result = self.dice_logic.roll_dice(dice_type, num_dice)
            
            # Start animation
            self.roll_count = 0
            self.dice_display.start_animation()
            self.animation_timer.start(50)  # Update every 50ms
    
    def update_rolling_display(self):
        """Update the dice display during animation"""
        dice_type = self.dice_type_combo.currentText()
        num_dice = self.num_dice_spin.value()
        
        # Show random intermediate results
        if self.roll_count < self.max_rolls:
            # Generate random dice values for animation
            temp_results = []
            for _ in range(num_dice):
                max_val = self.dice_logic.get_max_value(dice_type)
                temp_results.append(random.randint(1, max_val))
            
            total = sum(temp_results)
            self.dice_display.set_dice_value(dice_type, temp_results)
            self.result_label.setText(f'Rolling... {total}')
            self.roll_count += 1
        else:
            # Animation complete - show final result
            self.animation_timer.stop()
            self.dice_display.stop_animation()
            
            # Display final result
            total = sum(self.current_result)
            result_text = f'🎲 Result: {total}'
            if len(self.current_result) > 1:
                result_text += f'  (Individual rolls: {", ".join(map(str, self.current_result))})'
            
            self.result_label.setText(result_text)
            self.dice_display.set_dice_value(self.dice_type_combo.currentText(), self.current_result)
            
            # Add to history
            dice_type = self.dice_type_combo.currentText()
            num_dice = self.num_dice_spin.value()
            history_entry = f'{dice_type} x{num_dice}: {self.current_result} = {total}'
            self.history_text.append(history_entry)
            
            # Show detailed breakdown if multiple dice
            if len(self.current_result) > 1:
                self.detail_label.setText(f'Individual rolls: {", ".join(map(str, self.current_result))}')
            else:
                self.detail_label.setText('')
            
            self.statusBar().showMessage('Roll complete!')
            self.roll_button.setEnabled(True)
    
    def clear_history(self):
        """Clear the history text"""
        self.history_text.clear()
        self.statusBar().showMessage('History cleared')

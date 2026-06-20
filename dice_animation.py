# ============================================
# File: dice_animation.py
# ============================================
# Widget for displaying animated dice rolls
# ============================================

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QLinearGradient
import random
import math

class DiceAnimationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.dice_type = 'd6'
        self.values = [1]  # Default value
        self.rolling = False
        self.rotation_angle = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_rotation)
        
        # Set up background
        self.setMinimumSize(200, 200)
        
        # Animation properties
        self._scale = 1.0
        self.scale_animation = QPropertyAnimation(self, b'scale')
        self.scale_animation.setDuration(300)
        self.scale_animation.setEasingCurve(QEasingCurve.OutBounce)
        
    @pyqtProperty(float)
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()
    
    def start_animation(self):
        """Start the rolling animation"""
        self.rolling = True
        self.rotation_angle = 0
        self.animation_timer.start(30)
        
        # Bounce animation
        self.scale_animation.setStartValue(0.7)
        self.scale_animation.setEndValue(1.0)
        self.scale_animation.start()
    
    def stop_animation(self):
        """Stop the rolling animation"""
        self.rolling = False
        self.animation_timer.stop()
        self.rotation_angle = 0
        self.update()
    
    def update_rotation(self):
        """Update rotation angle for animation"""
        self.rotation_angle += 15
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.update()
    
    def set_dice_value(self, dice_type, values):
        """Set the dice values to display"""
        self.dice_type = dice_type
        self.values = values if isinstance(values, list) else [values]
        self.update()
    
    def paintEvent(self, event):
        """Draw the dice with animation effects"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate size and position
        width = self.width()
        height = self.height()
        size = min(width, height) * 0.8 * self._scale
        
        # Center the dice
        center_x = width // 2
        center_y = height // 2
        
        # Calculate how many dice to display
        num_dice = len(self.values)
        if num_dice == 1:
            # Single large die
            self.draw_single_die(painter, center_x, center_y, size, self.values[0])
        elif num_dice <= 4:
            # 2-4 dice in a grid
            cols = 2
            rows = (num_dice + 1) // 2
            dice_size = size / 2.2
            spacing = dice_size * 0.3
            
            for i, value in enumerate(self.values):
                row = i // cols
                col = i % cols
                x = center_x - (cols - 1) * (dice_size + spacing) / 2 + col * (dice_size + spacing)
                y = center_y - (rows - 1) * (dice_size + spacing) / 2 + row * (dice_size + spacing)
                self.draw_single_die(painter, x, y, dice_size, value)
        else:
            # 5+ dice - show smaller dice in a grid
            cols = 3
            rows = (num_dice + cols - 1) // cols
            dice_size = size / 3.5
            spacing = dice_size * 0.2
            
            for i, value in enumerate(self.values):
                if i >= cols * rows:
                    break
                row = i // cols
                col = i % cols
                x = center_x - (cols - 1) * (dice_size + spacing) / 2 + col * (dice_size + spacing)
                y = center_y - (rows - 1) * (dice_size + spacing) / 2 + row * (dice_size + spacing)
                self.draw_single_die(painter, x, y, dice_size, value)
    
    def draw_single_die(self, painter, x, y, size, value):
        """Draw a single die with the given value"""
        # Apply rotation for animation
        painter.save()
        painter.translate(x, y)
        
        if self.rolling:
            # Random rotation during animation
            rot = self.rotation_angle + random.randint(-5, 5)
            painter.rotate(rot)
        
        # Die background with gradient
        gradient = QLinearGradient(-size/2, -size/2, size/2, size/2)
        gradient.setColorAt(0, QColor(255, 255, 255))
        gradient.setColorAt(1, QColor(230, 230, 230))
        
        # Rounded rectangle for die
        radius = size * 0.1
        rect = (-size/2, -size/2, size, size)
        
        # Shadow
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 200, 200, 100))
        painter.drawRoundedRect(rect.x() + 3, rect.y() + 3, rect.width(), rect.height(), radius, radius)
        
        # Main die body
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(80, 80, 80), 2))
        painter.drawRoundedRect(rect.x(), rect.y(), rect.width(), rect.height(), radius, radius)
        
        # Draw pips (dots)
        if not self.rolling or random.random() > 0.3:  # Sometimes show random pips during animation
            self.draw_pips(painter, size, value)
        
        painter.restore()
    
    def draw_pips(self, painter, size, value):
        """Draw pips on the die based on the value"""
        if value is None or value == 0:
            return
        
        # Map value to pip positions (standard dice layout)
        pip_positions = {
            1: [(0, 0)],
            2: [(-0.35, -0.35), (0.35, 0.35)],
            3: [(-0.35, -0.35), (0, 0), (0.35, 0.35)],
            4: [(-0.35, -0.35), (0.35, -0.35), (-0.35, 0.35), (0.35, 0.35)],
            5: [(-0.35, -0.35), (0.35, -0.35), (0, 0), (-0.35, 0.35), (0.35, 0.35)],
            6: [(-0.35, -0.35), (0.35, -0.35), (-0.35, 0), (0.35, 0), (-0.35, 0.35), (0.35, 0.35)],
        }
        
        # Handle d4 (triangle) and d8 special cases
        if self.dice_type == 'd4' and value <= 4:
            # For d4, we show the number instead of pips
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.3), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(value))
            return
        elif self.dice_type == 'd8' and value <= 8:
            # For d8, show number
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.25), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(value))
            return
        elif self.dice_type == 'd10' and value <= 10:
            # For d10, show number (with 0 for 10)
            display_value = 10 if value == 0 else value
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.2), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(display_value))
            return
        elif self.dice_type == 'd12' and value <= 12:
            # For d12, show number
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.2), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(value))
            return
        elif self.dice_type == 'd20' and value <= 20:
            # For d20, show number
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.2), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(value))
            return
        elif self.dice_type == 'd100' and value <= 100:
            # For d100, show number
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.15), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(value))
            return
        
        # For standard dice with pips (d6)
        if value in pip_positions:
            pip_radius = size * 0.08
            painter.setBrush(QBrush(QColor(50, 50, 50)))
            painter.setPen(Qt.NoPen)
            
            for pos in pip_positions[value]:
                px = pos[0] * size * 0.35
                py = pos[1] * size * 0.35
                painter.drawEllipse(px - pip_radius, py - pip_radius, pip_radius * 2, pip_radius * 2)
        else:
            # Fallback - show number
            painter.setPen(QPen(QColor(50, 50, 50), 3))
            painter.setFont(QFont('Arial', int(size * 0.25), QFont.Bold))
            painter.drawText(-size/2, -size/2, size, size, Qt.AlignCenter, str(value))

# ============================================
# File: dice_roller.py
# ============================================
# Main entry point for the Dice Roller application
# ============================================

import sys
from PyQt5.QtWidgets import QApplication
from dice_roller_gui import DiceRollerGUI

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    window = DiceRollerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

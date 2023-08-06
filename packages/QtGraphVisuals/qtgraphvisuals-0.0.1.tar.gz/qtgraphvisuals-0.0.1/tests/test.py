
import sys
from PySide6.QtWidgets import QApplication
from QtGraphVisuals import QGraphViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    extra={ "secondaryDarkColor":"#232629", "font_size": '15px',}

    viewer = QGraphViewer()
    viewer.show()

    sys.exit(app.exec())

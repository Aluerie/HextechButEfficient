from common import setup_logging
from gui.app import HextechButEfficientApp

with setup_logging(debug=False):
    app = HextechButEfficientApp()
    app.mainloop()

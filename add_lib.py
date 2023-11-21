import sys
import os


baseFolder = os.path.dirname(__file__)
sys.path.append(os.path.join(os.getcwd(), baseFolder + "\\lib"))
sys._MEIPASS=os.path.join(sys._MEIPASS, baseFolder + "\\lib")
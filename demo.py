import os
from pathlib import Path
BASE_DIR = (__file__)
print(BASE_DIR)
print(Path(__file__).resolve().parent.parent)
print(__name__)
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")
print(TEMPLATE_DIR)
    
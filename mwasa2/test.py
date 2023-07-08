from pathlib import Path


import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Build paths inside the project like this: BASE_DIR / 'subdir'.

lista = os.listdir(BASE_DIR)

print(lista)

from pathlib import Path
from os import path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = path.join(PROJECT_ROOT, "images")
BERNIES_DIR = path.join(IMAGES_DIR, "bernies")

# files in IMAGES_DIR
BERNIE_JPEG = path.join(IMAGES_DIR, "bernie.jpeg")

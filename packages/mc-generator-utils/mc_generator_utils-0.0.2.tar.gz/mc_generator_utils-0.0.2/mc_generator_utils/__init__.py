from .img import stackImages, load
from .md import addGradleSetupInstructions

def assets(modname):
    return f"src/main/resources/assets/{modname}/"
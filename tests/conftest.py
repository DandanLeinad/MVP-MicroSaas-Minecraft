import pathlib
import sys

# Adiciona a pasta src ao path para import do módulo backup
root = pathlib.Path(__file__).parent.parent / "src"
sys.path.insert(0, str(root))

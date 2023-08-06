import sys
import os

# add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# now you can perform relative imports from the ontoloviz package
from ontoloviz import run_app

if __name__ == "__main__":
    run_app()

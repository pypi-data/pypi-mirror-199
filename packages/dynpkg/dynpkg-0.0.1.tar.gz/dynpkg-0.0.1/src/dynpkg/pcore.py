import importlib
import pip._internal as pip
import os, sys
import subprocess

def simport(package, version=None, package_as=None):
    
    try:
        importlib.import_module(package)
    except ImportError:
        
        if version == None:
            subprocess.call([sys.executable, "-m", "pip", "install", "--user", package])
        else:
            subprocess.call([sys.executable, "-m", "pip", "install", "--user", package+"=="+version])
    finally:
        if package_as == None:
            globals()[package] = importlib.import_module(package)
        else:
            globals()[package_as] = importlib.import_module(package) 
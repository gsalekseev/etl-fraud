import subprocess

def install_package(name):
    subprocess.call(['pip', 'install', name])
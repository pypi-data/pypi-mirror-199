import subprocess

def main():
    # run pip install command after package installation
    subprocess.run(['pip', 'install', '--upgrade', 'requests'])
    print('Upgrade completed successfully')

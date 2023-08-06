import subprocess
import platform
import shutil
import os
import json
import yaml
from urllib.request import urlopen
from .exceptions import *

BIN_PATH = os.path.join(os.getenv('HOME'),'Applications/telebit/bin/telebit')
IS_DOWNLAODED = os.path.exists(BIN_PATH)


class DownloadTelebit:

    def __init__(self) -> None:
        
        self.install_helper_script_url = 'https://get.telebit.io/'
        self.config_path = '.config/telebit/telebit.yml'        
        self.bash_path = shutil.which('bash')
    

    def install(self) -> None:
        if not IS_DOWNLAODED:
            if platform.system() in ('Linux','Darwin'): 
                script_content = urlopen(self.install_helper_script_url).read()
                subprocess.run(self.bash_path, input=script_content, shell=True)
            else:
                print('Windows implementation not done yet!!!')
    

    def uninstall(self) -> None:
        if platform.system() == 'Linux':
            cmd=b"""sudo systemctl --user disable telebit; systemctl --user stop telebit
            sudo rm -f ~/.config/systemd/user/telebit.service
            sudo rm -rf ~/telebit ~/Applications/telebit
            sudo rm -rf ~/.config/telebit ~/.local/share/telebit"""
            subprocess.run(self.bash_path, input=cmd,shell=True)
        elif platform.system() == 'Darwin':
            cmd=b"""sudo launchctl unload -w ~/Library/LaunchAgents/cloud.telebit.remote.plist
            sudo rm -f ~/Library/LaunchAgents/cloud.telebit.remote.plist
            sudo rm -rf ~/telebit ~/Applications/telebit
            sudo rm -rf ~/.config/telebit ~/.local/share/telebit"""
            subprocess.run(self.bash_path, input=cmd,shell=True)





class Telebit:

    def __init__(self) -> None:
        if not IS_DOWNLAODED:
            downloader = DownloadTelebit()
            downloader.install()


    def enable(self) -> bool:
        try:
            subprocess.run([BIN_PATH, 'enable'],stdout=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            return False
        else:
            return True
    

    def disable(self) -> bool:
        try:
            subprocess.run([BIN_PATH, 'disable'], stdout=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            return False
        else:
            return True

    
    def list(self) -> dict:
        out = subprocess.check_output([BIN_PATH, 'list']).decode()
        formated_out = '\n'.join(out.splitlines()[1:])
        json_format = yaml.safe_load(formated_out)
        return json_format      
    

    def restart(self) -> bool:
        try:
            subprocess.run([BIN_PATH, 'restart'], stdout=subprocess.DEVNULL, check=True)
        except subprocess.CalledProcessError:
            return False
        else:
            return True


    def status(self) -> dict:
        out = subprocess.check_output([BIN_PATH,'status']).decode()
        json_out = json.loads(''.join(out.split('\n')[1:]))
        return json_out
    

    def http(self,handler:str='none', subdomain:str='') -> tuple:
        if handler == 'none':
            out = subprocess.check_output([BIN_PATH, 'http', handler]).decode()
            return (out.splitlines()[-2].split(' ')[2], out.splitlines()[-2].split(' ')[4])
        elif os.path.isdir(handler) or os.path.isfile(handler):
            out = subprocess.check_output([BIN_PATH, 'http', handler, str(subdomain)]).decode()
            return (out.splitlines()[-2].split(' ')[2], out.splitlines()[-2].split(' ')[4])
        elif int(handler) > 0 and int(handler) < 65535:
            out = subprocess.check_output([BIN_PATH, 'http', handler, str(subdomain)]).decode()
            return (out.splitlines()[-2].split(' ')[2], out.splitlines()[-2].split(' ')[4])
        else:
            raise BadHandlerOrSubdoamin('Invalid handler or subdomain.')

    
    def tcp(self,handler:str='none',args='') -> tuple:
        if isinstance(handler, int) and int(handler) > 0 and int(handler) < 65535:
            if isinstance(args, int) and int(args) > 0 and int(args) < 65535:
                out = subprocess.check_output([BIN_PATH, 'tcp', str(handler), str(args)]).decode()
            elif args == '':
                out = subprocess.check_output([BIN_PATH, 'tcp', str(handler)]).decode()
            return (out.strip("\n").splitlines()[-1].split(' ')[2], out.strip("\n").splitlines()[-1].split(' ')[4])
        elif os.path.isdir(handler):
            out = subprocess.check_output([BIN_PATH, 'tcp', str(handler)]).decode()
            return (out.strip("\n").splitlines()[-1].split(' ')[2], out.strip("\n").splitlines()[-1].split(' ')[4])
        elif handler.lower() == 'none':
            if isinstance(args, int) and int(args) > 0 and int(args) < 65535:
                out = subprocess.check_output([BIN_PATH, 'tcp', str(handler), str(args)]).decode()
            else:
                out = subprocess.check_output([BIN_PATH, 'tcp', str(handler)]).decode()
            return (out.strip("\n").splitlines()[-1].split(' ')[2], out.strip("\n").splitlines()[-1].split(' ')[4])
        else:
            raise BadHandlerOrSubdoamin('Invalid Handler')

from email import utils
from os import path
import os
import platform
import re
import subprocess
import tarfile
from rich import print
import requests
from sa_csgo.utils.config import ConfigManager

steamCMDPath = ConfigManager.get('steamCMDPath')
csgoServerPath = ConfigManager.get('csgoServerPath')
tmpFolderPath = ConfigManager.get('tmpFolderPath')

#csgoServerInstallationProcessName = "csgoServerInstallation";
csgoServerOperationsProcessName = "csgoServerOperations";

def installAptPackage(packageName):
    try:
        subprocess.run(['sudo', 'apt-get','-yqq', 'install', '-o=Dpkg::Use-Pty=0', packageName], check=True)
    except:
        exit(f'Failed to Install {packageName}')

def verifySteamCMDInstallation():
    if path.exists(f'{steamCMDPath}/steamcmd.sh') and path.exists(f'{steamCMDPath}/linux32'):
        return steamCMDPath
    else:
        return False
    
def isUbuntuProConnected():
    result = subprocess.run(['sudo', 'ubuntu-advantage', 'status'], check=True, capture_output=True, text=True)
    return not ('Ubuntu Pro' in result.stdout)

def isRealTimeKernelEnabled():
    result = subprocess.run(['sudo', 'ubuntu-advantage', 'status'], check=True, capture_output=True, text=True)
    return not ('realtime-kernel  yes' in result.stdout)


def verifyCSGOServerInstallation():
    if path.exists(f'{csgoServerPath}/csgo/steam.inf'):
        with open(f'{csgoServerPath}/csgo/steam.inf') as f:
            content = f.read()
            version = re.search(r"PatchVersion=([\d.]+)",content).group(1)
        return (csgoServerPath, version)
    else:
        return False

def startCSGOServer(port = 27015, public = 'false', token = False):
    tokenCommand = ['+sv_steamaccount', token] if token else []
    processName = craftScreenProcess(csgoServerOperationsProcessName, [f'{csgoServerPath}/srcds_run', '-game', 'csgo', '-port', port, '+game_mode','1','+map','de_dust2','-tickrate 128'] + tokenCommand)
    return processName

def stopCSGOServer():
    subprocess.run(['screen', '-S', csgoServerOperationsProcessName, '-X', 'stuff' ,'exit' , 'echo -ne \'\\015\'' ], check=True)
    return False
    
def enableLiveKernel(proToken):
    subprocess.run(['sudo', 'pro', 'attach', proToken], check=True)
    subprocess.run(['pro', 'enable', 'realtime-kernel'], check=True)
    return

def installCSGOServer(version = 'public'):
    os.makedirs(os.path.dirname(csgoServerPath), exist_ok=True)
    return subprocess.run(['sudo', f'{steamCMDPath}/steamcmd.sh', '+force_install_dir', csgoServerPath, '+login', 'anonymous','+app_update', '740', '-beta', version, 'validate', '+quit'])

def craftScreenProcess(processName : str, commands :list):
    os.makedirs(os.path.dirname(tmpFolderPath), exist_ok=True)
    os.chdir(tmpFolderPath)
    subprocess.run(['screen', '-S', processName, '-d', '-m', "-L", "-Logfile", f'{processName}.log'] + commands, check=True)
    return processName

def openServerConsole():
    subprocess.run(['screen', '-r', 'csgoServerOperations'], check=True)

def installSteamCMD():
    system = platform.system()
    if (system == 'Windows'):
        pass
    elif (system == 'Linux'):
        distro = platform.freedesktop_os_release()['NAME']
        if (distro == 'Ubuntu' or distro == 'Debian'):

            print("[white bold]Installing prerequisites..")
            installAptPackage('lib32gcc-s1')
            print("[white bold]Downloading SteamCMD..")
            steamCMDPath = ConfigManager.get('steamCMDPath')
            tarFile = f'{steamCMDPath}/steamcmd_linux.tar.gz'
            os.makedirs(os.path.dirname(tarFile), exist_ok=True)
            response = requests.get("https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz", stream=True)
            if response.status_code == 200:
                with open(tarFile, 'wb') as f:
                    f.write(response.raw.read())
                    tar = tarfile.open(tarFile)
                    tar.extractall(steamCMDPath)
                    tar.close()
                    os.remove(tarFile)
            print(f'[SUCCESS] Installed latest version of SteamCMD in {steamCMDPath}')    
    pass
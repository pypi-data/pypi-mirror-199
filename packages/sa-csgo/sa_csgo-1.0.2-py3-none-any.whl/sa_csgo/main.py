import typer
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from sa_csgo.addons.gui import execProcedure, printGUIProcedures, printStatus
from sa_csgo.utils.config import ConfigManager
from sa_csgo.utils.format import printLogo
from sa_csgo.utils.os_commands import installCSGOServer, installSteamCMD, openServerConsole, startCSGOServer, stopCSGOServer

installApp = typer.Typer()
manageServerApp = typer.Typer()
app = typer.Typer()
app.add_typer(installApp,name='install',help='Installs applications (steamcmd, csgoserver).')
app.add_typer(manageServerApp,name='server',help='Manage Server (start, stop, open console).')

@app.command("gui",help= 'Opens GUI Menu.')
def gui():
    while True:
        console = Console()
        console.clear()
        printLogo()
        printStatus()
        printGUIProcedures()
        procedure = Prompt.ask("[white]Choose Procedure [yellow]<'quit' to exit>[/yellow]")
        if procedure == 'quit':
            break;
        try:
            procedure = int(procedure)
            execProcedure(procedure)
            typer.prompt('\n\nPress Enter to go back to menu',default='',show_default=False)
        except Exception as e:
            print(e)
            print('Invalid procedure, please retry.')

@installApp.command("steamcmd", help= 'Install latest steamcmd version.')
def steamcmd():
    installSteamCMD()
    return 

@installApp.command("csgoserver", help= 'Install cs:go server, multiple versions available.',)
def csgoserver(version = 'public'):
    installCSGOServer(version)
    return 

@manageServerApp.command("start", help= 'Starts server.',)
def startServer(port='27015', public=False, token=''):

    configToken = ConfigManager.get(token)
    if configToken:
        token = configToken
    else:
        ConfigManager.setProperty('token',token)

    configPort = ConfigManager.get(port)
    if configPort:
        port = configPort
    else:
        ConfigManager.setProperty('port',port)

    configPublic = ConfigManager.get(public)
    if configPublic:
        port = configPublic
    else:
        ConfigManager.setProperty('public',public)

    startCSGOServer(port,public,token)
    return 

@manageServerApp.command("stop", help= 'Stops server.',)
def stopServer():
    stopCSGOServer()
    return 

@manageServerApp.command("restart", help= 'Restarts server.',)
def restartServer():
    token = ConfigManager.get('token')
    port = ConfigManager.get('port')
    public = ConfigManager.get('public')
    stopServer()
    startCSGOServer(port, public, token)
    return 

@manageServerApp.command("console", help= 'Opens console. (CTRL + D + A to safely detach)',)
def openConsole():
    openServerConsole()
    return 
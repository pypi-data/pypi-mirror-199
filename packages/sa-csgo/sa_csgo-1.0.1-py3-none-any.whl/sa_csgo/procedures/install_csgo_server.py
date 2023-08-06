import datetime
import platform

import typer
from sa_csgo.addons.gui import Procedure
from sa_csgo.utils.os_commands import installCSGOServer, verifySteamCMDInstallation
from steam.client import SteamClient
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align

class CustomProcedure(Procedure):
    id = 2
    name = "Install [orange4]CS:GO[/orange4] Server"
    description= "Multiple versions are available"

    def run():
        system = platform.system()

        if not verifySteamCMDInstallation():
            print(
                'SteamCMD is not detected, it is required to install a CS:GO Server application.')
            proceed = typer.confirm(
                'Install steamCMD? (\'N\' will end the procedure) ')
            if (not proceed):
                return
        
        client = SteamClient()
        print('[white bold]Logging in steamCMD...')
        client.anonymous_login()
        print('[white bold]Fetching available CS:GO SRV versions.. ')
        product_info = client.get_product_info(apps=[740])
    
        typer.clear()
        print(Align('[white bold]Please select the cs:go server version to install: \n', align='center'))
        branches = product_info['apps'][740]['depots']['branches']
        for i, branch in enumerate(branches):
            timeUpdated = branches[branch]['timeupdated']
            branchTitle = branch = f'{branch}[bold red] PASSWORD REQUIRED [/bold red]' if 'pwdrequired' in branches[branch].keys() else f'[bold green]{branch}[/bold green]'
            print(Align(Panel(f'Release date: {datetime.datetime.fromtimestamp(int(timeUpdated))}',title= f'[{i+1}] {branchTitle}',expand=False),align='center'))
        choice = Prompt.ask(f'\n\n  Choose [[green]1-{len(branches.keys())}[/green]] <\'quit\' to exit>')
        
        if choice == 'quit':
            return
        try:
            choice = int(choice)
        except:
            print("Choiche is not valid.. Aborting...")

        version = str(list(branches)[int(choice) - 1])

        print(
            f'[white bold]Installing CS:GO Server version [/white bold]<[green bold]{version}[/green bold]>[white bold]..[/white bold] \n')
        try:
            installCSGOServer(version)
        except Exception as e:
            print(e)
            print(
                'Unable to install CS:GO Server. Please check that you are connected and have enough storage.')
            return
        return

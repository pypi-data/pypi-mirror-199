from abc import ABC, abstractmethod
import importlib
import inspect
import os
import platform
from typing import List
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich import box
from sa_csgo.utils.os_commands import verifyCSGOServerInstallation, verifySteamCMDInstallation
from rich import print
from rich.padding import Padding


class Procedure(ABC):
    
    id=0;

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def run():
        pass


procedures_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "procedures")

procedures: List[Procedure] = [];
procedure_files = [f for f in os.listdir(procedures_directory_path) if f.endswith('.py')]

for procedurePath in procedure_files:
    module_name = procedurePath[:-3]
    procedureClasses = [proc for proc in inspect.getmembers(importlib.import_module(f'sa_csgo.procedures.{module_name}'),inspect.isclass) if proc[0] == 'CustomProcedure']
    procedures.insert(0, procedureClasses[0][1])

procedures.sort(key=lambda x: x.id);

def printGUIProcedures(): 
    print(Padding("\n[bold green1]AVAILABLE PROCEDURES:[/bold green1]\n",(0,19)))
    for i, procedure in enumerate(procedures):
        print(Align(Panel(f'{procedure.description}',title= f'[b][[cyan]{i+1}[/cyan]] [[u]{procedure.name}[/u]][/b]', title_align='left' , box=box.HEAVY, width=60),align='center'));

def printStatus():

    steamCMDInstalled = verifySteamCMDInstallation()
    CSGOServerInstalled = verifyCSGOServerInstallation()
    table = Table(title=f"  [STATUS OVERVIEW]          [ OS: {platform.system()} | {platform.version() if platform.system() == 'Windows' else platform.freedesktop_os_release()['PRETTY_NAME']} ]", width=90, title_justify='center')
    table.add_column("Name", justify="Status", style="cyan", no_wrap=True)
    table.add_column("Status", justify="left", style="magenta")
    table.add_column("Info", justify="center", style="green")
    table.add_row("SteamCMD", "Installed" if steamCMDInstalled else "Not Installed", steamCMDInstalled if steamCMDInstalled else "")
    table.add_row("CS:GO Server", "Installed" if CSGOServerInstalled else "Not Installed", f'{CSGOServerInstalled[0]}\nVersion: {CSGOServerInstalled[1]}' if CSGOServerInstalled else "")
    table.add_row("SA-SM Plugin", "Not Installed", "[Coming Soon]")
    print(Align(table,align='center'))

def execProcedure(procedureId):
    filteredProcedure = list(filter(lambda procedure: procedure.id == procedureId, procedures))
    if len(filteredProcedure) > 0:
        filteredProcedure[0].run()
    else:
        print("Procedure not found.\n")
    return
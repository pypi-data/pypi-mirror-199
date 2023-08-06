import typer
from sa_csgo.addons.gui import Procedure
from sa_csgo.utils.os_commands import installSteamCMD, verifySteamCMDInstallation


class CustomProcedure(Procedure):
    id= 1
    name= "Install [blue_violet]SteamCMD[/blue_violet]"
    description= "Proceeds with the installation of the latest SteamCMD version."

    def run():

        if verifySteamCMDInstallation():
            proceed = typer.confirm('SteamCMD is already installed, are you sure that you want to proceed?')
            if(not proceed):
               return
        installSteamCMD()
        return
            
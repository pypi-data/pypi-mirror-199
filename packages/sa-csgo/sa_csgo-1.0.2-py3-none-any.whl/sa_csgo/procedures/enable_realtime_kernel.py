from sa_csgo.addons.gui import Procedure
import typer

from sa_csgo.utils.os_commands import enableLiveKernel, isRealTimeKernelEnabled, isUbuntuProConnected

class CustomProcedure(Procedure):
    id=5
    name= "Enable [red]R-T Kernel[/red]. (RESTART REQUIRED) "
    description= "([underline]Ubuntu Pro Subscription token required.[/underline])"

    def run():
        proceed = typer.confirm("This action will change your kernel operations, please note that this action in not revertable. Do you want to proceed?")
        if not proceed:
            print("Aborting...")

        if(isRealTimeKernelEnabled()):
            print("Real Time Kernel already enabled.")
            return
        
        if(not isUbuntuProConnected()):
            token = typer.prompt("Ubuntu PRO token")

        try:
            enableLiveKernel(token)
        except:
            print("Token not valid or Live Kernel not supported...")
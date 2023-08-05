import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.config.config import AuthConfig
from e2e_cli.core.alias_service import get_user_cred, option_check

class ConfigRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.config_commands is None:
            subprocess.call(['e2e_cli', 'config', '-h'])


        elif self.arguments.config_commands == 'add':
            if(self.arguments.alias=="file"):
                path=Py_version_manager.py_input("input the file path : ")
                auth_config_object = AuthConfig()
                auth_config_object.adding_config_file(path)
                return

            try:
                api_key = Py_version_manager.py_input("Enter your api key: ")
                auth_token = Py_version_manager.py_input("Enter your auth token: ")
                auth_config_object = AuthConfig(alias=option_check(self.arguments.alias),
                                                    api_key=api_key,
                                                    api_auth_token=auth_token)
                auth_config_object.add_to_config()
            except KeyboardInterrupt:
                Py_version_manager.py_print(" ")
                pass


        elif self.arguments.config_commands == 'delete':
            if(self.arguments.alias=="all"):
                Py_version_manager.py_print("sorry all is an reserve keyword for listing all registered alias/user")
                return
            
            confirmation =Py_version_manager.py_input("are you sure you want to delete press y for yes, else any other key : ")
            if(confirmation.lower()=='y'):
                auth_config_object = AuthConfig(alias=self.arguments.alias)
                try:
                    auth_config_object.delete_from_config()
                except:
                    Py_version_manager.py_print(" hi")
                    pass  


        elif self.arguments.config_commands == 'view':
            if(self.arguments.alias=="all"):
                for item in list(get_user_cred("all", 1)):
                    Py_version_manager.py_print(item)
            else:
                    Py_version_manager.py_print("Action not allowed")
            


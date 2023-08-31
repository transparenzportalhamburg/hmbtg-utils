class Command:
    _discription = ""


    def execute(self) -> bool:
        try:
            pass
        except Exception as e:
            pass

    def _execute_func(self) -> bool:
        pass
    
    def revert(self) -> bool:
        pass

    def _revert_func(self) -> bool:
        pass
    


# mkdir
class MakeDir(Command):

    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
    
    def _execute_func(self) -> bool:
        return super()._execute_func()


# chmod
class ChangeMod(Command):

    def __init__(self) -> None:
        super().__init__()


# mv
class Move(Command):

    def __init__(self) -> None:
        super().__init__()


# cp
class Copy(Command):

    def __init__(self) -> None:
        super().__init__()


# rm
class Remove(Command):

    def __init__(self) -> None:
        super().__init__()
# modify file

# apt
class Apt(Command):

    def __init__(self) -> None:
        super().__init__()



class InstallContext:
    """_summary_
    """
    def __init__(self) -> None:
        """_summary_
        """
        self._commands = []
        self._curent_state = 0
    
    
    def add(self, command) -> None:
        """_summary_

        Args:
            command (_type_): _description_
        """
        self._commands.append(command)
    
    def remove(self, command) -> None:
        self._commands.remove(command)
    

    def excecute(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        for command in self._commands:
            if not command.execute():
                return False
            self._curent_state +=1

    def revert(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        for command in reversed(self._commands):
            if not command.revert():
                return False

    def clean(self):
        """_summary_
        """
        for command in reversed(self._commands[:self._curent_state]):
            command.clean()
    
    def __len__(self):
        return len(self._commands)
    

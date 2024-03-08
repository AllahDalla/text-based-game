from colorama import just_fix_windows_console, Fore, Style

class TermColors:
    RED = Fore.RED
    BLUE = Fore.BLUE
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL

    def _print_red(self, text:str) -> None:
        print(f"{self.RED}{text}{self.RESET}")
    
    def _print_blue(self, text:str) -> None:
        print(f"{self.BLUE}{text}{self.RESET}")
    
    def _print_yellow(self, text:str) -> None:
        print(f"{self.YELLOW}{text}{self.RESET}")
    
    def _print_green(self, text:str) -> None:
        print(f"{self.GREEN}{text}{self.RESET}")
    
    
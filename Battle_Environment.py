from re import S
from Characters import *
from Items import BeginnerSword
from color import TermColors
from Attacks import Attack



class Battle_Env:
    location : str = ""
    player_list : list[Player] = []
    enemy_list : list[Enemy] = []
    turn_history : list[Attack] = []
    PLY = "PLAYER"
    EMY = "ENEMY"
    flee_bias : int = 10

    def __init__(self, player_list: list[Player], enemy_list: list[Enemy], location: str) -> None:
        self.location = location
        self.player_list = player_list
        self.enemy_list = enemy_list
        self.t = TermColors()

    def get_location(self) -> str:
        return self.location
    
    def set_location(self, new_location: str) -> None:
        self.location = new_location

    def get_flee_bias(self) -> int:
        return self.flee_bias

    def set_flee_bias(self, new_bias:int) -> None:
        self.flee_bias = new_bias

    def get_player_list(self) -> list[Player]:
        return self.player_list
    
    def set_player_list(self, new_list:list[Player]) -> None:
        self.player_list = new_list
    
    def get_enemy_list(self) -> list[Enemy]:
        return self.enemy_list

    def set_enemy_list(self, new_list:list[Enemy]) -> None:
        self.enemy_list = new_list
    
    def get_turn_history(self) -> list[Attack]:
        return self.turn_history
    
    def add_turn_history(self, atk:Attack) -> None:
        self.turn_history.append(atk)
    
    def display_defend_options(self, char:Player) -> int:
        t = TermColors()
        char.defend_action()
        t._print(f"[DEFEND] -> {char.get_name().upper()} CHOSE TO DEFEND")

    def display_see_stats_options(self, player: Player) -> None:
        system("cls")
        player.display_player_stats()
        self.t._print_green("[PRESS ENTER] ")
        input()
        system("cls")

    def flee_actions(self, char:Player) -> None:
        t = TermColors()
        bias = self.get_flee_bias()
        opts = ([True] * random.randint(1, 5)) + ([False] * bias)
        if random.choice(opts):
            t._print_yellow(f"[FLEE SUCCESSFUL] -> {char.get_name().upper()} SUCCESSFULLY FLED THE BATTLE FIELD")
            self.get_player_list().remove(char)
            return 
        t._print_green(f"[NO ESCAPE] -> {char.get_name().upper()} COULD NOT ESCAPE")

    def _battle_options(self, char: Character) -> int:
        if char.get_character_type() == self.PLY:
            self.t._print_green(f"[{char.get_name()} BATTLE OPTIONS]")
            self.t._print_green("1. ATTACK")
            self.t._print_green("2. DEFEND")
            self.t._print_green("3. SEE STATS")
            self.t._print_green("4. FLEE")
            self.t._print_green("[ENTER CHOICE] -> ")
            choice = int(input())
            return choice
        return 0

    def who_won(self) -> bool:
        ply_len = len(self.get_player_list())
        emy_len = len(self.get_enemy_list())
        if ply_len <= 0:
            system("cls")
            self.t._print_green("[BATTLE LOSS] -> YOUR PARTY WAS DEFEATED")
            return True
        elif emy_len <= 0:
            system("cls")
            self.t._print_green("[BATTLE WON] -> YOUR PARTY WAS VICTORIOUS IN BATTLE")
            return True
        return False

    def _turn(self, party_list:list[Character]) -> None:
        self.get_turn_history().clear()
        if len(party_list) > 0 and isinstance(party_list[0], Player): # check if incoming party_list is player_list
            for char in party_list: # go through each player
                choice = 3
                while choice == 3 or choice > 4 or choice < 1: # does loop if player wants to see stats -> does not lose turn AND if player chooses incorrect choice as input
                    choice = self._battle_options(char) # display battle options of player 
                    if choice == 1: # check battale options
                        system("cls")
                        # display screen to select attack and calc dmg
                        atk_dmg, atk_type, target_type, select_target = char.display_attack_options(self.get_enemy_list())
                        # create attack for player after calc dmg
                        atk = Attack(select_target=select_target-1, atk_type=atk_type, target_type=target_type, damage=atk_dmg, name=char.get_name())
                        self.add_turn_history(atk) # add attack to history
                        system("cls")
                        # end turn and go to next player
                        continue
                    elif choice == 2: # check if player wants to defend
                        system("cls")
                        # display/do defense
                        self.display_defend_options(char=char)

                    elif choice == 3: # check if player wants to see stats
                        system("cls")
                        # display stats
                        self.display_see_stats_options(player=char)
                    
                    elif choice == 4: # check if player want to flee
                        system("cls")
                        self.flee_actions(char=char) # do flee actions, see if player can flee the battle
                    
                    else: # check for incorrect choice from input
                        system("cls")
                        self.t._print_yellow("[INCORRECT CHOICE INPUT] -> CHOOSE BETWEEN 1 AND 4")
        elif len(party_list) > 0 and isinstance(party_list[0], Enemy):    
            for char in party_list:
                target = char.select_single_target(self.get_player_list())
                damage = char.calculate_damage()
                atk = Attack(atk_type="SINGLE", target_type="PLAYER", select_target=target, damage=damage, name=char.get_name())
                self.add_turn_history(atk=atk)
                system("cls")

        for atk in self.get_turn_history():
            atk.set_player_list(self.get_player_list())
            atk.set_enemy_list(self.get_enemy_list())
            new_player_list, new_enemy_list =  atk.phys_attack()
            self.set_player_list(new_player_list)
            self.set_enemy_list(new_enemy_list)
            

    def battle(self) -> None:
        self.t._print_green("[BATTLE ENCOUNTERED] -> FIGHT FOR YOUR LIFE!")
        while True:
            self._turn(self.get_player_list())
            self._turn(self.get_enemy_list())
            if self.who_won():
                break
        self.t._print_green("[BATTLE OVER]")

ply = Player("Test", 100, 100, 100, 100)
ply_2 = Player("Allah Dalla", 100, 100, 100, 100)
eny = Enemy("Enemy Test", 70, 70, 30, 30)
eny_2 = Enemy("Enemy Tester_2", 70, 70, 30, 30)

# env = Battle_Env([ply_2, ply], [eny, eny_2], "Somewhere")

# env.battle()

sword = BeginnerSword()

ply_2.set_inventory([sword])
ply_2.loadout()
                
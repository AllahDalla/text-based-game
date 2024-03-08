import random
from os import system
from time import sleep
from typing import Type

from Items import Item
from color import TermColors


class Character:
    name : str
    character_type : str
    max_health : int
    current_health : int
    max_mana : int
    current_mana : int
    max_bars_displayed : int = 20
    bar_type : str = "█"
    no_bar_type : str = "-"
    inventory : list[Item] = []

    def __init__(self, name:str, char_type:str, max_health:int, current_health:int, max_mana:int, current_mana:int) -> None:
        self.name = name
        self.character_type = char_type
        self.max_health = max_health
        self.current_health = current_health
        self.max_mana = max_mana
        self.current_mana = current_mana

    def get_name(self) -> str:
        return self.name.upper()
    
    def set_name(self, new_name:str) -> None:
        self.name = new_name
    
    def get_character_type(self) -> str:
        return self.character_type
    
    def set_character_type(self, char_type:str) -> None:
        self.character_type = char_type

    def get_max_health(self) -> int:
        return self.max_health
    
    def set_max_health(self, max_health:int) -> None:
        self.max_health = max_health

    def get_current_health(self) -> int:
        return self.current_health

    def set_current_health(self, current_health:int) -> None:
        self.current_health = current_health

    def current_health_adjust(self):
        if self.get_current_health() > self.get_max_health():
            self.set_current_health(self.get_max_health())
    
    def get_max_mana(self) -> int:
        return self.max_mana
    
    def set_max_mana(self, max_mana:int) -> None:
        self.max_mana = max_mana
    
    def get_current_mana(self) -> int:
        return self.current_mana
    
    def set_current_mana(self, current_mana:int) -> None:
        self.current_mana = current_mana
    
    def current_mana_adjust(self):
        if self.get_current_mana() > self.get_max_mana():
            self.set_current_mana(self.get_max_mana())

    def get_inventory(self) -> list[Item]:
        return self.inventory
    
    def set_inventory(self, inventory, add_to:bool=True) -> None:
        if add_to:
            if type(inventory) == list:
                self.inventory = self.inventory + inventory
            else:
                self.inventory.append(inventory)
        else:
            if type(inventory) != list:
                self.inventory = [inventory]
            else:
                self.inventory = inventory
    
    def remove_from_inventory(self, item) -> bool:
        try:
            self.inventory.remove(item)
            return True
        except ValueError:
            return False

    def get_inventory_len(self) -> int:
        return len(self.inventory)

    def display_health(self):
        remaining_health_bars = round(self.current_health/self.max_health * self.max_bars_displayed)
        lost_health_bars = self.max_bars_displayed - remaining_health_bars
        print(f"HEALTH : {self.current_health}/{self.max_health}")
        print(f"{TermColors.RED}|{remaining_health_bars * self.bar_type}{lost_health_bars * self.no_bar_type}|♥{TermColors.RESET}")
    
    def display_mana(self):
        remaining_mana_bars = round(self.current_mana/self.max_mana * self.max_bars_displayed)
        lost_mana_bars = self.max_bars_displayed - remaining_mana_bars
        print(f"MANA : {self.current_mana}/{self.max_mana}")
        print(f"{TermColors.BLUE}|{remaining_mana_bars * self.bar_type}{lost_mana_bars * self.no_bar_type}|♦{TermColors.RESET}")

    def lose_health(self, loss:int=0):
        self.current_health -= loss

    def lose_mana(self, loss:int=0):
        self.current_mana -= loss   

    def is_dead(self) -> bool:
        if self.get_current_health() <= 0:
            self.set_current_health(0)
            return True
        return False 

class Player(Character):

    class_type : str
    location : str
    atk_pts : int = 25
    def_pts : int = 25
    atk_options : dict = {"SLASH": 2, "STAB": 2, "TACKLE": 1.5}
    equipped_list = list[Item] = [None] * 5
    
    def __init__(self, name:str, max_health:int, current_health:int, max_mana:int, current_mana:int) -> None:
        super().__init__(name=name, char_type="PLAYER", max_health=max_health, current_health=current_health, max_mana=max_mana, current_mana=current_mana)
    
    def get_attack_pts(self) -> int:
        return self.atk_pts

    def set_attack_pts(self, new_atk_pts:int) -> None:
        self.atk_pts = new_atk_pts
    
    def get_defense_pts(self) -> int:
        return self.def_pts

    def set_defense_pts(self, new_def_pts:int) -> None:
        self.def_pts = new_def_pts

    def get_atk_options(self) -> dict:
        return self.atk_options
    
    def set_atk_options(self, new_atk:str, new_dmg: int) -> None:
        self.atk_options[new_atk.upper()] = new_dmg

    def get_class_type(self) -> str:
        return self.class_type

    def set_class_type(self, class_type: str) -> None:
        self.class_type = class_type

    def get_location(self) -> str:
        return self.location
    
    def set_location(self, new_location) -> None:
        self.location = new_location

    def get_equipped_list(self) -> list[Item]:
        return self.equipped_list
    
    def set_equipment(self, part:str, item:Item) -> None:
        WEAPON = "W"
        HEAD = "H"
        CHEST = "C"
        LEGS = "L"
        FEET = "F"

        if item in self.get_inventory():
            self.get_inventory().remove(item)

        if part.upper() == WEAPON:
            self.get_equipped_list()[0] = item                
        elif part.upper() == HEAD:
            self.get_equipped_list()[1] = item
        elif part.upper() == CHEST:
            self.get_equipped_list()[2] = item
        elif part.upper() == LEGS:
            self.get_equipped_list()[3] = item
        elif part.upper() == FEET:
            self.get_equipped_list()[4] = item
        else:
            print("INCORRECT STORAGE PART")

    def remove_equipment(self, part:str) -> None:
        WEAPON = "W"
        HEAD = "H"
        CHEST = "C"
        LEGS = "L"
        FEET = "F"

        if part.upper() == WEAPON:
            item = self.get_equipped_list()[0]
            self.get_equipped_list()[0] = None
            self.set_inventory(item)             
        elif part.upper() == HEAD:
            item = self.get_equipped_list()[1]
            self.get_equipped_list()[1] = None
            self.set_inventory(item) 
        elif part.upper() == CHEST:
            item = self.get_equipped_list()[2]
            self.get_equipped_list()[2] = None
            self.set_inventory(item) 
        elif part.upper() == LEGS:
            item = self.get_equipped_list()[3]
            self.get_equipped_list()[3] = None
            self.set_inventory(item) 
        elif part.upper() == FEET:
            item = self.get_equipped_list()[4]
            self.get_equipped_list()[4] = None
            self.set_inventory(item) 
        else:
            print("INCORRECT STORAGE PART")

    def display_player_stats(self) -> None:
        t = TermColors()
        t._print_green(text=f"NAME : {self.get_name()}")
        t._print_green(text=f"CLASS : {1}")
        self.display_health()
        self.display_mana()
    
    def display_inventory(self) -> None:
        inventory = self.get_inventory()
        inventory_len = self.get_inventory_len()
    
    def display_attack_options(self, enemy_list:list[Type["Enemy"]]) -> tuple:
        t = TermColors()
        t._print_green("[ATTACK OPTIONS]")
        counter = 1
        for key, value in self.get_atk_options().items():
            t._print_green(f"{counter}. {key}      -> {value}")
            counter += 1
        t._print_green("[CHOOSE ATTACK] -> ")
        choice = int(input())
        atk_opt_list = list(self.get_atk_options().keys())
        counter = 1
        for enemy in enemy_list:
            t._print_green(f"[ENEMY # {counter}]")
            enemy.display_enemy_stats()
            counter += 1
        t._print_green(f"[CHOOSE TARGET] -> ")
        target = int(input())
        return self.get_atk_options()[atk_opt_list[choice - 1]] * self.calculate_damage(), "SINGLE", "ENEMY", target

    def calculate_damage(self) -> int:
        bias = random.randint(1, 5)
        prob_atk_list = [self.get_attack_pts()] * bias
        counter = 2
        for dmg in range(1, 11 - bias):
            prob_atk_list.append(self.get_attack_pts() - counter)
            counter += 1
        return random.choice(prob_atk_list) 

    def defend_action(self, damage:int) -> int:
        percent = abs(round(damage/self.get_defense_pts() * 100)) # find percentage of attack on defense points
        defense = abs(round(percent/100 * damage)) # use percentage to give defense against attack by finding percentage of original on the damage
        if defense >= damage:
            return damage
        TermColors()._print_green(f"[{self.get_name().upper()} DEFENSE ACTIVATED] -> {100-percent}% OF ATTACK REDUCED!")
        return defense

    def loadout(self) -> None:
        t = TermColors()
        invent = self.get_inventory()
        t._print_green(f"[{self.get_name()} INVENTORY LIST]\n\n")
        for i in range(0, self.get_inventory_len()):
            item = invent[i]
            t._print_green(f"{i+1}. {item.get_item_name()} -> {item.cameo()}\n")
        
        if self.get_inventory_len() > 0:
            t._print_green("[END OF INVENTORY]")
        else:
            t._print_green("[NO ITEMS TO DISPLAY]")

    def equip(self) -> None:
        t = TermColors()
        invent = self.get_inventory()
        t._print_green("[EQUIPMENT SCREEN]")
        counter = 1
        for i in range(0, self.get_inventory_len()):
            item = invent[i]
            if item.get_item_type() == "WEAPON" or item.get_item_type() == "AMOUR":
                t._print_green(f"{counter}. {item.get_item_name()} -> {item.cameo()} -> EQUIPABLE\n")
                counter += 1
        t._print_green("[ENTER 0 TO EXIT]\n")
        t._print_green("[ENTER CHOICE] -> ")
        choice = input()

        # TODO: set equipment logic


class Enemy(Character):
    class_type : str
    location : str
    atk_pts : int = 15
    def_pts : int = 10
    atk_options : dict = {"SLASH": 1.5, "STAB": 1.5, "TACKLE": 0.5}


    def __init__(self, name:str, max_health:int, current_health:int, max_mana:int, current_mana:int) -> None:
        super().__init__(name=name, char_type="ENEMY", max_health=max_health, current_health=current_health, max_mana=max_mana, current_mana=current_mana)


    def get_attack_pts(self) -> int:
        return self.atk_pts

    def set_attack_pts(self, new_atk_pts:int) -> None:
        self.atk_pts = new_atk_pts
    
    def get_defense_pts(self) -> int:
        return self.def_pts

    def set_defense_pts(self, new_def_pts:int) -> None:
        self.def_pts = new_def_pts

    def get_atk_options(self) -> dict:
        return self.atk_options
    
    def set_atk_options(self, new_atk:str, new_dmg: int) -> None:
        self.atk_options[new_atk.upper()] = new_dmg

    def get_class_type(self) -> str:
        return self.class_type

    def set_class_type(self, class_type: str) -> None:
        self.class_type = class_type

    def get_location(self) -> str:
        return self.location
    
    def set_location(self, new_location) -> None:
        self.location = new_location

    def calculate_damage(self) -> int:
        bias = random.randint(1, 5)
        prob_atk_list = [self.get_attack_pts()] * bias
        counter = 2
        for dmg in range(1, 11 - bias):
            prob_atk_list.append(self.get_attack_pts() - counter)
            counter += 3
        return random.choice(prob_atk_list) * self.atk_options[random.choice(list(self.get_atk_options().keys()))]

    def select_single_target(self, target_list: list[Character]) -> int:
        return target_list.index(random.choice(target_list))
    
    def select_multiple_targets(self, target_list: list[Character]) -> list[Character]:
        t_list_len = len(target_list)
        new_target_list = []
        for x in range(0, t_list_len):
            new_target_list.append(random.choice(target_list))
        
        return new_target_list
    
    def display_enemy_stats(self) -> None:
        t = TermColors()
        t._print_green(f"NAME : {self.get_name()}")
        self.display_health()
        self.display_mana()

    def defend_action(self, damage:int) -> int:
        percent = damage/self.get_defense_pts() * 100 # find percentage of attack on defense points
        defense = abs(round(percent/100 * damage)) # use percentage to give defense against attack by finding percentage of original on the damage
        if defense >= damage:
            return damage
        TermColors()._print_green(f"[{self.get_name().upper()} DEFENSE ACTIVATED] -> {100-percent}% OF ATTACK REDUCED!")
        return defense


# ply_1 = Enemy("Test", 100, 100, 100, 100)
# print(ply_1.defend_action(9))








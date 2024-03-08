from color import TermColors


class Item:
    item_type : str = ""
    item_name : str = ""
    description : str = ""
    damage : int = 0
    defense : int = 0
    

    def __init__(self, item_type:str, item_name:str, damage:int, defense:int, description:str) -> None:
        self.item_type = item_type
        self.item_name = item_name
        self.damage = damage
        self.defense = defense
        self.description = description
        self.t = TermColors()

    def get_item_type(self) -> str:
        return self.item_type
    
    def set_item_type(self, new_type:str) -> None:
        self.item_type = new_type

    def get_item_name(self) -> str:
        return self.item_name.upper()

    def set_item_name(self, new_name:str) -> None:
        self.item_name = new_name

    def get_item_damage(self) -> int:
        return self.damage
    
    def set_item_damage(self, new_dmg:int) -> None:
        self.damage = new_dmg

    def get_item_defense(self) -> int:
        return self.defense
    
    def set_item_defense(self, new_def:int) -> None:
        self.defense = new_def

    def display_description(self) -> None:
        self.t._print_blue(self.description.upper())
    
    def set_description(self, new_desc:str) -> None:
        self.description = new_desc 

class Weapon(Item):

    attack_options : dict = {}
    
    def __init__(self, item_type: str, item_name: str, damage: int, defense: int, description: str, atk_options:dict) -> None:
        super().__init__(item_type, item_name, damage, defense, description)
        self.attack_options = atk_options

    def add_weapon(self, player) -> None:
        player.set_attack_pts(player.get_attack_pts() + self.get_item_damage())
        self.t._print_green(f"[{self.get_item_name()} EQUIPPED] -> {player.get_name()} EQUIPPED {self.get_item_name()}")

    def remove_weapon(self, player ) -> None:
        player.set_attack_pts(player.get_attack_pts() - self.get_item_damage())
        self.t._print_green(f"[{self.get_item_name()} REMOVED] -> {player.get_name()} REMOVED {self.get_item_name()}")

    def get_attack_options(self) -> dict:
        return self.attack_options
    
    def set_attack_options(self, new_atk_opts:dict) -> None:
        self.attack_options = new_atk_opts

    def process(self, player ) -> None:
        self.add_weapon(player)

    def deprocess(self, player ) -> None:
        self.remove_weapon(player)

    def cameo(self) -> str:
        return f"ATTACK: {self.get_item_damage()}; DEFENSE: {self.get_item_defense()};"

class Armour(Item):

    body_placement: int
    HEAD = 0
    CHEST = 1
    FEET = 2

    def __init__(self, item_type: str, item_name: str, damage: int, defense: int, description: str, body_placement: int) -> None:
        super().__init__(item_type, item_name, damage, defense, description)
        self.body_placement = body_placement

    
    def get_body_placement(self) -> str:
        return self.body_placement

    def add_amour(self, player) -> None:
        player.set_defense_pts(player.get_defense_pts() + self.get_item_defense())
        self.t._print_green(f"[{self.get_item_name()} EQUIPPED] -> {player.get_name()} IS WEARING {self.get_item_name()}")


    def remove_amour(self, player) -> None:
        player.set_defense_pts(player.get_defense_pts() - self.get_item_defense())
        self.t._print_green(f"[{self.get_item_name()} REMOVED] -> {player.get_name()} REMOVED {self.get_item_name()}")

    def process(self, player) -> None:
        self.add_amour(player)

    def deprocess(self, player) -> None:
        self.remove_amour(player)

    def cameo(self) -> str:
        return f"DEFENSE: {self.get_item_defense()}; ATTACK: {self.get_item_damage()};"

class Potion(Item):

    potion_type : str = ""
    target_value : int
    HEAL = "H"

    def __init__(self, item_type: str, item_name: str, damage: int, defense: int, description: str, target_value:int) -> None:
       super().__init__(item_type, (item_name + " POTION").upper(), damage, defense, description)
       self.target_value = target_value
    

    def get_potion_target_value(self) -> int:
        return self.target_value
    
    def set_potion_target_value(self, new_val:int) -> None:
        self.target_value = new_val

    def heal_action(self, player) -> None:
        player.set_current_health(player.get_current_health() + self.get_potion_target_value())
        player.current_health_adjust()
        self.t._print_green(f"[{player.get_name()} HEALED] -> {player.get_name()} USED '{self.get_item_name()}'")
        player.display_player_stats()
        input("[PRESS ENTER]")


class BeginnerSword(Weapon):

    def __init__(self) -> None:
        item_type = "WEAPON"
        item_name = "RUSTY SWORD"
        damage = 10
        defense = 0
        description = "A RUSTY SWORD FOR BEGINNERS"
        atk_options = {"SLASH": 2, "STAB": 2, "TACKLE": 1.5}
        super().__init__(item_type, item_name, damage, defense, description, atk_options)











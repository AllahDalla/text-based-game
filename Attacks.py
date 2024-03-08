from color import TermColors
from Characters import *


class Attack:
    instantiator : str
    atk_type : str
    target_type : str
    damage : int
    select_target : int
    player_list : list[Player] = []
    enemy_list : list[Enemy] = []
    # dead_player_list : list[Player] = []
    # dead_enemy_list : list[Enemy] = []
    AOE = "AOE"
    SINGLE = "SINGLE"
    PLY = "PLAYER"
    ENY = "ENEMY"

    def __init__(self, atk_type:str, target_type:str, select_target:int=0, damage:int=0, name: str="") -> None:
        self.instantiator = name
        self.damage = damage
        self.atk_type = atk_type
        self.target_type = target_type 
        self.select_target = select_target

    def get_instantiator(self) -> str:
        return self.instantiator
    
    def set_instantiator(self, new_inst:str) -> None:
        self.instantiator = new_inst
    
    def get_damage(self) -> int:
        return self.damage
    
    def set_damage(self, new_damage:int) -> None:
        self.damage = new_damage
    
    def get_player_list(self) -> list[Player]:
        return self.player_list

    def set_player_list(self, new_list:list[Player]) -> None:
        self.player_list = new_list
    
    def get_enemy_list(self) -> list[Enemy]:
        return self.enemy_list
    
    def set_enemy_list(self, new_list:list[Enemy]) -> None:
        self.enemy_list = new_list

    
    # def get_dead_player_list(self) -> list[Player]:
    #     return self.dead_player_list
    
    # def get_dead_enemy_list(self) -> list[Enemy]:
    #     return self.dead_enemy_list
    
    def get_attack_type(self) -> str:
        return self.atk_type
    
    def get_target_type(self) -> str:
        return self.target_type
    
    def get_select_target(self) -> int:
        return self.select_target 
    
    def remove_player(self, player:Player) -> None:
        self.get_player_list().remove(player)

    def remove_enemy(self, enemy: Enemy) -> None:
        self.get_enemy_list().remove(enemy)
    
    def _remove(self, c:Character) -> None:
        if isinstance(c, Player):
            play_len = len(self.get_player_list())
            new_player_list = []
            for player_idx in range(0, play_len):
                if(not(self.get_player_list()[player_idx].get_name().upper() == c.get_name().upper())):
                    new_player_list.append(self.get_player_list()[player_idx])
            self.set_player_list(new_player_list)
            return
        
        eny_len = len(self.get_enemy_list())
        new_enemy_list = []
        for enemy_idx in range(0, eny_len):
            if(not(self.get_enemy_list()[enemy_idx].get_name().upper() == c.get_name().upper())):
                new_enemy_list.append(self.get_enemy_list()[enemy_idx])
        self.set_enemy_list(new_enemy_list)
        return


    def is_enemy_alive(self, idx:int) -> bool:
        l = len(self.get_enemy_list()) # get length of enemy list
        return 0 <= idx < l

    def is_player_alive(self, idx:int) -> bool:
        l = len(self.get_player_list()) # get length of player list
        return 0 <= idx < l

    def get_target_enemy(self, idx) -> Enemy or None:
        enemy_list = self.get_enemy_list()
        player_list = self.get_player_list()
        # check if index is in enemy list and return enemy if true
        if self.get_target_type() == self.PLY and 0 <= idx < len(enemy_list) and self.is_player_alive(idx): 
            return player_list[idx]
        elif self.get_target_type() == self.ENY and 0 <= idx < len(player_list) and self.is_enemy_alive(idx):
            return enemy_list[idx]
            
        return None

    def phys_attack(self) -> tuple:
        t = TermColors()
        dead_player_list = []
        dead_enemy_list = []
        target_death = False

        if self.get_attack_type() == self.AOE:
            for target in self.get_enemy_list():
                calculated_damage = target.defend_action(self.get_damage())
                target.lose_health(calculated_damage)
                t._print_green(f"[DAMAGE DONE] -> {target.get_name()} HAS TAKEN {calculated_damage} DAMAGE")
                if isinstance(target, Player) and target.is_dead():
                    t._print_red(f"[PLAYER DIED] -> {target.get_name().upper()} DIED")
                    dead_player_list.append(target)
                    target_death = True
                elif isinstance(target, Enemy) and target.is_dead():
                    t._print_red(f"[ENEMY DIED] -> {target.get_name().upper()} KILLED")
                    dead_enemy_list.append(target)
                    target_death = True
            if target_death:
                for char in dead_player_list:
                    self.set_player_list(self._remove(char))
                for char in dead_enemy_list:
                    self.set_enemy_list(self._remove(char))
        elif self.get_attack_type() == self.SINGLE:
            target = self.get_target_enemy(self.get_select_target())
            if target:
                calculated_damage = target.defend_action(self.get_damage())
                target.lose_health(calculated_damage)
                t._print_green(f"[DAMAGE DONE] -> {target.get_name().upper()} HAS TAKEN {calculated_damage} DAMAGE BY {self.get_instantiator()}")
                if isinstance(target, Player) and target.is_dead():
                    t._print_red(f"[PLAYER DIED] -> {target.get_name().upper()} DIED")
                    self._remove(target)
                elif isinstance(target, Enemy) and target.is_dead():
                    t._print_red(f"[ENEMY DIED] -> {target.get_name().upper()} KILLED")
                    self._remove(target)
        return self.get_player_list(), self.get_enemy_list()
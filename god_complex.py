import random
import sys
from color import TermColors
from os import system
from time import sleep


class Player:
    
    max_bars_displayed = 20
    bar_type = "█"
    no_bar_type = "-"
    attack_set_list = ["SLASH", "STAB", "TACKLE"]
    attack_set_list_stats = {"SLASH":2, "STAB":2, "TACKLE":1.5}
    player_input_options = ["ATTACK", "DEFEND", "MAGIC", "STATS", "FLEE"]

    def __init__(self, name: str, _class: str):
        self.name = name
        self._class = _class
        self.max_health = 100
        self.current_health = 100
        self.max_mana = 50
        self.current_mana = 50
        self.attack_stat = 25
        self.defense_stat = None
        self.attack_type = "SLASH"

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

    def display_player_stats(self):
        print(f"{TermColors.GREEN}NAME: {self.name.upper()}{TermColors.RESET}")
        print(f"{TermColors.GREEN}CLASS : {self._class.upper()}{TermColors.RESET}")
        self.display_health()
        self.display_mana()

    def select_attack(self):
        counter = 1
        print(f"{TermColors.GREEN}[ATTACK TYPE]            [DAMAGE]\n{TermColors.RESET}")
        for key, value in self.attack_set_list_stats.items():
            print(f"{counter}. {key} -> {value}")
            counter += 1

        choice = int(input(f"{TermColors.GREEN}[CHOOSE ATTACK] -> {TermColors.RESET}"))
        self.attack_type = self.attack_set_list[choice - 1]
    
    def _gen_bias(self):
        bias = random.randint(1, 5)
        return bias
    
    def attack_move(self):
        self.select_attack()
        bias = self._gen_bias()
        max_attack_length = 9
        attack_list = [self.attack_stat] * bias
        for x in range(0, max_attack_length - len(attack_list)):
            attack_list.append(random.randint(round(self.attack_set_list_stats[self.attack_type] *  self.attack_stat - bias), round(self.attack_set_list_stats[self.attack_type] *  self.attack_stat - 1)))
        
        attack_pts = random.choice(attack_list)
        print(f"{TermColors.GREEN}[{self.name} ATTACK] -> {self.name} USED {self.attack_type}{TermColors.RESET}")
        print(f"{TermColors.RED}[DAMAGE] -> {attack_pts}{TermColors.RESET}")
        return attack_pts
    
    def display_player_options(self):
        opt_list_len = len(self.player_input_options)
        print(f"{TermColors.GREEN}\t[CHOOSE ACTION] -> 1 TO {opt_list_len}")
        for opt in range(0, opt_list_len):
            print(f"{opt + 1}. {self.player_input_options[opt]}")

class Enemy:

    max_bars_displayed = 20
    bar_type = "█"
    no_bar_type = "-"
    attack_types = ["STAB", "SLASH", "TACKLE"]

    def __init__(self, name:str):
        self.name = name
        self.max_health = 30
        self.current_health = 30
        self.max_mana = 10
        self.current_mana = 10
        self.attack_stat = 15
        self.defence_stat = None

    
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
        self.current_health = self.current_health - loss
        if self.current_health <= 0:
            del self

    def lose_mana(self, loss:int=0):
        self.current_mana = self.current_mana - loss

    def display_enemy_stats(self):
        print("NAME : GOBLIN")
        self.display_health()
        self.display_mana()

    def _gen_bias(self):
        bias = random.randint(1, 5)
        return bias
    
    def attack_move(self):
        bias = self._gen_bias()
        max_attack_length = 9
        attack_list = [self.attack_stat] * bias
        for x in range(0, max_attack_length - len(attack_list)):
            attack_list.append(random.randint(1, self.attack_stat - 1))
        
        attack_pts = random.choice(attack_list)
        print(f"{TermColors.GREEN}[ENEMY ATTACK] -> {self.name} USED {random.choice(self.attack_types)}{TermColors.RESET}")
        print(f"{TermColors.RED}[DAMAGE] -> {attack_pts}{TermColors.RESET}")
        return attack_pts


class BattleEnv:
    player_list = []
    enemy_list = []

    def __init__(self, player_list: list=[], enemy_list:list=[]):
        self.player_list = player_list
        self.enemy_list = enemy_list
    
    def _check_deaths(self):
        for player in self.player_list:
            if(player.current_health <= 0):
                player.current_health = 0
                print(f"{TermColors.RED}[PLAYER DEATH] -> PLAYER #{self.player_list.index(player) + 1} {player.name} WAS KILLED{TermColors.RESET}")
                self.player_list.remove(player)
        for enemy in self.enemy_list:
            if(enemy.current_health <= 0):
                enemy.current_health = 0
                print(f"{TermColors.YELLOW}[ENEMY DEATH] -> ENEMY #{self.enemy_list.index(enemy) + 1} {enemy.name} WAS KILLED{TermColors.RESET}")
                self.enemy_list.remove(enemy)

    def character_flee(self, character):
        if isinstance(character, Player):
            print(f"{TermColors.BLUE}[{character.name} FLED] -> {character.name} LEFT THE BATTLE SAFELY{TermColors.BLUE}")
            self.player_list.remove(character)
        else:
            print(f"{TermColors.BLUE}[{character.name} FLED] -> {character.name} LEFT THE BATTLE SAFELY{TermColors.BLUE}")
            self.enemy_list.remove(character)

    def display_enemy_targets(self):
        enemy_list_len = len(self.enemy_list)
        for enemy in range(0, enemy_list_len):
            print(f"{TermColors.BLUE}[ENEMY #{enemy + 1}]{TermColors.RESET}")
            self.enemy_list[enemy].display_enemy_stats()

    def _character_party_turn(self, character_list:list):
        if len(self.player_list) > 0:
            if len(character_list) > 0:
                for character in character_list:
                    if isinstance(character, Player):
                        character.display_player_options()
                        player_action = int(input(f"{TermColors.GREEN}[{character.name} TURN] -> ENTER ACTION \n{TermColors.RESET}"))
                        if player_action == 1:
                            self.display_enemy_targets()
                            target_enemy_idx = int(input(f"{TermColors.GREEN}[CHOOSE TARGET] -> {TermColors.RESET}"))
                            target_enemy = self.enemy_list[target_enemy_idx - 1]
                            player_atk_pts = character.attack_move()
                            if player_atk_pts > 0:
                                Attack([target_enemy], player_atk_pts, self.enemy_list).attack()
                                print(f"{TermColors.GREEN}[DAMAGE DEALT] -> {target_enemy.name} ENEMY #{self.enemy_list.index(target_enemy) + 1} TOOK {player_atk_pts} DAMAGE{TermColors.RESET}")
                            else:
                                print(f"{TermColors.YELLOW}[ATTACK MISSED] -> {character.name} MISSED ENEMY{TermColors.RESET}") 
                        elif player_action == 4:
                            character.display_player_stats()
                        elif player_action == 5:
                            self.character_flee(character)
                        self._check_deaths()
                        input(f"{TermColors.GREEN}[PRESS ENTER]{TermColors.RESET}")

                    else:
                        print(f"{TermColors.GREEN}[{character.name} #{self.enemy_list.index(character) + 1} TURN]{TermColors.RESET}")
                        enemy_atk_pts = character.attack_move()
                        target_player = random.choice(self.player_list)
                        sleep(2.5)
                        if enemy_atk_pts > 0:
                            Attack([target_player, enemy_atk_pts, self.player_list]).attack()
                            print(f"{TermColors.GREEN}[DAMAGE DEALT] -> {target_player.name} TOOK {enemy_atk_pts} DAMAGE{TermColors.RESET}")

                        else:
                            print(f"{TermColors.YELLOW}[ATTACK MISSED] -> {character.name} MISSED PLAYER {target_player.name}{TermColors.RESET}") 
                        self._check_deaths()
                        input(f"{TermColors.GREEN}[PRESS ENTER]{TermColors.RESET}")
                        

                    loader()

    def battle(self):
        while True:
            for enemy in self.enemy_list:
                print(f"{TermColors.RED}[ENEMY APPEARS   ->  {enemy.name}]{TermColors.RESET}")
                sleep(1)
            
            print(f"{TermColors.GREEN}[FIGHT ENCOUNTERED]{TermColors.RESET}")
            while len(self.enemy_list) > 0 or len(self.player_list) > 0:  
                self.display_enemy_targets()
                sleep(2.5)
                input(f"{TermColors.GREEN}[PRESS ENTER]{TermColors.RESET}")
                system("cls")
                self._character_party_turn(self.player_list)
                self._character_party_turn(self.enemy_list)
                sleep(2.5)
                input(f"{TermColors.GREEN}[PRESS ENTER]{TermColors.RESET}")
                loader()
            break

class Attack:

    def __init__(self, target_list:list, damage:int, enemy_list:list):
        self.target_character = target_list
        self.damage_pts = damage
        self.target_character_og_list = enemy_list

    def attack(self):
        for target in self.target_character:
            target.lose_health(self.damage_pts)
            print(f"{TermColors.GREEN}[DAMAGE DEALT] -> {target.name} ENEMY #{self.target_character_og_list.index(target) + 1} TOOK {self.damage_pts} DAMAGE{TermColors.RESET}")

        

def loader():
    bar_type = "█"
    no_bar_type = "-"
    counter = 1
    while counter <= 20:
        sys.stdout.write(f"{TermColors.BLUE}[LOADING] . . . |{bar_type * counter}{no_bar_type * (20 - counter)}|{TermColors.RESET}")
        sys.stdout.flush()
        system("cls")
        sleep(0.001)
        counter += 1

def play():
    player_name = input("[ENTER NAME] -> ")
    player_1 = Player(player_name, "NORMAL")
    player_list = [player_1]
    enemy_1 = Enemy("GOBLIN")
    enemy_2 = Enemy("GOBLIN")
    enemy_3 = Enemy("GOBLIN")
    enemy_4 = Enemy("GOBLIN")
    enemy_5 = Enemy("GOBLIN")
    enemy_list = [enemy_1, enemy_2, enemy_3, enemy_4, enemy_5]

    battle_env = BattleEnv(player_list, enemy_list)
    battle_env.battle()

play()



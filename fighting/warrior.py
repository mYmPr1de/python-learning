import random
from typing import Self


class Armor:
    def __init__(self, defence: int, class_armor: int):
        self.class_armor = class_armor
        self.armor = defence * self.multiplicity_check()

    def multiplicity_check(self) -> float:
        return {
            1: 1,
            2: 1.3,
            3: 1.5,
        }.get(self.class_armor, 1)

    def _can_absorb_all_damage(self, damage: int | float) -> bool:
        return damage <= self.armor

    def absorb(self, damage: int) -> int | float:
        if self._can_absorb_all_damage(damage):
            self.armor -= damage
            print(
                f"The armor absorbed the damage successfully. Remaining armor is: {self.armor}"
            )
            return self.armor
        else:
            remaining_damage = self.armor - damage
            self.armor = 0
            print(
                f"The armor don't absorb all the damage and part of the damage transfers to health. "
                f"Remaining damage is: {abs(remaining_damage)}"
            )
            return remaining_damage


class Weapon:
    def __init__(
        self,
        name: str,
        max_damage: int,
        min_damage: int,
        crit_chance: int,
        crit_strange: int,
    ):
        self.name = name
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.crit_chance = crit_chance
        self.crit_strange = crit_strange

    def _is_crit_triggered(self) -> int:
        return random.randint(1, 100) <= self.crit_chance

    def calculate_damage(self) -> int | float:
        actual_damage = random.randint(self.min_damage, self.max_damage)
        if self._is_crit_triggered():
            actual_damage *= (self.crit_strange / 100) + 1
            print(f"Crit attack {actual_damage} damage")
        else:
            print(f"Non-critical damage is: {actual_damage} damage")
        return actual_damage


class Warrior:
    def __init__(self, name: str, health: int, weapon: Weapon, armor: Armor):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.is_alive: bool = True

    def take_damage(self, damage: int):
        remaining_armor = self.armor.absorb(damage)
        if remaining_armor <= 0:
            self.health -= abs(remaining_armor)
            if self.health <= 0:
                self.health = 0
                self.is_alive = False
            print(
                f"The health after damage is: {self.health} and armor is: {self.armor.armor}"
            )

    def damage_of_health(self, damage: int) -> bool:
        return damage <= self.health

    def attack(self, opponent: Self):
        damage = self.weapon.calculate_damage()
        opponent.get_damage(damage)


def fight(warrior1: "Warrior", warrior2: "Warrior"):
    print(
        f"Warrior {warrior1.name} health: {warrior1.health} HP, armor: {warrior1.armor.armor} CP"
    )
    print(
        f"Warrior {warrior2.name} health: {warrior2.health} HP, armor: {warrior2.armor.armor} CP\n"
    )
    print("-" * 50)
    while warrior1.is_alive and warrior2.is_alive:
        print(f"Warrior {warrior1.name} attack warrior {warrior2.name}")
        warrior1.attack(warrior2)
        print(
            f"{warrior2.name} health: {warrior2.health} HP, armor: {warrior2.armor.armor} CP\n"
        )
        print("-" * 50)

        if not warrior2.is_alive:
            print(f"{warrior1.name} WON!!")
            print("-" * 50)
            break

        print(f"Warrior {warrior2.name} attack warrior {warrior1.name}")
        warrior2.attack(warrior1)
        print("-" * 50)

        if not warrior1.is_alive:
            print(f"{warrior2.name} WON!!")
            print("-" * 50)
            break

    print(
        f"The battle is over.\n"
        f"Warrior {warrior1.name} health: {warrior1.health} HP, armor: {warrior1.armor.armor} CP\n"
        f"{warrior2.name} health: {warrior2.health} HP, armor: {warrior2.armor.armor} CP."
    )


if __name__ == "__main__":
    armor_1 = Armor(defence=15000, class_armor=2)
    weapon_1 = Weapon(name="Hammer", min_damage=200, max_damage=5000, crit_chance=80, crit_strange=95)
    warrior_1 = Warrior(name="Aleksandr", health=6000, weapon=weapon_1, armor=armor_1)

    armor_2 = Armor(defence=16000, class_armor=3)
    weapon_2 = Weapon(name="Knife", min_damage=500, max_damage=5000, crit_chance=90, crit_strange=85)
    warrior_2 = Warrior(name="Vlad", health=7000, weapon=weapon_2, armor=armor_2)

    fight(warrior_1, warrior_2)
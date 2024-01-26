import random
from typing import Self
from enum import Enum


class ArmorClassEnum(int, Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3


ARMOR_MULTIPLIER_BY_ARMOR_CLASS = {
    ArmorClassEnum.FIRST: 1,
    ArmorClassEnum.SECOND: 1.3,
    ArmorClassEnum.THIRD: 1.5,
}


class Armor:
    def __init__(self, defence: int, class_armor: ArmorClassEnum):
        self.class_armor = class_armor
        self.armor = defence * self.multiplicity_check()

    def multiplicity_check(self) -> float:
        return ARMOR_MULTIPLIER_BY_ARMOR_CLASS[self.class_armor]

    def _can_absorb_all_damage(self, damage: int | float) -> bool:
        return damage <= self.armor

    def absorb_and_return_remaining_damage(self, damage: int) -> int | float:
        """
        Absorbs damage using the armor.
        This method checks if the armor can absorb all the damage.
        :param damage: The amount of damage to be absorbed.
        :return: Remaining damage after absorption
        If the damage is completely absorbed then it returns 0
        """
        if self._can_absorb_all_damage(damage):
            absorbed_damage = damage
            self.armor -= absorbed_damage
            return 0
        else:
            remaining_damage = damage - self.armor
            self.armor = 0
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
        return actual_damage


class Warrior:
    def __init__(self, name: str, health: int, weapon: Weapon, armor: Armor):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.is_alive: bool = True

    def take_damage(self, damage: int):
        remaining_damage = self.armor.absorb_and_return_remaining_damage(damage)
        self.health -= remaining_damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def attack(self, opponent: Self):
        damage = self.weapon.calculate_damage()
        opponent.take_damage(damage)


def fight(warrior1: "Warrior", warrior2: "Warrior"):
    print(
        f"Warrior {warrior1.name} health: {warrior1.health} HP, armor: {warrior1.armor.armor} CP"
    )
    print(
        f"Warrior {warrior2.name} health: {warrior2.health} HP, armor: {warrior2.armor.armor} CP\n"
    )
    print("-" * 50)
    while warrior1.is_alive and warrior2.is_alive:
        warrior1.attack(warrior2)
        if not warrior2.is_alive:
            break
        warrior2.attack(warrior1)
        if not warrior1.is_alive:
            break

    print(f"The battle is over")
    if warrior1.is_alive:
        print(
            f"Warrior {warrior1.name} won. Health: {warrior1.health} HP, armor: {warrior1.armor.armor} CP"
        )
    elif warrior2.is_alive:
        print(
            f"Warrior {warrior2.name} won. Health: {warrior2.health} HP, armor: {warrior2.armor.armor} CP"
        )


if __name__ == "__main__":
    armor_1 = Armor(defence=15000, class_armor=ArmorClassEnum.SECOND)
    weapon_1 = Weapon(
        name="Hammer", min_damage=200, max_damage=5000, crit_chance=80, crit_strange=95
    )
    warrior_1 = Warrior(name="Aleksandr", health=6000, weapon=weapon_1, armor=armor_1)

    armor_2 = Armor(defence=16000, class_armor=ArmorClassEnum.THIRD)
    weapon_2 = Weapon(
        name="Knife", min_damage=500, max_damage=5000, crit_chance=90, crit_strange=85
    )
    warrior_2 = Warrior(name="Vlad", health=7000, weapon=weapon_2, armor=armor_2)

    fight(warrior_1, warrior_2)

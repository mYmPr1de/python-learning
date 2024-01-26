import pytest
from warrior import Armor, ArmorClassEnum, ARMOR_MULTIPLIER_BY_ARMOR_CLASS


def test_can_absorb_all_damage_successfully():
    defence = 500
    armor_class = ArmorClassEnum.SECOND
    instance_armor = Armor(defence=defence, class_armor=armor_class)
    expected_armor = defence * ARMOR_MULTIPLIER_BY_ARMOR_CLASS[armor_class]
    assert instance_armor.armor == expected_armor
    remaining_damage = instance_armor.absorb_and_return_remaining_damage(500)
    expected_armor_after_damaging = expected_armor - 500
    assert remaining_damage == 0
    assert instance_armor.armor == expected_armor_after_damaging


def test_remaining_damage_after_absorb():
    defence = 500
    armor_class = ArmorClassEnum.SECOND
    armor = Armor(defence=defence, class_armor=armor_class)
    expected_armor = defence * ARMOR_MULTIPLIER_BY_ARMOR_CLASS[armor_class]
    absorbed_damage = 800
    remaining_damage = armor.absorb_and_return_remaining_damage(absorbed_damage)
    expected_remaining_damage = absorbed_damage - expected_armor
    assert remaining_damage == expected_remaining_damage
    assert armor.armor == 0

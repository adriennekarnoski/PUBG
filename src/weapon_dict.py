"""Dictionaries of weapon statistics.

https://pubgmap.io/weapons.html."""


class Weapon(object):
    """Creates a Weapon object."""

    def __init__(self, weapon_stats):
        """Add beginning statistics."""
        self.name = weapon_stats[0]
        self.ammo_type = weapon_stats[1]
        self.hit_damage = weapon_stats[2]
        self.ammo_compacity = weapon_stats[3]
        self.reload_speed = weapon_stats[4]
        self.weight = weapon_stats[5]

scar_l = {
    'begining_stats': ['Scar-L', '5.56mm', 43, '30', '3.100s', '500'],
    'available_attachemnts': ['Sights']
    }
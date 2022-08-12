# Components ##################################################################
###############################################################################


class Appearance:
    """Class containing creature's appearance

    Attributes:
        body_parts (pynwn.BodyParts): body_parts
        hair (int): hair
        id (int): Index into ``appearance.2da``
        phenotype (int): phenotype
        portrait_id (int): Index into ``portraits.2da``
        skin (int): skin
        tail (int): tail
        tattoo1 (int): tattoo1
        tattoo2 (int): tattoo2
        wings (int): wings"""

    pass


class BodyParts:
    """Class containing references to creature's body parts

    Attributes:
        belt (int): body part
        bicep_left (int): body part
        bicep_right (int): body part
        foot_left (int): body part
        foot_right (int): body part
        forearm_left (int): body part
        forearm_right (int): body part
        hand_left (int): body part
        hand_right (int): body part
        head (int): body part
        neck (int): body part
        pelvis (int): body part
        shin_left (int): body part
        shin_right (int): body part
        shoulder_left (int): body part
        shoulder_right (int): body part
        thigh_left (int): body part
        thigh_right (int): body part"""

    pass


class Common:
    """Class containing attributes common to all objects

    Attributes:
        resref (pynwn.Resref): resref
        tag (str): tag
        name (pynwn.LocString): name
        locals (pynwn.LocalData): locals
        location (pynwn.Location): location
        comment (str): comment
        palette_id (int): palette_id
    """

    pass


class CreatureStats:
    pass


class Equips:
    pass


class Inventory:
    pass


class LevelStats:
    pass


class LocalData:
    def delete_float(varname: str):
        """Deletes float variable"""
        pass

    def delete_int(varname: str):
        """Deletes int variable"""
        pass

    def delete_object(varname: str):
        """Deletes object variable"""
        pass

    def delete_string(varname: str):
        """Deletes string variable"""
        pass

    def delete_location(varname: str):
        """Deletes location variable"""
        pass

    def get_float(varname: str):
        """Gets float variable"""
        pass

    def get_int(varname: str) -> int:
        """Gets int variable"""
        pass

    def get_object(varname: str):
        """Gets object variable"""
        pass

    def get_string(varname: str) -> str:
        """Gets string variable"""
        pass

    def get_location(varname: str):
        """Gets location variable"""
        pass

    def set_float(varname: str, value: float):
        """Sets float variable"""
        pass

    def set_int(varname: str, value: int):
        """Sets int variable"""
        pass

    def set_object(varname: str):
        """Sets object variable"""
        pass

    def set_string(varname: str, value: str):
        """Sets string variable"""
        pass

    def set_location(varname: str):
        """Sets location variable"""
        pass

    def size():
        """Gets number of variables"""
        pass

    pass


class Location:
    pass


class Lock:
    """Class representing a lock on an object

    Attributes:
        key_name (str)
        key_required (bool)
        lockable (bool)
        locked (bool)
        lock_dc (int)
        unlock_dc (int)
        remove_key (bool)
    """

    pass


class SpellBook:
    pass


class Trap:
    """Class representing a trap on an object

    Attributes:
        detect_dc (int)
        detectable (bool)
        disarm_dc (int)
        disarmable (bool)
        is_trapped (bool)
        one_shot (bool)
        type
    """

    pass


# Formats #####################################################################
###############################################################################


class TwoDA:
    """Implementation of 2da file format

    Args:
        filename (str): 2da file to load
    """

    def __init__(self, filename: str):
        """Loads 2da from `filename`"""
        pass

    def get(self, row: int, column: int | str):
        """Gets a TwoDA value

        Args:
            row (int): Row number
            column (int | str): Column number or label

        Returns:
            An int | float | string depending on the underlying value
        """
        pass

    def set(self, row: int, column: int | str, value: int | float | str):
        """Sets a TwoDA value

        Args:
            row (int): Row number
            column (int | str): Column number or label
            value (int | float | str): New value
        """
        pass


# Objects #####################################################################
###############################################################################


class ObjectBase:
    def handle(self):
        """Gets object handle"""
        pass

    pass


class Area:
    pass


class Creature(ObjectBase):
    """Class that represents a Creature object

    Attributes:
        appearance
        bodybag
        chunk_death
        combat_info
        conversation (pynwn.Resref): Dialog resref
        cr
        cr_adjust
        decay_time
        deity
        description
        disarmable
        faction_id
        gender
        good_evil
        hp
        hp_current
        hp_max
        immortal
        interruptable
        lawful_chaotic
        levels
        lootable
        name_first
        name_last
        pc
        perception_range
        plot
        race
        scripts
        soundset
        starting_package
        stats (:class:`pynwn.CreatureStats`): Offensive and defensive stats.
        subrace (str): Subrace
        walkrate
    """

    def __init__(self, filename: str):
        pass


class CreatureScripts:
    """A class containing a creature's script set.

    Attributes:
        on_attacked (pynwn.Resref): A script
        on_blocked (pynwn.Resref): A script
        on_conversation (pynwn.Resref): A script
        on_damaged (pynwn.Resref): A script
        on_death (pynwn.Resref): A script
        on_disturbed (pynwn.Resref): A script
        on_endround (pynwn.Resref): A script
        on_heartbeat (pynwn.Resref): A script
        on_perceived (pynwn.Resref): A script
        on_rested (pynwn.Resref): A script
        on_spawn (pynwn.Resref): A script
        on_spell_cast_at (pynwn.Resref): A script
        on_user_defined (pynwn.Resref): A script
    """

    pass


class Door:
    """Class that represents a Door object

    Attributes:
        animation_state
        appearance
        conversation (pynwn.Resref): Door's conversation resref
        description
        faction
        generic_type
        hardness
        hp
        hp_current
        interruptable
        linked_to
        linked_to_flags
        loadscreen
        lock
        plot
        portrait_id
        saves
        scripts
        trap
    """

    pass


class Encounter:
    """Class that represents an Encounter object

    Attributes:
        active (bool)
        creatures
        creatures_max (int)
        creatures_recommended
        difficulty
        difficulty_index
        faction
        geometry
        player_only
        reset
        reset_time
        respawns
        scripts
        spawn_option
        spawn_points
    """

    pass


class Item:
    """Class that represents an Item object

    Attributes:
        additional_cost
        baseitem
        charges
        cost
        cursed
        description (pynwn.LocString): Description
        description_id (pynwn.LocString): Description after being identified.
        identified
        inventory
        model_colors
        model_parts
        model_type
        plot (bool): Is a plot item.
        properties
        stacksize
        stolen
    """

    pass


class Module:
    """Class that represents a Module object

    Attributes:
        creator
        dawn_hour
        description
        dusk_hour
        entry_area
        entry_orientation
        entry_position
        expansion_pack
        haks
        id
        is_save_game
        locals
        min_game_version
        minutes_per_hour
        name
        scripts
        start_day
        start_hour
        start_month
        start_movie
        start_year
        tag
        tlk
        version
        xpscale
    """

    def __iter__(self):
        """Get iterator of areas in the module"""
        pass

    def __len__(self):
        """Get the number of areas in the module"""
        pass

    pass


class ModuleScripts:
    """Module Scripts

    Attributes:
        on_client_enter
        on_client_leave
        on_cutsnabort
        on_heartbeat
        on_item_acquire
        on_item_activate
        on_item_unaquire
        on_load
        on_player_chat
        on_player_death
        on_player_dying
        on_player_equip
        on_player_level_up
        on_player_rest
        on_player_uneqiup
        on_spawnbtndn
        on_start
        on_user_defined
    """

    pass


class Placeable:
    """Class that represents a Placeable object

    Attributes:
        animation_state
        appearance
        bodybag
        common
        conversation
        description
        faction
        hardness
        has_inventory
        hp
        hp_current
        interruptable
        inventory
        lock
        plot
        portrait_id
        saves
        scripts (pynwn.PlaceableScripts):
        static
        trap
        useable
    """

    pass


class Sound(ObjectBase):
    """Class that represents a Sound object

    Attributes:
        active
        common (pynwn.Common): Common object component
        continuous
        distance_max
        distance_min
        elevation
        generated_type
        hours
        interval
        interval_variation
        looping
        pitch_variation
        positional
        priority
        random
        random_position
        random_x
        random_y
        sounds ([pynwn.Resref]): Sounds
        times
        volume
        volume_variation
    """

    def __init__(self, filename: str):
        pass

    pass


class Store(ObjectBase):
    """Class that represents a Store object

    Attributes:
        armor
        blackmarket
        blackmarket_markdown
        gold
        identify_price
        markdown
        markup
        max_price
        miscellaneous
        potions
        rings
        scripts
        weapons

    //.def_readonly("will_not_buy", &nw::Store::will_not_buy)
    //.def_readonly("will_only_buy", &nw::Store::will_only_buy)
    """

    pass


class Trigger(ObjectBase):
    """Class that represents a Trigger object

    Attributes:
        cursor
        faction
        geometry
        highlight_height
        linked_to
        linked_to_flags
        loadscreen
        portrait
        scripts
        trap (pynwn.Trap): A trap component
        type
    """

    pass


class Waypoint:
    """Class that represents a Waypoint object

    Attributes:
        appearance
        description (pynwn.LocString)
        has_map_note (bool): Has a map note
        linked_to (str): Tag of linked object
        map_note (pynwn.LocString)
        map_note_enabled
    """

    pass


# Resources ###################################################################
###############################################################################


# Serialization ###############################################################
###############################################################################

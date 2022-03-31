import pynwn


def test_creature_default_construct():
    w = pynwn.Creature()
    # assert w.common().id == pynwn.OBJECT_INVALID

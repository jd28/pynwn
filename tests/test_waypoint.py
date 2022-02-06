import pynwn


def test_waypoint_default_construct():
    w = pynwn.Waypoint()
    assert w.common().id == pynwn.OBJECT_INVALID

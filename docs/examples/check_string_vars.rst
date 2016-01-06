Checking Local Variables
========================

This checks all blueprints and all placed object instances looking for string variables that can be converted to integers or floating point numbers in case of any variable type bugs.

.. code::

    #!/usr/bin/env python

    from itertools import chain
    from pynwn import Module

    def check_vars(obj):
        for var, val in obj.vars.string.list():
            try:
                x = int(val)
                print ("    %s: Variable %s (%s) is convertable to int!" % (obj.resref, var, val))
                continue # continue since if it's convertible to int it will also convert to float.
            except:
                pass

            try:
                x = float(val)
                print("    %s: Variable %s (%s) is convertable to float!" % (obj.resref, var, val))
            except:
                pass

    if __name__ == '__main__':
        mod = Module('test.mod')

        print("Checking blueprints...")
        for obj in chain(mod.glob('*.ut[cdeimptw]'), mod.areas):
            check_vars(obj)

        print("\nChecking instances...")
        for area in mod.areas:
            for obj in chain(area.creatures, area.doors, area.placeables,
                             area.triggers, area.stores, area.encounters,
                             area.waypoints, area.items):
                check_vars(obj)

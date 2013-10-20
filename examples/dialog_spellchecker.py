#/usr/bin/env python

# Pretty simple command line spellchecker for NWN dialogs...
# Note this requires PyEnchant and it's command line is some
# what wonky.  Type 'h' at the command prompt to get options
# for correcting wor

import enchant
import enchant.checker
from enchant.checker.CmdLineChecker import CmdLineChecker

from pynwn.module import Module

if __name__ == '__main__':
    # Using US english dictionary.
    chkr = enchant.checker.SpellChecker('en_US')
    cmdln = CmdLineChecker()
    cmdln.set_checker(chkr)

    mod = Module('test.mod')
    
    for dlg in mod.glob('*.dlg'):
        print dlg.resref
        for n in dlg.entries:
            if n.get_text(0) is None or len(n.get_text(0)) == 0:
                continue

            print n.get_text(0)
            chkr.set_text(n.get_text(0))
            cmdln.run()
            n.set_text(0, chkr.get_text())

        for n in dlg.replies:
            if n.get_text(0) is None or len(n.get_text(0)) == 0:
                continue

            print n.get_text(0)
            chkr.set_text(n.get_text(0))
            cmdln.run()
            n.set_text(0, chkr.get_text())

    mod.container.save()

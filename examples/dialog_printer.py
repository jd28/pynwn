#!/usr/bin/env python

# This example prints all the dialogs in a module in tree form.

from pynwn.module import Module

INDENT_WIDTH = 2


def dialog_to_str(dlg):
    def fmt(string, level, link=False):
        justify = INDENT_WIDTH * level
        # Note if the node has no dialog, the string will be None
        if not string:
            res = '<EMPTY>'
        else:
            res = string.strip().replace('\n', '\n'.ljust(justify + 1))

        if link:
            res = "Link: " + res

        res += '\n'
        return res.rjust(justify + len(res))

    def node_to_str(node, level):
        res = fmt(node.get_text(0), level)
        for ptr in node.pointers:
            node = ptr.get_node(ptr.index)
            # Make sure the dialog pointer isn't a link or else
            # there would be an infinite loop.
            if not ptr.is_link:
                level += 1
                res += node_to_str(node, level)
                level -= 1
            else:
                # Add extra indent for links...
                res += fmt(node.get_text(0), level + 1, True)
        return res

    result = ''
    for start in [s.index for s in dlg.starts]:
        result += node_to_str(dlg.entries[start], 0)

    return result


if __name__ == '__main__':
    mod = Module('test.mod')

    for dlg in mod.glob('*.dlg'):
        print(dlg.resref)
        print(dialog_to_str(dlg), '\n\n')

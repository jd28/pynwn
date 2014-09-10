#!/usr/bin/env python

# Minimap Generator similar to the one in pspeed's nwn java tools
# NOTE: THIS EXAMPLE REQUIRES the Python Imaging Library!

from pynwn.resource import ResourceManager
from pynwn.util.helper import chunks
import ConfigParser, sys
import Image

if __name__ == '__main__':
    mgr      = ResourceManager.from_module('test.mod')
    scale    = 1
    minimum  = 32
    tga_dict = {}

    for area in mgr.module.areas:
        print("Generating minimap for %s" % area.get_name(0))

        config = ConfigParser.ConfigParser()

        try:
            tile_tgas = []
            tga_size  = sys.maxint
            config.readfp(mgr[area.tileset + '.set'].to_io())

            for tile in area.tiles:
                tga = config.get('TILE%d' % tile.id, 'ImageMap2D').lower()
                tga_fname = tga+'.tga'
                if not tga_fname in tga_dict:
                    tga_dict[tga_fname] = Image.open(mgr[tga_fname].to_io())

                tga = tga_dict[tga_fname]

                # I chose here to scale all the minimap images to the
                # smallest size so if one is 8x8 they will all be scaled
                # to 8x8.
                tga_size = min(tga_size, tga.size[0])
                tile_tgas.append((tga, tile.orientation))

            # Note: The tile list begins in the bottom left corner
            # so I'm going to reverse so that it starts in the top
            # left and draw down rather than up.
            tile_tgas = chunks(tile_tgas, area.width)[::-1]

            # minimum minimap tile size 16x16, just so some of the
            # smaller 8x8s are a little larger.
            tga_size = max(minimum, tga_size * scale)

            new_im = Image.new('RGBA', (area.width * tga_size,
                                        area.height * tga_size))

            for h in xrange(area.height):
                for w in xrange(area.width):

                    im, rot = tile_tgas[h][w]
                    new_loc = (w * tga_size, h * tga_size)

                    if im.size[0] != tga_size:
                        im = im.resize((tga_size, tga_size))

                    new_im.paste(im.rotate(rot*90), new_loc)

            new_im.save(area.resref + '.png')

        except Exception as e:
            print(e)
            continue

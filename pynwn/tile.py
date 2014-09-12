from pynwn.file.gff import make_gff_property

TRANSLATION_TABLE = {
    'id'          : ('Tile_ID', "ID."),
    'orientation' : ('Tile_Orientation', "Orientation."),
    'height'      : ('Tile_Height', "Height."),
}

class TileInstance(object):
    """There is no base Tile class, Tiles can only be instances"""
    def __init__(self, gff, parent_obj):
        self.gff = gff
        self.is_intance = True
        self.parent_obj = parent_obj

    @property
    def main_lights(self):
        return (self.gff['Tile_MainLight1'], self.gff['Tile_MainLight2'])

    @property
    def source_lights(self):
        return (self.gff['Tile_MainLight1'], self.gff['Tile_MainLight2'])

    @property
    def anim_loops(self):
        return (self.gff['Tile_AnimLoop1'],
                self.gff['Tile_AnimLoop2'],
                self.gff['Tile_AnimLoop3'])

for key, val in TRANSLATION_TABLE.items():
    setattr(TileInstance, key, make_gff_property('gff', val))

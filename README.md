[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ci](https://github.com/jd28/pynwn/actions/workflows/build.yml/badge.svg)](https://github.com/jd28/pynwn/actions/workflows/build.yml)
[![CodeQL](https://github.com/jd28/pynwn/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/jd28/pynwn/actions/workflows/codeql-analysis.yml)

# pynwn

pynwn is now a wrapper (or will be) around [rollnw](https://github.com/jd28/rollnw).  Older versions can be found on `master-obsolete` and `develop-obsolete`.  Getting CI going, first.. then the rest.

```python

import pynwn

pynwn.kernel.start()
mod = pynwn.kernel.load_module("mymodule.mod")
for area in mod:
    # Do neat things

```

## Status

### formats
- [x] Image
- [ ] Ini
- [x] Nss
- [x] NssLexer
- [ ] NssParser
- [x] TwoDA

### i18n

- [x] Language
- [x] LocString
- [x] Tlk
- [x] conversion - unneeded, Python strings are already utf8

### kernel

- [ ] Config
- [ ] Kernel
- [ ] Objects
- [ ] Resources
- [ ] Strings


### objects

- [x] Area
- [x] Creature
- [ ] Dialog
- [x] Door
- [x] Encounter
- [ ] Faction
- [x] Item
- [ ] Journal
- [x] Module
- [x] ObjectBase
- [ ] Palette
- [x] Placeable
- [x] Sound
- [x] Store
- [x] Trigger
- [x] Waypoint

#### components

- [x] Appearance
- [ ] CombatInfo
- [x] Common
- [x] CreatureStats
- [x] Equips
- [x] Inventory
- [ ] LevelStats
- [x] LocalData
- [x] Location
- [x] Lock
- [x] Saves
- [ ] SpellBook
- [x] Trap

### resources

- [ ] Bif - unexposed
- [x] Container
- [x] Directory
- [x] Erf
- [x] Key
- [x] NWSync
- [x] Resource
- [x] ResourceDescriptor
- [x] ResourceType
- [x] Resref
- [x] Zip

### serialization

- [ ] Archives
- [ ] GffInputArchive
- [ ] GffOutputArchive
- [ ] Serialization
- [ ] gff_common

### util

- [x] ByteArray
- [x] Tokenizer - unneeded
- [x] base64 - unneeded
- [ ] compression
- [x] enum_flags - unneeded
- [x] game_install
- [x] macros - unneeded
- [ ] platform
- [x] scope_exit - unneeded
- [ ] string - unneeded
- [x] templates - unneeded

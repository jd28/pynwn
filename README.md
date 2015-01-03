PyNWN
=====

Neverwinter Nights 1/2 file formats Python library.

The following library combines Jordan McCoy's GFF File Format
Reader/Writer and a port of a large part of Elven's
[nwn-lib](https://github.com/niv/nwn-lib) into Python 3.

## Status
Alpha - Some documentation is out of date...

## File Formats
* GFF files: BIC, UTI, UTC, et al.
* ERF files: HAK, MOD, ERF
* TLK
* 2DA
* Meaglyn's [TLS format](http://neverwintervault.org/project/nwn1/other/tool/meaglyns-nwn-tlk-compiler) (Basically...)

## Objects
All NWN1 GFF types have classes that provide an abstracted interface
to the underlying GFF structure.  This is more pleasant to work with
and they unify particular things.  E.g, one doesn't have to concern
themselves with the fact that some resrefs are stored in "ResRef" and
others in "TemplateResRef" fields.

Any modifications to objects are automatically 'staged', that is their
(or in the case of instances their parent's) GFF structure is add to a
list in their respective containers and will all be saved when the
container is saved.  This is true even of DirectoryContainers: no
modifications will automatically be written to disk.

## License
All code is licensed under the terms specified by the original
authors.  All code written by me is under the same license as the
nwn-lib license (MIT).  I will add licenses info to each file.

# melplot

_Plot melodeon[^dba] layout diagrams_

[![Version on PyPI](https://img.shields.io/pypi/v/melplot.svg)](https://pypi.org/project/melplot/)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

<img src="https://user-images.githubusercontent.com/15079414/170375705-f7c56244-2f58-4237-8f70-1562df22206e.png"
     alt="Standard 2-row, 21-key D/G layout"
     width="667"
     >

## Notes

### Inspiration

- standard 21-key D/G with acc. notes highlighted and piano-key octave numbers marked:
  <http://forum.melodeon.net/files/site/keyboards/2%20Row%20-%20D_G%20-%20with%20accidentals.jpg>
- standard 21-key D/G with notes on stave, from [Mel Forum](http://forum.melodeon.net):
  <http://forum.melodeon.net/files/site/DGwithStave.pdf>
- as above, with ABC notation labels added, from [Daddy Long Les](https://www.daddylongles.com/dg-melodeon-resources):
  <https://www.daddylongles.com/_files/ugd/2a4ead_6501161c36fa470fbb1f64d24261ad9d.pdf>
- Dipper blank 30-key Anglo concertina scheme, with push/pull "pills" and piano keyboard with octaves highlighted:
  <http://www.johndipper.co.uk/downloads/blank-scheme.pdf>
- 20-key Anglo concertina with fancy buttons and octaves notated, [from concertina.com](http://www.concertina.com/fingering/index.htm):
  <http://www.concertina.com/fingering/images/anglo20-W1000H300.gif>
- Rick Mohr's layout, described [here](http://rickmohr.net/music/melodeon.asp), simple and clean, effective use of colors:
  <http://rickmohr.net/music/3row.pdf>
- standard 12-key G/C with notes on stave, fixed solfège, and octave numbers, from Mel Forum:
  <http://forum.melodeon.net/files/site/keyboards/GC_with_accidentals_showing_notes_on_stave.pdf>
- 3-row D/G/acc with fixed solfège coloring treble buttons by octave, by Bob Ellis:
  <http://forum.melodeon.net/files/site/Ellis3row.pdf>

### TODO

_and ideas_

- [x] basic diagram using mpl
- [ ] different ways to indicate octaves (e.g. color; piano key notation or wrt. root)
- [ ] different options for pitch labels (ABC, piano key notation, scale degrees)
- [ ] plotting notes on stave
- [x] CLI
- [x] first PyPI release
- [ ] HTML/CSS output option
- [ ] fancier button style option (some 3-D-ness)
- [ ] draw connections in bellows direction for consecutive notes or chord
- [ ] docs build with layout library

### Input format

ASCII representation of the layout.

Ideas:

- notes in ABC notation, push/pull separated by `/` or `|`, push/pull pairs separated by whitespace
- for each row, specify horizontal offset in the layout (zero implicit; e.g. 0.5 for the second row in a typical 11/10 layout)
  - maybe like `x0.5` instead of just `0.5`, to emphasize just space
- bass chords also in ABC notation, but maybe also support the common `+`/`-`?

### Layout sources

- [Mel Forum 2-row](http://forum.melodeon.net/index.php/page,keyboard_2_row.html)
- [Mel Forum 2.5-row](http://forum.melodeon.net/index.php/page,keyboard_25_row.html)
- [Mel Forum 3-row](http://forum.melodeon.net/index.php/page,keyboard_3_row.html)
- [bass layouts from Squeezehead](http://squeezehead.com/keyboard-layouts/basses/LAYOUTS.html)
- [various layouts and notes from Orest](http://www.geocities.ws/kozulich/layouts.html) [^pop]

[^dba]: [Diatonic button accordion](https://en.wikipedia.org/wiki/Diatonic_button_accordion) (DBA) / melodeon / "box" / accordéon diatonique / diato / etc. Also may later extend to plotting the layouts of other button accordion family instruments like concertinas.
[^pop]: Be careful opening this link on mobile browsers, I've gotten annoying / potentially dangerous pop-ups.

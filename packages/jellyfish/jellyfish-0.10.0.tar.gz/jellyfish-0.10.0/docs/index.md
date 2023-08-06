# Overview

**jellyfish** is a library for approximate & phonetic matching of strings.

Source: [https://github.com/jamesturk/jellyfish](https://github.com/jamesturk/jellyfish)

Documentation: [https://jamesturk.github.io/jellyfish/](https://jamesturk.github.io/jellyfish/)

Issues: [https://github.com/jamesturk/jellyfish/issues](https://github.com/jamesturk/jellyfish/issues)

[![PyPI badge](https://badge.fury.io/py/jellyfish.svg)](https://badge.fury.io/py/jellyfish)
[![Test badge](https://github.com/jamesturk/jellyfish/workflows/Python%20package/badge.svg)](https://github.com/jamesturk/jellyfish/actions?query=workflow%3A%22Python+package)
[![Coveralls](https://coveralls.io/repos/jamesturk/jellyfish/badge.png?branch=master)](https://coveralls.io/r/jamesturk/jellyfish)


## Included Algorithms

String comparison:

* Levenshtein Distance
* Damerau-Levenshtein Distance
* Jaro Distance
* Jaro-Winkler Distance
* Match Rating Approach Comparison
* Hamming Distance

Phonetic encoding:

* American Soundex
* Metaphone
* NYSIIS (New York State Identification and Intelligence System)
* Match Rating Codex

## Implementations

Each algorithm has C and Python implementations.

On a typical CPython install the C implementation will be used. The Python versions
are available for PyPy and systems where compiling the CPython extension is not
possible.

To explicitly use a specific implementation, refer to the appropriate module::

``` python
  import jellyfish._jellyfish as pyjellyfish
  import jellyfish.cjellyfish as cjellyfish
```

If you've already imported jellyfish and are not sure what implementation you
are using, you can check by querying `jellyfish.library`.

``` python
  if jellyfish.library == 'Python':
      # Python implementation
  elif jellyfish.library == 'C':
      # C implementation
```

## Example Usage

``` python
>>> import jellyfish
>>> jellyfish.levenshtein_distance(u'jellyfish', u'smellyfish')
2
>>> jellyfish.jaro_distance(u'jellyfish', u'smellyfish')
0.89629629629629637
>>> jellyfish.damerau_levenshtein_distance(u'jellyfish', u'jellyfihs')
1

>>> jellyfish.metaphone(u'Jellyfish')
'JLFX'
>>> jellyfish.soundex(u'Jellyfish')
'J412'
>>> jellyfish.nysiis(u'Jellyfish')
'JALYF'
>>> jellyfish.match_rating_codex(u'Jellyfish')
'JLLFSH'
```

# Usage

## Theory

This lib will try to extract normalized changes from a given raw history.

_It's up to the user to provide this merged history._

To realize this job, parsing is done in two rounds:

- first round extrats formal changes messages: e.g.: `<change_type>(<change_target>): <change_message>`
- secound round extracts lines from remaining ones, based on keywords dictionnaries

/// warning | searching policy
When formal search (1), _lines must contain at least 2 words_
When keywords search (2), _lines must contain at least 3 words_
///

/// note | ignored lines
lines with comment tags are ignored:

- `[0..N space]//`
- `[0..N space]#`
///

## Installation

From pypi repository (prefered):

    python -m pip install pychangelogfactory
    
From downloaded .whl file:

    python -m pip install pychangelogfactory-<VERSION>-py3-none-any.whl
    
From master git repository:

    python -m pip install git+https://chacha.ddns.net/gitea/chacha/pychangelogfactory.git@master


## Use in your project

### Sample code
``` py
from pychangelogfactory import ChangeLogFormater

raw_changelog='''
feat: add a nice feature to the project
style: reindent the full Foo class
security: fix a security leak on the Foo2 component
'''
ChangeLogFormater.FactoryProcessFullChangelog(raw_changelog)
changelog = ChangeLogFormater.RenderFullChangelog()
print(changelog)
```
### Output(Raw)

    #### Features      :sparkles::
    > add a nice feature to the project
    #### Security :shield::
    > fix a security leak on the Foo2 component
    #### Style :art::
    > reindent the full Foo class
    
### Output (rendered)
#### Features      :sparkles::
> add a nice feature to the project
#### Security :shield::
> fix a security leak on the Foo2 component
#### Style :art::
> reindent the full Foo class
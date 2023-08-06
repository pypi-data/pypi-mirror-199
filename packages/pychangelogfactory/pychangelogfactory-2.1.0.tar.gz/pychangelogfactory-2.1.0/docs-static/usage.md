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
from pychangelogfactory import ChangelogFactory

raw_changelog = (
    "feat: add a nice feature to the project\n"
    "style: reindent the full Foo class\n"
    "security: fix a security issue on the Foo2 component\n"
    "security: fix another security problem on the Foo2 component\n"
    "improve core performances by reducing complexity\n"
    "some random changes in the text content\n"
)
hdlr = ChangelogFactory()
hdlr.ProcessFullChangelog(self.raw_changelog)
changelog = hdlr.RenderFullChangelog()
print(changelog)
```

#### Or shorted version:

``` py
hdlr = ChangelogFactory(self.raw_changelog)
changelog = hdlr.RenderFullChangelog()
```
#### Or one-liner version:

``` py
changelog = ChangelogFactory(self.raw_changelog).RenderFullChangelog()
```

### Output(Raw)

    #### Features      :sparkles: :
    > add a nice feature to the project
    #### Security :shield: :
    > security: fix a security issue on the Foo2 component
    > security: fix another security problem on the Foo2 component
    #### Performance Enhancements :rocket: :
    > improve core performances by reducing complexity
    #### Style :art: :
    > reindent the full Foo class
    
### Output (rendered)
#### Features      :sparkles: :
> add a nice feature to the project
#### Security :shield: :
> security: fix a security issue on the Foo2 component

> security: fix another security problem on the Foo2 component
#### Performance Enhancements :rocket: :
> improve core performances by reducing complexity
#### Style :art: :
> reindent the full Foo class

### Options
#### Display unknown messages types
``` py
from pychangelogfactory import ChangelogFormater

raw_changelog = (
    "feat: add a nice feature to the project\n"
    "style: reindent the full Foo class\n"
    "security: fix a security issue on the Foo2 component\n"
    "security: fix another security problem on the Foo2 component\n"
    "improve core performances by reducing complexity\n"
    "some random changes in the text content\n"
)
changelog = ChangelogFactory(self.raw_changelog).RenderFullChangelog(include_unknown=True)
print(changelog)
```
### Output (rendered)
#### Features      :sparkles::
> add a nice feature to the project
#### Security :shield::
> fix a security issue on the Foo2 component
> fix another security problem on the Foo2 component
#### Performance Enhancements :rocket::
> improve core performances by reducing complexity
#### Style :art::
> reindent the full Foo class
#### Others :question::
> some random changes in the text content

## Supported types

| Type/Tag  | Priority | Keywords                               | Title                                                 | Class Name                    |
|-----------|----------|----------------------------------------|-------------------------------------------------------|-------------------------------|
| break     | 20       | break                                  | :rotating_light: Breaking changes :rotating_light: :  | `ChangelogFormater_break`     |
| feat      | 20       | feat, new, create, add                 | Features      :sparkles: :                            | `ChangelogFormater_feat`      |
| fix       | 0        | fix, issue, problem                    | Fixes :wrench: :                                      | `ChangelogFormater_fix`       |
| security  | 20       | safe, leak                             | Security :shield: :                                   | `ChangelogFormater_security`  |
| chore     | 10       | task, refactor, build, better, improve | Chore :building_construction: :                       | `ChangelogFormater_chore`     |
| perf      | 15       | fast, perf                             | Performance Enhancements :rocket: :                   | `ChangelogFormater_perf`      |
| wip       | 0        | temp                                   | Work in progress changes :construction: :             | `ChangelogFormater_wip`       |
| doc       | 0        | doc, manual                            | Documentations :book: :                               | `ChangelogFormater_wip`       |
| style     | 5        | beautify                               | Style :art: :                                         | `ChangelogFormater_style`     |
| refactor  | 0        |                                        | Refactorings :recycle: :                              | `ChangelogFormater_refactor`  |
| ci        | 0        | jenkins, git                           | Continuous Integration :cyclone: :                    | `ChangelogFormater_ci`        |
| test      | -5       | unittest, check, testing               | Testings :vertical_traffic_light: :                   | `ChangelogFormater_test`      |
| build     | 0        | compile, version                       | Builds :package: :                                    | `ChangelogFormater_build`     |
| revert    | 0        | revert, fallback                       | Reverts :back: :                                      | `ChangelogFormater_revert`    |
| other     | -20      |                                        | Others :question: :                                   | `ChangelogFormater_others`    |

## Add new types

New formaters can be easily added by subclassing `ChangelogFormater`:

### Inject custom formater locally (prefered way)

``` py
from pychangelogfactory import ChangelogFormater,ChangelogFactory

class ChangelogFormater_others(ChangelogFormater):
    """My formater"""

    prefix: str = "mytag"
    title: str = "My Title :"
    keywords: list[str] = ["foo","42"]
    priority: int = 10

hdlr = ChangelogFactory()
hdlr.RegisterFormater(ChangelogFormater_others)
...
```

### Inject custom formater module-wide

``` py
from pychangelogfactory import ChangelogFormater,ChangelogFormaterRecordType

@ChangelogFormaterRecordType
class ChangelogFormater_others(ChangelogFormater):
    """My formater"""

    prefix: str = "mytag"
    title: str = "My Title :"
    keywords: list[str] = ["foo","42"]
    priority: int = 10

hdlr = ChangelogFactory()
...
```

/// note | Scope
This will register your new formater for all next new factories, maybe not only in your own code !
///
### Test

``` py
raw_changelog = ("mytag: add a nice feature to the project\n" 
                 "foo modification in my file\n" 
                 "need 42 coffee\n"
                )
hdlr = ChangelogFactory(raw_changelog)
changelog = hdlr.RenderFullChangelog(include_unknown=True)
print(changelog)
```

### Output
#### My Title :
> add a nice feature to the project

> foo modification in my file

> need 42 coffee


### Revert changes
#### Reset to original list class-wise (all modules):
``` py
ChangelogFactory.ResetBaseFormaterList()
...
```
#### Reset to original list instance-wise:
``` py
hdlr = ChangelogFactory()
hdlr.ResetFormaterList()
...
```
#### Removing a specific formater:
``` py
hdlr = ChangelogFactory()
hdlr.unRegisterFormater(ChangelogFormater_others)
...
```
/// warning
There is no way to remove a specific formater class-wise (all modules) except using ResetFormaterList().
///

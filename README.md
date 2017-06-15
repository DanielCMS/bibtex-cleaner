# bibtex-cleaner
This tool processes bibtex items to remove duplications and mark suspicious items. It originates from the refurbishment project of Netlab website (http://netlab.caltech.edu), where we need to clean up a large collection of publications from the group members.

### How does it work
It basically runs two steps. First, it matches a set of pre-defined rules against the input items, and mark the ones that fail to pass all rules. Second, it searches duplications among the list based on their title. Several operation modes are available. After the clean up, both retained and dumped items are written to the output folder.

### Installation
* `sudo pip install -r requirements.txt`
* `sudo pip install -r requirements-test.txt`

The second command is necessary only if you want to run tests.

### Run
* `bin/run`

### Test
* `py.test`

### Config
In the config folder, you can specify the mode how the cleaner works. There are two fields:

`filterMode`, which determines how suspicious items are removed:
* `harsh`: Items that violate any rule will be brutally removed
* `casual`: Items that are usually fine will be retained
* `careful`: Items that are usually fine will be retained. Removal of other items would be based on user interactive input
* `manual`: All item removal would be based on user interactive input
`duplicationResolveMode`, which determines how duplicate items are resolved:
* `primal`: Items are chosen based on the order of: journal > conference > axiv > others
* `first`: The first item among duplications would be chosen
* `manual`: Duplication will be resolved based on user input

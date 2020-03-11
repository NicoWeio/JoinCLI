# CLI for joaomgcd's **[Join](https://joaoapps.com/join/)**

## Requirements
- This script uses *Python 3* and needs the *requests* library in order to transfer files.

## Install
- Copy or move the main.py file to **/usr/local/bin** and rename it to e.g. **join-cli**.
- Run `join-cli setup`. It will ask you to go to [this page](https://joinjoaomgcd.appspot.com/) to obtain an API key.

## Examples
- `join-cli push -d Redmi -f test.txt` pushes your file *test.txt* to a device whose name matches "Redmi". Note that [0x0.st](https://0x0.st/) is used to transfer files.
- `join-cli push -d Redmi Mint --clipboard "Hello World!"` will set the clipboard and/or write *Hello World!* on my *Redmi Note 8 Pro* and *Linux Mint* devices.
- `join-cli push -d Mint -u "https://nicolaiweitkemper.de/"` opens that URL on the specified device.

## Notes
- Your API key and settings are stored in **.join-cli-config.json** in your home folder.

## Contributing
PRs are always welcome. I developed this script to be useful, not to be feature-complete, so there are many things that could be improved.

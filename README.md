# CLI for joaomgcd's **[Join](https://joaoapps.com/join/)**

## Requirements

-   This script uses _Python 3_ and needs the _requests_ library in order to transfer files.

## Install

-   a)
    -   Download the **main.py** file from this repository.
    -   Copy or move the **main.py** file to **/usr/local/bin** and rename it to e.g. **join-cli**.
-   b)
    -   If you run Debian, Ubuntu, Linux Mint or something similar, you can install [the provided _.deb_ file](https://github.com/NicoWeio/JoinCLI/releases)
-   Run `join-cli setup`. It will ask you to go to [this page](https://joinjoaomgcd.appspot.com/) to obtain an API key.

## Examples

-   `join-cli push -d Redmi -f test.txt` pushes your file _test.txt_ to a device whose name matches "Redmi". Note that [0x0.st](https://0x0.st/) is used to transfer files.
-   `join-cli push -d Redmi Mint --clipboard "Hello World!"` will set the clipboard and/or write _Hello World!_ on my _Redmi Note 8 Pro_ and _Linux Mint_ devices.
-   `join-cli push -d Mint -u "https://nicolaiweitkemper.de/"` opens that URL on the specified device.

## Notes

-   Your API key and settings are stored in **.join-cli-config.json** in your home folder.

## Contributing

PRs are always welcome. I developed this script to be useful, not to be feature-complete, so there are many things that could be improved.

# Epistle

Take miscellaneous notes using vim. Save them in a private (or public) gist.

## Requirements

Git, Python, Vim

## Installation

Clone this repo.

Run `setup.py`. This will 

  - create a directory in `~/.epistles` 
  - create the config file `~/.epistles/epistle.conf`
  - clone your repo (if present) into `~/.epistles/epistles`
  - symlink epistle.py into `/bin/epistle` 
  - `chmod +x /bin/epistle`

## Usage
  
Create a note: `$ epistle <name_of_note>`

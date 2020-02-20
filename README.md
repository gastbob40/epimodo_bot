# EpiModo

![Discord](https://img.shields.io/badge/Discord-project-brightgreen)
![python](https://img.shields.io/badge/Language-Python-blueviolet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

EpiModo is a discord bot for server moderation, and includes several points:
- Management of member Warns
- Management of member Mute
- Management of member Kicks
- Management of member Bans
- Management of clearing message
- All based on a configuration file and website API
- ...

EpiModo is a project by [gastbob40](https://github.com/gastbob40) with contributions from [Baptman21](https://github.com/bat021).

## Requirements

You will need all these elements for the proper working of the project.

- [Python 3](https://www.python.org/downloads/)
- [A Discord Bot Token](https://discordapp.com/developers/applications/)
- [A EpiModo WebSite Token](mailto:quentin.briolant@epita.fr?subject=[GitHub]%20Demande%20de%20Token)


## Getting started

1. **First, you will have to clone the project.**

```shell
git clone https://github.com/gastbob40/epimodo_bot
```

2. **Create a `virtual environment`, in order to install dependencies locally.** For more information about virtual environments, [click here](https://docs.python.org/3/library/venv.html).

```shell
python -m venv .venv
```

3. **Activate the virtual environment**

Linux/macOS:

```shell
# Using bash/zsh
source .venv/bin/activate
# Using fish
. .venv/bin/activate.fish
# Using csh/tcsh
source .venv/bin/activate.csh
``` 

Windows:

```
# cmd.exe
.venv\Scripts\activate.bat
# PowerShell
.venv\Scripts\Activate.ps1
```


4. **Finally, install the dependencies**

````shell
pip install -r requirements.txt
````

5. **Configure EpiModo**. This is necessary to use the bot. Check the next section for instructions.

6. **Run `python index.py` to launch EpiModo.** Also make sure that the venv is activated when you launch EpiModo (you should see `venv` to the left of your command prompt).

## Configuration

The `run/config` folder contains all the data of the program configuration.

### tokens.default.yml

This file contain all data about tokens. This file looks like this:
 
```yaml
discord_token: ~
epimodo_website_token: ~
```

You must fill in the file and rename it to `tokens.yml`

### permissions.default.yml

This file contain all data about permissions. This file looks like this:
 
```yaml
dev: ~
epilogin: ~
```

You must fill in the file and rename it to `permissions.yml`.

Warning, these two items are lists of Discord user IDs.

### newsgroups.yml

This file contains all the data concerning the the repost of EPITA news.

You can add new newsgroups and new channels.

For example:

```yaml
address: news.epita.fr # Address for news
encoding: utf-8 # The encoding to use. Always UTF-8 according to the nntp RFC.
delta_time: 60 # Time between news updates (in seconds)
groups: # List of groups
  assistants: # group name (not actually used)
    name: assistants.news # Name of the newsgroup
    last_update: "15/02/2020 00:00:00" # Time of the last update (to get just new news)
    channels:
      - 678944434242715648 # list of channel ids where to repost the news
```

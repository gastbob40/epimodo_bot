# EpiModo

![Discord](https://img.shields.io/badge/Discord-project-brightgreen)
![python](https://img.shields.io/badge/Language-Python-blueviolet)

## About

EpiModo is a discord bot for server moderation, and includes several points:
- Management of member Warns
- Management of member Mute
- Management of member Kicks
- Management of member Bans
- Management of clearing message
- All based on a configuration file and website API
- ...


## Requirements

You will need all these elements for the proper working of the project.

- [Python 3](https://www.python.org/downloads/)
- [A Discord Bot Token](https://discordapp.com/developers/applications/)
- [A EpiModo WebSite Token](mailto:quentin.briolant@epita.fr?subject=[GitHub]%20Demande%20de%20Token)


## How to install it ?

1. First, you will have to clone the project.

```shell
git clone https://github.com/gastbob40/epimodo_bot
```

2. Consider creating a `virtual environment`, in order to install dependencies locally.

```shell
python -m venv venv
```

3. You need to activate the virtual environment now

```shell
# If you are on Linux or Mac ?
source venv/bin/activate 

# If you are on Windows
./venv/Scripts/activate
``` 

4. Finally, install the dependencies

````shell
pip install -r requirements.txt
````


## How it works ?

The `run/config` folder contains all the data of the program configuration.

### tokens.default.yml

This file contain all data about tokens. This file looks like this:
 
```yaml
discord_token: ~
epimodo_website_token: ~
```

You should fill the file and rename it to `tokens.yml`

### permissions.default.yml

This file contain all data about permissions. This file looks like this:
 
```yaml
dev: ~
epilogin: ~
```

You should fill the file and rename it to `permissions.yml`.
Warning, these two items are lists of dicscord IDs.

### newsgroups.yml

This file contains all the data concerning the retransmission of EPITA news.
You can add new news and new channels.

For example:

```yaml
address: news.epita.fr # Address for news
encoding: utf-8 # 
delta_time: 60 # Time between news update
groups: # List of groups
  assistants: # group name (useless)
    name: assistants.news # Name of the news (in epita)
    last_update: "15/02/2020 00:00:00" # Time of the last update (to get just new news)
    channels:
      - 678944434242715648 # list of channel ids
```
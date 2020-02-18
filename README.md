# EpiModo

## About

EpiModo is a discord bot for server moderation, and includes several points:
- Management of member Warns
- Management of member Mute
- Management of member Kicks
- Management of member Bans
- Management of clearing message
- All based on a configuration file and website API
- ...

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
pip install requirements.txt
````


## How it works ?

The `run/config` folder contains all the data of the program configuration.

### tokens.default.yml

This folder contain all data about tokens. This file looks like this:
 
```yaml
discord_token: ~
epimodo_website_token: ~
```

You should fill the file and rename it to `tokens.yml`

### permissions.default.yml

This folder contain all data about permissions. This file looks like this:
 
```yaml
dev: ~
epilogin: ~
```

You should fill the file and rename it to `permissions.yml`.
Warning, these two items are lists of dicscord IDs.
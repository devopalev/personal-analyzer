# Personal Analyzer Bot


## Quick start
1. Rename the file `.env.example` to `.env` and write your bot token in it to the BOT_TOKEN variable (for example, 
BOT_TOKEN=your_token). 

#### Docker compose
2. Install docker-compose (see https://docs.docker.com/compose/install/linux/)
3. Run `docker-compose up`

#### Docker
2. Install docker (see https://docs.docker.com/engine/install/debian/)
3. Run `docker build -t personal-analyzer ./`
4. Run `docker run -d --env-file=./.env --name=personal-analyzer personal-analyzer`

#### Notes for run
* If you do not specify the variables `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc., then the application will use the 
default local sqlite3 database.
* It is recommended to change the variables `POSTGRES_USER` and `POSTGRES_PASSWORD` for 
the sake of increased security.

## Features
* Notify you when users join or exit the channel.
* Support for various languages.

## Support languages
There is an SQL dump in the `alembic/default_data/language_objects.sql`, you can add translations of messages in other 
languages to it. Alternatively, you can add message translations directly to the database. 

**Attention**! The text contains values in curly brackets, for example {title}, do not change them in any case.

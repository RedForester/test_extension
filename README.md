# RedForester simple extension

Quick start to develop [RedForester](https://redforester.com/en/main-page/) extensions

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/RedForester/test-extension)

## Features

 - One-click deploy with [Heroku](https://heroku.com)
 - Simple registration and connection of the extension

## Setup

1. Clone repository
```bash
$ git clone https://github.com/RedForester/test-extension.git && cd test-extension
```
2. Edit `EXT_NAME`, `EXT_DESCRIPTION`, `EXT_EMAIL` and `USER_COOKIE` in `config.py`.
3. Deploy with [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
```bash
$ heroku login
$ heroku create # command return PROJECT_NAME_IN_HEROKU and urls
# or heroku git:remote -a PROJECT_NAME_IN_HEROKU if app already exist
$ heroku labs:enable runtime-dyno-metadata -a PROJECT_NAME_IN_HEROKU
$ git push heroku master
```
4. Update `EXT_BASE_URL` in `config.py`. For example `https://PROJECT_NAME_IN_HEROKU.herokuapp.com` or your public ip/domain.
5. Register extension in RedForester
```bash
$ python register_extension.py
```

# Twitter Archiver 🐋
Archive twitter posts for analytical purpos and further usage.

## Functionality:
- SQLite database
- Completely customizable
- Cross-plattform (linux & windows tested)
- Runs as crontab
- Emoji support 😍!

## Install
Please consider using Python3, it was built and tested with it.<br>
If you haven't installed it already, head over to [python.org](https://www.python.org/) and get the newest version of Python3 for your system.<br><br>
When python is installed, make sure to get the packages from the [requirements.txt](https://github.com/mikeunge/twitter-archiver/blob/master/requirements.txt) file.<br>
> $ pip install -r requirements.txt <br>
> or <br>
> $ pip3 install -r requirements.txt

## Usage
Before you can actually run the script, go into the /config path and edit the [twitter.conf](https://github.com/mikeunge/twitter-archiver/blob/master/config/twitter.conf) file.<br>

1. Add your twitter API keys
2. Change the username you want to query
3. Set a maximum of tweets to fetch (200 is the limit!)
4. (if needed) change the names/paths in the [DEFAULT] section as you like
5. You are set and ready to go!

To get your twitter API keys, go to [dev.twitter.com](https://developer.twitter.com/en/apps) and create a new app. Just follow the steps and you'll get them.<br><br>

## Todo
- [✔️] ~~change paths from dynamic to static~~
    - ~~database path (data/database.db)~~
    - ~~log path (var/log/twitter_bot.log)~~
- [✔️] ~~log folder & file checks~~
- [✔️] ~~add banner / logo~~
- [❌] better texts (log & output)
- [❌] outsource the credentials
- [❌] handle multiple configuration files
- [❌] filter (@) replys and store them into another table
- [❌] add an update function and routine
- [✔️] ~~handle twitter_auth exception~~
- [❌] add new table 'added_to_db' with a timestamp to db
- [❌] change the version/build in config if not the same version
- [❌] create [Documentations](https://github.com/mikeunge/twitter-archiver/tree/master/docs) for setting up and maintaining crontab

## Contribute
For feature requests or bug reports, use [Github Issues](https://github.com/mikeunge/twitter-archiver/issues).

## License
MIT License, see [LICENSE.txt](https://github.com/mikeunge/twitter-archiver/blob/master/LICENSE.txt)

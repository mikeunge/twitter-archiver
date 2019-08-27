#!/bin/python3 *
# -*- coding: utf-8 -*-
import os, sys, platform, logging
import tweepy, sqlite3, configparser

# create global vars..
logger, logging_enabled, logging_path, configpath, os_system = "", "", "", "", ""

# define the version and build
VERSION = "0.5"
BUILD = "0.5.2"
BUILD_STATE = "nightly"

# check for the BUILD_STATE and then change the BUILD_ICON
if (BUILD_STATE == "nightly"):
    BUILD_ICON = '🌑'
elif (BUILD_STATE == "stable"):
    BUILD_ICON = '🌱'
else:
    BUILD_ICON = '🔥'

class Database:
    def create(file, path):
        database_path = App.fixPath(path, file)
        App.writeLog("DEBUG", "Database: " + str(database_path))
        # check if the database exists and if I can connect to it
        if (App.checkFolder(path, True) == True):
            try:
                if (App.checkFile(database_path) == False):
                    App.writeLog("INFO", "Database doesn't exist.. creating new one.")
                    App.printOut("❌   database doesn't exist..\n⭕   trying to create it..")
                conn = sqlite3.connect(database_path)
            except Exception as ex:
                err_msg = "❌   I could't connect to the database, sorry.. please try run again..\n" + str(ex)
                App.writeLog("ERROR", "Couldn't create database file.Error: " + str(ex))
                return err_msg
            # create the cursor
            cur = conn.cursor()
            # create the table if it doesn't exist
            cur.execute("CREATE TABLE IF NOT EXISTS tweet (twitter_id INTEGER, text TEXT, screen_name TEXT, created_at DATE)")
            # commit changes to the db
            conn.commit()
            # close the db connection
            conn.close()
            App.printOut("✔   database connection success!")
            App.writeLog("INFO", "database connection success!")
            return True
        else:
            # database path couldn't be created..
            err_msg = "❌   couldn't create database path.. please check your permissions.."
            return err_msg


    def insertData(self, data, verify):
        # recieve a tweet and write it to the db
        conn = sqlite3.connect(self)
        cur = conn.cursor()
        App.writeLog("DEBUG", "Database connection established..")
        
        # replie filter goes here, before the verification..
        if (verify == True):
            if (Database.verifyData(self, data) == True):
                # execute the sql statement..
                cur.execute("INSERT INTO tweet VALUES (?,?,?,?)", data)
                # commit changes to db
                conn.commit()
                val = True
            else:
                val = False
        else:
            # execute the sql statement..
            cur.execute("INSERT INTO tweet VALUES (?,?,?,?)", data)
            # commit changes to db
            conn.commit()
            val = True
        conn.close()
        return val


    # add a new parameter (replie), so the query can switch and filter both tables ;)
    def verifyData(self, data):
        # function for verifying the tweet, checking if the tweet already exists..
        # accepts self => database_path, data => data to be verified
        # returns a bool // true, false
        conn = sqlite3.connect(self)
        cur = conn.cursor()
        # fetch all the existing twitter_id's
        cur.execute("SELECT twitter_id FROM tweet WHERE twitter_id=?", (data[0],))
        output = cur.fetchone()
        conn.close()
        # check if the output is 'None'
        # this happens if the DB is new without any entries
        if (output == None):
            return True
        else:
            # iterate the list and probe if the 'twitter_id' doesn't exist
            for out in output:
                if (out != data[0]):
                    return True
                else:
                    return False


    # under construction!
    # will implement later, but I need to change the whole sql part before that..
    def filterReplies(self):
        # get rid of those nasty replies
        # thanks to pythons built-in functions ^^
        if (self.startswith('@')):
            return True
        else:
            return False


class Twitter:
    # authenticatethe bot
    def authenticate(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
        try:
            # OAuth authentication
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
            # login and bind the otput to a variable
            api = tweepy.API(auth)
            App.printOut("✔   successfully connected with the twitter_api..")
            App.writeLog("INFO", "Successfully connected with the twitter_api..")
            # return the api so it can be used somewhere else
            return api
        except Exception as ex:
            # if the API tokens aren't correct, this error occurs
            App.printOut("\nerror message:\n❌  couldn't connect to the twitter API..")
            App.writeLog("CRITICAL", "Could not connect to the twitter API, please check your CONSUMER and ACCESS keys!")
            sys.exit(1)


    # get all the user info
    def get_tweets(self, username, max_tweets):
        # define the number of tweets that should be fetched
        number_of_tweets = max_tweets
        App.writeLog("INFO", "Trying to gather " +str(max_tweets)+ " tweets..")
        App.printOut("⭕  trying to gather " +str(max_tweets)+ " tweets..")
        # here is where all tweets get fetched
        try:
            tweets  = self.user_timeline(screen_name=username, count=max_tweets)
            App.writeLog("INFO", "Successfully gathered all Tweets!")
            App.printOut("✔   success! we got all the tweets!")
            # return the array to the app
            return tweets
        except Exception as ex:
            # this (mostly) occurs because of an expired or invalid token.
            App.writeLog("CRITICAL", "Cannot retrieve tweets, probably are your tokens expired or invalid.")
            App.printOut("\nerror message:\n❌  unable to retrieve tweets, plese check if your tokens are right and not expired.")
            sys.exit(1)


class Config:
    # function for reading the configfile
    def get_config(self, parent, child):
        # set the configparser
        config = configparser.ConfigParser()
        # start and try to read the configfile
        try:
            config.read(self)
        except IOError as io:
            # if we cannot read the file, rais an IOError and end the bot..
            App.writeLog("FATAL", "Couldn't read/write configfile.. program error: " + str(io))
            App.printOut("❌   couldn't read/write to configfile..")
            sys.exit(1)
        else:
            # store the values in a variable and return the requested string
            request = config[parent][child]
            return request


class App:
    # global logger function!
    def log(self, file, path):
        file_path = App.fixPath(path, file)

        if (App.checkFolder(path, True) == True):
            if (App.checkFile(file_path) == False):
                App.printOut("❌   logfile doesn't exist.. trying to create it..")
            try:
                LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
                # setting the right logging level (global)
                if self == "DEBUG":
                    logging.basicConfig(filename=file_path, level=logging.DEBUG, format=LOG_FORMAT)
                if self == "INFO":
                    logging.basicConfig(filename=file_path, level=logging.INFO, format=LOG_FORMAT)
                if self == "ERROR":
                    logging.basicConfig(filename=file_path, level=logging.ERROR, format=LOG_FORMAT)
                if self == "CRITICAL":
                    logging.basicConfig(filename=file_path, level=logging.CRITICAL, format=LOG_FORMAT)
                if self == "WARNING":
                    logging.basicConfig(filename=file_path, level=logging.WARNING, format=LOG_FORMAT)
                if self == "FATAL":
                    logging.basicConfig(filename=file_path, level=logging.FATAL, format=LOG_FORMAT)
                logger = logging.getLogger()
                return True
            except IOError as io:
                err_msg = "❌   I'm sorry to tell you, but I'm not allowed to read/write to the logging file. Please check the permission or if the file is already open.\n" + str(io)
                return err_msg
            except Exception as ex:
                err_msg = "❌   something didn't work out.. I'm sorry but this error shouldn't happen, please try and run again..\n" + str(ex)
                return err_msg
        else:
            err_msg = "❌   couldn't create the log file.."
            return err_msg


    def writeLog(self, message):
        # it's easier to write logs with a function than checking everythime if logging is enabled and so..
        if logging_enabled == True:
            # lower the string!!
            # check every available logging function..
            if (self == "INFO"):
                logger.info(message)
            elif (self == "DEBUG"):
                logger.debug(message)
            elif (self == "ERROR"):
                logger.error(message)
            elif (self == "CRITICAL"):
                logger.critical(message)
            elif (self == "WARNING"):
                logger.warning(message)
            elif (self == "FATAL"):
                logger.fatal(message)
            else:
                # if nothing fits, it's a debgu. period.
                logger.debug(self)


    def printOut(self):
        # little function for checking if console output is allowed or not
        if (print_data == True) or (print_data == "True"):
            print(self)


    def checkFile(self):
        # check if the requested file exists
        if os.path.exists(self):
            App.writeLog("DEBUG", "[checkFile] - file: " +str(self)+ " exists!")
            return True
        else:
            App.writeLog("ERROR", "[checkFile] - file: " +str(self)+ " doesn't exist!")
            return False


    def fixPath(path, file):
        # check the os and fix the path
        if (os_system == "Windows"):
            fixed_path = path + "\\" + file
        else:
            # linux and macos support
            fixed_path = path + "/" + file
        return fixed_path



    def checkFolder(self, create):
        # check if the folder exists..
        if not os.path.exists(self):
            # create the path..
            if (create == True):
                try:
                    os.mkdir(self)
                    App.printOut("✔   folder ("+ self +") successfully created..")
                    App.writeLog("INFO", "Folder ("+ self +") successfully created.")
                    return True
                except Exception as ex:
                    App.printOut("❌    couldn't create the folder ("+ self +")..")
                    App.writeLog("ERROR", "Folder ("+ self +") couldn't be created.")
                    return False
            else:
                App.writeLog("ERROR", "Folder ("+ self +") couldn't be created. Permission not set in function!")
                return False
        else:
            App.printOut("✔   folder ("+ self +") exists..")
            App.writeLog("INFO", "Folder ("+ self +") already exists.")
            return True

    
    def banner():
        # create the banner and gather information
        bnr = "       .-' \n"
        bnr +="  '--./ /     _.---.  \n"
        bnr +="  '-,  (__..-`       \      twitter-archiver 🐋\n"
        bnr +="     \          .     |     version: "+str(VERSION)+" ~"+str(BUILD_STATE)+" "+str(BUILD_ICON)+" \n"
        bnr +="      `,.__.   ,__.--/      made with ❤️  by mikeunge \n"
        bnr +="        '._/_.'___.-`  \n"
        App.printOut(bnr)


    def app():
        # set (global-) config path
        configpath = App.fixPath(os.path.dirname(os.path.abspath(__file__))+"/config", "twitter.conf")
        # get the operating system
        system = platform.system()

        # check if the messages should be printed
        global print_data
        print_data = Config.get_config(configpath, "DEFAULT", "print_data")
        # convert the input..
        if (print_data == "True"):
            print_data = True
        else:
            print_data = False

        # twitter-archivers banner
        App.banner()

        # check if the logger is enabled..
        logging_enabled = Config.get_config(configpath, "DEFAULT", "logging")
        if (logging_enabled == "True"):
            # change the type (string -> bool), it's easier to re-check in other functions..
            logging_enabled = True
            # get the logging_level
            log_level = Config.get_config(configpath, "DEFAULT", "logging_level")
            log_level.upper()
            
            # get the logging information (name, path)
            log_file = Config.get_config(configpath, "DEFAULT", "logging_name")
            log_path = Config.get_config(configpath, "DEFAULT", "logging_path")

            # start the logger
            setup_logger = App.log(log_level, log_file, log_path)
            if (setup_logger == True):
                App.printOut("✔   logger ["+ log_level +"] is up and running..")
                App.writeLog("INFO", "Logger ["+ log_level +"] is up and running.")
            else:
                App.printOut("❌   sorry to say, but something is broken..\n\nThe error message:\n" + str(setup_logger))
                sys.exit(1)
        else:
            # if logging is disabled, let the user know about it!
            App.printOut("❌  logging is disabled!")

        # load the database name and it's path..
        # create variables and create the full path ;)
        db_path = Config.get_config(configpath, "DEFAULT", "database_path")
        database_path = App.fixPath(os.path.dirname(os.path.abspath(__file__)), db_path)
        database = Config.get_config(configpath, "DEFAULT", "database")

        # check if the data needs to be verified..
        verfiy_data = Config.get_config(configpath, "DEFAULT", "verify_data")
        # convert the input from string to bool..
        if (verfiy_data == "True"):
            verfiy_data = True
        else:
            verfiy_data = False
            App.printOut("❌   Data verification is disabled!")
        App.writeLog("DEBUG", "Verify Data: " +str(verfiy_data))        

        # get and define the API keys
        CONSUMER_KEY = Config.get_config(configpath, "TWITTER", "CONSUMER_KEY")
        CONSUMER_SECRET = Config.get_config(configpath, "TWITTER", "CONSUMER_SECRET")
        ACCESS_TOKEN = Config.get_config(configpath, "TWITTER", "ACCESS_TOKEN")
        ACCESS_SECRET = Config.get_config(configpath, "TWITTER", "ACCESS_SECRET")
        # specify the username I want to fetch
        username = Config.get_config(configpath, "TWITTER", "USERNAME")
        # specify the number of tweets that should get extracted (Note: 200 is the maximum that can be extrated, API limitation)
        max_tweets = Config.get_config(configpath, "TWITTER", "MAX_TWEETS")

        # authenticate the bot and get it running
        api = Twitter.authenticate(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

        # get the tweets
        tweets = Twitter.get_tweets(api, username, max_tweets)

        # create the database
        create_db = Database.create(database, database_path)
        # if something happened, write the error and exit
        if create_db != True:
            App.printOut(create_db)
            App.writeLog("ERROR", create_db)
            sys.exit(1)

        database_path = App.fixPath(database_path, database)
        i = 0            # get the total number of tweets
        success = 0     # only for different Foutput..
        App.printOut("👍   starting to insert..")
        App.writeLog("INFO", "Prepare for all the tweets {")
        for tweet in tweets:
            # get the tweet and extract the right data..
            i = i+1
            data = [tweet.id, tweet.text, tweet.user.screen_name, tweet.created_at]
            # insert the data..
            if (Database.insertData(database_path, data, verfiy_data) == True):
                # print the data (if debug..)
                success = success+1
                App.printOut("✔   success! we added '"+ str(data[1]) +"' to the database!")
                App.writeLog("INFO", "Success! We added '"+ str(data) +"' to the database.")
            else:
                App.printOut("😢   tweet already exists..")
                App.writeLog("INFO", "Tweet already exists! Data: " + str(data))
        if (success >= 1):
            App.printOut("✔   wuhu, we did it! all ["+ str(success) +"/"+ str(max_tweets) +"] tweets were saved.. 👍")
        else:
            App.printOut("❌   no tweets to save..")
        App.writeLog("INFO", "} End of the tweets.")
        App.writeLog("INFO", "Bot shut's down, bye!")
        App.printOut("👍   Bot shut's down, bye!")
        sys.exit(0)



if __name__ == "__main__":
    # start this baby ^^
    App.app()
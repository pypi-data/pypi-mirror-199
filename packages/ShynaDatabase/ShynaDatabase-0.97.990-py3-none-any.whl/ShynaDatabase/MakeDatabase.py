import mysql.connector
import os


class InsertDB:
    database_user = os.environ.get('user')
    default_database = ''
    host = os.environ.get('host')
    passwd = os.environ.get('passwd')
    query = ''

    def create_insert_update_or_delete(self):
        """ Insert value in database with no return."""
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(self.query)
            my_db.commit()
        except Exception as e:
            print(e)
        finally:
            my_db.close()


class MakeTables:
    s_data = InsertDB()
    # s_data.host = input("Enter the Host")
    # s_data.passwd = input("Enter the password")
    url_dict = {
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms": ["indiatimes", "top stories"],
        "https://timesofindia.indiatimes.com/rssfeeds/1221656.cms": ["indiatimes", "recent stories"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms": ["indiatimes", "india news"],
        "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms": ["indiatimes", "world news"],
        "https://timesofindia.indiatimes.com/rssfeeds/7098551.cms": ["indiatimes", "nri news"],
        "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms": ["indiatimes", "business news"],
        "https://timesofindia.indiatimes.com/rssfeeds_us/72258322.cms": ["indiatimes", "US news"],
        "https://timesofindia.indiatimes.com/rssfeeds/54829575.cms": ["indiatimes", "cricket news"],
        "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms": ["indiatimes", "sports news"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms": ["indiatimes", "science news"],
        "https://timesofindia.indiatimes.com/rssfeeds/2647163.cms": ["indiatimes", "environment news"],
        "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms": ["indiatimes", "gadgets news"],
        "https://timesofindia.indiatimes.com/rssfeeds/913168846.cms": ["indiatimes", "education news"],
        "https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms": ["indiatimes", "entertainment news"],
        "https://timesofindia.indiatimes.com/rssfeeds/2886704.cms": ["indiatimes", "lifestyle news"],
        "https://timesofindia.indiatimes.com/rssfeedmostread.cms": ["indiatimes", "most read"],
        "https://timesofindia.indiatimes.com/rssfeedmostcommented.cms": ["indiatimes", "most commented"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128838597.cms": ["indiatimes", "mumbai news"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128839596.cms": ["indiatimes", "delhi news"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms": ["indiatimes", "bangalore news"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128816011.cms": ["indiatimes", "hyderabad news"],
        "https://timesofindia.indiatimes.com/rssfeeds/6547154.cms": ["indiatimes", "gurugram news"],
        "https://timesofindia.indiatimes.com/rssfeeds/8021716.cms": ["indiatimes", "noida news"],
        "https://timesofindia.indiatimes.com/rssfeeds/-2128819658.cms": ["indiatimes", "lucknow news"],
        "https://zeenews.india.com/rss/india-national-news.xml": ["zeenews", "india national"],
        "https://zeenews.india.com/rss/world-news.xml": ["zeenews", "world news"],
        "https://zeenews.india.com/rss/india-news.xml": ["zeenews", "state news"],
        "https://zeenews.india.com/rss/asia-news.xml": ["zeenews", "south asia"]
    }

    def make_table(self):
        print("Working on Database, Please wait", self.s_data.host)
        self.s_data.default_database = os.environ.get("alarm_db")
        self.s_data.query = "CREATE TABLE `alarm` (  `count` int(11) NOT NULL AUTO_INCREMENT,  `task_date` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `task_time` varchar(45) COLLATE utf8_unicode_ci " \
                            "DEFAULT NULL,  `alarm_title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,  " \
                            "`alarm_date` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `alarm_time` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `snooze_status` varchar(45) COLLATE utf8_unicode_ci " \
                            "DEFAULT 'True',  `snooze_duration` varchar(45) COLLATE utf8_unicode_ci DEFAULT '15',  " \
                            "`repeat_status` varchar(45) COLLATE utf8_unicode_ci DEFAULT 'False',  `repeat_frequency` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT 'Never',  `alarm_status` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT 'True',  PRIMARY KEY (`count`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 " \
                            "COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "CREATE TABLE `greeting` (  `count` int(11) NOT NULL AUTO_INCREMENT,  `new_date` varchar(45)" \
                            " COLLATE utf8_unicode_ci DEFAULT NULL,  `new_time` varchar(45) COLLATE utf8_unicode_ci " \
                            "DEFAULT NULL,  `greet_string` varchar(255) COLLATE utf8_unicode_ci NOT NULL,  " \
                            "PRIMARY KEY (`count`)) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 " \
                            "COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.default_database = os.environ.get("status_db")
        self.s_data.query = "CREATE TABLE `connection_check` (  `count` int(11) NOT NULL AUTO_INCREMENT,  " \
                            "`connection_type` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `from_application` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `new_date` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `new_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT " \
                            "NULL,  PRIMARY KEY (`count`)) ENGINE=InnoDB AUTO_INCREMENT=497 DEFAULT CHARSET=utf8 " \
                            "COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "CREATE TABLE `last_run_check` (  `count` int(11) NOT NULL AUTO_INCREMENT,  `process_name` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `task_date` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `task_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL," \
                            "  `from_device` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  PRIMARY KEY (`count`), " \
                            " UNIQUE KEY `process_name_UNIQUE` (`process_name`)) ENGINE=InnoDB AUTO_INCREMENT=4 " \
                            "DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.default_database = os.environ.get("news_db")
        self.s_data.query = "CREATE TABLE `news_alert` (`count` int(11) NOT NULL AUTO_INCREMENT,`news_title` varchar(" \
                            "255) COLLATE utf8_unicode_ci DEFAULT NULL, `news_description` varchar(3600) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL, `news_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT " \
                            "NULL, `news_date` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`news_link` varchar(" \
                            "255) COLLATE utf8_unicode_ci DEFAULT NULL,`task_date` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,`task_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT " \
                            "NULL,`publish_date_time` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`categories` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`keyword_process` varchar(45) COLLATE " \
                            "utf8_unicode_ci NOT NULL DEFAULT 'False', PRIMARY KEY (`count`)) ENGINE=InnoDB " \
                            "AUTO_INCREMENT=2774 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci; "
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "CREATE TABLE `news_keyword` (`count` int(225) NOT NULL,`news_keyword` varchar(225) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,`repeat_count` varchar(225) COLLATE utf8_unicode_ci " \
                            "NOT NULL,`look_status` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`task_date` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`task_time` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,PRIMARY KEY (`count`),UNIQUE KEY `news_keyword_UNIQUE` (" \
                            "`news_keyword`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci; "
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "CREATE TABLE `news_url` ( `count` int(255) NOT NULL AUTO_INCREMENT,  `news_urls` " \
                            "varchar(200) COLLATE utf8_unicode_ci NOT NULL,  `host_name` varchar(20) COLLATE " \
                            "utf8_unicode_ci NOT NULL,  `category` varchar(20) COLLATE utf8_unicode_ci NOT NULL,  " \
                            "PRIMARY KEY (`count`),  UNIQUE KEY `news_urls` (`news_urls`)) " \
                            "ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        for key, value in self.url_dict.items():
            self.s_data.query = "INSERT INTO `news_url`(`news_urls`,`host_name`,`category`)" \
                                "VALUES('" + str(key) + "','" + str(value[0]) + "','" + str(value[1]) + "');"
            self.s_data.create_insert_update_or_delete()
        self.s_data.default_database = os.environ.get("location_db")
        self.s_data.query = "CREATE TABLE `shivam_device_location` (`count` int(11) NOT NULL AUTO_INCREMENT," \
                            "`new_date` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`new_time` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,`new_latitude` varchar(3000) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,`new_longitude` varchar(3000) COLLATE utf8_unicode_ci " \
                            "DEFAULT NULL,`new_altitude` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL," \
                            "`new_accuracy` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`new_vertical_accuracy` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`new_bearing` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,`new_speed` varchar(45) COLLATE utf8_unicode_ci DEFAULT " \
                            "NULL,`new_elapsedMS` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`new_provider` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,`shivam_distance_from_previous` " \
                            "varchar(45) COLLATE utf8_unicode_ci NOT NULL DEFAULT '0.0',`shivam_speed` varchar(45) " \
                            "COLLATE utf8_unicode_ci NOT NULL DEFAULT '0.0',PRIMARY KEY (`count`)) ENGINE=InnoDB " \
                            "AUTO_INCREMENT=514 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci; "
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "CREATE TABLE `shivam_standard_location_long_lat` (`count` int(11) NOT NULL " \
                            "AUTO_INCREMENT,`loc_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,`latitude` " \
                            "varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,`longitude` varchar(255) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,PRIMARY KEY (`count`),UNIQUE KEY `loc_name_UNIQUE` (" \
                            "`loc_name`),UNIQUE KEY `latitude_UNIQUE` (`latitude`), UNIQUE KEY `longitude_UNIQUE` (" \
                            "`longitude`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci; "
        self.s_data.create_insert_update_or_delete()
        self.s_data.default_database = os.environ.get("twelveam_db")
        self.s_data.query = "CREATE TABLE `weather_table` (`count` int(11) NOT NULL AUTO_INCREMENT,  `task_date` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `task_time` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `sunrise` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL," \
                            "  `sunset` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `weather_description` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `main_temp` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `main_feels_like` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `main_humidity` varchar(45) COLLATE utf8_unicode_ci " \
                            "DEFAULT NULL,  `wind_gust` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `wind_speed`" \
                            " varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `clouds` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `loc_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT " \
                            "NULL,  `speak_sentence` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `visibility` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `wind_direction` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `precipitation` varchar(45) COLLATE utf8_unicode_ci DEFAULT" \
                            " NULL,  `moonrise` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `moonset` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `last_update_date` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `last_update_time` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  PRIMARY KEY (`count`)) ENGINE=InnoDB DEFAULT " \
                            "CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.default_database = os.environ.get("taskmanager_db")
        self.s_data.query = "CREATE TABLE `Task_Manager` (  `count` int(11) NOT NULL AUTO_INCREMENT,  `new_date` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `new_time` varchar(45) COLLATE " \
                            "utf8_unicode_ci DEFAULT NULL,  `task_id` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL," \
                            "  `task_date` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `task_time` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `task_type` varchar(45) COLLATE utf8_unicode_ci" \
                            " DEFAULT NULL,  `Speak` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `snooze_status`" \
                            " varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `snooze_duration` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `task_status` varchar(45) COLLATE utf8_unicode_ci " \
                            "DEFAULT NULL,  PRIMARY KEY (`count`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 " \
                            "COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.query = "CREATE TABLE `TTM_sent` (  `count` int(11) NOT NULL AUTO_INCREMENT,  `task_date` " \
                            "varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,  `task_time` varchar(45) " \
                            "COLLATE utf8_unicode_ci DEFAULT NULL,  `sent` varchar(3600) COLLATE utf8_unicode_ci " \
                            "DEFAULT NULL,  `status` varchar(45) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'False', " \
                            "PRIMARY KEY (`count`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        self.s_data.create_insert_update_or_delete()
        self.s_data.default_database = os.environ.get('location_db')
        st_list = [['boss home', '28.698248', '77.461437', 'home'],
                   ['Armada Mart', '28.696934978932198', '77.46229160428712', 'super store'],
                   ['Shiv Temple', '28.694532785193434', ' 77.4617873490047', 'temple'],
                   ['Shani Temple', '28.693019317582937', '77.45969425559605', 'temple'],
                   ['hotel fortune', '28.684858632607664', '77.4532089895043', 'hotel'],
                   ['Bharat Petroleum', '28.687253989389138', ' 77.4514280027265', 'petrol'],
                   ['Vishal Mega Mart', '28.686543388296688', '77.45243114888247', 'super store'],
                   ['Punjab national bank', '28.68919105883029', '77.45275837838662', 'bank'],
                   ['HDFC bank', '28.689241058632074', '77.45275033175854', 'bank'],
                   ['Goyal Store', '28.689749878762115', '77.4526061630241', 'super store'],
                   ['P block', '28.689712820271644', '77.45301184713166', 'Market'],
                   ['H bock', '28.690737408082782', '77.45205648211878', 'Market'],
                   ['Kendriya Vidhyalaya', '28.67997752572127', '77.46396030701874', 'school'],
                   ['Sampada Ayurvedic center', '28.670752814407074', '77.44923930954567', 'Clinic'],
                   ['Krishna Sagar', '28.67612784297411', '77.4438110567231', 'Restaurant'],
                   ['Bikanervala Raj Nagar', '28.675189789971242', '77.44247408914005', 'Restaurant'],
                   ['MongoDB', '28.493823442902887', '77.08919365708378', 'office']
                   ]
        for i in st_list:
            self.s_data.query = "Insert into shivam_standard_location_long_lat (loc_name, latitude, longitude, " \
                                "category) values('" + str(i[0]) + "', '" + str(i[1]) + "', '" + str(i[2]) + "', '" + str(i[3]) + "')"
            self.s_data.create_insert_update_or_delete()


if __name__ == "__main__":
    MakeTables().make_table()

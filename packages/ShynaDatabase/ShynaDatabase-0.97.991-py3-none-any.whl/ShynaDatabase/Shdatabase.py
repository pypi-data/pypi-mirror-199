import mysql.connector
from Shynatime import ShTime
import os


class ShynaDatabase:
    """ ShynaDatabase Package

    1) check_connectivity : Check database connectivity
    2) create_insert_update_or_delete: as per name, no return
    3) select_from_table : return output as list
    4) set_date_system: update last run in status_db
    5) insert_or_update_or_delete_with_status: as per name, return will True or False

    """
    s_time = ShTime.ClassTime()
    database_user = os.environ.get('user')
    default_database = ''
    host = os.environ.get('host')
    passwd = os.environ.get('passwd')
    query = ''
    device_id = os.environ.get('device_id')
    comment = False
    message = "Need Message"

    def check_connectivity(self):
        """
        Check connectivity with database.
        Before running function, define the default database at class object level.
        This function will try making connection with it
        :return: True or False

        """
        status = False
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            if my_db.is_connected():
                status = True
            else:
                status = False
        except Exception as e:
            print(e)
            status = False
        finally:
            if my_db.is_connected():
                my_db.close()
            return status

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

    def select_from_table(self):
        """Select all row using the given query and return the result in dictionary format."""
        result = []
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(self.query)
            cursor = my_cursor.fetchall()
            if len(cursor) > 0:
                for row in cursor:
                    result.append(row)
            else:
                result.append('Empty')
        except Exception as e:
            print("Exception is: \n", e)
            result = "Exception"
        finally:
            my_db.close()
            return result

    def set_date_system(self, process_name):
        # print("Device_id", self.device_id)
        self.default_database = os.environ.get("status_db")
        if self.comment is False:
            self.query = "Insert into last_run_check (task_date, task_time, from_device, process_name) " \
                         "VALUES('" + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + \
                         "', '" + str(self.device_id) + "','" + str(process_name) + "') " \
                         "ON DUPLICATE KEY UPDATE task_date='" + str(self.s_time.now_date) + "', task_time='" \
                         + self.s_time.now_time + "', from_device='" + str(self.device_id) + "'"
            self.create_insert_update_or_delete()
        else:
            self.query = "Insert into last_run_check (task_date,task_time,from_device,comment,process_name)" \
                         "VALUES('" + str(self.s_time.now_date) + "', '" + str(self.s_time.now_time) + \
                         "', '" + str(self.device_id) + "','" + str(self.comment) + "','" \
                         + str(process_name) + "') ON DUPLICATE KEY UPDATE task_date='" \
                         + str(self.s_time.now_date) + "', task_time='" + str(self.s_time.now_time) + "',from_device='"\
                         + str(self.device_id) + "'"
            self.create_insert_update_or_delete()

    def insert_or_update_or_delete_with_status(self):
        insert_status = False
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(self.query)
            my_db.commit()
            insert_status = True
        except mysql.connector.Error as err:
            insert_status = False
            print("error number is", err.errno)
        finally:
            my_db.close()
            return insert_status

    def add_speak_sentence(self, speak_sentence, priority):
        try:
            speak_sentence = str(speak_sentence).replace("'", "\\'")
            self.default_database = os.environ.get("notify_db")
            device_id = os.environ.get('device_id')
            self.query = "Insert into speak_sentence (task_date, task_time,sentence_to_speak,device,priority)VALUES ('"\
                         + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "','" \
                         + str(speak_sentence) + "','" + str(device_id) + "', '" + str(priority) + "')"
            self.create_insert_update_or_delete()
        except Exception as e:
            print(e)

    def bot_send_msg_to_master(self):
        try:
            self.message = str(self.message).replace("'", "\\'")
            self.default_database = os.environ.get("notify_db")
            device_id = os.environ.get('device_id')
            self.query = "Insert into bot_msg_backup (text_date, text_time,bot_name,message,device) VALUES ('" \
                         + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "','bot_token','" \
                         + str(self.message) + "','" + str(device_id) + "')"
            self.create_insert_update_or_delete()
        except Exception as e:
            print(e)

    def bot_send_news_to_master(self):
        try:
            self.message = str(self.message).replace("'", "\\'")
            self.default_database = os.environ.get("notify_db")
            device_id = os.environ.get('device_id')
            self.query = "Insert into bot_msg_backup (text_date, text_time,bot_name,message,device) VALUES ('" \
                         + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "','news_bot_token','" \
                         + str(self.message) + "','" + str(device_id) + "')"
            self.create_insert_update_or_delete()
        except Exception as e:
            print(e)

    def bot_send_broadcast_msg_to_master(self):
        try:
            self.message = str(self.message).replace("'","\\'")
            self.default_database = os.environ.get("notify_db")
            device_id = os.environ.get('device_id')
            self.query = "Insert into bot_msg_backup (text_date, text_time,bot_name,message,device) VALUES ('" \
                         + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "','broadcast_bot_token','" \
                         + str(self.message) + "','" + str(device_id) + "')"
            self.create_insert_update_or_delete()
        except Exception as e:
            print(e)

    def clean_query(self, query_text):
        try:
            self.query = str(query_text).replace("'", "\\'")
            return self.query
        except Exception as e:
            return self.query

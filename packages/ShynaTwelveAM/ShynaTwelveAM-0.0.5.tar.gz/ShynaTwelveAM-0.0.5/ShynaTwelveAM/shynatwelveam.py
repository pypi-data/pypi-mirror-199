import os
from ShynaWeather import UpdateWeather
from Shynatime import ShTime
from ShynaDatabase import Shdatabase
import inspect


class ShynaTwelveAM:
    """
    Process 12 AM task

    1) Update weather to the table for morning greetings
    2) Clean up tables old data.
        a) Shivam_face
        b) Shivam_location
        c) connection_check

    """
    s_weather = UpdateWeather.UpdateWeather()
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    result = ''

    def run_at_twelve(self):
        try:
            self.s_weather.update_weather_sentence()
            self.clean_tables()
        except Exception as e:
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()

    def clean_tables(self):
        try:
            # cleaning up started
            self.s_data.message = "Initiating Clean up Process"
            self.s_data.bot_send_news_to_master()
            delete_date_table = []
            delete_date = self.s_time.subtract_date(from_date=self.s_time.now_date, how_many=2).date()
            print("Clean up Shivam_face table")
            # Clean up Shivam_face table
            self.s_data.default_database = os.environ.get('data_db')
            self.s_data.query = "Select count, task_date from shivam_face order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from shivam_face where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("Clean up shivam_device_location table")
            # Clean up shivam_device_location table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('location_db')
            self.s_data.query = "Select count, new_date from shivam_device_location order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from shivam_device_location where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("Clean up connection_check table")
            # Clean up connection_check table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('status_db')
            self.s_data.query = "Select count, new_date from connection_check order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from connection_check where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean mom_call table")
            # clean mom_call table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('twelve_db')
            self.s_data.query = "Select count from Mom_call order by count ASC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    delete_date_table.append(item[0])
                if delete_date_table and len(delete_date_table) > 4:
                    self.s_data.query = "Delete from Mom_call where count IN (" \
                                        "" + str(delete_date_table[:-3]).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the TTM_sent table")
            # clean the TTM_sent table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('taskmanager_db')
            self.s_data.query = "Select count, task_date from TTM_sent order by count DESC"
            self.result = self.s_data.select_from_table()
            # print(self.result[0])
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from TTM_sent where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the Alarm table")
            # clean the Alarm table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('alarm_db')
            self.s_data.query = "Select count, task_date from alarm order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from alarm where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the greeting table")
            # clean the greeting table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('alarm_db')
            self.s_data.query = "Select count, new_date from greeting order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from greeting where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the news_alert table")
            # clean the news_alert table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('news_db')
            self.s_data.query = "Select count, task_date from news_alert order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from news_alert where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the bot_msg_backup table")
            # clean the bot_msg_backup table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('notify_db')
            self.s_data.query = "Select count, text_date from bot_msg_backup order by count DESC"
            self.result = self.s_data.select_from_table()
            # print(self.result)
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from bot_msg_backup where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the get_sent table")
            # clean the get_sent table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('notify_db')
            self.s_data.query = "Select count from get_sent where process_status = 'True' order by count DESC "
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    delete_date_table.append(item[0])
                delete_date_table = delete_date_table[:-10]
                if delete_date_table:
                    self.s_data.query = "Delete from get_sent where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the speak_sentence table")
            # clean the speak_sentence table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('notify_db')
            self.s_data.query = "Select count, task_date from speak_sentence order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from speak_sentence where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the bot_msg_backup table")
            # clean the bot_msg_backup table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('taskmanager_db')
            self.s_data.query = "Select count, new_date from Task_Manager order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from Task_Manager where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
            print("clean the bot_msg_backup table")
            # clean the bot_msg_backup table
            delete_date_table = []
            self.result = ''
            self.s_data.default_database = os.environ.get('weather_db')
            self.s_data.query = "Select count, task_date from weather_table order by count DESC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                pass
            else:
                for item in self.result:
                    if self.s_time.string_to_date(date_string=str(delete_date)) > self.s_time.string_to_date(
                            date_string=str(item[1])):
                        delete_date_table.append(item[0])
                    else:
                        pass
                if delete_date_table:
                    self.s_data.query = "Delete from weather_table where count IN (" \
                                        "" + str(delete_date_table).replace('[', '').replace(']', '') + " )"
                    # print(self.s_data.query)
                    self.s_data.create_insert_update_or_delete()
                else:
                    print("list is empty")
        except Exception as e:
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)


if __name__ == "__main__":
    ShynaTwelveAM().run_at_twelve()

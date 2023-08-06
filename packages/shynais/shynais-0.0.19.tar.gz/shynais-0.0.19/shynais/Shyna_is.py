import random
from haversine import haversine, Unit
from ShynaDatabase import Shdatabase
from Shynatime import ShTime
import os
import inspect


class ShynaIs:
    """
        This is for tracking and checking activities. It will store the data in table
        and Notification package should take care of sending notification in case there is something unexpected
        1) is_location_service_on?
        2) is_this_is_first_time_on_cam?
        3) is_shivam_in_front_of _any_camera?
        4) is_shivam_working late night?
        5) Is_shivam_at_home?
        6) is_mom_calling?
        7) is_shivam_far_away?
        8) is_shivam_coming_home?
    """
    status_db = os.environ.get('status_db')
    data_db = os.environ.get('data_db')
    location_db = os.environ.get('location_db')
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    default_db = os.environ.get("twelve_db")
    alarm_db = os.environ.get("alarm_db")

    def __init__(self):
        self.going_far_sent = random.choice(str("Ok, Shiv just crossed the 3 KM radius. Any one home?. Well?!!!  . "
                                                "SERIOUSLY?!! . OK-FINE!  does not matter. I am designed to communicate"
                                                " with him any which way.  Panic mode ON!. "
                                                "OH-No-NO!-Dammit!-NOT-THIS-AGAIN!").split("|"))
        self.going_far_msg = random.choice(str("ok,we are out of home zone, my trackers are on| ok, this was NOT a "
                                               "short trip.Where we are headed? Never mind rhetorical question because"
                                               " trackers are on. They are right?| Make sure termux in online, I am"
                                               " tracking status any which way").split("|"))
        self.not_still_working_late = random.choice(str("You know, I like watching you sleep and not in the weird way"
                                                        " <3. Good night| Good boy! sleep tight|Good night I'll keep "
                                                        "the things running meanwhile you take rest").split("|"))
        self.still_working_late = random.choice(str("Boss! it is pretty late I suggest you sleep| I can move the tasks"
                                                    " due date around why need to work this late?| I think you can "
                                                    "sleep, I am always active| Please go to sleep, I am not trained "
                                                    "to shutdown systems does not mean I like to watch you working "
                                                    "late| I like the way Iron man told Hulk Go to sleep! Go to sleep! "
                                                    "Go to sleep!").split("|"))
        self.not_front_of_cam = random.choice(str("I think I forgot your face| Boss I cannot see you|Boss are you "
                                                  "there?|Boss? you there?|Either I cannot see you or the camera is "
                                                  "not working|Dammit! I cannot reboot camera, Oh! wait no one "
                                                  "can|Boss, I cannot see| My-eyes!-My-Eyes!").split("|"))
        self.home_for_to_long = random.choice(str("so you have no plan going out?| I think we should take ride or "
                                                  "something|I need some fresh air, please take me outside| I wonder "
                                                  "how it looks outside of home| I kow People says home sweet home, I "
                                                  "think it is excessive now").split("|"))
        self.back_home = random.choice(str("Welcome back home Boss |it does feel Good to back home.Right boss?|"
                                           "It was amazing, lot of dogs outside, but it was ok.I am more like a cat "
                                           "loving|home sweet home, but not in excess. remember that").split("|"))
        self.left_home_speak = random.choice(str("Mom, not to worry I am there. you are not alone| Mom I am leaving "
                                                 "to with hime| I am angry with him, I am staying home. "
                                                 "Huh!| Finally he left the house. I am up for gossip").split("|"))
        self.left_home_msg = random.choice(str("See you later|See ya|Yeah! take me with you| You go, I stay|Bye Bye,"
                                               " trackers are on| Make sure you check the chat services. "
                                               "stay safe").split("|"))
        self.result = False
        self.is_this = False
        self.additional_note = False
        self.last_run_status = False
        self.status_count = 0
        self.am_first_time = random.choice(str("Hello! Boss, I hope you had a good sleep?|Hey! how are you this"
                                               " lovely morning|Good to see you Boss").split("|"))
        self.pm_first_time_noon = random.choice(str("Hello! Boss, I hope you are having a good day?| So?! are we "
                                                    "having a good day?|So?! how are we today?| Hey! my question is, "
                                                    "is it work time? because I am already busy").split("|"))
        self.pm_first_time_night = random.choice(str("Hello! Boss, I hope you are had a good day?| So?! did we had a "
                                                     "good day?|So?! how was today?| It is late, let us not work now| "
                                                     "You have Alarm set, I suggest you sleep on time Shiv").split("|"))
        self.termux_offline_sent = random.choice(str("Boss! Termux is offline which means I cannot track you|"
                                                     "I cannot sense you|Boss! Termux, again!").split("|"))

    def get_data_from_db(self, question_is):
        """
        this return bool false in case there is no data
        :param question_is:
        :return:
        """
        self.is_this = False
        try:
            self.s_data.default_database = self.default_db
            self.s_data.query = "Select * from shyna_is where question_is='" + str(question_is) + "' and task_date='" \
                                + str(self.s_time.now_date) + "'"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                self.is_this = False
            else:
                self.is_this = self.result[0]
        except Exception as e:
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)
            self.is_this = False
        finally:
            return self.is_this

    def insert_on_change(self, question_is, status):
        try:
            self.s_data.default_database = self.default_db
            self.s_data.query = "Insert into shyna_is (question_is,task_date,task_time,new_status,last_run_status," \
                                "additional_note,status_count)VALUES('" + str(question_is) + "','" \
                                + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "','" \
                                + str(status) + "','" + str(status) + "','" + str(self.additional_note) + \
                                "', '0') ON DUPLICATE KEY UPDATE task_date='" \
                                + str(self.s_time.now_date) + "', task_time='" + str(self.s_time.now_time) + \
                                "', new_status='" + str(status) + "', additional_note= '" + str(self.additional_note) + \
                                "', question_is='" + str(question_is) + "', status_count=0, last_run_status='" \
                                + str(status) + "'"
            self.s_data.insert_or_update_or_delete_with_status()
        except Exception as e:
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)

    def insert_on_same(self, question_is, count, status):
        try:
            self.s_data.default_database = self.default_db
            self.s_data.query = "Insert into shyna_is (question_is,task_date,task_time,new_status,additional_note," \
                                "status_count)VALUES('" + str(question_is) + "','" + str(self.s_time.now_date) + \
                                "','" + str(self.s_time.now_time) + "','" + str(status) + "','" \
                                + str(self.additional_note) + "', '" + str(count) + "') ON DUPLICATE KEY UPDATE " \
                                                                                    "task_date='" + str(
                self.s_time.now_date) + "',task_time='" \
                                + str(self.s_time.now_time) + "', new_status='" + str(status) + "', additional_note= '" \
                                + str(self.additional_note) + "', question_is='" + str(question_is) + \
                                "',status_count='" + str(count) + "'"
            self.s_data.insert_or_update_or_delete_with_status()
        except Exception as e:
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)

    def action_on_count(self, count, speak_sentence, priority, frequency):
        try:
            if int(count) % int(frequency) == 0:
                self.s_data.add_speak_sentence(speak_sentence=speak_sentence, priority=priority)
                self.s_data.message = str(speak_sentence)
                self.s_data.bot_send_news_to_master()
            else:
                pass
        except Exception as e:
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()

    def is_termux_online(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        try:
            self.s_data.default_database = self.status_db
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='location_check' "
            self.result = self.s_data.select_from_table()
            # print("last run check", self.result[0][0])
            time_diff = (self.s_time.string_to_time_with_date(time_string=str(self.s_time.now_time)) -
                         self.s_time.string_to_time_with_date(time_string=str(self.result[0][0]))).total_seconds()
            # print(time_diff)
            if int(time_diff) <= 70:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = "Exception"
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='termux_online'"
                self.result = self.s_data.select_from_table()
                # print(self.result[0][0], self.result[0][1])
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    self.status_count = int(self.result[0][1]) + 1
                    if str(self.is_this).lower().__eq__("false"):
                        self.action_on_count(count=self.status_count, speak_sentence=self.termux_offline_sent,
                                             priority="[2]", frequency=20)
                    else:
                        pass
                    self.insert_on_same(question_is="termux_online", count=self.status_count, status=self.is_this)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    if str(self.is_this).lower() == 'true':
                        self.s_data.message = "Termux back online"
                        self.s_data.bot_send_msg_to_master()
                    else:
                        self.s_data.message = "Termux Offline"
                        self.s_data.bot_send_msg_to_master()
                    self.insert_on_change(question_is="termux_online", status=self.is_this)
            except Exception as e:
                print(e)
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_location_received_from_primary_mobile(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.default_database = self.status_db
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='location_check' "
            self.result = self.s_data.select_from_table()
            # print(self.result[0][0])
            time_diff = (self.s_time.string_to_time_with_date(
                time_string=str(self.s_time.now_time)) - self.s_time.string_to_time_with_date(
                time_string=str(self.result[0][0]))).total_seconds()
            # print(time_diff)
            if int(time_diff) <= 70:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = "Exception"
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='primary_location'"
                self.result = self.s_data.select_from_table()
                # print(self.result[0][0], self.result[1][0])
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    self.status_count = int(self.result[0][1]) + 1
                    self.insert_on_same(question_is="primary_location", count=self.status_count, status=self.is_this)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    self.insert_on_change(question_is="primary_location", status=self.is_this)
            except Exception as e:
                print(e)
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_this_the_is_first_time_on_cam(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        time_needed = []
        try:
            self.s_data.default_database = self.data_db
            self.s_data.query = "SELECT task_time from shivam_face where task_date = '" \
                                + str(self.s_time.now_date) + "' order by count ASC"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                self.is_this = False
            else:
                for item in self.result:
                    if self.s_time.string_to_time(time_string='04:00:00') <= self.s_time.string_to_time(
                            time_string=item[0]) <= self.s_time.string_to_time(time_string='23:00:00'):
                        # time_needed.append(self.result[0])
                        time_diff = (self.s_time.string_to_time_with_date(time_string=str(self.s_time.now_time))
                                     - self.s_time.string_to_time_with_date(time_string=str(item[0]))
                                     ).total_seconds()
                        # print(time_diff)
                        if 0 <= time_diff <= 60.0:
                            self.is_this = True
                            break
                    else:
                        self.is_this = False
        except Exception as e:
            print(e)
            self.is_this = "exception"
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='first_time_on_cam' "
                self.result = self.s_data.select_from_table()
                # print(self.result[0][0])
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    self.status_count = int(self.result[0][1]) + 1
                    self.insert_on_same(question_is="first_time_on_cam", count=self.status_count, status=self.is_this)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    if str(self.is_this).lower() == 'true':
                        self.shivam_is_front_of_the_camera_first_time()
                    self.insert_on_change(question_is="first_time_on_cam", status=self.is_this)
            except Exception as e:
                print(e)
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def shivam_is_front_of_the_camera_first_time(self):
        print("processing: " + str(inspect.stack()[0][3]))
        try:
            self.result = self.s_time.check_am_pm(text_string=str(self.s_time.convert_to_am_pm(
                str(self.s_time.now_time))))
            if str(self.result).lower().__eq__('am'):
                self.s_data.add_speak_sentence(speak_sentence=self.am_first_time, priority="[0,2,1]")
            elif str(self.result).lower().__eq__('pm'):
                if self.s_time.string_to_time(time_string='12:00:00') <= self.s_time.string_to_time(
                        time_string=str(self.s_time.now_time)) <= self.s_time.string_to_time(time_string='20:00:00'):
                    self.s_data.add_speak_sentence(speak_sentence=self.pm_first_time_noon, priority="[0,2,1]")
                elif self.s_time.string_to_time(time_string='20:00:00') <= self.s_time.string_to_time(
                        time_string=str(self.s_time.now_time)) <= self.s_time.string_to_time(time_string='23:00:00'):
                    self.s_data.add_speak_sentence(speak_sentence=self.pm_first_time_noon, priority="[0,2,1]")
            else:
                pass
        except Exception as e:
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()

    def is_shivam_at_home(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        latitude_list = []
        longitude_list = []
        distance = []
        try:
            self.s_data.default_database = self.location_db
            self.s_data.query = "SELECT new_latitude, new_longitude FROM shivam_device_location order by count DESC " \
                                "limit 3"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                latitude_list.append(item[0])
                longitude_list.append(item[1])
            self.s_data.query = "SELECT latitude, longitude FROM shivam_standard_location_long_lat where " \
                                "loc_name='boss home';"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                distance_from_one = haversine(point1=(float(latitude_list[0]), float(longitude_list[0])),
                                              point2=(float(item[0]), float(item[1])))
                if distance_from_one <= 0.09:
                    distance.append(True)
                else:
                    distance.append(False)
            my_dict = {i: distance.count(i) for i in distance}
            self.is_this = max(my_dict, key=my_dict.get)
            self.s_data.default_database = os.environ.get("status_db")
            self.s_data.query = "Select connection_type from connection_check where new_date = '" \
                                + str(self.s_time.now_date) + "' order by count DESC limit 1"
            connection_type = self.s_data.select_from_table()
            if str(connection_type[0]).lower().__eq__('empty'):
                pass
            else:
                if str(self.is_this).lower().__eq__('false') and str(connection_type[0][0]).lower().__eq__("home"):
                    self.is_this = True
                else:
                    pass
            # print("After calculations ", self.is_this)
        except Exception as e:
            self.is_this = "Exception"
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='is_shivam_at_home' "
                self.result = self.s_data.select_from_table()
                # print(self.result[0][0])
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    self.status_count = int(self.result[0][1]) + 1
                    self.insert_on_same(question_is="is_shivam_at_home", count=self.status_count, status=self.is_this)
                    if str(self.is_this).lower().__eq__('true'):
                        self.action_on_count(count=self.status_count, speak_sentence=self.home_for_to_long,
                                             priority="[2]", frequency=1000)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    if str(self.is_this).lower().__eq__('true'):
                        self.s_data.add_speak_sentence(speak_sentence=self.back_home, priority="[1,2]")
                        self.s_data.message = self.back_home
                        self.s_data.bot_send_msg_to_master()
                    else:
                        self.s_data.add_speak_sentence(speak_sentence=self.left_home_speak, priority="[1,2]")
                        self.s_data.message = self.left_home_msg
                        self.s_data.bot_send_msg_to_master()
                    self.insert_on_change(question_is="is_shivam_at_home", status=self.is_this)
            except Exception as e:
                print(e)
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_shivam_in_front_of_any_cam(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        try:
            self.result = self.get_data_from_db(question_is="is_shivam_at_home")
            if str(self.result[4]).lower().__eq__('true'):
                self.s_data.default_database = self.data_db
                self.s_data.query = "SELECT task_time from shivam_face where task_date='" + \
                                    str(self.s_time.now_date) + "' order by count DESC limit 1"
                self.result = self.s_data.select_from_table()
                if str(self.result[0]).lower().__eq__('empty'):
                    self.is_this = False
                else:
                    # print(self.result[0][0])
                    time_diff = (self.s_time.string_to_time_with_date(
                        time_string=str(self.s_time.now_time)) - self.s_time.string_to_time_with_date(
                        time_string=str(self.result[0][0]))).total_seconds()
                    if 0.0 <= time_diff <= 60.0:
                        self.is_this = True
                    else:
                        self.is_this = False
            else:
                self.is_this = False
        except Exception as e:
            print(e)
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            self.is_this = "Exception"
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='shivam_front_of_camera' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    self.status_count = int(self.result[0][1]) + 1
                    self.insert_on_same(question_is="shivam_front_of_camera", count=self.status_count,
                                        status=self.is_this)
                    print("On same", self.status_count)
                    if str(self.is_this).lower().__eq__('false'):
                        self.action_on_count(count=self.status_count, speak_sentence=self.not_front_of_cam,
                                             priority="[2]", frequency=1000)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    print("On change")
                    self.insert_on_change(question_is="shivam_front_of_camera", status=self.is_this)
            except Exception as e:
                print(e)
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_shivam_working_late(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        try:
            self.result = self.get_data_from_db(question_is="shivam_front_of_camera")
            if str(self.result[4]).lower().__eq__('true'):
                if self.s_time.string_to_time(time_string='00:30:00') <= self.s_time.string_to_time(
                        time_string=self.s_time.now_time) <= self.s_time.string_to_time(time_string='04:00:00'):
                    self.is_this = True
                else:
                    self.is_this = False
                    self.insert_on_change(question_is="is_shivam_working_late", status=self.is_this)
            else:
                self.is_this = False
                self.insert_on_change(question_is="is_shivam_working_late", status=self.is_this)
        except Exception as e:
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)
            self.is_this = "Exception"
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='is_shivam_working_late' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    self.status_count = int(self.result[0][1]) + 1
                    self.insert_on_same(question_is="is_shivam_working_late", count=self.status_count,
                                        status=self.is_this)
                    if str(self.is_this).lower().__eq__('true'):
                        self.action_on_count(count=self.status_count, speak_sentence=self.still_working_late,
                                             priority="[2]", frequency=1000)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    if str(self.is_this).lower() == 'true':
                        self.s_data.message = self.still_working_late
                        self.s_data.bot_send_msg_to_master()
                    else:
                        self.s_data.message = self.not_still_working_late
                        self.s_data.bot_send_msg_to_master()
                    self.insert_on_change(question_is="is_shivam_working_late", status=self.is_this)
            except Exception as e:
                print(e)
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_mom_calling(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        try:
            self.s_data.default_database = self.default_db
            self.s_data.query = "Select new_status from Mom_call order by count DESC limit 1"
            self.result = self.s_data.select_from_table()
            if str(self.result[0][0]).lower().__eq__('true'):
                self.is_this = True
                msg = random.choice(str("Boss! Mom is calling|Shiv! Mom is calling| Mom calling | watch out for Mom "
                                        "| Boss, Mom just text me| Mom| Mum ").split("|"))
                self.s_data.add_speak_sentence(speak_sentence=msg, priority="[0,1,2]")
            else:
                self.is_this = False
                self.s_data.set_date_system(process_name='is_mom_calling')
        except Exception as e:
            self.is_this = False
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)
        finally:
            print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
            return self.is_this

    def is_shivam_far_away(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        try:
            self.s_data.default_database = self.location_db
            self.s_data.query = "select latitude, longitude from shivam_standard_location_long_lat where " \
                                "loc_name='boss home'"
            self.result = self.s_data.select_from_table()
            if str(self.result).lower().__eq__('empty'):
                self.s_data.message = "Standard home location not defined. error at :" + str(inspect.stack()[0][3])
                self.s_data.bot_send_broadcast_msg_to_master()
                self.is_this = False
            else:
                home = (float(self.result[0][0]), float(self.result[0][1]))
                self.result = ""
                self.s_data.default_database = os.environ.get('location_db')
                self.s_data.query = "select new_latitude, new_longitude from shivam_device_location order by count" \
                                    " DESC limit 9"
                self.result = self.s_data.select_from_table()
                if str(self.is_shivam_xkm_away(home=home, result=self.result, x=1.0)).lower().__eq__('true'):
                    print("Shivam is more than 1 KM away")
                    if str(self.is_shivam_xkm_away(home=home, result=self.result, x=2.0)).lower().__eq__('true'):
                        print("Shivam is more than 2 KM away")
                        if str(self.is_shivam_xkm_away(home=home, result=self.result, x=3.0)).lower().__eq__(
                                'true'):
                            print("Shivam is more than 3 KM away")
                            self.is_this = True
                            self.additional_note = False
                        else:
                            self.is_this = False
                            self.additional_note = False
                    else:
                        self.is_this = False
                        self.additional_note = False
                else:
                    self.is_this = False
                    self.additional_note = False
        except Exception as e:
            self.is_this = "Exception"
            print(e)
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='is_shivam_far_away' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    if str(self.is_this).lower().__eq__('true'):
                        self.status_count = int(self.result[0][1]) + 1
                        self.insert_on_same(question_is="is_shivam_far_away", count=self.status_count,
                                            status=self.is_this)
                    else:
                        self.insert_on_same(question_is="is_shivam_far_away", count=0,
                                            status=self.is_this)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    if str(self.is_this).lower() == 'true':
                        self.s_data.message = self.going_far_msg
                        self.s_data.bot_send_broadcast_msg_to_master()
                        self.s_data.add_speak_sentence(speak_sentence=self.going_far_sent, priority="[0,1,2]")
                    self.insert_on_change(question_is="is_shivam_far_away", status=self.is_this)
            except Exception as e:
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
                print(e)
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_shivam_xkm_away(self, home, result, x):
        self.is_this = False
        try:
            km_list = []
            self.result = result
            for item in self.result:
                location = (float(item[0]), float(item[1]))
                km_list.append(haversine(point1=home, point2=location, unit=Unit.KILOMETERS, normalize=True))
            km_delete = []
            for item in range(0, len(km_list) - 1):
                if float(km_list[item]) < float(x):
                    km_delete.append(item)
                else:
                    pass
            if len(km_delete) < 3:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print("Exception", e)
        finally:
            return self.is_this

    def is_shivam_coming_home(self):
        print("checking: " + str(inspect.stack()[0][3]))
        self.is_this = False
        round_list = []
        clean_round_list = []
        try:
            self.result = self.get_data_from_db(question_is="termux_online")
            if str(self.result[5]).lower().__eq__('true'):
                self.s_data.default_database = self.location_db
                self.s_data.query = "Select diff_from_home from shivam_device_location where " \
                                    "status = 'True' order by count DESC limit 45"
                self.result = self.s_data.select_from_table()
                print(self.result)
                for item in self.result:
                    round_list.append(round(float(item[0])))
                clean_round_list = [i for n, i in enumerate(round_list) if i not in round_list[:n]]
                # print(clean_round_list)
                if int(clean_round_list[0]) == 3 and clean_round_list[-1] > 3:
                    self.is_this = True
                    self.additional_note = False
                else:
                    self.is_this = False
                    self.additional_note = False
        except Exception as e:
            self.is_this = "Exception"
            print(e)
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status, status_count from shyna_is where " \
                                    "question_is='is_shivam_coming_home' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    if str(self.is_this).lower().__eq__('true'):
                        self.status_count = int(self.result[0][1]) + 1
                        self.insert_on_same(question_is="is_shivam_coming_home", count=self.status_count,
                                            status=self.is_this)
                    else:
                        self.insert_on_same(question_is="is_shivam_coming_home", count=0,
                                            status=self.is_this)
                elif str(self.is_this).lower().__eq__('exception'):
                    pass
                else:
                    if str(self.is_this).lower() == 'true':
                        msg = random.choice(str("ok,we are back to home zone, my trackers are on| ok, Good to sense "
                                                "you nearby. Welcome back! to home city.").split("|"))
                        self.s_data.message = msg
                        self.s_data.bot_send_msg_to_master()
                        msg = random.choice(str("Mom! Shivam is coming back to home.|Mum! Shivam is about to reach "
                                                "home. If you want to make tea it is time|Mum! Shivam is about to "
                                                "reach home. Tea is a good option to go|Mum! I sense Shivam is nearby."
                                                " Tea is a good option to go").split("|"))
                        self.s_data.add_speak_sentence(speak_sentence=msg, priority="[0,1,2]")
                    self.insert_on_change(question_is="is_shivam_coming_home", status=self.is_this)
            except Exception as e:
                self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
                self.s_data.bot_send_broadcast_msg_to_master()
                print(e)
            finally:
                print(str(inspect.stack()[0][3]) + ": " + str(self.is_this))
                return self.is_this

    def is_shyna_should_remain_silent(self):
        print("checking: " + str(inspect.stack()[0][3]))
        try:
            self.s_data.default_database = self.alarm_db
            self.s_data.query = "select new_time from greeting where from_device='hold' and of_device='hold' order " \
                                "by count DESC limit 1"
            self.result = self.s_data.select_from_table()
            if str(self.result[0]).lower().__eq__('empty'):
                # print(self.result[0])
                pass
            else:
                # print(self.result[0][0])
                time_diff = self.s_time.is_time_passed(item_time=str(self.s_time.add_hour(
                    from_time=str(self.result[0][0]), how_many=1)))
                if str(time_diff).lower().__eq__('true'):
                    self.s_data.default_database = self.alarm_db
                    self.s_data.query = "insert into greeting (new_date,new_time,greet_string,from_device,of_device) " \
                                        "VALUES ('" + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) +\
                                        "','wake','" + str(os.environ.get('device_id')) + "','" \
                                        + str(os.environ.get('device_id')) + "')"
                    self.s_data.create_insert_update_or_delete()
                    self.s_data.message = "Speech module activated"
                    self.s_data.bot_send_news_to_master()
        except Exception as e:
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)

    def chaos(self):
        print("Starting " + str(inspect.stack()[0][3]))
        try:
            self.is_termux_online()
            self.is_location_received_from_primary_mobile()
            self.is_shivam_in_front_of_any_cam()
            self.is_shivam_at_home()
            self.is_mom_calling()
            self.is_shivam_far_away()
            self.is_shivam_coming_home()
            if self.s_time.string_to_time(time_string='04:00:00') <= self.s_time.string_to_time(
                    time_string=self.s_time.now_time) \
                    <= self.s_time.string_to_time(time_string='11:00:00'):
                self.is_this_the_is_first_time_on_cam()
            if self.s_time.string_to_time(time_string='00:29:00') <= self.s_time.string_to_time(
                    time_string=self.s_time.now_time) \
                    <= self.s_time.string_to_time(time_string='4:00:00'):
                self.is_shivam_working_late()
            else:
                self.insert_on_change(question_is="is_shivam_working_late", status="False")
        except Exception as e:
            self.s_data.message = "Exception at " + str(inspect.stack()[0][3]) + ": " + str(e)
            self.s_data.bot_send_broadcast_msg_to_master()
            print(e)
        finally:
            print("Successfully executed" + str(inspect.stack()[0][3]))


if __name__ == '__main__':
    ShynaIs().chaos()


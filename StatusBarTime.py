#
#    Made by lowliet
#

import sublime, sublime_plugin
from datetime import datetime

STATUSBARTIME_FORMAT_KEY = 'StatusBarTime_format'
STATUSBARTIME_CLOCK_TYPE_KEY = 'StatusBarClock_Type'
STATUSBARTIME_SETTING_FILE = 'StatusBarTime.sublime-settings'
STATUSBARTIME_CLOCKDELAY_KEY = 'StatusBarClock_Interval'
STATUSBARTIME_CLOCKDISPLAY_ONLYINVIEW_KEY = "StatusBarClock_display_onlyinview"
DEFAULT_FORMAT = '%H:%M:%S'

class StatusBarTime(sublime_plugin.EventListener):
    stBarStartTime = 0  # variable to hold start time
    def on_activated(self, view):
        settings = sublime.load_settings(STATUSBARTIME_SETTING_FILE)
        # Get Update interval for clock
        update_interval = settings.get(STATUSBARTIME_CLOCKDELAY_KEY, 1000)
        # New Setting load From setting file
        clock_Type = settings.get(STATUSBARTIME_CLOCK_TYPE_KEY, 0)
        # Get setting for only in view display
        onlyinview = settings.get(STATUSBARTIME_CLOCKDISPLAY_ONLYINVIEW_KEY, True)
        # Start Timer if its empty (This is supposed to happen only once)
        if not self.stBarStartTime: self.stBarStartTime=datetime.now()
        if not clock_Type: Timer(settings.get(STATUSBARTIME_FORMAT_KEY, DEFAULT_FORMAT)).displayTime(view, update_interval, onlyinview)
        else: Timer().displayUpTime(view, self.stBarStartTime, update_interval, onlyinview)

class Timer():
    status_key = 'statusclock'
    def __init__(self, format=DEFAULT_FORMAT):
        self._format = format

    # helper method which converts given duration to days, hours, minutes and seconds
    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = seconds//3600
        minutes = (seconds % 3600)//60
        seconds = seconds % 60
        return days, hours, minutes, seconds
    
    def displayTime(self, view, delay, onlyinview):
        view.set_status(self.status_key, datetime.now().strftime(self._format))
        actwin = sublime.active_window()
        if actwin:
            if not onlyinview or (actwin.active_view() and actwin.active_view().id() == view.id()):
               sublime.set_timeout(lambda: self.displayTime(view, delay, onlyinview), delay)
        else:
            view.set_status(self.status_key, '')
        return
        
    # Method for handling uptime display
    def displayUpTime(self, view, startTime, delay, onlyinview):
        upTime = datetime.now() - startTime
        days, hours, minutes, seconds = self.convert_timedelta(upTime)
        out = ''
        if days: out += str("%s days, " % (days))
        if hours: out += str("%02d:%02d:%02d" % (hours, minutes, seconds))
        elif minutes: out += str("%02d:%02d" % (minutes, seconds))
        elif seconds: out += str("%02d seconds" % (seconds))
        view.set_status(self.status_key, out)
        actwin = sublime.active_window()
        if actwin:
            if not onlyinview or (actwin.active_view() and actwin.active_view().id() == view.id()):
               sublime.set_timeout(lambda: self.displayUpTime(view, startTime, delay, onlyinview), delay)
        else:
            view.set_status(self.status_key, '')
        return
        
import datetime
import pickle

class Schedule:
    def __init__(self):
        self.running = True
        self.now = datetime.datetime.now()
        self.calendar = []
        self.filename = 'calendar.txt'
        # self.create_calendar()
        self.load_calendar()
        print('It is: '+str(self.now))
    
    def create_calendar(self):
        self.calendar = [[self.now, 'test.py']]
        self.save_calendar()
       
    def check_time(self, wait):
        # Checks to see if next event is wothon 5 min
        date_time = self.calendar[0][0]
        self.now = datetime.datetime.now()
        minutes_diff = abs(self.now - date_time).total_seconds() / 60.0
        if minutes_diff < 5:
            self.calendar.pop(0)
            self.sort_calendar()
            return True
        if wait:
            wait_seconds = (minutes_diff * 60) - 5
            time.sleep(wait_seconds)
            self.calendar.pop(0)
            self.sort_calendar()
            return True
        else:
            return False
    
    def sort_calendar(self):
        calendar_len = len(self.calendar)
        for a in range(0, calendar_len - 1):
            for b in range(0, calendar_len-a-1):
                if self.calendar[b][0] > self.calendar[b+1][0]:
                    self.calendar[b], self.calendar[b+1] = self.calendar[b+1], self.calendar[b]
        
    def add_event(self, file_name, date_time):
        self.calendar.append([date_time, file_name])
        print('Added event to calendar.')
        self.save_calendar()
    
    def remove_event(self, index):
        if index > 0 and index < len(self.calendar)-1:
            print('Removed event: '+str(calendar[index]))
            self.calendar.pop(index)
        else:
            print('Invalid index')
       
    def save_calendar(self):
        self.sort_calendar()
        with open(self.filename, 'wb') as fh:
           pickle.dump(self.calendar, fh)
              
    def load_calendar(self):
        myFile = open (self.filename, 'rb')
        self.calendar = pickle.load(myFile)

# Test cases
# schedule = Schedule()
# schedule.add_event('test.py', datetime.datetime.now())
# schedule.add_event('test.py', datetime.datetime.now())
# print(schedule.calendar)
# result = schedule.check_time(True)
# print(schedule.calendar)
# schedule.remove_event(0)
# print(result)

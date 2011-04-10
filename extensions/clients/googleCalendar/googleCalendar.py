from pylabs import q
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import gdata.calendar.client
import atom
import time
import datetime
import re


class retry(object):
    def __init__(self, retries):
        self.retries = retries

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            for i in range(1, self.retries+1):
                try:
                    f(*args, **kwargs)
                except gdata.service.RequestError as ex:
                    q.logger.log('trying to %s - trial %s of %s'%(f.__name__, i, self.retries), 2)
                    q.logger.log(ex)
                else:
                    q.logger.log('%s carried out successfully in %s tries'%(f.__name__, i), 2)
                    return
            q.logger.log('failed to %s after %s tries'%(f.__name__, self.retries), 2)
        return wrapped_f


class GoogleCalendar(object):
    def getConnection(self, email, password=None, saveCredentials=False):
        return GoogleCalConnection(email, password, saveCredentials)



class GoogleCalConnection(object):
    def __init__(self, username, password=None, saveCredentials=False):
        self._client = gdata.calendar.service.CalendarService()
        cfgpath = q.system.fs.joinPaths(q.dirs.extensionsDir, 'clients', 'googleCalendar', 'googleCalendar.cfg')
        cfgfile = q.tools.inifile.open(cfgpath)
        
        
        if password:
            self._client.password = password
            if saveCredentials:
                cfgfile.addSection(username)
                params = {'email':username, 'password':password}
                for k, v in params.items():
                    cfgfile.addParam(username, k, v)
        else:
            if cfgfile.checkSection(username):
                credentials = cfgfile.getSectionAsDict(username)
                self._client.password = credentials['password']
            else:
                raise RuntimeError('Credentials not stored, please enter full credentials')
            
            
        self._client.email = username
        self._client.source = "pylabs"
        self._client.ProgrammaticLogin()
        
        self._initialized = False
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            attrs.append('calendars')
        return attrs
    
    def _reload(self):
        q.logger.log('reloading connection', 5)
        email = self._client.email
        password = self._client.password
        self.__init__(email, password)


    def __getattribute__(self, name):
        if name == 'calendars' and not object.__getattribute__(self, '_initialized'):
            self.calendars = Calendars(self, object.__getattribute__(self, '_client'))
            self._initialized = True
            return object.__getattribute__(self, 'calendars')
        elif name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)

        
#    def _getOwnCalFeed(self):
#        if not self._initialized:
#            try:
#                self._ownCalFeed = self._client.GetOwnCalendarsFeed()
#            except gdata.service.RequestError:
#                q.logger.log('Request Error while initializing Calendars - Please Try Later', 2)
#                self.__reload()
#            else:
#                q.logger.log('Calendars initialized')
#                self.calendars = Calendars(object.__getattribute__(self, '_client'), object.__getattribute__(self, '_ownCalFeed').entry)
#                self._initialized = True
    
    @retry(10)
    def _getOwnCalFeed(self):
        self._ownCalFeed = self._client.GetOwnCalendarsFeed()
        q.logger.log('Calendars initialized', 2)
        self.calendars = Calendars(object.__getattribute__(self, '_client'), object.__getattribute__(self, '_ownCalFeed').entry)
        self._initialized = True
    
    @retry(10)        
    def new(self, title='New Calendar', summary='New Calendar', place='A-Server', color='#2952A3', timezone='Africa/Cairo', hidden='false'):

        calendar = gdata.calendar.CalendarListEntry()
        calendar.title = atom.Title(text=title)
        calendar.summary = atom.Summary(text=summary)
        calendar.where = gdata.calendar.Where(value_string=place)
        calendar.color = gdata.calendar.Color(value=color)
        calendar.timezone = gdata.calendar.Timezone(value=timezone)
        calendar.hidden = gdata.calendar.Hidden(value=hidden)
        
        new_calendar = self._client.InsertCalendar(new_calendar=calendar)
        
        title = cleanString(title)
        self.calendars._addCalendar(self, self._client, new_calendar)
        q.logger.log('Calendar %s added'%title, 2)
        
        return new_calendar

        
            
class Calendars(object):
    def __init__(self, connection, calClient):
        self._connection = connection
        self._calClient = calClient
        self._initialized = False
        self._cals = {}
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            self._retrieveCals()
            attrs.extend(self._cals.keys())
        return attrs
    
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_retrieveCals')()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
            
#    def _retrieveCals(self):
#        self._cals={}
#        try:
#            self._calFeed = self._calClient.GetOwnCalendarsFeed()
#        except gdata.service.RequestError:
#            q.logger.log('Request Error while Requesting Calendar Feed - Please Try Later', 2)
#            self._connection._reload()
#        else:
#            q.logger.log('Calendars Added')
#            map(lambda calObj: self._addCalendar(self._connection, self._calClient, calObj), self._calFeed.entry)
#            self._initialized = True
            
    @retry(10)
    def _retrieveCals(self):
        self._calFeed = self._calClient.GetOwnCalendarsFeed()
        q.logger.log('Calendars Added')
        map(lambda calObj: self._addCalendar(self._connection, self._calClient, calObj), self._calFeed.entry)
        self._initialized = True
    

    def _addCalendar(self, conn, client, calObject):
        title = cleanString(calObject.title.text)
        self._cals['%s'%title] = calObject
        setattr(self, title, Calendar(conn, client, calObject))
        
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_retrieveCals').__call__()
        key = cleanString(key)
        return self.__dict__[key]
    
    def __iter__(self):
        if not self._initialized:
            self._retrieveCals()
        return GoogleCalIterator(self.__dict__)

            
class Calendar(object):
    
    def __init__(self, calConnection, calClient, calendarObject):
        self._conn = calConnection
        self._client = calClient
        self._calObj = calendarObject
        self._initialized = False
        self.events = Events(self._conn, self._client, self._calObj)
    
    @retry(10)        
    def delete(self):
        path = self._calObj.GetAlternateLink().href
        path.replace('http:','https:')
        self._client.Delete(path)
        self._conn.calendars.__dict__.pop(self._calObj.title.text)
        self._conn.calendars._initialized = False
        
        
    def __getitem__(self, key):
        return self.events.__getitem__(key)
    
    def __iter__(self):
        return self.events.__iter__()
    
    @retry(10)
    def new(self, title='New Event', content='New Event', place='A-Server',start_year=None, start_month=None, start_day=None,
            start_hour=None, start_min=0, end_year=None, end_month=None, end_day=None, end_hour=None, end_min=0, all_day=False):
        event = gdata.calendar.CalendarEventEntry()
        event.title = atom.Title(text=title)
        event.content = atom.Content(text = content)
        event.where.append(gdata.calendar.Where(value_string=place))
        
        time_now = time.localtime()
        
        start_year = start_year or time_now.tm_year
        start_month = start_month or time_now.tm_mon
        start_day = start_day or time_now.tm_mday

        if not all_day and start_hour is None:
            start_hour = time_now.tm_hour
            if start_min == 0:
                start_min = time_now.tm_min
        
        if all_day:
            start_date = datetime.date(start_year, start_month, start_day)
            start_time = start_date.strftime('%Y-%m-%d')
        else:
            start_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((start_year, start_month, start_day, start_hour, start_min, 0, 0, 0, 0)))
        
        end_year = end_year or start_year
        end_month = end_month or start_month
        end_day = end_day or start_day

        if not all_day and end_hour is None:
            end_hour = start_hour + 1
            if end_min == 0:
                end_min = start_min
                
        if all_day:
            end_date = datetime.date(end_year, end_month, end_day)
            end_time = end_date.strftime('%Y-%m-%d')
        else:
            end_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((end_year, end_month, end_day, end_hour, end_min, 0, 0, 0, 0)))
        
        
        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
        
        path = self._calObj.GetAlternateLink().href
        path.replace('http:','https:')
        
#        for trial in range(1, retries+1):
#            try:
#                new_event = self._client.InsertEvent(event, path)
#            except gdata.service.RequestError as ex:
#                ownInit = False
#                q.logger.log('Request Error while creating event "%s" - Retrying #%s of %s'%(title, trial, retries), 2)
#                self._conn._reload()
#            if ownInit:
#                break
#            
#        if ownInit:
#            self.events._addEvent(self._conn, self._client, self, new_event)
#            q.logger.log('event "%s" created successfully'%title, 2)
#            return new_event
#        else:
#            q.logger.log('Request Error while creating event "%s" - Please Try Later'%title, 2)
            
            
        new_event = self._client.InsertEvent(event, path)
        self.events._addEvent(self._conn, self._client, self, new_event)
        q.logger.log('event "%s" created successfully'%title, 2)
        return new_event    
            
class Events(object):
    def __init__(self, calConnection, calClient, calObject):
        self._conn = calConnection
        self._client = calClient
        self._calObj = calObject
        self._initialized = False
        self._events = {}
        
    def __dir__(self):
        attrs = object.__getattribute__(self, '__dict__').keys()
        if not object.__getattribute__(self, '_initialized'):
            self._initEvents()
            attrs.extend(self._events.keys())
        return attrs
    
    def __getattribute__(self, name):
        if not name.startswith('_') and not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_initEvents')()
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        else:
            return object.__getattribute__(self, name)
    
    @retry(10)    
    def _getEventFeed(self):
        path = self._calObj.GetAlternateLink().href
        path.replace('http:','https:')
        
        self._eventFeed = self._client.GetCalendarEventFeed(path)
        q.logger.log('Event feed initialized')
        self._initialized = True
        
        
#        try:
#            self._eventFeed = self._client.GetCalendarEventFeed(path)
#        except gdata.service.RequestError:
#            q.logger.log('Request Error while Requesting Event Feed for calendar - Please Try Later', 2)
#            self._conn._reload()
#        else:
#            q.logger.log('Event feed initialized')
#            self._initialized = True
     
    def _initEvents(self):
        if not self._initialized:
            self._events = {}
            self._getEventFeed()
        map(lambda eventObj: self._addEvent(self._conn, self._client, self, eventObj), self._eventFeed.entry)

    
    def _addEvent(self, conn, client, calendar, event):
        title = cleanString(event.title.text)
        self._events['%s'%title] = event
        setattr(self, title, Event(conn, client, calendar, event))
    
    
#    @retry(10)  
#    def new(self, title='New Event', content='New Event', place='A-Server',start_year=None, start_month=None, start_day=None,
#            start_hour=None, start_min=0, end_year=None, end_month=None, end_day=None, end_hour=None, end_min=0, retries = 10):
#        event = gdata.calendar.CalendarEventEntry()
#        event.title = atom.Title(text=title)
#        event.content = atom.Content(text = content)
#        event.where.append(gdata.calendar.Where(value_string=place))
#        
#        time_now = time.localtime()
#        
#        start_year = start_year or time_now.tm_year
#        start_month = start_month or time_now.tm_mon
#        start_day = start_day or time_now.tm_mday
#
#        if start_hour is None:
#            start_hour = time_now.tm_hour
#            if start_min == 0:
#                start_min = time_now.tm_min
#        
#        start_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((start_year, start_month, start_day, start_hour, start_min, 0, 0, 0, 0)))
#        
#        end_year = end_year or start_year
#        end_month = end_month or start_month
#        end_day = end_day or start_day
#
#        if end_hour is None:
#            end_hour = start_hour + 1
#            if end_min == 0:
#                end_min = start_min
#            
#        end_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.struct_time((end_year, end_month, end_day, end_hour, end_min, 0, 0, 0, 0)))
#        
#        
#        event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
#        
#        path = self._calObj.GetAlternateLink().href
#        path.replace('http:','https:')
#        
##        for trial in range(1, retries+1):
##            try:
##                new_event = self._client.InsertEvent(event, path)
##            except gdata.service.RequestError:
##                ownInit = False
##                q.logger.log('Request Error while creating event "%s" - Retrying #%s of %s'%(title, trial, retries), 2)
##                self._conn._reload()
##            if ownInit:
##                break
##            
##        if ownInit:
##            setattr(self, cleanString(new_event.title.text), Event(self._conn, self._client, self, new_event))
##            q.logger.log('event "%s" created successfully'%title, 2)
##            return new_event
##        else:
##            q.logger.log('Request Error while creating event "%s" - Please Try Later'%title, 2)
#
#
#        new_event = self._client.InsertEvent(event, path)
#        setattr(self, cleanString(new_event.title.text), Event(self._conn, self._client, self, new_event))
#        q.logger.log('event "%s" created successfully'%title, 2)
#        return new_event
    
    def __getitem__(self, key):
        if not object.__getattribute__(self, '_initialized'):
            object.__getattribute__(self, '_initEvents')()
        key = cleanString(key)
        return self.__dict__[key]
    
    def __iter__(self):
        if not self._initialized:
            self._initEvents()
        return GoogleCalIterator(self.__dict__)



class Event(object):
    def __init__(self, calConnection, calClient, parentEvents, eventObject):
        self._client = calClient
        self._parentEvents = parentEvents
        self._conn = calConnection
        self._eventObj = eventObject
        self.title = self._eventObj.title.text
        self._guests = self._eventObj.who
        self.guestEmails = None
        self.guestNames = None
        if not len(self._guests) == 1:
            self.guestEmails = map(lambda guest: guest.email, self._guests)
            self.guestNames = map(lambda guest: guest.name, self._guests)
        self.author = self._eventObj.author[0].name.text
        if not len(self._eventObj.when) == 0:
            self._start_time = self._eventObj.when[0].start_time
            self._end_time = self._eventObj.when[0].end_time
            
            self.starts = Date(self._start_time)
            
            self.ends = Date(self._end_time)
            
        if not len(self._eventObj.where) == 0:
            self.place = self._eventObj.where[0].value_string
        else:
            self.__dict__.pop('place')
    
    @retry(10)
    def inviteGuest(self, name, email=None):
        guest = gdata.calendar.Who()
        guest.valueString = name
        guest.email = email or name
        self._eventObj.who.append(guest)
        self._client.ssl = False
        path = self._eventObj.GetEditLink().href
        path.replace('http:','https:')
        self._client.UpdateEvent(path, self._eventObj)
        if self.guestEmails:
            self.guestEmails.append(guest.email)
            self.guestNames.append(guest.valueString)
        else:
            self.guestEmails = [guest.email]
            self.guestNames = [guest.valueString]
        
    
    @retry(10)
    def delete(self):
        path = self._eventObj.GetEditLink().href
        path.replace('http:','https:')
        self._client.DeleteEvent(path)
        q.logger.log('Event "%s" deleted successfully'%self.title, 2)
        self._parentEvents.__dict__.pop(cleanString(self.title))
    
#    @retry(10)
#    def _delete(self, path):
#        self._client.DeleteEvent(path)
        
#        for trial in range(1, retries+1):
#            try:
#                self._client.DeleteEvent(path)
#            except gdata.service.RequestError:
#                ownInit = False
#                q.logger.log('Request Error while deleting event "%s" - Retrying #%s of %s'%(self.title, trial, retries), 2)
#                self._conn._reload()
#            else:
#                ownInit = True
#                q.logger.log('Event "%s" deleted successfully'%self.title, 2)
#                self._parentEvents.__dict__.pop(cleanString(self.title))
#                break
#            
#        if not ownInit:
#            q.logger.log('Request Error while deleting event "%s" - Please Try Later'%self.title, 2)
            
            
#    def _delete(self):
#        path = self._eventObj.GetEditLink().href
#        path.replace('http:', 'https:')
#        self._client.DeleteEvent(path)


class Date(object):
    
    def __init__(self, year, month=None, day=None, hour=None, minute=None):
        try:
            int(year)
        except ValueError:
            self.year = year[0:4]
            self.month = year[5:7]
            self.day = year[8:10]
            
            self.hour = year[11:13]
            self.minute = year[14:16]
        else:
            self.year = year
            self.month = month
            self.day = day
            
            self.hour = hour
            self.minute = minute
        
    def __repr__(self):
        return 'Date: %s/%s/%s\nTime: %s:%s'%(self.day, self.month, self.year, self.hour, self.minute)



class GoogleCalIterator(object):
    def __init__(self, dict):
        self.inputDict = dict
        self.attributes = map(lambda attr: self.inputDict[attr], filter(lambda attr: attr not in ['new', 'calendars', 'events', 'delete', None], filter(lambda attr: not attr.startswith('_'), self.inputDict.keys())))
        self.index = 0

    
    def __iter__(self):
        return self
    
    
    def next(self):
        if self.index == len(self.attributes):
            raise StopIteration()
        attr = self.attributes[self.index]
        self.index += 1
        return attr   
        
        

def cleanString(s):
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    s = re.sub('^[^a-zA-Z_]+', '', s)
    return s 



from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import xml.etree.ElementTree as ET
import json
from controllers.handler_base import BaseHandler


numbers_dict = {'zero': 0, ''}

class IndexHandler(BaseHandler):
    @ndb.toplevel
    def get(self):
        self.render_template('index.html')

    @ndb.toplevel
    def post(self):
        data_source = self.request.get('data-source')
        if data_source == 'METAR':
            url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KBFI&hoursBeforeNow=10'
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                flight_category = ET.fromstring(result.content).find('data')[0].find('flight_category').text
                self.response.write(json.dumps({'success': True, 'condition': flight_category}))
        elif data_source == 'AUTO':
            # This is the result of running a recording of Reid Hill View ATIS through HPE Haven, obviously there needs to be improvement here.
            # result = "with their zero for seven zoo when two nine one seven is the one thousand two
            #           one nine point eight three zero one seven Thank you in return I did put a new twenty and where
            #           only one left on porches was about to report request condo tower on one point eight advise on
            #           this or contact you with it was about to depart request condo tower on one point eight advise on
            #           this in contact with we do here with me"
            #
            # Actual transcription by hand
            result = """Reid Hillview information whisky zero zero four seven zulu.  Wind two niner zero at one seven.
                Visibility one zero.  Few clouds five thousand.  Temperature one niner.  Dew point eight.  Altimeter
                three zero one seven.  R-Nav Yankee runway three one right in use.  Landing and departing runways three
                one right, three one left.  All departures advise ground control of your departure request.  Arrivals
                contact tower on one one niner point eight.  Advise on initial contact you have whiskey."""
            split_result = result.split(' ')
            # Some example parsing
            information = split_result[split_result.index('information') + 1]

            self.response.write(json.dumps({'success': True, 'recording': result}))

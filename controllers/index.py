from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import xml.etree.ElementTree as ET
import json
from controllers.handler_base import BaseHandler


class IndexHandler(BaseHandler):
    @ndb.toplevel
    def get(self):
        self.render_template('index.html')

    @ndb.toplevel
    def post(self):
        url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=KBFI&hoursBeforeNow=10'
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            flight_category = ET.fromstring(result.content).find('data')[0].find('flight_category').text
            self.response.write(json.dumps({'success': True, 'condition': flight_category}))

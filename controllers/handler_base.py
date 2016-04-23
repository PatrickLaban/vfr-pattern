import os

import jinja2
import webapp2


dirname = os.path.dirname
path = os.path.join(dirname(dirname(__file__)))
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(path, 'views')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        super(BaseHandler, self).__init__(request, response)
        self.template_values = {}

    def render_template(self, template_path):
        template = JINJA_ENVIRONMENT.get_template(template_path)
        self.response.write(template.render(self.template_values))

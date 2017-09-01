# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(_file_), 'templates')
jinja_env = jinja2.Environment(loader =  jinja2.FileSystemLoader(template_dir), 
	autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):
	subject = db.StringProperty(required = True)
	blog = db.TextProperty(required = True)
	post_date = db.DateTimeProperty(auto_now_add = True)


c = db.execute("SELECT * FROM Blog ORDER BY post_date")
post_list = Blog(*c.fetchmany())


class MainPage(Handler):
	def render_front(self, subject = '', blog = '', error = ''):
		self.render('front.html', subject = subject, blog = blog, error = error)

    def get(self):
    	self.render_front

class NewPostPage(Handler):
	def render_front(self, subject = '', blog = '', error = ''):
		self.render('newpost.html', subject = subject, blog = blog, error = error)

    def post(self):
    	subject = self.request.get('subject')
    	blog = self.request.get('blog')
    	a = Blog(subject = subject, blog = blog)
    	a.put()
    	blog_id = obj.key().id()
    	self.redirect('/blog/blog_id')


app = webapp2.WSGIApplication([
    ('/blog', MainPage), ('/blog/newpost', NewPostPage)
], debug=True)
from google.appengine.api import users
import webapp2, cgi

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MyOpenID' : 'myopenid.com',
}

MAIN_PAGE_HTML = """\
<html>
  <body>
	<p>Hallo, <em>%s</em>! [<a href="%s">uitloggen</a>]</p>
    <form action="/prik" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Prik op het prikbord"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
			self.response.out.write(MAIN_PAGE_HTML % (
				user.nickname(), users.create_logout_url(self.request.uri)))
        else:
            self.response.out.write('Hallo, wereld! Log in via: ')
            for name, uri in providers.items():
                self.response.out.write('[<a href="%s">%s</a>]' % (
                    users.create_login_url(federated_identity=uri), name))

class PrikBord(webapp2.RequestHandler):
	def post(self):
		self.response.write('<html><body>Je bericht:<pre>')
		self.response.write(cgi.escape(self.request.get('content')))
		self.response.write('</pre> [<a href="/">terug</a>]</body></html>')

application = webapp2.WSGIApplication([('/', MainPage),('/prik', PrikBord),], debug=True)

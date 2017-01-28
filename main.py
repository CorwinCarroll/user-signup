import re
import cgi
from string import letters

import webapp2

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Sign-Up</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">User Sign Up</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
    """
    # have_error = False
    # user_name = ""
    # password = ""
    # verify_password = ""
    # user_email = ""

    def get(self):

        edit_header = "<h3>To register, fill out the forms below. </h3>"

        # a form for adding new movies
        username = """
        <form action="/signup" method="post">
            <label>
                Username
                <input type="text" name="username" value=""/>
            </label>
        </form>
        """

        # a form for crossing off movies
        # (first we build a dropdown from the current watchlist items)
        # crossoff_options = ""
        # for movie in getCurrentWatchlist():
        #     crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

        password = """
        <form action="/password" method="post">
            <label>
                Password
                <input type="password" name="password" value=""/>
            </label>
        </form>
        """

        verify = """
        <form action="/password" method="post">
            <label>
                Re-Enter Password
                <input type="password" name="verify" value=""/>
            </label>
        </form>
        """

        email = """
        <form action="/" method="post">
            <label>
                Email (optional)
                <input type="text" name="email" value=""/>
            </label>
            	<br>
                <input type="submit" value="Submit"/>
        </form>
        """

		# """.format(crossoff_options)

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        if error:
            error_element = "<p class='error'>" + cgi.escape(error, quote=True) + "</p>"
        else:
            error_element = ""

        # create the page
        main_content =  edit_header + username + password + verify + email + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)


# class AddMovie(webapp2.RequestHandler):
#     """ Handles requests coming in to '/add'
#         e.g. www.flicklist.com/add
#     """

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.redirect('/', **params)
        else:
            self.redirect('/welcome' + username)

        sentence = "Welcome!"
        content = page_header + "<p>" + sentence + "</p>" + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    # ('/signup', Signup),
    # ('/welcome', Welcome)
], debug=True)
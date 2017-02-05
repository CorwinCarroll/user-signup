import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

def make_form(values):
    form="""
    <form method="POST">
            <table>
                <tr>
                    <td><label>Username:</label></td>
                    <td><input type="text" name="username" value="%(username)s" /></td>
                    <td><span class="error">%(username_error)s</span></td>
                </tr>

                <tr>
                    <td><label>Password:</label></td>
                    <td><input type="password" name="password" value="%(password)s" /></td>
                    <td><span class="error">%(password_error)s</span></td>
                </tr>
                    
                <tr>
                    <td><label>Verify Password:</label></td>
                    <td><input type="password" name="verify" value="%(verify)s" /></td>
                    <td><span class="error">%(verify_error)s</span>
                   
                </tr>

                <tr>
                    <td><label>Email (optional):</label></td>
                    <td><input type="text" name="email" value="%(email)s" /></td>
                    <td><span class="error">%(email_error)s</span></td>
                </tr>

                <tr>
                    <td></td>
                    <td><input type="submit" value="Sign Up!"/></td>
            </table>
        </form>
    """
    return page_header + (form % values) + page_footer

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

USER_PW = re.compile(r"^.{3,20}$")
def valid_password(password):
    return USER_PW.match(password)

USER_EM = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return USER_EM.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            'username': '',
            'password': '',
            'verify': '',
            'email': '',
            'username_error': '',
            'password_error': '',
            'verify_error': '',
            'email_error': ''
        }
        self.response.write(make_form(values))

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        if not username:
            username = ''
        if not password:
            password = ''
        if not verify:
            verify = ''
        if not email:
            email = ''

        values = {
            'username': username,
            'password': password,
            'verify': verify,
            'email': email,
            'username_error': '',
            'password_error': '',
            'verify_error': '',
            'email_error': ''
        }

        if username.isspace() or (username.strip() == ""):
            values['username_error'] = "Please enter a user name"
            have_error = True
        else:
            if not valid_username(username):
                values['username_error'] = "Please enter valid user name"
                have_error = True

        if not valid_password(password):
            values['password'] = ''
            # make a helpful error message
            values['password_error'] = "Please enter valid password"
            have_error = True
            
        if verify != password:
            values['password'] = ''
            values['verify'] = ''
            values['verify_error'] = "Passwords do not match."
            have_error = True

        if (not email.isspace()) and (email.strip() != ""):
            if not valid_email(email):
                values['email_error'] = "Please enter valid email"
                have_error = True

        if have_error:
            self.response.write(make_form(values))
        else:
            self.redirect('/welcome?username=' + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.response.write("<h2>Welcome, " + username + ", to the other side!" + "</h2>")
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
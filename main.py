import webapp2, re, cgi

page_header = """
<html>
    <head>
       <title>User Sign-Up</title>
    <body>
"""

page_footer = """
    </body>
</html>
"""
signup_form = """
<fieldset>
    <legend><a href="/">User Sign Up</a></legend>
    <form action="/welcome" method="post" autocomplete="on">
        <table>
            <tr>
                <td><label for="username"> Username:</label> </td>
                <td><input name="username" type="text" {}></td>
                <td style="color: red;"> {}</td>
            </tr>
            
            <tr>
                <td><label for="password"> Password: </label></td>
                <td><input name="password" type="password"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            
            <tr>
                <td><label for="valid_pw"> Confirm Password:</label></td>
                <td><input name="valid_pw" type="password"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            
            <tr>
                <td><label for="email"> Email (optional):</label></td>
                <td><input name="email" type="text"> </td>
                <td style="color: red;"> {} </td>
            </tr>
            <tr>
                <td></td>
                <td><input type="submit" value="Sign Up!"/> <input type="reset" value="Reset" /></td>

            </tr>
        </table>
    </form>
</fieldset>
"""
def valid_username(username):
    valid = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return valid.match(username)

def valid_email(email):
    valid = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return valid.match(email)

def valid_password(password):
    valid = re.compile(r"^.{3,20}$")
    return valid.match(password)

class MainHandler(webapp2.RequestHandler):
    """ handles index page request """

    # def write_form(self, (un_error, pw_error, vaildpw_error, email_error)=('','','','')):
    #     self.response.write(page_header + signup_form.format(un_error, pw_error, vaildpw_error, email_error) 
    #     + page_footer)
        

    def get(self):
        # self.write_form()

        username = self.request.get('username')
        saved_user = 'value="' + username + '"'

        un_error = self.request.get('un_error')
        un_error_element = '<p class="error">' + un_error + "</p>" if un_error else ""

        
        pw_error = self.request.get('pw_error')
        pw_error_element = '<p class="error">' + pw_error + "</p>" if pw_error else ""
        
        vaildpw_error = self.request.get('vaildpw_error')
        vaildpw_error_element = '<p class="error">' + vaildpw_error + "</p>" if vaildpw_error else ""
        
        email_error = self.request.get('email_error')
        email_error_element = '<p class="error">' + email_error + "</p>" if email_error else ""
        
        self.response.write(page_header + signup_form.format(saved_user, un_error, pw_error, vaildpw_error, email_error) 
        + page_footer)

class Welcome(webapp2.RequestHandler):
    """ handles welcome page request """
    def post(self):
        error = ""
        username = self.request.get('username')
        password = self.request.get('password')
        valid_pw = self.request.get('valid_pw')
        email = self.request.get('email')
        saved_user = 'value="' + username + '"'
        
        if not valid_username(username):
            error += "un_error=Invalid Username"
            
        if not valid_password(password):
            if error != "":
                error += "&"
            error += "pw_error=Invalid Password"
        
        if not password == valid_pw:
            if error != "":
                error += "&"
            error += "vaildpw_error=Passwords do not match"
        
        if email: 
            if not valid_email(email):
                if error != "":
                    error += "&"
                error += "email_error=Invalid Email"

        username = cgi.escape(username)
        password = cgi.escape(password)
        valid_pw = cgi.escape(valid_pw)
        email = cgi.escape(email)
        
        if error != "":
            self.redirect("/?" + error)
            saved_user = 'value="' + username + '"'
 
        self.response.write(page_header + "Welcome to the other side, {}".format(username) + "!" + page_footer)
              

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import cgi
from cgi import escape


def valid_user(name):
    if ' ' not in name:
        return name

def valid_pass(pass_w):
    if pass_w:
        return pass_w

def valid_valid(pass_v, pass_w):
    if pass_v:
        if pass_v == pass_w:
            return pass_v

def valid_email(email):
    if '@' in email:
        if email[-4:]== ".com":
            return email


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">User-Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
main_post = """
<form method = "post">
    <table>
        <tbody>
        <tr>
            <td>
            <label for="username">Username</label>
            </td>
            <td>
            <input name="username" type ="text" value = "%(username)s">
            </td>
            <td class ="error" style ="color: red">%(user_error)s</td>

        </tr>
        <tr>
            <td>
            <label for="password">Password</label>
            </td>
            <td>
            <input name="password" type="password">
            </td>
            <td class ="error" style ="color: red">%(pass_error)s</td>

        </tr>
        <tr>
            <td>
            <label for="verify">Password</label>
            </td>
            <td>
            <input name="verify" type="password">
            </td>
            <td class = "error" style ="color: red">%(verify_error)s</td>

        </tr>
        <tr>
            <td>
            <label for="email">Email(optional)</label>
            <td>
            <input name="email" type="email" value = "%(email)s">
            </td>
            <td class ="error" style ="color: red">%(email_error)s</td>
        </tr>
        </tbody>
    </table>
    <input type = "submit">
</form>

"""


class MainHandler(webapp2.RequestHandler):
    def write_form(self, user_error="", username="", email="", pass_error="", verify_error="", email_error=""):
        self.response.out.write(page_header + main_post % {"user_error": user_error,
                                            "username": username,
                                            "email" : email,
                                            "pass_error": pass_error,
                                            "verify_error": verify_error,
                                            "email_error": email_error
                                            } + page_footer)

    def get(self):
        self.write_form()

    def post(self):
                user_username = valid_user(self.request.get("username"))
                user_password = valid_pass(self.request.get("password"))
                user_validated = valid_valid(self.request.get("verify"), self.request.get("password"))
                user_email = valid_email(self.request.get("email"))

                user_error = ""
                pass_error = ""
                verify_error = ""
                email_error = ""

                if not user_username:
                    user_error = "Username invalid"
                if not user_password:
                    pass_error = "Invalid Password"
                if not user_validated:
                    verify_error = "Invalid Password"
                if not user_email:
                    email_error = "Invalid Email"


                if not (user_username and user_password and user_validated and user_email):
                    self.write_form(user_error, user_username, user_email, pass_error, verify_error, email_error)
                else:
                    self.redirect("/welcome")

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome!")

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/welcome', WelcomeHandler)
], debug=True)

#!/usr/bin/env python
import os
import jinja2
import webapp2
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html", {"User": "Jan Mrhar"})


class EditHandler(BaseHandler):
    def get(self):
        return self.render_template("edit.html", {"Genders": [
            {"id": "M", "label": "male"},
            {"id": "F", "label": "female"},
            {"id": "A", "label": "alien"},
        ],
            "Name": "Jan Mrhar", "Age": 7, "Gender": "A", })


class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")

    def post(self):
        email = self.request.get("email")
        message = self.request.get("message")

        if (len(email) == 0):
            return self.render_template("contact.html", {"Status": "alert", "Message": "Ni veljavnega Email naslova!"})

        if (len(message) < 25):
            return self.render_template("contact.html",
                                        {"Status": "alert", "Message": "Sporocilo mora biti dolgo vsaj 25 znakov!"})

        # formatedMessage = "%s \n\r -------------- \n\r Message sent by: %s" % (message, email)
        #
        # gmailUser = 'jan.jn3@gmail.com'
        # recipient = 'jan.jn3@gmail.com'
        # gmailPassword = 'test123456ASD'
        #
        # msg = MIMEMultipart()
        # msg['From'] = gmailUser
        # msg['To'] = recipient
        # msg['ReplyTo'] = email
        # msg['Subject'] = "Sent from contact form"
        #
        # msg.attach(MIMEText(formatedMessage))
        # mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        # mailServer.ehlo()
        # mailServer.starttls()
        # mailServer.ehlo()
        # mailServer.login(gmailUser, gmailPassword)
        # mailServer.sendmail(gmailUser, recipient, msg.as_string())
        # mailServer.close()

        return self.render_template("contact.html", {"Status": "success", "Message": "Email uspesno poslan!"})


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/edit', EditHandler),
    webapp2.Route('/save-user', EditHandler),
    webapp2.Route('/contact-us', ContactHandler),
], debug=True)

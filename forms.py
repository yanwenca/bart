from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

#RegisterForm
class UserForm(FlaskForm): 
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=60)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=60)])

#LoginForm
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=60)])

'''
#TripForm
class TripForm(FlaskForm):
    ROUTE_ABBREV = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')
                
    state = wtforms.SelectField(label='State', 
            choices=[(state, state) for state in STATE_ABBREV])


List out sequence of API calls
1- get a list of all routes
2- get a list of all stations
3- get a list of depart time

* try on Insomnia and figure out if the response data is what i want
USER CLICK SEARCH -> basic route - select routes
FETCH STATION FROM DROP DOWN 

rest response
user select 

how to call from API
what you get from API?


#API data pull: 
#Routes: http://api.bart.gov/docs/route/routes.aspx 
#Departing Station: http://api.bart.gov/docs/stn/stns.aspx 
#Arrival Station: http://api.bart.gov/docs/stn/stns.aspx 
#Departure Time: http://api.bart.gov/docs/sched/depart.aspx 


'''

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""

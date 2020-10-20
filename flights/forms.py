import datetime

from django.forms import Form, ChoiceField, DateField, DateTimeInput, DateInput

from flights.models import Flight


class FlightForm(Form):
    flights = ChoiceField(choices=[], required='true')
    date = DateField(initial=datetime.date.today, widget=DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        self.fields['flights'].choices = [(x.pk, x.get_full_name()) for x in Flight.objects.all()]


from django import forms
from trip.models import Trip, TripEmp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django_summernote.widgets import SummernoteWidget
class DateInput(forms.DateInput):
	input_type = 'date'


class TripForm(forms.ModelForm):
    description = forms.CharField(label="Deskrisaun", widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}), required=False)
    date_out = forms.DateField(widget=DateInput(), required=False)
    date_in = forms.DateField(widget=DateInput(), required=False)
    class Meta:
        model = Trip
        fields = ['name','ttype','country','municipality','date_out','date_in',\
            'file', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = 'Assuntu'
        self.fields['file'].label = 'Pareser'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('ttype', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('municipality', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_out', css_class='form-group col-md-4 mb-0'),
                Column('date_in', css_class='form-group col-md-4 mb-0'),
                Column('file', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class TripEmpForm(forms.ModelForm):
    class Meta:
        model = TripEmp
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['employee'].label = 'Hili Staff'
        self.fields['employee'].required = True
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
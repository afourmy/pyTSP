from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField

class CreationForm(FlaskForm):
    validators = [FileAllowed(['xls', 'xlsx'], 'Excel file only')]
    file = FileField()

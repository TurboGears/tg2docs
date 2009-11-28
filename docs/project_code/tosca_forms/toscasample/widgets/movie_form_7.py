"""Movie Form"""

from tw.api import CSSLink
from tw.forms import (TableForm, CalendarDatePicker,
    SingleSelectField, Spacer, TextField, TextArea, FileField)
from tw.forms.validators import Int, NotEmpty, DateConverter
from tg import url

class MovieForm(TableForm):

    template = "toscasample.widgets.templates.table_form"
    css = [CSSLink(link=url('/css/tooltips.css'))]
    show_errors = True
    genre_options = [x for x in enumerate((
        'Action & Adventure', 'Animation', 'Comedy',
        'Documentary', 'Drama', 'Sci-Fi & Fantasy'))]

    fields = [
        TextField('title', validator=NotEmpty,
            label_text='Movie Title',
            help_text='Please enter the full title of the movie.'),
        Spacer(),
        TextField('year', validator=Int(min=1900, max=2100), size=4,
            help_text='Please enter the year this movie was made.'),
        CalendarDatePicker('release_date', validator=DateConverter(),
            help_text='Please pick the exact release date.'),
        SingleSelectField('genre', options=genre_options,
            help_text = 'Please choose the genre of the movie.'),
        Spacer(),
        TextArea('description', attrs=dict(rows=3, cols=25),
            help_text = 'Please provide a short description of the plot.'),
        Spacer(),
        FileField('picture_filename',
            help_text = 'Please provide a picture for this movie.'),
        Spacer()

    ]

    submit_text = 'Save Movie'


create_movie_form = MovieForm("create_movie_form",  action='create')

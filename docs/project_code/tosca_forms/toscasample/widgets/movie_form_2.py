"""Movie Form"""

from tw.forms import (TableForm, CalendarDatePicker, Label,
    SingleSelectField, Spacer, TextField, TextArea)


class MovieForm(TableForm):

    genre_options = [x for x in enumerate((
        'Action & Adventure', 'Animation', 'Comedy',
        'Documentary', 'Drama', 'Sci-Fi & Fantasy'))]

    fields = [
        TextField('title', label_text='Movie Title'),
        Spacer(),
        TextField('year', size=4),
        CalendarDatePicker('release_date', date_format='%y-%m-%d'),
        SingleSelectField('genre', options=genre_options),
        Spacer(),
        Label(text='Please provide a short description of the plot:'),
        TextArea('description', attrs=dict(rows=3, cols=25)),
        Spacer()]

    submit_text = 'Save Movie'


create_movie_form = MovieForm("create_movie_form")

"""Movie Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class MovieForm(TableForm):

    class fields(WidgetsList):
        title = TextField()
        year = TextField()
        release_date = CalendarDatePicker()
        genre_options = [x for x in enumerate((
            'Action & Adventure', 'Animation', 'Comedy',
            'Documentary', 'Drama', 'Sci-Fi & Fantasy'))]
        genre = SingleSelectField(options=genre_options)
        description = TextArea()


create_movie_form = MovieForm("create_movie_form")

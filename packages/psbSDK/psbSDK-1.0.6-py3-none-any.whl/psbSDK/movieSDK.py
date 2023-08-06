from movieAPI import MovieAPI
from movieFilters import Filters
import json

class Movies:
    def __init__(self, Token=None, Type="MovieList", MovieId=None, FilterObj=None):
        self.Token = Token
        self.Type = Type
        self.MovieId = MovieId
        self.FilterObj = FilterObj

    def get_movie(self):
        m = MovieAPI(movieObj=self)
        return json.dumps(m.get_movie(), sort_keys=True, indent=4)

    def get_movie_by_name(self, Name=None):
        if Name:
            obj = Filters()
            obj.add_filter(field="name", oper="eq", value=Name)
            self.FilterObj = obj

            m = MovieAPI(movieObj=self)
            return json.dumps(m.get_movie(), sort_keys=True, indent=4)
        else:
            raise Exception("Please provide a Name")

import requests

class MovieAPI:
    def __init__(self, movieObj=None):
        self.base_url = "https://the-one-api.dev/v2"
        self.headers = {"Accept": "application/json", "Authorization": f"Bearer {movieObj.Token}"}
        self.MovieId = movieObj.MovieId
        self.MovieType = movieObj.Type
        self.filterObj = None
        if movieObj.FilterObj:
            self.filterObj = self.parse_filter(movieObj.FilterObj.filters)
    
    def parse_filter(self, obj):
        filter = ""
        for op, values in obj.items():
            for v in values:
                if v[0]:
                    filter += str(v[0])
                filter += str(op)+str(v[1])
                filter += "&"
        return filter[:-1]
    
    def form_url(self):
        url = f"{self.base_url}"
        if self.MovieType == "MovieList":
            url = url + "/movie"
        elif self.MovieType == "MovieId":
            url += f"/movie/{self.MovieId}"
        elif self.MovieType == "MovieQuotes":
            url += f"/movie/{self.MovieId}/quote"
        
        if self.filterObj:
            url += "?" + self.filterObj
        return url

    def get_movie(self):
        url = self.form_url()
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            return "An Http Error occurred:" + str(response.status_code) + "-" + response.reason
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred\n" + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred\n" + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred\n" + repr(err)
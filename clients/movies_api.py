from custom_requester.custom_requester import CustomRequester
from config.base_urls import API_BASE_URL

MOVIES = "/movies"

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_movies(self, params=None, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            params=params,
            **kwargs
        )

    def create_movie(self, movie_data, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            data=movie_data,
            **kwargs
        )

    def get_movie(self, movie_id, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}",
            **kwargs
        )

    def delete_movie(self, movie_id, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}",
            **kwargs
        )

    def update_movie(self, movie_id, movie_data, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            data=movie_data,
            **kwargs
        )


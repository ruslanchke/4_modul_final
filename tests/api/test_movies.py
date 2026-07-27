import requests
from config.base_urls import API_BASE_URL
from custom_requester.custom_requester import CustomRequester

def test_get_movies():
    session = requests.Session()
    requester = CustomRequester(session=session, base_url=API_BASE_URL)

    response = requester.send_request(
        "GET",
        "/movies",
        params={"page": 1, "pageSize": 1}
    )

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200
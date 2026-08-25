import datetime

import pytz
import requests
from pydantic import BaseModel, Field


class WorldClockResponse(BaseModel):
    id: str = Field(alias="$id")
    currentDateTime: str
    utcOffset: str
    isDayLightSavingsTime: bool
    dayOfTheWeek: str
    timeZoneName: str
    currentFileTime: int
    ordinalDate: str
    serviceResponse: None

    class Config:
        populate_by_name = True


class DateTimeRequest(BaseModel):
    currentDateTime: str


class WhatIsTodayResponse(BaseModel):
    message: str


def get_worldclockapi_time() -> WorldClockResponse:
    response = requests.get(
        "http://worldclockapi.com/api/json/utc/now"
    )

    assert response.status_code == 200, "WorldClockAPI недоступен"

    return WorldClockResponse(**response.json())


class TestTodayIsHolidayServiceAPI:

    def test_worldclockapi(self):
        world_clock_response = get_worldclockapi_time()

        current_date_time = world_clock_response.currentDateTime

        print(f"Текущая дата и время: {current_date_time=}")

        assert current_date_time == datetime.datetime.now(
            pytz.utc
        ).strftime("%Y-%m-%dT%H:%MZ")

    def test_what_is_today(self):
        world_clock_response = get_worldclockapi_time()

        request_data = DateTimeRequest(
            currentDateTime=world_clock_response.currentDateTime
        )

        response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            json=request_data.model_dump()
        )

        assert response.status_code == 200

        what_is_today_data = WhatIsTodayResponse(
            **response.json()
        )

        assert what_is_today_data.message == (
            "Сегодня нет праздников в России."
        )
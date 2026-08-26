import allure
import datetime
import pytest
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

    @allure.epic("Cinescope API")
    @allure.feature("Интеграция с внешними сервисами")
    @allure.story("Получение текущего времени")
    @allure.title("Проверка WorldClockAPI")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.integration
    def test_worldclockapi(self):

        with allure.step("Получить текущее время из WorldClockAPI"):
            world_clock_response = get_worldclockapi_time()

        current_date_time = world_clock_response.currentDateTime

        with allure.step("Проверить соответствие текущей даты и времени"):
            assert current_date_time == datetime.datetime.now(
                pytz.utc
            ).strftime("%Y-%m-%dT%H:%MZ")


    @allure.epic("Cinescope API")
    @allure.feature("Интеграция с внешними сервисами")
    @allure.story("Проверка сервиса TodayIsHoliday")
    @allure.title("Определение праздника по текущей дате")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.integration
    def test_what_is_today(self):

        with allure.step("Получить текущую дату из WorldClockAPI"):
            world_clock_response = get_worldclockapi_time()

        with allure.step("Подготовить данные для TodayIsHoliday"):
            request_data = DateTimeRequest(
                currentDateTime=world_clock_response.currentDateTime
            )

        with allure.step("Отправить запрос в TodayIsHoliday"):
            response = requests.post(
                "http://127.0.0.1:16002/what_is_today",
                json=request_data.model_dump()
            )

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200

        with allure.step("Провалидировать схему ответа"):
            what_is_today_data = WhatIsTodayResponse(
                **response.json()
            )

        with allure.step("Проверить название праздника"):
            assert what_is_today_data.message == (
                "Сегодня нет праздников в России."
            )
import aiohttp
import jwt
import math
from ..utils import bcolors
from ..utils import RequestError
from ..utils import DataNull
import sys


def get_customer_id(token):
    try:
        btoken = bytes(token, encoding="utf-8")
        jwt_object = jwt.decode(
            btoken, algorithms=["HS256"], options={"verify_signature": False}
        )
        return jwt_object["customerId"]

    except Exception as error:
        print(f"\n{bcolors.FAIL}TokenError: token invalid\n")
        sys.exit(1)


class Request:
    def __init__(self, endpoint, token_config, get_customer_id):
        self.__endpoint = endpoint
        self.__token = token_config.token()
        self.__header = token_config.auth_header()
        self.__customer_id = get_customer_id

    def api_meta_string(self):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/{self.__endpoint}"

    def api_data_string(self, page):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/{self.__endpoint}?page={page}"

    def api_summary_meta_string(self, timestamp):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/cc/summaries/{self.__endpoint}?timestamp={timestamp}"

    def api_summary_data_string(self, timestamp, page):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/cc/summaries/{self.__endpoint}?timestamp={timestamp}&page={page}"

    def api_summary_event_meta_string(self, agent_event_id):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/cc/summaries/{self.__endpoint}?agentEventId={agent_event_id}"
    
    def api_summary_event_data_string(self, page, agent_event_id):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/cc/summaries/{self.__endpoint}?page={page}&agentEventId={agent_event_id}"
    
    def api_summary_event_timestamp_meta_string(self, timestamp):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/cc/summaries/{self.__endpoint}?timestamp={timestamp}"
    
    def api_summary_event_timestamp_data_string(self, timestamp, page):
        return f"https://{self.__customer_id}.api.vonixcc.com.br/cc/summaries/{self.__endpoint}?timestamp={timestamp}&page={page}"
   

    async def async_meta_request(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    self.api_meta_string(), headers=self.__header
                ) as response:
                    data = await response.json()
                    status = response.status

                if "Message" in data:
                    raise RequestError("Failure to request data from API")

                if data["meta"]["count"] == 0:
                    raise DataNull()

            except RequestError as error:
                raise SystemExit(f"\n{str(error)}") from error
            except DataNull as error:
                raise SystemExit(f"\n{str(error)}") from error

        api_page = 50
        pages = math.ceil(data["meta"]["count"] / api_page)

        if pages < 1:
            pages = 0

        return pages

    async def async_data_request(self, page):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_data_string(page), headers=self.__header
            ) as response:
                data = await response.json()
                data_array = data["data"]

            return data_array

    async def async_summary_meta_request(self, timestamp):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_summary_meta_string(timestamp), headers=self.__header
                ) as response:
                    data = await response.json()
                    status = response.status

            if "Message" in data:
                raise RequestError(data["Message"], status)

            if data["meta"]["count"] == 0:
                raise DataNull(status)

        except RequestError as error:
            raise SystemExit(f"\n{str(error)}") from error

        except DataNull as error:
            print(SystemExit(f"\n{str(error)}"))
            return 0

        api_page = 50

        pages = math.ceil(data["meta"]["count"] / api_page)

        if pages < 1:
            pages = 0

        return pages

    async def async_summary_data_request(self, timestamp, page):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_summary_data_string(timestamp, page),
                headers=self.__header,
            ) as response:
                data = await response.json()
                data_array = data["data"]

            return data_array

    async def async_summary_event_meta_request(self, agent_event_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_summary_event_meta_string(agent_event_id),
                    headers=self.__header,
                ) as response:
                    data = await response.json()
                    status = response.status

            if "message" in data:
                raise RequestError(data["message"], status)
            if data["meta"]["count"] == 0:
                raise DataNull(status)

        except RequestError as error:
            raise SystemExit(f"\n{str(error)}") from error

        except DataNull as error:
            print(SystemExit(f"\n{str(error)}"))
            return 0

        api_page = 50

        pages = math.ceil(data["meta"]["count"] / api_page)

        if pages < 1:
            pages = 0

        return pages

    async def async_summary_event_data_request(self, page, agent_event_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_summary_event_data_string(page, agent_event_id),
                headers=self.__header,
            ) as response:
                data = await response.json()
                data_array = data["data"]

            return data_array

    async def async_summary_event_timestamp_meta_request(self, agent_event_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_summary_event_timestamp_meta_string(agent_event_id),
                    headers=self.__header,
                ) as response:
                    data = await response.json()
                    status = response.status

            if "message" in data:
                raise RequestError(data["message"], status)
            if data["meta"]["count"] == 0:
                raise DataNull(status)

        except RequestError as error:
            raise SystemExit(f"\n{str(error)}") from error

        except DataNull as error:
            print(SystemExit(f"\n{str(error)}"))
            return 0

        api_page = 50

        pages = math.ceil(data["meta"]["count"] / api_page)

        if pages < 1:
            pages = 0

        return pages

    async def async_summary_event_timestamp_data_request(self, page, timestamp):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.api_summary_event_timestamp_data_string(timestamp, page),
                headers=self.__header,
            ) as response:
                data = await response.json()
                data_array = data["data"]

            return data_array

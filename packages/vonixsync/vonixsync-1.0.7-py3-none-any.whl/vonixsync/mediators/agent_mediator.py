import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import (
    fxn,
    print_finalized,
    NullPages,
)


async def sync_agent(request, repository_dict):
    if "agent" not in repository_dict:
        return

    try:
        pages = await request.async_meta_request()

        if pages == 0:
            raise NullPages("the agent list")

    except NullPages as error:
        print(SystemExit(f"\n{str(error)}"))

    last_page = pages + 1
    try:
        for page in range(1, last_page):
            data_array = await request.async_data_request(page)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    for agent in data_array:
                        repository_dict["agent"].insert(
                            int(agent["id"]),
                            agent["name"],
                            agent["nickname"],
                            agent["active"],
                            agent["defaultQueueId"],
                        )

            except IntegrityError as error:
                pass
    finally:
        print_finalized("the agent list")

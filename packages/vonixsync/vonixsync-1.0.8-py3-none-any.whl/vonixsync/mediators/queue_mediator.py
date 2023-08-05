import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import fxn, print_finalized, NullPages


async def sync_queue(request, repository_dict):
    if "queue" not in repository_dict:
        return

    try:
        pages = await request.async_meta_request()

        if pages == 0:
            raise NullPages("the queue list")

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
                    for queue in data_array:
                        repository_dict["queue"].insert(
                            queue["id"],
                            queue["name"],
                            queue["description"],
                            queue["directionIn"],
                            queue["directionOut"],
                            queue["directionAuto"],
                            queue["dialerMode"],
                        )

            except IntegrityError as error:
                pass
    finally:
        print_finalized("the queue lists")

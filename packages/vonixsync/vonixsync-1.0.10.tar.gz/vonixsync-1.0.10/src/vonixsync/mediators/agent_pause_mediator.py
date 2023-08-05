import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import (
    fxn,
    print_finalized,
    NullPages,
)


async def sync_agent_pause(request, repository_dict, query_timestamp):
    if "agent_pause" not in repository_dict:
        return

    timestamp = repository_dict["agent_pause"].select_date(query_timestamp)

    try:
        pages = await request.async_summary_meta_request(timestamp)
        if pages == 0:
            raise NullPages("the agent pause summary")

    except NullPages as error:
        print(SystemExit(f"\n{str(error)}"))

    last_page = pages + 1
    try:
        for page in range(1, last_page):
            data_array = await request.async_summary_data_request(timestamp, page)
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    for agent_pause in data_array:
                        repository_dict["agent_pause"].insert(
                            agent_pause["agentId"],
                            agent_pause["queueId"],
                            agent_pause["period"],
                            agent_pause["pauseSecs"],
                            agent_pause["pauseReasonId"],
                        )
            except IntegrityError as error:
                pass
    finally:
        print_finalized("the agent summary pauses")

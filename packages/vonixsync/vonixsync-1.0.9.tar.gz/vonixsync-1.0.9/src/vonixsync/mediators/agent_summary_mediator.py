import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import (
    fxn,
    print_finalized,
    NullPages,
)


async def sync_agent_summary(request, repository_dict, query_timestamp):
    if "agent_summary" not in repository_dict:
        return
    timestamp = repository_dict["agent_summary"].select_date(query_timestamp)

    try:
        pages = await request.async_summary_meta_request(timestamp)

        if pages == 0:
            raise NullPages("the agent summary list")

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
                    for agent_summary in data_array:
                        repository_dict["agent_summary"].insert(
                            agent_summary["agentId"],
                            agent_summary["queueId"],
                            agent_summary["period"],
                            agent_summary["inCompleted"],
                            agent_summary["outCompleted"],
                            agent_summary["outDiscarded"],
                            agent_summary["autoCompleted"],
                            agent_summary["rejections"],
                            agent_summary["loginSecs"],
                            agent_summary["pauseSecs"],
                            agent_summary["inRingSecs"],
                            agent_summary["outRingSecs"],
                            agent_summary["inCallSecs"],
                            agent_summary["outCallSecs"],
                            agent_summary["autoCallSecs"],
                            agent_summary["callSecs"],
                            agent_summary["ringSecs"],
                        )
            except IntegrityError as error:
                pass
    finally:
        print_finalized("the agent summary list")

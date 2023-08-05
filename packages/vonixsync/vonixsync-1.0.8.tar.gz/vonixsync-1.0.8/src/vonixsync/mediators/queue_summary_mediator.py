import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import fxn, print_finalized, NullPages


async def sync_queue_summary(request, repository_dict, query_timestamp):
    if "queue_summary" not in repository_dict:
        return
    timestamp = repository_dict["queue_summary"].select_date(query_timestamp)

    try:
        pages = await request.async_summary_meta_request(timestamp)

        if pages == 0:
            raise NullPages("the queue summary list")

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
                    for queue_summary in data_array:
                        repository_dict["queue_summary"].insert(
                            queue_summary["queueId"],
                            queue_summary["period"],
                            queue_summary["inCompleted"],
                            queue_summary["inTransferred"],
                            queue_summary["inAbandoned"],
                            queue_summary["inCompletedSla"],
                            queue_summary["inAbandonedSla"],
                            queue_summary["outCompleted"],
                            queue_summary["outTransferred"],
                            queue_summary["outDiscarded"],
                            queue_summary["autoCompleted"],
                            queue_summary["autoTransferred"],
                            queue_summary["autoDiscarded"],
                            queue_summary["autoAbandoned"],
                            queue_summary["inCallSecs"],
                            queue_summary["outCallSecs"],
                            queue_summary["autoCallSecs"],
                            queue_summary["inHoldSecsCompleted"],
                            queue_summary["inHoldSecsAbandoned"],
                            queue_summary["outTrySecsCompleted"],
                            queue_summary["outTrySecsDiscarded"],
                            queue_summary["autoHoldSecsCompleted"],
                            queue_summary["autoHoldSecsAbandoned"],
                            queue_summary["autoTrySecsCompleted"],
                            queue_summary["autoTrySecsDiscarded"],
                        )

            except IntegrityError as error:
                pass
    finally:
        print_finalized("the queue summary lists")

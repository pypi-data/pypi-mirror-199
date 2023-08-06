import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import (
    fxn,
    print_finalized,
    NullPages,
)


async def sync_call(request, repository_dict, query_timestamp):
    if "call" not in repository_dict:
        return
    call_rating_declared_by_user = "call_rating" in repository_dict
    tree_declared_by_user = "trees" in repository_dict
    profilers_declared_by_user = "profilers" in repository_dict
    timestamp = repository_dict["call"].select_date(query_timestamp)

    try:
        pages = await request.async_summary_meta_request(timestamp)

        if pages == 0:
            raise NullPages("the call summary")

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
                    for call in data_array:
                        repository_dict["call"].insert(
                            call["id"],
                            call["queueId"],
                            call["direction"],
                            call["agentOffers"],
                            call["callerNumber"],
                            call["callerInfo"],
                            call["holdSecs"],
                            call["talkSecs"],
                            call["ringSecs"],
                            call["status"],
                            call["reason"],
                            call["localityId"],
                            call["callTypeId"],
                            call["trunkingId"],
                            None,
                            call["abandonKey"],
                            call["initialPosition"],
                            call["abandonPosition"],
                            call["createdAt"],
                            call["answerAt"],
                            call["hangupAt"],
                            call["transferredTo"],
                            call["agentId"],
                        )

                        if profilers_declared_by_user:
                            profiler_array = call["profilers"]
                            profiler_array_length = len(profiler_array)

                            if profiler_array_length > 0:
                                for profiler in profiler_array:
                                    repository_dict["profilers"].insert(
                                        profiler["id"],
                                        profiler["callId"],
                                        0,
                                        profiler["createdAt"],
                                        profiler["name"],
                                        profiler["value"],
                                    )

                        if tree_declared_by_user:
                            tree_array = call["trees"]
                            tree_array_length = len(tree_array)

                            if tree_array_length > 0:
                                for tree in tree_array:
                                    repository_dict["trees"].insert(
                                        tree["id"],
                                        tree["callId"],
                                        0,
                                        call["createdAt"],
                                        tree["label"],
                                    )

                        if call_rating_declared_by_user == True:
                            call_rating_array = call["callsRatings"]
                            call_rating_array_length = len(call_rating_array)

                            if call_rating_array_length > 0:
                                for call_rating in call_rating_array:
                                    repository_dict["call_rating"].insert(
                                        call_rating["callId"],
                                        call_rating["name"],
                                        call_rating["createdAt"],
                                        call_rating["value"],
                                    )

            except IntegrityError as error:
                pass

    finally:
        print_finalized("the call summary list")
        if call_rating_declared_by_user:
            print_finalized("the call ratings")
        if profilers_declared_by_user:
            print_finalized("the profilers")
        if tree_declared_by_user:
            print_finalized("the trees")

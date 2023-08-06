import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import (
    fxn,
    print_finalized,
    NullPages,
)


async def sync_chat(request, repository_dict, query_timestamp):
    if "chat" not in repository_dict:
        return

    chat_message_declared_by_user = "chat_message" in repository_dict
    profilers_declared_by_user = "profilers" in repository_dict
    tree_declared_by_user = "trees" in repository_dict

    timestamp = repository_dict["chat"].select_date(query_timestamp)
    try:
        pages = await request.async_summary_meta_request(timestamp)
        if pages == 0:
            raise NullPages("the chat summary")

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
                    for chat in data_array:
                        repository_dict["chat"].insert(
                            chat["id"],
                            chat["agentId"],
                            chat["queueId"],
                            chat["source"],
                            chat["sourceId"],
                            chat["name"],
                            chat["direction"],
                            chat["status"],
                            chat["holdSecs"],
                            chat["talkSecs"],
                            chat["chatSecs"],
                            chat["createdAt"],
                            chat["answeredAt"],
                            chat["finishedAt"],
                        )

                        if chat_message_declared_by_user:
                            chat_message_array = chat["chatMessages"]
                            chat_message_array_length = len(chat_message_array)

                            if chat_message_array_length > 0:
                                for message in chat_message_array:
                                    repository_dict["chat_message"].insert(
                                        message["chatId"],
                                        message["id"],
                                        message["message"],
                                        message["direction"],
                                        message["createdAt"],
                                        message["deliveredAt"],
                                        message["readedAt"],
                                        message["answeredAt"],
                                        message["type"],
                                    )

                        if profilers_declared_by_user:
                            profiler_array = chat["profilers"]
                            profiler_array_length = len(profiler_array)

                            if profiler_array_length > 0:
                                for profiler in profiler_array:
                                    repository_dict["profilers"].insert(
                                        profiler["id"],
                                        "0",
                                        profiler["chatId"],
                                        profiler["createdAt"],
                                        profiler["name"],
                                        profiler["value"],
                                    )

                        if tree_declared_by_user:
                            tree_array = chat["trees"]
                            tree_array_length = len(tree_array)

                            if tree_array_length > 0:
                                for tree in tree_array:
                                    repository_dict["trees"].insert(
                                        tree["id"],
                                        "0",
                                        tree["chatId"],
                                        chat["createdAt"],
                                        tree["label"],
                                    )

            except IntegrityError as error:
                pass

    finally:
        print_finalized("the chat summary list")
        if chat_message_declared_by_user:
            print_finalized("the chat messages")
        if profilers_declared_by_user:
            print_finalized("the profilers")
        if tree_declared_by_user:
            print_finalized("the trees")

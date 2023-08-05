import warnings
from sqlalchemy.exc import IntegrityError
from ..utils import (
    fxn,
    print_finalized,
    NullPages,
)


async def sync_agent_event(request, repository_dict,timestamp):
    if "agent_event" not in repository_dict:
        return

    agent_event_id = repository_dict["agent_event"].select_agent_event_id()

    try:
        
        agent_event_table_is_empty = agent_event_id is None
        
        if agent_event_table_is_empty:
            pages = await request.async_summary_event_timestamp_meta_request(timestamp)
        
        if not agent_event_table_is_empty:
            pages = await request.async_summary_event_meta_request(agent_event_id)

        if pages == 0:
            raise NullPages("the agent event history")

    except NullPages as error:
        print(SystemExit(f"\n{str(error)}"))

    last_page = pages + 1
    
    try:
        for page in range(1, last_page):
            
            if agent_event_table_is_empty:
                 data_array = await request.async_summary_event_timestamp_data_request(
                    page, timestamp
                )
            if not agent_event_table_is_empty:    
                data_array = await request.async_summary_event_data_request(
                    page, agent_event_id
                )
                
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    for agent_event in data_array:
                        if "event" not in agent_event:
                            continue

                        if "reason" not in agent_event and "extensionId" in agent_event:
                            repository_dict["agent_event"].insert(
                                agent_event["id"],
                                agent_event["createdAt"],
                                agent_event["queueId"],
                                agent_event["agentId"],
                                agent_event["event"],
                                None,
                                agent_event["extensionId"],
                            )
                            continue

                        if "extensionId" not in agent_event and "reason" in agent_event:
                            repository_dict["agent_event"].insert(
                                agent_event["id"],
                                agent_event["createdAt"],
                                agent_event["queueId"],
                                agent_event["agentId"],
                                agent_event["event"],
                                agent_event["reason"],
                                None,
                            )
                            continue

                        repository_dict["agent_event"].insert(
                            agent_event["id"],
                            agent_event["createdAt"],
                            agent_event["queueId"],
                            agent_event["agentId"],
                            agent_event["event"],
                            agent_event["reason"],
                            agent_event["extensionId"],
                        )

            except IntegrityError as error:
                pass
    finally:
        print_finalized("the agent event history")

import asyncio
import sys
from ..api import Request, get_customer_id
from ..configs import UserConfigs
from ..mediators import sync_agent
from ..mediators import sync_agent_pause
from ..mediators import sync_agent_summary
from ..mediators import sync_call
from ..mediators import sync_chat
from ..mediators import sync_queue
from ..mediators import sync_queue_summary
from ..mediators import sync_agent_event

from ..repository import AgentsRepository
from ..repository import AgentSummaryRepository
from ..repository import AgentPauseRepository
from ..repository import QueueRepository
from ..repository import QueueSummaryRepository
from ..repository import ProfilerRepository
from ..repository import CallRatingRepository
from ..repository import CallRepository
from ..repository import ChatMessageRepository
from ..repository import ChatRepository
from ..repository import TreeRepository
from ..repository import AgentEventRepository

from ..utils import TokenError

from .create_database import create_database


class Syncronizer:
    def __init__(
        self,
        token=None,
        connection=None,
        fromPeriod=None,
        echo=False,
        agent_event="",
        agent_pause="",
        agent_summary="",
        agent="",
        call_rating="",
        calls="",
        chat_message="",
        chat="",
        queue_summary="",
        queue="",
        profilers="",
        trees="",
    ):
        try:
            self.__token = token
            self.__string_connection = connection
            self.__echo = echo
            self.agent_table_name = agent
            self.agent_event_table_name = agent_event
            self.agent_pause_table_name = agent_pause
            self.agent_summary_table_name = agent_summary
            self.call_rating_table_name = call_rating
            self.calls_table_name = calls
            self.chat_message_table_name = chat_message
            self.chat_table_name = chat
            self.queue_summary_table_name = queue_summary
            self.queue_table_name = queue
            self.profiler_table_name = profilers
            self.tree_table_name = trees
            self.__repositories_connected = self.__configure_repositories(self.__echo)
            self.__timestamp = fromPeriod
            self.__customer_id = get_customer_id(self.__token)

            if self.__token == None:
                raise TokenError("token was not provided\n")
        except TokenError as error:
            print(SystemExit(f"\n{str(error)}"))
            sys.exit(1)

    def __configure_repositories(self, echo):
        columns_choosen = {}
        declared_columns = {
            "agent_event": self.agent_event_table_name,
            "agent_pause": self.agent_pause_table_name,
            "agent_summary": self.agent_summary_table_name,
            "agent": self.agent_table_name,
            "call_rating": self.call_rating_table_name,
            "call": self.calls_table_name,
            "chat_message": self.chat_message_table_name,
            "chat": self.chat_table_name,
            "profilers": self.profiler_table_name,
            "queue_summary": self.queue_summary_table_name,
            "queue": self.queue_table_name,
            "trees": self.tree_table_name,
        }
        repository_dictionary = {
            "agent_event": AgentEventRepository(
                self.__string_connection, self.agent_event_table_name, echo
            ),
            "agent_pause": AgentPauseRepository(
                self.__string_connection, self.agent_pause_table_name, echo
            ),
            "agent_summary": AgentSummaryRepository(
                self.__string_connection, self.agent_summary_table_name, echo
            ),
            "agent": AgentsRepository(
                self.__string_connection, self.agent_table_name, echo
            ),
            "call_rating": CallRatingRepository(
                self.__string_connection, self.call_rating_table_name, echo
            ),
            "call": CallRepository(
                self.__string_connection, self.calls_table_name, echo
            ),
            "chat_message": ChatMessageRepository(
                self.__string_connection, self.chat_message_table_name, echo
            ),
            "chat": ChatRepository(
                self.__string_connection, self.chat_table_name, echo
            ),
            "profilers": ProfilerRepository(
                self.__string_connection, self.profiler_table_name, echo
            ),
            "queue_summary": QueueSummaryRepository(
                self.__string_connection, self.queue_summary_table_name, echo
            ),
            "queue": QueueRepository(
                self.__string_connection, self.queue_table_name, echo
            ),
            "trees": TreeRepository(
                self.__string_connection, self.tree_table_name, echo
            ),
        }

        for key, value in declared_columns.items():
            if value != "":
                columns_choosen.update({key: repository_dictionary[key]})

        return columns_choosen

    def syncronize(self):
        create_database(
            database_connection=self.__string_connection,
            agent_event_table_name=self.agent_event_table_name,
            agent_pause_table_name=self.agent_pause_table_name,
            agent_summary_table_name=self.agent_summary_table_name,
            agent_table_name=self.agent_table_name,
            call_rating_table_name=self.call_rating_table_name,
            calls_table_name=self.calls_table_name,
            chat_message_table_name=self.chat_message_table_name,
            chat_table_name=self.chat_table_name,
            profiler_table_name=self.profiler_table_name,
            queue_summary_table_name=self.queue_summary_table_name,
            queue_table_name=self.queue_table_name,
            tree_table_name=self.tree_table_name,
            echo=self.__echo,
        )

        connected_repositories = self.__repositories_connected

        return (
            asyncio.run(
                sync_call(
                    Request("calls", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                    self.__timestamp,
                )
            ),
            asyncio.run(
                sync_agent(
                    Request("agents", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                )
            ),
            asyncio.run(
                sync_agent_pause(
                    Request("pauses", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                    self.__timestamp,
                )
            ),
            asyncio.run(
                sync_agent_summary(
                    Request("agents", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                    self.__timestamp,
                )
            ),
            asyncio.run(
                sync_chat(
                    Request("chats", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                    self.__timestamp,
                )
            ),
            asyncio.run(
                sync_queue(
                    Request("queues", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                )
            ),
            asyncio.run(
                sync_queue_summary(
                    Request("queues", UserConfigs(self.__token), self.__customer_id),
                    connected_repositories,
                    self.__timestamp,
                )
            ),
            asyncio.run(
                sync_agent_event(
                    Request(
                        "agents/history", UserConfigs(self.__token), self.__customer_id
                    ),
                    connected_repositories,
                    self.__timestamp,
                )
            ),
        )

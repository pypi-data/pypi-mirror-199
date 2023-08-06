import asyncio
import json
from typing import Any, Callable, Dict, List
from urllib.parse import urljoin

import httpx
from httpx import Response

from kayak.ksql.models import Server, Stream, Topic, Table, Query

TIMEOUT_1H = 60 * 60

KSQL_HEADERS = {"Accept": "application/vnd.ksql.v1+json"}


class KsqlService:
    def __init__(
        self,
        server: str,
        user: str | None = None,
        password: str | None = None,
    ):
        self.server = server
        self.user = user
        self.password = password

    def info(self) -> Server:
        response = self.introspect("info")
        response.raise_for_status()

        def json_to_server(obj: dict[Any, Any], server: str) -> Any:
            if "KsqlServerInfo" in obj:
                return obj["KsqlServerInfo"]
            if "version" in obj:
                return Server(
                    id=obj["kafkaClusterId"],
                    service_id=obj["ksqlServiceId"],
                    status=obj["serverStatus"],
                    version=obj["version"],
                    server=server,
                )
            return obj

        server_obj: Server = response.json(object_hook=lambda d: json_to_server(d, self.server))
        return server_obj

    def streams(self) -> List[Stream]:
        response = self.statement("LIST STREAMS;")
        response.raise_for_status()

        def json_to_stream(obj: dict[Any, Any]) -> Any:
            if "streams" in obj:
                return obj["streams"]
            if "name" in obj:
                return Stream(
                    name=obj["name"],
                    topic=obj["topic"],
                    key_format=obj["keyFormat"],
                    value_format=obj["valueFormat"],
                )
            return obj

        streams: List[Stream] = response.json(object_hook=json_to_stream)[0]
        return streams

    def tables(self) -> List[Table]:
        response = self.statement("LIST TABLES;")
        response.raise_for_status()

        def json_to_table(obj: dict[Any, Any]) -> Any:
            if "tables" in obj:
                return obj["tables"]
            if "name" in obj:
                return Table(
                    name=obj["name"],
                    topic=obj["topic"],
                    key_format=obj["keyFormat"],
                    value_format=obj["valueFormat"],
                )
            return obj

        tables: List[Table] = response.json(object_hook=json_to_table)[0]
        return tables

    def queries(self) -> List[Query]:
        response = self.statement("LIST QUERIES;")
        response.raise_for_status()

        def json_to_query(obj: dict[Any, Any]) -> Any:
            if "queries" in obj:
                return obj["queries"]
            if "id" in obj:
                return Query(
                    id=obj["id"],
                    topics=obj["sinkKafkaTopics"],
                    query_type=obj["queryType"],
                    state=obj["state"],
                )
            return obj

        queries: List[Query] = response.json(object_hook=json_to_query)[0]
        return queries

    def topics(self) -> List[Topic]:
        response = self.statement("LIST TOPICS;")
        response.raise_for_status()

        def json_to_topic(obj: dict[Any, Any]) -> Any:
            if "topics" in obj:
                return obj["topics"]
            if "name" in obj:
                return Topic(
                    name=obj["name"],
                )
            return obj

        topic_list: List[Topic] = response.json(object_hook=json_to_topic)[0]
        return topic_list

    def auth(self) -> tuple[str, str] | None:
        return None if None in [self.user, self.password] else (str(self.user), str(self.password))

    def introspect(self, resource: str) -> Response:
        url = urljoin(self.server, resource)
        response = httpx.get(
            url,
            headers=KSQL_HEADERS,
            auth=self.auth(),
        )
        return response

    def statement(self, statement: str) -> Response:
        data = {"ksql": statement}
        url = urljoin(self.server, "/ksql")
        response = httpx.post(
            url,
            json=data,
            headers=KSQL_HEADERS,
            auth=self.auth(),
        )
        return response

    async def query(
        self,
        query: str,
        earliest: bool = False,
        on_init: Callable[[dict[str, Any]], None] = lambda data: None,
        on_new_row: Callable[[list[Any]], None] = lambda row: None,
        on_close: Callable[[], None] = lambda: None,
        on_error: Callable[[int, str], None] = lambda code, content: None,
    ) -> None:
        url = urljoin(self.server, "/query-stream")
        data = {
            "sql": query,
            "properties": {"auto.offset.reset": "earliest"} if earliest else {},
        }

        async with httpx.AsyncClient(
            http2=True,
            timeout=TIMEOUT_1H,
            auth=self.auth(),
        ) as client:
            async with client.stream(method="POST", url=url, json=data) as stream:
                async for chunk in stream.aiter_text():
                    if chunk:
                        results = json.loads(chunk)

                        if stream.status_code != 200:
                            on_error(stream.status_code, chunk)
                            break

                        if isinstance(results, Dict):
                            on_init(results)
                        elif isinstance(results, List):
                            on_new_row(results)

        on_close()

    def close_query(self, id: str) -> None:
        url = urljoin(self.server, "/close-query")
        data = {"queryId": id}
        httpx.post(
            url,
            json=data,
            headers=KSQL_HEADERS,
            auth=self.auth(),
        )


if __name__ == "__main__":
    service = KsqlService("http://localhost:8088")

    print("--REQUESTS--")

    print("info", service.info())
    print("streams", service.streams())
    print("topics", service.topics())
    print("tables", service.tables())
    print("queries", service.queries())

    print("--QUERIES--")

    asyncio.run(
        service.query(
            "SELECT * FROM orders;",
            on_init=print,
            on_new_row=print,
            on_close=lambda: print("orders finished"),
        )
    )

    query_id = ""

    async def close_query() -> None:
        global query_id
        await asyncio.sleep(10)
        service.close_query(query_id)

    async def pull_query() -> None:
        def on_init(data: dict[str, Any]) -> None:
            global query_id
            query_id = data["queryId"]
            print(query_id)
            print(data["columnTypes"])

        query = asyncio.create_task(
            service.query(
                "SELECT * FROM orderSizes EMIT CHANGES;",
                True,
                on_init=on_init,
                on_new_row=print,
                on_close=lambda: print("orderSizes finished"),
            )
        )

        close = asyncio.create_task(close_query())

        await query
        await close

    asyncio.run(pull_query())

    print("--QUERY ERROR--")

    asyncio.run(
        service.query(
            "SELECT * FROM orders",
            on_error=lambda code, content: print("response status:", code, "content:", content),
            on_close=lambda: print("error closed"),
        )
    )

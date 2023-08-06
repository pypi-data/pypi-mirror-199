import asyncio
from enum import Enum
from typing import Any, Final, List, Literal, Type

from rich.columns import Columns
from rich.console import RenderableType
from rich.json import JSON
from rich.text import Text
from textual.app import App, ComposeResult, CSSPathType
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.driver import Driver
from textual.keys import Keys
from textual.reactive import reactive
from textual.widgets import DataTable, Footer, Input, Label, Static, Switch, Tree
from textual.widgets._tree import EventTreeDataType, TreeNode

from kayak import logger
from kayak.ksql.ksql_service import KsqlService
from kayak.ksql.models import Server
from kayak.renderables.kayak_name import KayakName
from kayak.renderables.server_info import ServerInfo
from kayak.styles.colors import DESIGN, ERROR, GREEN

RIGHT: Final = "right"
LEFT: Final = "left"


class Statuses(Enum):
    RUNNING = f"bold {GREEN}"
    IDLE = "bold"
    ERROR = f"bold {ERROR}"


class Status(Container):
    status = reactive(Statuses.IDLE)

    def render(self) -> RenderableType:
        return Text.from_markup(f"STATUS: [{self.status.value}]{self.status.name}[/]")


class Settings(Container):
    earliest = True

    def on_switch_changed(self, event: Switch.Changed) -> None:
        self.earliest = event.value

    def compose(self) -> ComposeResult:
        yield Label("SETTINGS", classes="title")
        yield Horizontal(Static("EARLIEST:     ", classes="label"), Switch(value=self.earliest))


class JsonViewer(Container, can_focus=True):
    json = reactive("{}")

    def watch_json(self, json: str) -> None:
        json_widget = self.query_one(Json)
        json_widget.update(JSON(json))
        self.scroll_home()

    def compose(self) -> ComposeResult:
        yield Container(Json(expand=True))


class Json(Static):
    pass


class Editor(Container):
    pass


class Header(Static):
    server = Server()

    def render(self) -> RenderableType:
        kayak_name = KayakName()
        ksql_info = ServerInfo(self.server)
        return Columns([kayak_name, ksql_info], padding=3)


class Tui(App[None]):
    CSS_PATH = "tui.css"
    BINDINGS = [
        Binding(Keys.ControlC, "quit", "QUIT"),
        # Binding(Keys.F1, "push_screen('help')", "HELP"),
        Binding(Keys.ControlX, "kill_query", "KILL QUERY"),
        Binding(Keys.ControlS, "toggle_settings", "TOGGLE SETTINGS"),
    ]

    status = reactive(Statuses.IDLE)
    query_id: str | None = None

    def __init__(
        self,
        server: str,
        user: str | None,
        password: str | None,
        driver_class: Type[Driver] | None = None,
        css_path: CSSPathType | None = None,
        watch_css: bool = False,
    ):
        super().__init__(driver_class, css_path, watch_css)
        self.ksql_service = KsqlService(server, user, password)
        self.server = self.ksql_service.info()
        self.topics = self.ksql_service.topics()
        self.streams = self.ksql_service.streams()

    def on_mount(self) -> None:
        input_query = self.query_one(Input)
        input_query.placeholder = "QUERY"
        input_query.focus()

        header = self.query_one(Header)
        header.server = self.server

        tree = self.query_one(Tree)
        tree.show_root = False
        tree.root.expand()
        tree.cursor_line = -1

        stream_node = tree.root.add("STREAMS", expand=True, data="STREAMS")
        for stream in self.streams:
            stream_node.add_leaf(stream.name, data=stream.name)

        topic_node = tree.root.add("TOPICS", expand=True, data="TOPICS")
        for topic in self.topics:
            topic_node.add_leaf(topic.name, data=topic.name)

        table = self.query_one(DataTable)
        table.cursor_type = "row"

        self.design = DESIGN
        self.refresh_css()

    async def action_kill_query(self) -> None:
        logger.debug("Killing query %s", self.query_id)
        if self.query_id:
            self.ksql_service.close_query(self.query_id)

    async def action_toggle_settings(self) -> None:
        input_widget = self.query_one(Input)

        settings = self.query_one(Settings)
        switch = settings.query_one(Switch)

        if switch.has_focus:
            input_widget.focus()
        else:
            switch.focus()

    def watch_status(self, status: Statuses) -> None:
        status_widget = self.query_one(Status)
        status_widget.status = status

    async def on_tree_node_selected(
        self, selected_node_event: Tree.NodeSelected[EventTreeDataType]
    ) -> None:
        node: TreeNode[EventTreeDataType] = selected_node_event.node

        if node.parent is None:
            return

        parent: TreeNode[EventTreeDataType] = node.parent

        str_parent: str = str(parent.data)
        str_child: str = str(node.data)

        logger.debug("parent selected node: %s", str_parent)
        logger.debug("selected node: %s", str_child)

        if str_parent.upper() == "STREAMS":
            input_query = self.query_one(Input)
            input_query.value = f"DESCRIBE {str_child};"
            input_query.focus()

    async def on_input_submitted(self, input_submitted_event: Input.Submitted) -> None:
        input_value = input_submitted_event.value

        if not input_value:
            return

        await self.action_kill_query()

        settings = self.query_one(Settings)
        json_viewer = self.query_one(JsonViewer)
        table = self.query_one(DataTable)

        if input_value.upper().startswith("SELECT"):
            table.remove_class("hidden")
            json_viewer.add_class("hidden")
            table.focus()

            table.clear(columns=True)

            columns = []

            def on_close() -> None:
                self.query_id = None
                if self.status == Statuses.RUNNING:
                    self.status = Statuses.IDLE

            def on_init(data: dict[str, Any]) -> None:
                self.status = Statuses.RUNNING
                self.query_id = data["queryId"]
                nonlocal columns

                column_names: List[str] = data["columnNames"]
                justify_list: List[Literal["left", "right"]] = [
                    LEFT if column_type.upper() in ["VARCHAR", "STRING"] else RIGHT
                    for column_type in data["columnTypes"]
                ]

                columns = list(
                    zip(
                        column_names,
                        justify_list,
                    )
                )
                logger.debug("adding columns: %s", columns)
                for column_name, justify in columns:
                    table.add_column(Text(str(column_name), justify=justify))

            def on_new_row(row: list[Any]) -> None:
                nonlocal columns
                zip_row = list(zip(row, [justify for column_name, justify in columns]))
                logger.debug("adding row: %s", zip_row)
                row = [Text(str(cell), justify=justify) for cell, justify in zip_row]
                table.add_row(*row)
                table.scroll_end()

            def on_error(code: int, content: str) -> None:
                json_viewer.remove_class("hidden")
                table.add_class("hidden")
                json_viewer.focus()
                json_viewer.json = content
                json_viewer.add_class("error")
                self.status = Statuses.ERROR

            asyncio.create_task(
                self.ksql_service.query(
                    query=input_value,
                    earliest=settings.earliest,
                    on_init=on_init,
                    on_new_row=on_new_row,
                    on_close=on_close,
                    on_error=on_error,
                )
            )
        else:
            json_viewer.remove_class("hidden")
            table.add_class("hidden")
            json_viewer.focus()

            response = self.ksql_service.statement(input_value)
            json_viewer.json = response.text

            if response.status_code != 200:
                json_viewer.add_class("error")
                self.status = Statuses.ERROR
            else:
                json_viewer.remove_class("error")
                self.status = Statuses.IDLE

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Settings(classes="-hidden")
        yield Tree("")
        with Editor():
            yield Input()
            yield DataTable()
            yield JsonViewer(classes="hidden")
            yield Status()

import typing as t

from pydantic import BaseModel


class AdminTable(BaseModel):
    table_name: t.Optional[str] = None
    visible_columns: t.Optional[list[str]] = None
    visible_filters: t.Optional[list[str]] = None
    rich_text_columns: t.Optional[str] = None
    link_column: t.Optional[str] = None
    menu_group: t.Optional[str] = None


class AdditionalConfig(BaseModel):
    tables: t.Optional[list[AdminTable]] = None
    sidebar_links: t.Optional[dict[str, str]] = None

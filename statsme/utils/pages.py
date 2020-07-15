from discord.ext import menus

from .tabulate import tabulate


class TablePages(menus.ListPageSource):
    def __init__(self, data, *, language="prolog", title="", per_page=10):
        entries = tabulate(data, as_list=True)
        super().__init__(entries, per_page=per_page)

        self.language = language
        self.title = title

    def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        table = "\n".join(v for i, v in enumerate(entries, start=offset))

        max_pages = self.get_max_pages()
        page_num = f"Page {menu.current_page + 1}/{max_pages}" if max_pages > 1 else ""
        return f"**{self.title}**\n```{self.language}\n{table}\n```\n{page_num}"

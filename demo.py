"""
demo.py — Демонстрация протокольного рендеринга в Rich.

Показывает, как объект, не наследующий ничего из Rich,
может быть отрисован Console благодаря реализации
протоколов __rich_console__ и __rich_measure__.
"""

#!pip install rich
#Установка библиотеки rich если её нет в системе

from rich.console import Console
from rich.table import Table
from rich.segment import Segment
from rich.style import Style
from rich.measure import Measurement


class StatusBadge:
    """
    Кастомный renderable: цветной бейдж со статусом.
    
    НЕ наследуется от ConsoleRenderable или чего-либо в Rich.
    Реализует протокол структурно: просто определяет нужные методы.
    """

    def __init__(self, status: str, color: str = "green"):
        self.status = status
        self.style = Style(color=color, bold=True)

    def __rich_console__(self, console, options):
        """
        Основной метод протокола.
        
        Console вызывает его и ожидает итератор,
        который выдаёт Segment (или вложенные renderable).
        """
        # Генерируем один сегмент: текст бейджа в рамке из символов
        badge_text = f" {self.status} "
        yield Segment(badge_text, style=self.style)

    def __rich_measure__(self, console, options):
        """
        Метод измерения.
        
        Нужен, чтобы Rich знал, сколько места занимает объект,
        когда он находится внутри Table или Panel.
        Возвращает Measurement(min_width, max_width).
        """
        # Ширина текста + 2 пробела по краям
        width = len(self.status) + 2
        return Measurement(width, width)


def main():
    console = Console()

    console.rule("[bold]1. Прямой вывод кастомного объекта[/]")
    badge = StatusBadge("OK", "green")
    console.print(badge)

    badge_warn = StatusBadge("WARN", "yellow")
    console.print(badge_warn)

    console.rule("[bold]2. Кастомный объект внутри Table[/]")
    # Благодаря __rich_measure__ таблица корректно рассчитает ширину колонки
    table = Table(title="System Status")
    table.add_column("Service")
    table.add_column("Status")

    table.add_row("Auth Service", StatusBadge("RUNNING", "green"))
    table.add_row("Cache Service", StatusBadge("DEGRADED", "yellow"))
    table.add_row("Storage Service", StatusBadge("FAILED", "red"))

    console.print(table)

    console.rule("[bold]3. Доказательство: класс не наследуется от Rich[/]")
    console.print(f"Базовые классы StatusBadge: {StatusBadge.__bases__}")
    console.print(
        "Но Console всё равно его отрисовал — благодаря утиной типизации."
    )


if __name__ == "__main__":
    main()
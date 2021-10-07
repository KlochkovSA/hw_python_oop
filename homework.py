"""Определяет калькулятор калорий и денежный калькулятор."""
from typing import Dict, Optional, List, Tuple
import datetime as dt


class Record:
    """Представляет новый тип данных Record 'Запись'.

    Энкапсулирует в себе поля:
    amount - целочисленные данные
    comment - коментарий к записи
    date - для какой даты хранится запись
    """

    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None):
        """Создает запись о тратах с коментарием.

        Аргументы:
        amount - траты
        comment - коментарий к записи
        date - (опциоальный) для какой даты хранится запись
                значение по умолчанию - datetime.date.today()
        """
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    """Сохраняет обьекты в списке."""

    def __init__(self, limit: int) -> None:
        """Создает обьект Calculator с заданным лимитом."""
        self.limit = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """Сохраняет запись о трате."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Итерируется по списку трат и возращает сумму трат за сегодня."""
        today = dt.date.today()
        today_stats = sum([record.amount for record in self.records
                           if record.date.day == today.day])
        return today_stats

    def get_week_stats(self) -> int:
        """Итерируется по списку трат и возращает сумму трат за неделю."""
        week_stats = 0
        # week_ago - вычисляем дату которая была неделю назад
        week_ago = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            # сауммируем траты за прошедшую неделю
            if dt.date.today() >= record.date >= week_ago:
                week_stats += record.amount
        return week_stats

    def get_remained(self) -> int:
        """Возвращает разницу между лимитом и суммой трат за день."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """CaloriesCalculator хранит записи о потребленных калориях."""

    def get_calories_remained(self) -> str:
        """Считает сколько осталось съесть сегодня.

        Если дневной лимит по калориям не привышен, возвращает сообщение:
        'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью
        не более {remained_calories} кКал'
        Возврашает сообщение 'Хватит есть!', если превышен лимит по калориям
        """
        remained_calories = self.get_remained()
        if remained_calories > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    ' но с общей калорийностью не более '
                    f'{remained_calories} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Денежный калькулятор CashCalculator хранит записи о тратах."""

    USD_RATE = 60.0
    EURO_RATE = 70.0
    currencies: Dict[str, Tuple[str, float]] = {'eur': ('Euro', EURO_RATE),
                                                'usd': ('USD', USD_RATE),
                                                'rub': ('руб', 1.0),
                                                }

    def get_today_cash_remained(self, currency: str) -> str:
        """Для выбранной валюты возврашает сообщение о тратах за день.

        Если траты today_stats меньше лимита, выводит
        'На сегодня осталось {today_stats} {code}'
        Если траты today_stats равны лимиту, выводит
        'Денег нет, держись'
        Если есть долг, выводит
        'Денег нет, держись: твой долг - {debt} {code}'
        """
        today_stats = self.get_remained() / self.currencies[currency][1]
        code = self.currencies[currency][0]
        if today_stats > 0:
            today_stats = round(today_stats, 2)
            return f'На сегодня осталось {today_stats} {code}'
        elif today_stats < 0:
            debt = abs(round(today_stats, 2))
            return f'Денег нет, держись: твой долг - {debt} {code}'
        else:
            return 'Денег нет, держись'

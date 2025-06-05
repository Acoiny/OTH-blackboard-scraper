from urllib.request import urlopen
import csv
import datetime as dt

class Meal:
    def __init__(self, name: str, kennzeichnung: str, price_students: str, price_workers: str, price_guest: str) -> None:
        self.name = name
        self.kennzeichnung = kennzeichnung
        self.price_students = float(price_students.replace(',', '.'))
        self.price_workers = float(price_workers.replace(',', '.'))
        self.price_guest = float(price_guest.replace(',', '.'))
    def __str__(self) -> str:
        return f'{self.name} - {self.kennzeichnung}: {self.price_students}€'

class Weekday:
    def __init__(self, datum: str) -> None:
        self.datum = dt.datetime.strptime(datum, "%d.%m.%Y").date()
        self.suppen: list[Meal] = []
        self.vorspeisen: list[Meal] = []
        self.hauptspeisen: list[Meal] = []
        self.beilagen: list[Meal] = []
        self.nachspeisen: list[Meal] = []

    def add_meal(self, meal: Meal, meal_type: str) -> None:
        if meal_type.startswith('HG'):
            self.hauptspeisen.append(meal)
        elif meal_type.startswith('B'):
            self.beilagen.append(meal)
        elif meal_type.startswith('Suppe'):
            self.suppen.append(meal)
        elif meal_type.startswith('N'):
            self.nachspeisen.append(meal)
        else:
            raise Exception(f'Unknown meal type: {meal_type}')

    def to_markdown_str(self) -> str:
        res = '## Suppen\n'
        for su in self.suppen:
            res += f'- {su}\n'
        res += '## Vorspeisen\n'
        for vs in self.vorspeisen:
            res += f'- {vs}\n'
        res += '## Hauptspeisen\n'
        for hs in self.hauptspeisen:
            res += f'- {hs}\n'
        res += '## Nachspeisen\n'
        for ns in self.nachspeisen:
            res += f'- {ns}\n'

        return res
    
    def __str__(self) -> str:
        res = '    Suppen:\n'

        for su in self.suppen:
            res += f'       - {su}\n'
        res += '    Vorspeisen:\n'
        for vs in self.vorspeisen:
            res += f'       - {vs}\n'
        res += '    Hauptspeisen:\n'
        for hs in self.hauptspeisen:
            res += f'       - {hs}\n'
        res += '    Nachspeisen:\n'
        for ns in self.nachspeisen:
            res += f'       - {ns}\n'

        return res

class Mensaplan:
    """
    Gets the current mensaplan and handles stringifying it and
    formatting as markdown
    """
    def __init__(self, calendar_week: int | None = None) -> None:
        if calendar_week == None: calendar_week = dt.date.today().isocalendar()[1]
        self.url = f'https://www.stwno.de/infomax/daten-extern/csv/HS-R-tag/{calendar_week}.csv'
        self.days: dict[str, Weekday] = {}

    def get(self) -> None:
        """
        Fetches the current mensaplan and stores it
        """
        with urlopen(self.url) as url:
            lines = [l.decode('latin-1').strip() for l in url.readlines()]
            csv_reader = csv.reader(lines, delimiter=';')

            # discard fields
            next(csv_reader)

            for row in csv_reader:
                day = self.days.get(row[1])
                if day == None:
                    day = Weekday(row[0])
                    self.days[row[1]] = day
                meal = Meal(row[3], row[4], row[6], row[7], row[8])
                day.add_meal(meal, row[2])


    def to_markdown_str(self) -> str:
        res = ''

        keys_to_names = [
            ('Mo', 'Montag'),
            ('Di', 'Dienstag'),
            ('Mi', 'Mittwoch'),
            ('Do', 'Donnerstag'),
            ('Fr', 'Freitag')
        ]

        for key, name in keys_to_names:
            res += f'# {name}\n'
            res += f'{self.days[key].to_markdown_str()}'

        return res

    def stringify_day(self, index: int | str) -> str:
        keys_to_names = [
            ('Mo', 'Montag'),
            ('Di', 'Dienstag'),
            ('Mi', 'Mittwoch'),
            ('Do', 'Donnerstag'),
            ('Fr', 'Freitag')
        ]
        keys_to_name_dict = {
            'Mo': 'Monday',
            'Di': 'Dienstag',
            'Mi': 'Mittwoch',
            'Do': 'Donnerstag',
            'Fr': 'Freitag'
        }


        try:
            if isinstance(index, int):
                return f'{keys_to_names[index][1]}:\n{self.days[keys_to_names[index][0]]}\n'
            else:
                if keys_to_name_dict.get(index) == None:
                    return f'Invalid day: {index}!'
                return f'{keys_to_name_dict[index]}:\n{self.days[index]}\n'
        except:
            return ''

    def __str__(self) -> str:
        res = ''

        for i in range(4):
            res += self.stringify_day(i)

        return res

if __name__ == '__main__':
    m = Mensaplan()
    m.get()
    print(m)

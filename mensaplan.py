from urllib.request import urlopen
import csv
import datetime as dt

class Meal:
    def __init__(self, name: str, kennzeichnung: str, price_students: str, price_workers: str, price_guest: str) -> None:
        self.name = name
        self.kennzeichnung = kennzeichnung
        self.price_students = float(price_students)
        self.price_workers = float(price_workers)
        self.price_guest = float(price_guest)

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

    def to_markdown(self) -> str:
        res = ''
        
        return res

class Mensaplan:
    """
    Gets the current mensaplan and handles stringifying it and
    formatting as markdown
    """
    def __init__(self, url: str) -> None:
        self.url = url
        self.days: dict[str, Weekday] = {}

    def get(self) -> None:
        """
        Fetches the current mensaplan and stores it
        """
        with urlopen(self.url) as url:
            lines = [l.decode('latin-1').strip() for l in url.readlines()]
            csv_reader = csv.reader(lines, delimiter=';')

            # aquire the different fields
            fields = next(csv_reader)
            print(fields)

            for row in csv_reader:
                day = self.days.get(row[1])
                if day == None:
                    day = Weekday(row[0])
                    self.days[row[1]] = day
                meal = Meal(row[3], row[4], row[6], row[7], row[8])
                day.add_meal(meal, row[2])


m = Mensaplan('https://www.stwno.de/infomax/daten-extern/csv/HS-R-tag/23.csv')
m.get()

import mysql.connector
from mysql.connector import Error
class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='2002',
                database='flights'
            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('Connection error')

    def fetch_dest_city_names(self):

        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(origin) FROM flights.flights
        UNION
        SELECT DISTINCT(dest) FROM flights.flights;
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city
    def fetch_source_city_names(self):

        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(origin) FROM flights.flights
        
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])

        return city

    def fetch_all_flights(self, origin, destination,flight_date):

        self.mycursor.execute("""
               SELECT flight_date, dep_time, arr_time, name, origin, dest
               FROM flights
               WHERE origin = %s AND dest = %s AND flight_date = %s;
           """, (origin, destination, flight_date))


        data = self.mycursor.fetchall()

        return data
    def fetch_airline_frequency(self):
        airline=[]
        frequency=[]
        self.mycursor.execute("""
        SELECT name, count(*) FROM flights.flights
        GROUP BY name
        """)
        data=self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])
        return airline, frequency

    def busy_airport(self):
        city=[]
        frequency=[]
        self.mycursor.execute("""
        SELECT origin, COUNT(*) FROM (SELECT origin FROM flights.flights UNION ALL SELECT dest FROM flights.flights) t
        GROUP BY t.origin
        ORDER BY COUNT(*) DESC
        """)
        data=self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            frequency.append(item[1])
        return city, frequency

    def daily_frequency(self):
        date=[]
        frequency=[]
        self.mycursor.execute("""
        SELECT flight_date, COUNT(*) FROM flights.flights
        GROUP BY flight_date
        """)
        data=self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            frequency.append(item[1])
        return date, frequency
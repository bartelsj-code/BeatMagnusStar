import sqlite3
import api_requests
from datetime import datetime, timedelta, timezone
import pytz

class DataAccess:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.set_up_database()
        self.check_frequency = 1 # hours

    def prepare_player_data(self, username):
        if self.player_update_needed(username):
            self.renew_closed_status_api(username)

    def get_games_since_date(self, username, start_date):
        self.prepare_player_data(username)


        tups = api_requests.get_games_since_date(username, start_date)
        print(tups)




    #################################### api stuff ####################################

    def renew_closed_status_api(self, username):
        self.upsert_player(username, 
                           closed = api_requests.get_player_closed(username)
                           )


    def pull_player_data_from_api(self, username):
        year, month = api_requests.get_player_start_date(username)
        closed = api_requests.get_player_closed(username)
        self.upsert_player(username, 
                           first_year= int(year), 
                           first_month= int(month), 
                           closed= closed
                           )

    ###################################### SQL stuff ###################################

    def reset_updated(self, username):
        c = self.conn.cursor()
        c.execute("UPDATE players SET updated = CURRENT_TIMESTAMP WHERE username = ?", (username,))
        self.conn.commit()

    def player_update_needed(self, username):
        c = self.conn.cursor()
        c.execute("SELECT updated FROM players WHERE username = ?", (username,))
        result = c.fetchone()
        if result is None:
            #i.e. player not yet exists
            self.pull_player_data_from_api(username)
            return False
        else:
            last_update_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
            last_update_time = pytz.UTC.localize(last_update_time)
            if datetime.now(timezone.utc)-last_update_time > timedelta(hours = self.check_frequency):
                return True
        return False

    def set_up_database(self):
        c = self.conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                white_player TEXT,
                white_rating INTEGER,
                black_player TEXT,
                black_rating INTEGER,
                w_result TEXT,
                b_result TEXT,
                time_control TEXT,
                year INTEGER,
                month INTEGER, 
                url TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                first_year INTEGER,
                first_month INTEGER, 
                closed BOOL,
                updated DATETIME DEFAULT CURRENT_TIMESTAMP 
                
            );
                        
            CREATE TABLE IF NOT EXISTS player_games (
                player_id INTEGER,
                game_id INTEGER,
                PRIMARY KEY (player_id, game_id),
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (game_id) REFERENCES games(id)
            );
                        
        """)

        self.conn.commit()

    def upsert_player(self, username, first_year = None, first_month = None, closed = None):
        try:
            c = self.conn.cursor()

            c. execute("SELECT id FROM players WHERE username = ?", (username,))
            player = c.fetchone()

            if player:
                query = "UPDATE players SET"
                params = []

                if first_year is not None:
                    query += " first_year = ?,"
                    params.append(first_year)
                if first_month is not None:
                    query += " first_month = ?,"
                    params.append(first_month)
                if closed is not None:
                    query += " closed = ?,"
                    params.append(closed)

                query = query.strip(',')
                query += "WHERE username = ?"
                params.append(username)

                c.execute(query, tuple(params))
            else:
                c.execute("""
                INSERT INTO players (username, first_year, first_month, closed)
                VALUES (?, ?, ?, ?)
                """, (username, first_year, first_month, closed))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Error upserting player: ", e)
    

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()

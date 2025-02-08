import sqlite3
import api_requests
from format_conversion import game_json_to_tup, tup_to_game
from datetime import datetime, timedelta, timezone
import pytz

class DataAccess:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.set_up_database()
        self.check_frequency = 24 # hours
        self.request_counter = 0

    def update_games(self, username):
        print(f"adding recent games for {username}")
        original_records_date = self.get_records_date(username)
        self.set_records_date(username, (None, None))
        last_update = self.get_update_date(username)
        date =last_update.split("-")[:2]
        self.prep_games_since_date(username, tuple(int(x) for x in date))
        self.set_records_date(username, original_records_date)
        
        self.reset_updated(username)

    def prepare_player_data(self, username):
        if self.player_update_needed(username):
            self.renew_closed_status_api(username)
            self.update_games(username)
            
    def get_matching_games(self, *, username, start_date, is_winning=None, filter=None, loser=None):
        self.prepare_player_data(username)
        self.prep_games_since_date(username, start_date)
        tups =  self.pull_games(username=username, start_date=start_date, is_winning=is_winning, filter=filter, loser_username=loser)
        return [tup_to_game(tup) for tup in tups]
            
    ###################################### SQL stuff ###################################

    def get_update_date(self, username):
        c = self.conn.cursor()
        c.execute("""
        SELECT updated FROM players WHERE username = ? LIMIT 1
        """, (username,))
        return c.fetchone()[0]

    def set_records_date(self, username, date):
        c = self.conn.cursor()
        c.execute("""UPDATE players SET records_year = ?, records_month = ? WHERE username = ?""", (date[0], date[1], username))
        self.conn.commit()

    def is_player_closed(self, username):
        c = self.conn.cursor()
        c.execute("SELECT closed FROM players WHERE username = ? LIMIT 1", (username,))
        result = c.fetchone()
        return result[0]

    def pull_games(self, *, username = None, start_date = None, is_winning = None, filter=None, loser_username = None):
        query_opener = """SELECT g.* FROM games g Join player_games pg ON g.id = pg.game_id WHERE """
        query = []
        params = []
        if username is not None:
            player_id = self.get_player_id(username)
            query.append("""pg.player_id = ?""")
            params.append(player_id)
        if start_date is not None:
            query.append("""(g.year > ? OR (g.year = ? AND g.month >= ?))""")
            params += [start_date[0], start_date[0], start_date[1]]
        if is_winning is not None:
            if is_winning:
                query.append("""((g.white_username = ? AND g.white_result = "win") OR (g.black_username = ? AND g.black_result = "win"))""")
            else:
                query.append("""((g.white_username = ? AND g.black_result = "win") OR (g.black_username = ? AND g.white_result = "win"))""")
            params += [username, username]
        if filter is not None:
            for item in filter:
                query.append(f"""(g.{item} IN ({(" ?,"*len(filter[item])).strip(",")}))""")
                params += filter[item]
        if loser_username is not None:
            query.append("""((g.white_username = ? AND g.black_result = "win") OR (g.black_username = ? AND g.white_result = "win"))""")
            params += [loser_username, loser_username]


        
        query = query_opener + """ AND """.join(query)
        c = self.conn.cursor()
        c.execute(query, tuple(params))
        return c.fetchall()
   
    def get_player_id(self, username):
        # if exists, get ID, otherwise first add, then get ID
        c = self.conn.cursor()
        c.execute("SELECT id FROM players WHERE username = ? LIMIT 1", (username,))
        result = c.fetchone()
        if result:
            return result[0]
        
        self.upsert_player(username)
        c.execute("SELECT id FROM players WHERE username = ? LIMIT 1", (username,))
        return c.fetchone()[0]

    def get_first_date(self, username):
        c = self.conn.cursor()
        c.execute("SELECT first_year, first_month FROM players WHERE username = ? LIMIT 1", (username,))
        result = c.fetchone()
        return tuple(result)


    def get_records_date(self, username):
        c = self.conn.cursor()
        c.execute("SELECT records_year, records_month FROM players WHERE username = ? LIMIT 1", (username,))
        result = c.fetchone()
        return tuple(result)

    def reset_updated(self, username):
        c = self.conn.cursor()
        c.execute("UPDATE players SET updated = CURRENT_TIMESTAMP WHERE username = ?", (username,))
        self.conn.commit()

    def player_update_needed(self, username):
        c = self.conn.cursor()
        c.execute("SELECT updated FROM players WHERE username = ? LIMIT 1", (username,))
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
    
    def get_game_id(self, url):
        c = self.conn.cursor()
        c.execute("SELECT id FROM games WHERE url = ? LIMIT 1", (url,))
        return c.fetchone()[0]


    def set_up_database(self):
        c = self.conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rules TEXT,
                rated BOOL,
                white_username TEXT,
                white_rating INTEGER,
                white_result TEXT,
                black_username TEXT,
                black_rating INTEGER,
                black_result TEXT,
                time_class TEXT,
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
                records_year INTEGER,
                records_month INTEGER,
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

    def insert_games(self, tups, user_id):
        c = self.conn.cursor()
        c.executemany("""
        INSERT OR IGNORE INTO games (rules, rated, white_username, white_rating, white_result, black_username, black_rating, black_result, time_class, year, month, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """, tups)
        

        urls = [tup[-1] for tup in tups]
        c.execute(f"SELECT id, url FROM games WHERE url IN ({','.join(['?']*len(urls))})", urls)
        url_to_id = {url: game_id for game_id, url in c.fetchall()}

        ids = [(user_id, url_to_id[tup[-1]]) for tup in tups]

    
        c.executemany("""
        INSERT OR IGNORE INTO player_games (player_id, game_id)
        VALUES (?, ?)
        """, ids)

        self.conn.commit()

    


    def upsert_player(self, username, first_year = None, first_month = None, records_month = None, records_year = None, closed = None):
        try:
            c = self.conn.cursor()

            c.execute("SELECT id FROM players WHERE username = ? LIMIT 1", (username,))
            id = c.fetchone()

            if id:
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
                if records_month is not None:
                    query += " records_month = ?,"
                    params.append(records_month)
                if records_year is not None:
                    query += " records_year = ?,"
            
                    params.append(records_year)

                query = query.strip(',')
                query += " WHERE username = ?"
                
                params.append(username)
                c.execute(query, tuple(params))
                self.conn.commit()
                return id
            else:
                c.execute("""
                INSERT INTO players (username, first_year, first_month, closed, records_year, records_month)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (username, first_year, first_month, closed, records_year, records_month))
            self.conn.commit()

        except sqlite3.Error as e:
            print("Error upserting player: ", e)
    

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()

    #################################### api stuff ####################################

    def prep_games_since_date(self, username, start_date):
        self.request_counter += 1
        games = []
        
        user_id = self.get_player_id(username)
        records_date = self.get_records_date(username)
        first_date = self.get_first_date(username)
        dates_to_search = self.get_dates(start_date, first_date, records_date)

        if len(dates_to_search) > 0:
            for date in dates_to_search:
                game_jsons = api_requests.get_month_games(username, date)
                if game_jsons == None:
                    continue
                tups = [game_json_to_tup(gj, date) for gj in game_jsons]
                self.insert_games(tups, user_id)
            searched_till = dates_to_search[-1]
            self.upsert_player(username, records_year=searched_till[0], records_month=searched_till[1])

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


    ####################################  Dates stuff #############################


    def subtract_month(self, date):
        year = date[0]
        month = date[1]
        month -= 1
        if month < 1:
            month += 12
            year -= 1
        return (year, month)

    def get_dates(self, requested, first_possible, done):
        to_be_searched = []
        start_date = max(requested, first_possible)
        if done[0] == None:
            tod = datetime.today()
            done = (tod.year, tod.month)
        else:
            done = self.subtract_month(done)

        curr = done
        while curr >= start_date:
            if curr <= done:
                to_be_searched.append(curr)
            curr = self.subtract_month(curr)
       
        return to_be_searched



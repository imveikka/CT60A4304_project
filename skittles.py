# Script to generate skittles database.
# If skittles.db exists do not run this code!
# !! NO WARRANTY !! 


from faker import Faker
import random
import itertools
import time
import sqlite3

if __name__ == "__main__":

    random.seed(4)
    Faker.seed(0)
    F = Faker()


    # generate random date
    def str_time_prop(start, end, time_format, prop):
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))
        ptime = stime + prop * (etime - stime)
        return time.strftime(time_format, time.localtime(ptime))


    # Team data, source: https://www.wordlab.com/team-name-generator/
    team_names = ["Salty Net Avalanche", "Macho Marsh OwnGoalers", "Salty Score Worms", "Good Happy Rockets", "Hopping Mauve Orphans", "The Bug Racers", "Dancing Steel Sensation", "Terrible Midnight Puppets", "Sweet Brick Outlaws", "Big Titanium Scumbags", "Infamous Axe Silos", "Invisible Diamond Frogs", "Running Cloud Chard", "Hilltop Dog Assassins", "Small Gonzo Syndrome", "Purple End Monkeys"]
    team_shorts = ["".join([word[:2] for word in words]) for words in [name.split() for name in team_names]]
    team_data = [(index + 1, index * 4 + 1, name, short) for index, (name, short) in enumerate(zip(team_names, team_shorts))]


    # Player data
    player_names = [f"{F.first_name()} {F.last_name()}".split() for _ in range(4 * len((team_names)))]
    fk_team_ids = sorted([num + 1 for _ in range(4) for num in range(len(team_names))]) 
    player_data = [(id + 1, name[0], name[1], t_id, random.randint(1, 5)) for id, (name, t_id) in enumerate(zip(player_names, fk_team_ids))]


    # Ranking data (zero points)
    rank_team_ids = [data[0] for data in sorted(team_data, key = lambda team: team[2])]
    ranking_data = [(id + 1, 0, t_id) for id, t_id in enumerate(rank_team_ids)]


    # Statistics
    fk_play_ids = [data[0] for data in sorted(player_data, key = lambda player: f"{player[1]} {player[2]}")]
    stats_data = [(id + 1, random.randint(20, 50), random.randint(0, 20), fk_id) for id, fk_id in enumerate(fk_play_ids)]


    # Stadion
    # stadions: https://www.fantasynamegenerators.com/stadium-names.php
    # cities: https://www.fantasynamegenerators.com/city-names.php
    stadium_names = ["Melody Ring", "Blossom Field", "Helix Field", "Huntress Park", "Dominion Bowl", "Promise Park", "Curator Field", "Genie Field", "Zodiac Ground", "Serenity Park"]
    stadium_cities = ["Sloiding", "Baldale", "Crensea", "Zraphia", "Yitol"]
    stadium_type = ["Sand", "Grass"]
    stadium_data = [(id + 1, name, random.choice(stadium_cities), random.choice(stadium_type)) for id, name in enumerate(stadium_names)]


    # Matches
    pairs_ids = list(itertools.combinations(range(1, 17), 2))
    for i in range(120):
        pairs_ids[i] = list(pairs_ids[i])
        random.shuffle(pairs_ids[i])
    random.shuffle(pairs_ids)
    results = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(120)]
    fields = [random.randint(1, 5) for _ in range(120)]
    dates = [str_time_prop("01-01-2065", "31-12-2065", "%d-%m-%Y", random.random()) for _ in range(120)]
    match_data = [(id + 1, field, date, r1, r2, t1, t2, t1 if r1 < r2 else t2 if r2 < r1 else None) for id, (date, (r1, r2), (t1, t2), field) in enumerate(zip(dates[:40], results, pairs_ids, fields))]


    # Add rankings
    ranking_data.sort(key=lambda data: data[2])
    for m in match_data:
        ranking_data[m[5]-1] = list(ranking_data[m[5]-1])
        ranking_data[m[6]-1] = list(ranking_data[m[6]-1])
        ranking_data[m[5]-1][1] += (2 if m[5] == m[7] else 1 if m[7] == None else 0)
        ranking_data[m[6]-1][1] += (2 if m[6] == m[7] else 1 if m[7] == None else 0)
        ranking_data[m[5]-1] = tuple(ranking_data[m[5]-1])
        ranking_data[m[6]-1] = tuple(ranking_data[m[6]-1])
    ranking_data.sort(key=lambda data: data[0])


    # Create database file
    connection = sqlite3.connect("skittles.db")
    cursor = connection.cursor()


    # Read and create tables
    with open("skittles.sql", "r") as sql_file:
        tables = sql_file.read()
    cursor.executescript(tables)


    # Insert players
    cursor.executemany("INSERT INTO Player VALUES(?, ?, ?, ?, ?)", player_data)
    connection.commit()


    # Insert teams
    cursor.executemany("INSERT INTO Team VALUES(?, ?, ?, ?)", team_data)
    connection.commit()


    # Insert ranking
    cursor.executemany("INSERT INTO Ranking VALUES(?, ?, ?)", ranking_data)
    connection.commit()


    # Insert statistics
    cursor.executemany("INSERT INTO Statistics VALUES(?, ?, ?, ?)", stats_data)
    connection.commit()


    # Insert stadiums
    cursor.executemany("INSERT INTO Stadium VALUES(?, ?, ?, ?)", stadium_data)
    connection.commit()


    # Insert matches
    cursor.executemany("INSERT INTO Match VALUES(?, ?, ?, ?, ?, ?, ?, ?)", match_data)
    connection.commit()


    connection.close()

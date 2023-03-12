####################################################

import sqlite3
db = sqlite3.connect('skittles.db')
cur = db.cursor()
def initializeDB():
    try:
        f = open("sqlcommands.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        cur.executescript(commandstring)
    except sqlite3.OperationalError:
        print("Database exists, skip initialization")
    except:
        print("No SQL file to be used for initialization") 

####################################################

def main():
    initializeDB()
    userInput = -1
    while(userInput != "0"):
        print("\nMenu options:")
        print("1: Print Teams")
        print("2: Print Matches")
        print("3: Print Players and Stats")
        print("4: MVP")
        print("5: Pike king")
        print("6: Search team")
        print("7: Modify match")
        print("0: Quit")
        userInput = input("What do you want to do? ")
        print("Your choice: " + userInput)
        if userInput == "1":
            printTeams()
        elif userInput == "2":
            printMatches()
        elif userInput == "3":
            printPlayersAndStats()
        elif userInput == "4":
            MVP()
        elif userInput == "5":
            pikeKing()
        elif userInput == "6":
            searchTeam() 
        elif userInput == "7":           
            modifyMatch()
        elif userInput == "0":
            print("Kiitos ohjelman käytöstä.")
        else:
            print("Unknown command! Try again.") 
    db.close()        
    return

####################################################

def printTeams():
    print("Printing teams:")
    cur.execute(
        "SELECT team_name, team_name_short, (Player.first_name || ' ' || Player.last_name) FROM Team \
        INNER JOIN Player ON Player.player_id = Team.FK_captain_ID \
        ORDER BY team_name ASC;"
    )
    results = cur.fetchall()
    name, short, captain = "Team name", "Short", "Captain"
    title = f"{name:^30s}|{short:^10s}|{captain:^20s}"
    print(title)
    print("-" * len(title))

    for (n, s, c) in results:
        print(f"{n:^30s}|{s:^10s}|{c:^20s}")
    return

####################################################

def printMatches():
    print("Printing matches:")
    cur.execute(
        "SELECT \
        match_date, \
        (Stadium.stadium_name || ', ' || Stadium.stadium_town), \
        ( \
            (SELECT team_name_short FROM Team WHERE team_ID = FK_team1_ID) \
            || ' vs ' || \
            (SELECT team_name_short FROM Team WHERE team_ID = FK_team2_ID) \
        ), \
        (result_team1 || ' - ' || result_team2) \
        FROM Match \
        INNER JOIN Stadium ON Stadium.stadium_ID = Match.FK_stadium_ID \
        ORDER BY match_date;"
    )
    results = cur.fetchall()
    date, stadium, teams, result = "Date", "Stadium", "Team 1 (home) vs Team 2", "Result"
    
    title = f"{date:^12s}|{stadium:^28s}|{teams:^26s}|{result:^10s}"
    print(title)
    print("-" * len(title))

    for d, s, t, r in results:
        print(f"{d:^12s}|{s:^28s}|{t:^26s}|{r:^10s}")
    return

####################################################

def printPlayersAndStats():

    print("Printing players and stats")
    cur.execute(
        "SELECT  \
            Player.first_name || ' ' || Player.last_name, \
            (SELECT team_name_short FROM Team WHERE Team.team_ID = Player.FK_team_ID), \
            total_score * 1.0 / (SELECT COUNT(*) FROM Match WHERE Match.FK_team1_ID = Player.FK_team_ID OR Match.FK_team2_ID = Player.FK_team_ID) AS mean, \
            pikes \
        FROM Statistics \
        INNER JOIN Player ON Player.player_id = Statistics.FK_player_id \
        ORDER BY mean DESC;"
    )
    results = cur.fetchall()
    
    name, team, mean, pikes = (
        "Name", "Team name", "Mean score", "Pikes"
    )
    title = f"{name:^22}|{team:^12}|{mean:^12}|{pikes:^7}"
    print(title)
    print("-" * len(title))

    for name, team, mean, pikes in results:
        print(f"{name:^22}|{team:^12}|{mean:^12.2f}|{pikes:^7}")
    return

####################################################

# statsit hoitaa, tilalle jpoku NM relaatiota hyödyntävä
# def MVP():
#     cur.execute(
#         "SELECT \
#             Player.first_name || ' ' || Player.last_name, \
#             (SELECT team_name FROM Team WHERE Team.team_ID = Player.FK_team_ID), \
#             total_score \
#         FROM Statistics \
#         INNER JOIN Player ON Player.player_id = Statistics.FK_player_id \
#         ORDER BY total_score DESC;"
#     )
#     for fname, lname, team, score in cur.fetchall():
#         print(fname, lname, team, score)
#     return

####################################################



####################################################


def pikeKing():
    cur.execute(
        "SELECT  \
            Player.first_name || ' ' || Player.last_name, \
            (SELECT team_name_short FROM Team WHERE Team.team_ID = Player.FK_team_ID), \
            pikes \
        FROM Statistics \
        INNER JOIN Player ON Player.player_id = Statistics.FK_player_id \
        WHERE pikes = (SELECT MAX(pikes) FROM Statistics) \
        ORDER BY Player.first_name;"
    )
    results = cur.fetchall()
    
    print(f"Current pike king(s) has {results[0][2]} pikes:")

    name, team = (
        "Name", "Team name"
    )
    title = f"{name:^22}|{team:^12}"
    print(title)
    print("-" * len(title))

    for name, team, _ in results:
        print(f"{name:^22}|{team:^12}")
    return

####################################################

def modifyMatch():
    matchID = input("What is the matchID of the match you want to modify? ")
    option = -1
    while option != "0":
        option = input("Modify options:\n1: Add a new match\n2: Move a match\n3: Remove a match\n0: Return to menu\nWhat do you want to do? ")
        if option == "1":
            matchdate = input("Give matchdate: ")
            stadium = input("Give stadium ID: ")
            team1 = input("Give team 1 ID: ")
            team2 = input("Give team 2 ID: ")
            result = input("Give result: ")
            winner = input("Give winner ID: ")
            cur.execute("INSERT INTO Match VALUES (?,?,?,?,?,?);", (matchdate, stadium, team1, team2, result, winner,))
            print("Added match")
        elif option == "2":
            newMatchDate = input ("What is the new matchdate you want to set?")
            if newMatchDate == "NULL":
                cur.execute("UPDATE Match SET FK_stadium_ID=(?),match_date=(?),result=(?),FK_team1_ID=(?),FK_team2_ID=(?),winner_ID=(?) WHERE match_ID=(?);", (None, None, None, None, None, None, matchID,))
            else:
                cur.execute("UPDATE Match SET match_date=(?) WHERE match_ID=(?);", (newMatchDate, matchID,))
            print("Match moved successfully.")                
        elif option == "3": 
            cur.execute("DELETE FROM Match WHERE match_ID=(?);", (matchID,))
            print("Match removed successfully.")
        elif option == "0":
            print("Returning to menu...")
        else:
            print("Unknown option.")
    return

####################################################

def searchTeam():
    teamName = input("What is the teamname? ")
    cur.execute("SELECT * FROM Team WHERE team_name = (?);", (teamName,))
    oneRow = cur.fetchone()

    print("ID:" + str(oneRow[0]))
    print("Team name:" + str(oneRow[2]))
    print("Short team name:" + str(oneRow[1]))
    return

####################################################    

main()

####################################################
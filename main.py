# CT60A4304 Basics of database systems - Project
# Authors: Joona Lappalainen AND Veikka Immonen
# The main CLI for searching and modifying database
# Dependensies: sqlite3, datetime


import sqlite3
import datetime


db = sqlite3.connect('skittles.db')
cur = db.cursor()


def main():
    userInput = -1
    while(userInput != "0"):
        print("\nMenu options:")
        print("1: Print teams")
        print("2: Print matches")
        print("3: Print players and stats")
        print("4: Print players that has won matches in their home stadium")
        print("5: Print pike king(s)")
        print("6: Search team")
        print("7: Modify match")
        print("8: Print current ranking")
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
            print_players_wins_from_home()
        elif userInput == "5":
            pikeKing()
        elif userInput == "6":
            searchTeam() 
        elif userInput == "7":           
            modifyMatch()
        elif userInput == "8":
            print_ranking()
        elif userInput == "0":
            print("Kiitos ohjelman käytöstä.")
        else:
            print("Unknown command! Try again.") 
    db.close()        
    return


def printTeams():
    print("\nPrinting teams:\n")
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


def printMatches():
    print("\nPrinting matches:\n")
    cur.execute(
        "SELECT \
        match_ID, \
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
    id, date, stadium, teams, result = "ID", "Date", "Stadium", "Team 1 (home) vs Team 2", "Result"
    
    title = f"{id:^5}|{date:^12s}|{stadium:^28s}|{teams:^26s}|{result:^10s}"
    print(title)
    print("-" * len(title))

    for id, d, s, t, r in results:
        print(f"{id:^5}|{d:^12s}|{s:^28s}|{t:^26s}|{r:^10s}")
    return


def printPlayersAndStats():

    print("\nPrinting players and stats\n")
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


def print_players_wins_from_home():
    cur.execute(
        "SELECT \
            (Player.first_name || ' ' || Player.last_name) as player, \
            Team.team_name_short, \
            (stadium_name || ', ' || stadium_town), \
            COUNT(Match.winner_ID) \
        FROM Stadium \
        INNER JOIN Player ON Player.FK_home_stadium_ID = Stadium.stadium_ID \
        INNER JOIN Match ON Match.FK_stadium_ID = Stadium.stadium_ID \
        INNER JOIN Team ON Team.team_ID = Player.FK_team_ID \
        WHERE Match.winner_ID = Player.FK_team_ID \
        GROUP BY player;"
    )

    print("\nPlayers that has won matches in their home stadium:\n")

    name, team, stadion, count = "Player", "Team", "Home stadium", "Count"
    title = f"{name:^22}|{team:^8}|{stadion:^28}|{count:^7}"
    print(title)
    print("-" * len(title))

    for name, team, stadion, count in cur.fetchall():
        print(f"{name:^22}|{team:^8}|{stadion:^28}|{count:^7}")
    return


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
    
    print(f"\nCurrent pike king(s) has {results[0][2]} pikes:\n")

    name, team = ("Name", "Team name")
    
    title = f"{name:^22}|{team:^12}"
    print(title)
    print("-" * len(title))

    for name, team, _ in results:
        print(f"{name:^22}|{team:^12}")
    return


def searchTeam():
    teamName = input("\nWhat is the teamname? ")
    cur.execute(
        f"SELECT team_name, team_name_short, GROUP_CONCAT(Player.first_name || ' ' || Player.last_name, ', ') \
        FROM Team \
        INNER JOIN Player ON Player.FK_team_id = Team.team_ID \
        WHERE team_name = '{teamName}';")

    oneRow = cur.fetchone()

    if oneRow[0] == None:
        print(f"Team {teamName} not found.")
        return

    print("\nTeam name: " + str(oneRow[0]))
    print("Short team name: " + str(oneRow[1]))
    print("Players: " + str(oneRow[2]))
    return


def modifyMatch():
    option = -1
    while option != "0":
        option = input("\nModify options:\n1: Add a new match\n2: Move a match date\n3: Remove a match\n0: Return to menu\nWhat do you want to do? ")
        if option == "1":
            matchdate = input("\nGive matchdate (dd-mm-yyyy): ")
            try:
                datetime.datetime.strptime(matchdate, "%d-%m-%Y")
            except ValueError:
                print("Incorrect date, modification failed.")
                continue
            stadium = input("Give stadium ID: ")
            team1 = input("Give team 1 ID: ")
            team2 = input("Give team 2 ID: ")
            result1 = input("Give result of team 1: ")
            result2 = input("Give result of team 2: ")
            winner = input("Give winner ID: ")
            cur.execute("INSERT INTO Match VALUES (((SELECT max(match_ID) FROM MATCH) +1),?,?,?,?,?,?,?);", (stadium, matchdate, result1, result2, team1, team2, winner,))
            db.commit()
            print("\nNew match added.")
        elif option == "2":
            matchID = input("\nWhat is the matchID of the match you want to move? ")
            newMatchDate = input ("\nWhat is the new matchdate you want to set (dd-mm-yyyy)? ")
            try:
                datetime.datetime.strptime(newMatchDate, "%d-%m-%Y")
            except ValueError:
                print("Incorrect date, modification failed.")
                continue
            cur.execute("UPDATE Match SET match_date=(?) WHERE match_ID=(?);", (newMatchDate, matchID,))
            db.commit()
            print("\nMatch moved successfully.")                
        elif option == "3": 
            matchID = input("\nWhat is the matchID of the match you want to remove? ")
            cur.execute("DELETE FROM Match WHERE match_ID=(?);", (matchID,))
            db.commit()
            print("\nMatch removed.")
        elif option == "0":
            print("\nReturning to menu...")
        else:
            print("\nUnknown option.")
    return


def print_ranking():
    cur.execute(
        "SELECT \
            Team.team_name_short, \
            ranking_points \
        FROM Ranking \
        INNER JOIN Team ON Team.team_ID = Ranking.FK_team_ID \
        ORDER BY ranking_points DESC;"
    )
    results = cur.fetchall()
    
    print(f"\nCurrent ranking is:\n")

    team, points = ("Team", "Points")
    
    title = f"{team:^8}|{points:^8}"
    print(title)
    print("-" * len(title))

    for team, points in results:
        print(f"{team:^8}|{points:^8}")
    return


if __name__ == "__main__": main()

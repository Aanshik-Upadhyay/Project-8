#CSE 231 Project 8
#Algorithm- developed a Python program that makes use of steam data and answer user search queries by finding appropriate games from the database.
#Functions- open_file(s), read_file, read_discount, in_year, by_genre, by_dev, per_discount, by_dev_year, by_genre_no_disc, by_dev_with_disc, main().

import csv
from operator import itemgetter


MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
        
def open_file(s): 
    #The function prompts the user to input a csv file name to open and keeps prompting until a correct name is entered. The parameter s is a string to incorporate into your prompt so you are prompting the user for a particular type of file ( "games" , "discount" ).
    while True: 
        file = input(f'\nEnter {s} file: ')
        try:
            return open(file, "r", encoding="utf-8")
        except Exception:
            print('\nNo Such file')

def read_file(fp_games):
    # This function uses the provided file pointer and reads the games data file.
    next(fp_games)

    return {
        row[0]: [
            row[1],
            row[2].split(';'),
            row[3].split(';'),
            (0 if row[4].split(';')[0].lower() == 'multi-player' else 1),
            (
                float(row[5].replace(',', '')) * 0.012
                if row[5].replace(',', '').isnumeric()
                else 0.0
            ),
            row[6],
            int(row[7]),
            int(row[8].replace('%', '')),
            (
                ['win_support'] * int(row[9])
                + ['mac_support'] * int(row[10])
                + ['lin_support'] * int(row[11])
            ),
        ]
        for row in csv.reader(fp_games)
    }

def read_discount(fp_discount):
    #The function would read the discount file and create a dictionary with key as the name of the game and value as the discount as a float rounded to 2 decimals.
    next(fp_discount, None)
    dictionary = {}
    fp = csv.reader(fp_discount)    
    
    for row in fp:
        name = row[0]
        dictionary[name] = round(float(row[1]), 2)
    
    return dictionary
    
def in_year(master_D, year):
    #Returns a sorted list of keys from a dictionary whose values contain a specific year as a string.
    match_keys = [key for key, value in master_D.items() if str(year) in value[0]]
    return sorted(match_keys)

def by_genre(master_D,genre): 
    #The function filters out games that are of a specific genre from the main dictionary you have created in the read_file function (master_D).
    game = []
    game_names = []
    
    for items in master_D.items():
        name = items[0]
        genres = items[1][2]
        percent = items[1][7]
        if genre in genres:
            game.append([percent, name])
    
    list_sorted = sorted(game, key=itemgetter(0), reverse=True)

    for lst in list_sorted:
        game_names.append(lst[1])
    
    return game_names 
        
def by_dev(master_D, developer):
    #Returns a list of keys from a dictionary filtered by developer and sorted by descending order of release year.
    list_selection = [(key, master_D[key][0].split('/')[2]) for key in master_D if developer in master_D[key][1]]
    list_sorted = sorted(list_selection, key=itemgetter(1), reverse=True)
    return [element[0] for element in list_sorted]

def per_discount(master_D, games, discount_D):
    #Returns a list of discounted prices for a list of games, based on a discount dictionary.
    prices = []
    for game in games:
        if game in discount_D:
            discount = discount_D[game] / 100
            price = master_D[game][4] * (1 - discount)
            prices.append(round(price, 6))
        else:
            prices.append(master_D[game][4])
    return prices

def by_dev_year(master_D, discount_D, developer, year):
    #Returns a list of games from a dictionary filtered by developer and release year, and sorted by ascending order of price with discount applied.
    selection_list = []
    for game in master_D:
        if developer in master_D[game][1] and str(year) in master_D[game][0]:
            if game in discount_D:
                discount = discount_D[game] / 100
                price = master_D[game][4] * (1 - discount)
            else:
                price = master_D[game][4]
            selection_list.append((game, round(price, 6)))
    list_sorted = sorted(selection_list, key=itemgetter(1), reverse=False)
    return [element[0] for element in list_sorted]

def by_genre_no_disc(master_D,discount_D,genre):
    #This function filters out games by a specific genre that do not offer a discount on their price. It returns a list of game names sorted from cheapest to most expensive. If there is a tie, it should be sorted by the percentage positive reviews in descending order.
    
    g_and_c = []
    game_sorted = []
    games = by_genre(master_D, genre)
    
    for game in games:
        cost = master_D[game][4]
        if game not in discount_D.keys():
            g_and_c.append([cost, game])
    
    list_sorted = sorted(g_and_c, key=itemgetter(0))

    for s in list_sorted:
        game_sorted.append(s[1])

    return game_sorted 


def by_dev_with_disc(master_D, discount_D, developer):
    '''docstring'''
    selection_list = [(game, master_D[game][4]) for game in master_D 
                      if developer in master_D[game][1] and game in discount_D]
    return [element[0] for element in sorted(selection_list, key=itemgetter(1))]
             
def main(): #main
    game_fp = open_file('games')
    master_D = read_file(game_fp)
    discount_fp = open_file('discount')
    discount_D = read_discount(discount_fp)

    options_user = input(MENU)
    while options_user != '7':

        if options_user == '1':
            while True:
                year = input('\nWhich year: ')

                try:
                    year = int(year)

                    if in_year(master_D, year) == []:
                        print("\nNothing to print")
                    
                    else:
                        print(f"\nGames released in {year}:\n{', '.join(in_year(master_D, year))}")

                    break

                except:
                    print("\nPlease enter a valid year")
                    continue

            options_user = input(MENU)
            
        elif options_user == '2':
            developer = input('\nWhich developer: ')
            games_by_dev = by_dev(master_D, developer)

            if games_by_dev != []:
                print(f"\nGames made by {developer}:\n{', '.join(games_by_dev)}")
            else:
                print("\nNothing to print")

            options_user = input(MENU)

        elif options_user == '3':
            genre = input('\nWhich genre: ')
            games_by_genre = by_genre(master_D, genre)

            if games_by_genre != []:
                print(f"\nGames with {genre} genre:\n{', '.join(games_by_genre)}")
            else:
                print("\nNothing to print")

            options_user = input(MENU)

        elif options_user == '4':
            developer = input('\nWhich developer: ')
            year = input('\nWhich year: ')
            games_by_dev_year = by_dev_year(master_D,discount_D,developer,year)

            try:
                year = int(year)

                if games_by_dev_year != []:
                    print(f"\nGames made by {developer} and released in {year}:\n{', '.join(games_by_dev_year)}")

                else:
                    print("\nNothing to print")

            except:
                print("\nPlease enter a valid year")

            options_user = input(MENU)

        elif options_user == '5':
            genre = input('\nWhich genre: ')
            games_by_genre_no_disc = by_genre_no_disc(master_D,discount_D,genre)

            if games_by_genre_no_disc != []:
                print(f"\nGames with {genre} genre and without a discount:\n{', '.join(games_by_genre_no_disc)}")

            else:
                print("\nNothing to print")

            options_user = input(MENU)

        elif options_user == '6':
            developer = input('\nWhich developer: ')
            games_by_dev_disc = by_dev_with_disc(master_D,discount_D,developer)
            
            if games_by_dev_disc != []:
                print(f"\nGames made by {developer} which offer discount:\n{', '.join(games_by_dev_disc)}")

            else:
                print("\nNothing to print")

            options_user = input(MENU)
        
        else:
            print("\nInvalid option")
            options_user = input(MENU)

    print("\nThank you.")


if __name__ == "__main__":
    main()

#end

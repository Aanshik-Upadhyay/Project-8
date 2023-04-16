import csv
from operator import itemgetter

def open_file(s):
    ''' Docstring'''
    while True: # Infinite Loop
        try:
            file = input(f'\nEnter {s} file: ')
            file_name = f'{file}.csv'
            fp = open(file_name, encoding='UTF-8') # Open the file 
            break

        except FileNotFoundError:
            print('\nNo Such file') 
            continue

    return fp

def read_file(fp_games):
    ''' Docstring'''
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
    '''Reads a CSV file and returns a dictionary with rounded float values.'''
    file_reader = csv.reader(fp_discount)
    next(file_reader) # skip header row
    return {row[0]: round(float(row[1]), 2) for row in file_reader}
    

def in_year(master_D, year):
    '''Returns a sorted list of keys from a dictionary whose values contain a specific year as a string.'''
    match_keys = [key for key, value in master_D.items() if str(year) in value[0]]
    return sorted(match_keys)

def by_genre(master_D, genre):
    '''Returns a list of keys from a dictionary filtered by genre and sorted by descending order of genre-specific score.'''
    list_selection = [(key, master_D[key][7]) for key in master_D if genre in master_D[key][2]]
    list_sorted = sorted(list_selection, key=itemgetter(1), reverse=True)
    return [element[0] for element in list_sorted]
        
def by_dev(master_D, developer):
    '''Returns a list of keys from a dictionary filtered by developer and sorted by descending order of release year.'''
    list_selection = [(key, master_D[key][0].split('/')[2]) for key in master_D if developer in master_D[key][1]]
    list_sorted = sorted(list_selection, key=itemgetter(1), reverse=True)
    return [element[0] for element in list_sorted]

def per_discount(master_D, games, discount_dict):
    '''Returns a list of discounted prices for a list of games, based on a discount dictionary.'''
    prices = []
    for game in games:
        if game in discount_dict:
            discount = discount_dict[game] / 100
            price = master_D[game][4] * (1 - discount)
            prices.append(round(price, 6))
        else:
            prices.append(master_D[game][4])
    return prices

def by_dev_year(master_D,discount_D,developer,year):
    ''' Docstring'''

    for game in master_D:
        if developer in master_D[game][1] and str(year) in master_D[game][0]:
            if game not in discount_D:
                final_list.append((game, master_D[game][4]))
            else:
                final_list.append((game, round((1- (discount_D[game]/100))*master_D[game][4],6)))
    

    return [element[0] for element in sorted(selection_list, key=itemgetter(1), reverse=False)]
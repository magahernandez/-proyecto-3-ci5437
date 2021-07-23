from datetime import datetime
import json
import sys
import time
import os

# Type: 0 start and 1 end
def exact_hour(type_hour,hour):
    if(hour[3:5] == '00'):
        return hour
    else:
        if(type_hour == 0):
            return str(int(hour[0:2]) + 1) + ':00'
        else:
            return hour[0:3] + '00'
    return hour

def play_at_least_one(clauses,inf):
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            if i != j:
                clause = []
                for d in range(inf['number_of_days']):
                    for b in range(inf['games_per_day']):
                        clause.append(set_literal(i, j, d, b))
                clauses.append(clause)
    return clauses

def play_max_one(clauses,inf):
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            if i != j:
                for d in range(inf['number_of_days']):
                    for b in range(inf['games_per_day']):
                        for d_fixed in range(d+1, inf['number_of_days']):
                            for b_fixed in range(inf['games_per_day']):
                                clauses.append([-set_literal(i, j, d, b),-set_literal(i, j, d_fixed, b_fixed)])
    return clauses

def play_twice_with_each_others(clauses,inf):
    clauses = play_at_least_one(clauses,inf)
    clauses = play_max_one(clauses,inf)
    return clauses

def no_games_at_the_same_time(clauses,inf):
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            if i != j:
                for d in range(inf['number_of_days']):
                    for b in range(inf['games_per_day']):
                        for i_fixed in range(inf['number_of_teams']):
                            for j_fixed in range(inf['number_of_teams']):
                                if (i != i_fixed or j != j_fixed) and i_fixed != j_fixed:
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i_fixed, j_fixed, d, b)])
    return clauses

def play_once_a_day(clauses,inf):
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            if i != j:
                for d in range(inf['number_of_days']):
                    for b in range(inf['games_per_day']):
                        for j_fixed in range(inf['number_of_teams']):
                            if i != j_fixed and j_fixed != j:
                                for b_fixed in range(inf['games_per_day']):
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i, j_fixed, d+1, b_fixed)])
                        for i_fixed in range(inf['number_of_teams']):
                            if j != i_fixed and i_fixed != i:
                                for b_fixed in range(inf['games_per_day']):
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i_fixed, j, d+1, b_fixed)])    
    return clauses

def consecutives_dates(clauses,inf):
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            if i != j:
                for d in range(inf['number_of_days']-1):
                    for b in range(inf['games_per_day']):
                        for j_fixed in range(inf['number_of_teams']):
                            if i != j_fixed and j_fixed != j:
                                for b_fixed in range(inf['number_of_days']):
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i, j_fixed, d+1, b_fixed)])
                        for i_fixed in range(inf['number_of_teams']):
                            if j != i_fixed and i_fixed != i:
                                for b_fixed in range(inf['number_of_days']):
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i_fixed, j, d+1, b_fixed)])
    return clauses

def max_one(clauses,inf):
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            if i != j:
                for d in range(inf['number_of_days']):
                    for b in range(inf['games_per_day']):
                        for b_fixed in range(b+1,inf['games_per_day']):
                            if i < j:
                                clauses.append([-set_literal(i, j, d, b),-set_literal(i, j, d, b_fixed)])
                                clauses.append([-set_literal(i, j, d, b),-set_literal(j, i, d, b_fixed)])
                                clauses.append([-set_literal(j, i, d, b),-set_literal(i, j, d, b_fixed)])
                                clauses.append([-set_literal(j, i, d, b),-set_literal(j, i, d, b_fixed)])
                            for j_fixed in range(inf['number_of_teams']):
                                if j != j_fixed and i != j_fixed:
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i, j_fixed, d, b_fixed)])
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(j_fixed, i, d, b_fixed)])
                                    clauses.append([-set_literal(j, i, d, b),-set_literal(j_fixed, i, d, b_fixed)])
                                    clauses.append([-set_literal(j, i, d, b),-set_literal(i, j_fixed, d, b_fixed)])  
    return clauses

def set_literal(i,j,d,b):
    maximum = max([inf['number_of_teams'],inf['number_of_days'],inf['games_per_day']])
    return i*(maximum**3) + j*(maximum**2) + d*(maximum**1) +b*(maximum**0)

def num_of_literales(i,d,b):
    return i*i*d*b

def write_clauses(clauses,file):
    for clause in clauses:
        for literal in clause:
            file.write(str(literal))
            file.write(" ")
        file.write("0\n")
    return

def get_valid_literals(nameFile):
    lista = []
    with open(nameFile, 'r') as file:
        data = file.read().replace('\n', '')
        lista = data.split(" ")
        lista = filter(get_valid_literal, lista)
    lista = list(lista)
    return list(map(get_index_literal, lista))

def get_valid_literal(x):
    maximum = max([inf['number_of_teams'],inf['number_of_days'],inf['games_per_day']])
    is_valid = False
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            for d in range(inf['number_of_days']):
                for b in range(inf['games_per_day']):
                    if(i*(maximum**3) + j*(maximum**2) + d*(maximum**1) +b*(maximum**0) == int(x)):
                        is_valid = True
                        return is_valid
    return 

def get_index_literal(x):
    maximum = max([inf['number_of_teams'],inf['number_of_days'],inf['games_per_day']])
    for i in range(inf['number_of_teams']):
        for j in range(inf['number_of_teams']):
            for d in range(inf['number_of_days']):
                for b in range(inf['games_per_day']):
                    if(i*(maximum**3) + j*(maximum**2) + d*(maximum**1) +b*(maximum**0) == int(x)):
                        return [i,j,d,b]

def get_arguments(inf):
    return {
        "number_of_teams": len(inf['participants']),
        "start_date": str(datetime.strptime(inf['start_date'], '%Y-%m-%d')),
        "end_date": str(datetime.strptime(inf['end_date'], '%Y-%m-%d')),
        "start_hour": str(datetime.strptime(exact_hour(0,inf['start_time']), '%H:%M')),
        "end_hour": str(datetime.strptime(exact_hour(1,inf['end_time']), '%H:%M')),
        "number_of_days": (datetime.strptime(inf['end_date'], '%Y-%m-%d') - datetime.strptime(inf['start_date'], '%Y-%m-%d')).days,
        "valid_time": str(datetime.strptime(exact_hour(1,inf['end_time']), '%H:%M') - datetime.strptime(exact_hour(0,inf['start_time']), '%H:%M')),
        "games_per_day": int(((datetime.strptime(exact_hour(1,inf['end_time']), '%H:%M') - datetime.strptime(exact_hour(0,inf['start_time']), '%H:%M')).seconds//(3600*2)))
    }

def cnf(data,nameFile):

    global inf
    inf = get_arguments(data)
    clauses = []

    name_txt = 'cnf/'+nameFile + '_cnf.txt'

    os.makedirs('cnf', exist_ok=True)
    with open(f'%s' %name_txt, 'w') as cnf_file:

        clauses = play_twice_with_each_others(clauses,inf)
        clauses = no_games_at_the_same_time(clauses,inf)
        clauses = play_once_a_day(clauses,inf)
        clauses = consecutives_dates(clauses,inf)
        clauses = max_one(clauses,inf)

        cnf_file.write('p cnf ' + str(num_of_literales(inf['number_of_teams'], inf['number_of_days'],inf['games_per_day']))+' '+ str(len(clauses)) +' ' + '\n')

        write_clauses(clauses,cnf_file)
        cnf_file.close()

    return

def main():
    with open(str('test/'+sys.argv[1]), "r") as fichero:
        data = json.load(fichero)
        fichero.close()

    return cnf(data,sys.argv[1].replace('.json',''))

if __name__ == "__main__":
    main()
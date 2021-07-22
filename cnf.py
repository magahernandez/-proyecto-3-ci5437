from datetime import datetime

import json
import sys
import time

# Type: 0 start and 1 end
# Rest 5
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
                            for b_fixed in range(inf['games_per_day']):
                                if j_fixed != j and b_fixed != b:
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(i, j_fixed, d, b_fixed)])
                                    clauses.append([-set_literal(i, j, d, b),-set_literal(j_fixed, i, d, b_fixed)])
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


def set_literal(i,j,d,b):
    maximum = max([i,j,d,b])
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

def get_arguments(inf):
    return {
        "number_of_teams": len(inf['participants']),
        "start_date": datetime.strptime(inf['start_date'], '%Y-%m-%d'),
        "end_date": datetime.strptime(inf['end_date'], '%Y-%m-%d'),
        "start_hour": datetime.strptime(exact_hour(0,inf['start_time']), '%H:%M'),
        "end_hour": datetime.strptime(exact_hour(1,inf['end_time']), '%H:%M'),
        "number_of_days": (datetime.strptime(inf['end_date'], '%Y-%m-%d') - datetime.strptime(inf['start_date'], '%Y-%m-%d')).days,
        "valid_time": datetime.strptime(exact_hour(1,inf['end_time']), '%H:%M') - datetime.strptime(exact_hour(0,inf['start_time']), '%H:%M'),
        "games_per_day": int(((datetime.strptime(exact_hour(1,inf['end_time']), '%H:%M') - datetime.strptime(exact_hour(0,inf['start_time']), '%H:%M')).seconds//(3600*2)))
    }

def cnf(data,nameFile):

    inf = get_arguments(data)
    clauses = []

    name_txt = nameFile + '_cnf.txt'

    with open(f'%s' %name_txt, 'w') as cnf_file:
        #cnf_file.write('c test1 \n')
        #cnf_file.write('c\n')

        # Rest 1
        clauses = play_twice_with_each_others(clauses,inf)

        # Rest 2
        clauses = no_games_at_the_same_time(clauses,inf)

        # Rest 3
        clauses = play_once_a_day(clauses,inf)

        # Rest 4
        clauses = consecutives_dates(clauses,inf)

        cnf_file.write('p cnf ' + str(num_of_literales(inf['number_of_teams'], inf['number_of_days'],inf['games_per_day']))+' '+ str(len(clauses)) +' ' + '\n')

        write_clauses(clauses,cnf_file)
        cnf_file.close()

    return

def main():
    with open(sys.argv[1], "r") as fichero:
        data = json.load(fichero)
        fichero.close()

    return cnf(data,sys.argv[1].replace('.json',''))

if __name__ == "__main__":
    main()
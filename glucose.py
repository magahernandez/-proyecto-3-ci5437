import sys

import os
import subprocess
import shutil
import ics_transform


def main(nameFile):
    sys.path.insert(2, 'glucose-syrup-4.1/simp/glucose_static')
    os.system('ls')
    shutil.copy(nameFile.replace('.json','_cnf.txt'), "glucose-syrup-4.1/simp/"+nameFile.replace('.json','_cnf.txt'))
    os.system('ls')
    os.chdir('glucose-syrup-4.1/simp/')
    subprocess.call(["./glucose_static", nameFile.replace('.json','_cnf.txt'), "-model", ">>>", nameFile.replace('.json','_glucose.txt')])
    
    f = open(nameFile.replace('.json','_glucose.txt'), "r")
    for linea in f:
        if(linea.find("UNSAT") == 0):
            print("No se puede satisfacer este caso")
            f.close()
            return

    f.close()

    shutil.copy(nameFile.replace('.json','_glucose.txt'), "../../"+nameFile.replace('.json','_glucose.txt'))
    ics_transform.main(nameFile.replace('.json','_glucose.txt'))

if __name__ == "__main__":
    main(nameFile)
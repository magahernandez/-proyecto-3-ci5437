import sys

import os
import subprocess
import shutil


def main(nameFile):
    sys.path.insert(2, 'glucose-syrup-4.1/simp/glucose_static')
    shutil.copy(nameFile.replace('.json','_cnf.txt'), "glucose-syrup-4.1/simp/"+nameFile.replace('.json','_cnf.txt'))
    os.chdir('glucose-syrup-4.1/simp/')
    subprocess.call(["./glucose_static", nameFile.replace('.json','_cnf.txt'), "-model", ">>>", nameFile.replace('.json','_glucose.txt')])

    shutil.copy(nameFile.replace('.json','_glucose.txt'), "../../"+nameFile.replace('.json','_glucose.txt'))

    #subprocess.call(["echo", "1", ">>", "t.txt"], shell=True)


if __name__ == "__main__":
    main(nameFile)
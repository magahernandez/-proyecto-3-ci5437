from datetime import datetime

import json
import sys
import time

import cnf
import glucose

def main():
    if len(sys.argv) > 1:
        cnf.main()
        glucose.main(sys.argv[1])
    else:
        x = (input("Enter JSON file: "))

# Ejemplo de como correr: python3 main.py name.json
if __name__ == '__main__':
    main()
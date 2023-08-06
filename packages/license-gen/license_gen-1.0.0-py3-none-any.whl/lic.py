from sys import argv, exit
from os import listdir
from shutil import copyfile

def copy_license(name, filename):
    copyfile(f'../licenses/{name}', filename)

def create_license(name, filename):
    copyfile(filename, f'../licenses/{name}.txt')

def main():
    args = argv[1:]

    licenses = listdir('../licenses')

    if(len(args)<1):
        print("No arguments recieved.")
        exit(0)

    if '-o' in args:
        ofile = args[args.index('-o')+1]
    else:
        ofile = 'LICENSE'

    if 'create' in args:
        index = args.index('create')
        create_license(args[index+1], args[index+2])

    for arg in args:
        if (arg+'.txt') in licenses:
            copy_license(arg+'.txt', ofile)

if __name__ == '__main__':
    main()

import requests
import click
import os

domains = []
def check(path):
    global domains
    with open(path, 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('<BR>', '\n')
    with open(path,'w') as f:
        f.write(new_data)
    with open(path, 'r') as f:
        domains = f.readlines()

    if '/' in path:
        file = str(path.split('/')[-1])
        file = file.replace('.txt','')
        print("Result will be saved in " + file)
        try:
            # Create target Directory
            os.mkdir(file)
        except FileExistsError:
            print("Error, this folder already exists")
            inp = str(input("Clear result files? Y/n: "))
            inp = inp.lower()
            if inp == "y":
                with open(file + '/' + 'result_not200.txt', 'w') as f:
                    f.write("")

    for d in domains:
        d = d.replace('\n','')
        if 'http:' in d or 'https:' in d:
            pass
        else:
            d = "http://"+d
        try:
            req = requests.get(d,timeout=0.6)
            st = req.status_code
            print ("Url: "+d+" Status code: "+str(st))
            if st == 301 or st == 302 or st == 403 or st == 404 or st == 500:
                with open(file + '/'+'result_not200.txt', 'a') as f:
                    f.write(d + '\n')
            elif st == 200:
                with open(file + '/'+'result_200.txt', 'a') as f:
                    f.write(d + '\n')
        except:
            pass



@click.command()
@click.option(
    '--path', '-p',
    help='your path to file',
)
def main(path):
    """
    A little tool for sort your domains by response code

    How to use?

    python3 domaincheck.py -p /path/to/file.txt
    """

    check(path)

if __name__ == "__main__":
    main()

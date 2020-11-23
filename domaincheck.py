import requests
import click
import os
import urllib3
import threading
import numpy as np

domains = []
folder_name = ''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable https warnings


def dir_create(path):
    global folder_name
    if '/' in path:
        folder_name = str(path.split('/')[-1]).replace('.txt', '')  # Get folder name from the path
        print("Result will be saved in " + folder_name)
    else:
        folder_name = path.replace('.txt', '')

    try:
        os.mkdir(folder_name)
    except FileExistsError:
        print("Error, this folder already exists")
        inp = str(input("Clear result files? Y/n: "))
        inp = inp.lower()
        if inp == "y":
            with open(folder_name + '/' + 'result_not200.txt', 'w') as f:
                f.write("")
            with open(folder_name + '/' + 'result_200.txt', 'w') as f:
                f.write("")


def check(domains):
    for d in domains:
        d = d.replace('\n', '')
        if 'http://' in d or 'https://' in d:
            pass
        else:
            d = "http://" + d

        try:
            req = requests.get(d, timeout=3, allow_redirects=True, verify=False)
            d_redirected = ''
            if req.url[:-1] != d and req.url[:-1] != '':  # req.url[:-1] - removes "/" at the end of url
                d_redirected = ' --> ' + req.url[:-1]
            print("Url: " + d + d_redirected + " Status code: " + str(req.status_code))
            if req.status_code == 200:
                with open(folder_name + '/'+'result_200.txt', 'a') as f:
                    f.write(d + d_redirected + '\n')
            else:
                with open(folder_name + '/'+'result_not200.txt', 'a') as f:
                    f.write(d + d_redirected + '\n')
        except requests.exceptions.SSLError as ex_ssl:
            print("SSL ERROR!")

        except requests.exceptions.ConnectionError as ex:
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

    dir_create(path)
    global domains

    with open(path, 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('<BR>', '\n')
    with open(path, 'w') as f:
        f.write(new_data)
    with open(path, 'r') as f:
        domains = f.readlines()

    domains_parts = np.array_split(domains, 50)

    for i in range(0, 50):
        thr = threading.Thread(target=check, args=(domains_parts[i], ))
        thr.start()


if __name__ == "__main__":
    main()

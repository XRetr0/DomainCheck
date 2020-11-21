import requests
import click
import os
import urllib3

domains = []
folder_name = ''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def dir_create(path):
    global folder_name
    if '/' in path:
        folder_name = str(path.split('/')[-1]).replace('.txt', '')
        print("Result will be saved in " + folder_name)
    else:
        folder_name = path.replace('.txt', '')

    try:
        os.mkdir(folder_name)  # Create target Directory
    except FileExistsError:
        print("Error, this folder already exists")
        inp = str(input("Clear result files? Y/n: "))
        inp = inp.lower()
        if inp == "y":
            with open(folder_name + '/' + 'result_not200.txt', 'w') as f:
                f.write("")


def check(path):
    global domains
    with open(path, 'r') as f:
        old_data = f.read()
    new_data = old_data.replace('<BR>', '\n')
    with open(path, 'w') as f:
        f.write(new_data)
    with open(path, 'r') as f:
        domains = f.readlines()

    dir_create(path)

    for d in domains:
        d = d.replace('\n', '')
        if 'http:' in d or 'https:' in d:
            pass
        else:
            d = "http://" + d

        try:
            req = requests.get(d, timeout=3, allow_redirects=True, verify=False)
            st = req.status_code
            if 'https://' in req.url:
                d = req.url
            print("Url: " + d + " Status code: " + str(st))
            if st == 200:  # bad code
                with open(folder_name + '/'+'result_200.txt', 'a') as f:
                    f.write(d + '\n')
            else:
                with open(folder_name + '/'+'result_not200.txt', 'a') as f:
                    f.write(d + '\n')
        except requests.exceptions.SSLError as ex_ssl:
            print(str(ex_ssl))
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

    check(path)


if __name__ == "__main__":
    main()

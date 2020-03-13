import requests
import click

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

    for d in domains:
        print(d)


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
import click
from flows import rick_and_morty_flow

@click.command()
def main():
    rick_and_morty_flow()
    
if __name__ == '__main__':
    main()
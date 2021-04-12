import pandas as pd
import click



def get_label(i, n, tweet):
    """
    Possible labels will be positive(<left-arrow>),
    neutral(<down-arrow>), negative(<right-arrow>),
    invalid(<up-arrow>)
    """
    click.echo(f"{i}/{n}: {tweet}")
    while True:
        click.echo("Label (←(-1)/↓(0)/→(1)/↑(None)): ")
        c = click.getchar()
        if c == '\x1b[D':
            click.echo('')
            return -1
        elif c == '\x1b[C':
            click.echo('')
            return 1
        elif c == '\x1b[B':
            click.echo('')
            return 0
        elif c == '\x1b[A':
            click.echo('')
            return None
        click.echo("Invalid option")
    

def main():

    df = pd.read_csv('data.csv')

    labels = []
    n = len(df.index)
    for i, (index, tweet) in enumerate(df.iterrows(), 1):
        label = get_label(i, n, tweet['text'])
        labels.append(label)

    df['labels'] = pd.Series(labels)

    df.to_csv('labelled-data.csv')
            
        
__name__ == '__main__' and main()

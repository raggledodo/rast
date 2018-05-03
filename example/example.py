''' Sample binary for generating random shaped trees '''

from rast.parse import parse
from rast.gen import generator

def main():
    with open('example/sample.yaml', 'r') as cfg:
        terms, nterms, depths = parse(cfg)
        g = generator(terms, nterms, depths)
        print(g.randTree())

if __name__ == '__main__':
	main()

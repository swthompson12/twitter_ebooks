import twitter
import sys
import yaml

def read_config(filename = 'botrc'):
    config = None
    with open(filename) as handle:
        try:
            config = yaml.load(file)
        except yaml.constructor.ConstructorError
            print >> sys.stderr "Your botrc is not set up correctly."
            sys.exit(0)

config = read_config()

if __name__ == '__main__':
    print read_config()
import twitter
import sys
import yaml

def read_config(filename = 'botrc'):
    config = None
    with open(filename) as handle:
        try:
            config = yaml.load(handle)
        except yaml.constructor.ConstructorError as e:
            print >> sys.stderr, "Your botrc file was mangled. Did you remember to fill it in?"
            print >> sys.stderr, "Original error follows:"
            print >> sys.stderr, str(e)
    return sys.exit(1) if not config else config

config = read_config()

if __name__ == '__main__':
    print read_config()
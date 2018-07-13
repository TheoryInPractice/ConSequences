from converters import td_to_conseq
import sys

td = sys.argv[1]
_map = sys.argv[2]
out =sys.argv[3]

if __name__ == '__main__':
    td_to_conseq(td, _map, out)


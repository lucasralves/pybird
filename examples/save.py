import sys
sys.path.append('./src')

import pybird


if __name__ == '__main__':
    pybird.init()
    pybird.load('./examples/data/data.case')
    pybird.model.name = 'novo nome'
    pybird.save('./examples/data/data_2.case')
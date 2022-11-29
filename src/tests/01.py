"""
    Load and save test
"""
import sys
sys.path.append('./src/')

import pybird

if __name__ == '__main__':
    model = pybird.create_model()
    model.load('./src/tests/data/input/data.case')
    model.info.name = 'novo nome'
    model.save('./src/tests/data/input/data2.case')
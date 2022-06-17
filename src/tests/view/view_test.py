import sys
sys.path.append('./src')

import pybird

if __name__ == '__main__':

    model = pybird.model('view_test')

    model.view.mesh()
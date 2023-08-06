
import os
base_path = os.path.abspath(os.path.dirname(__file__))


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    config = Configuration('mod2', parent_package, top_path)

    return config
if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(maintainer='scikit-image Developers',
          maintainer_email='skimage@discuss.scientific-python.org',
          description='module 2nd',
          url='#',
          license='Modified BSD',
          **(configuration(top_path='').todict())
          )

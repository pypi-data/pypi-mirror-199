import cython
import pyximport; pyximport.install()
from alacorder import cal as alac

if __name__ == "__main__":
	alac.loadgui()
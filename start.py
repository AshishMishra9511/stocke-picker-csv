import sys
import os
from stock_picker import StockPicker

if __name__=="__main__":
    filename = sys.argv[1]
    stock_picker = StockPicker(filename)
    if not os.path.exists(filename):
        print(filename + " does not exists")
        sys.exit()
    stock_picker.run()
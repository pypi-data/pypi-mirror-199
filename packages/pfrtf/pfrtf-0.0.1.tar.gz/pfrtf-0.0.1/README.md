# pfrtf - Pandas fast reading table file by using pickle

This module will speed up the loading of data into Pandas from files that rarely change. Supports file formats (.xlsx, .xls, .xlsm, .xlsb and .csv). This module tracks file hashes and saves data in *.pkl format. If the file has already been read, re-reading occurs from the *.pkl file. This significantly speeds up the loading of data. In my case, it speeds up data reading by 100 times.

# Requirements
    Pandas>=1.4.4
    openpyxl>=2.6.0

# Install
    pip install pfrtf

# Tutorial:
    import pfrtf
    import os
    path_file = os.path.join(os.getcwd(),'SampleData.xlsx')
    df = pfrtf.fast_read_file(path_file)

    import pfrtf
    df = pfrtf.fast_read_file(r'C:\Users\user\SampleData.xlsx')

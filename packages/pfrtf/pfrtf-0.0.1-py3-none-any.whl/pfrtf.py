#pfrtf.py
from pandas import read_pickle, read_excel, read_csv, DataFrame
from hashlib import md5
from os import path



def fast_read_file(path_file, header=0):
    path_file = path.normcase(path_file)
    pre, ext = path.splitext(path_file)
    path_file_pkl = pre+'_pkl.pkl'
    if this_file_has_been_read(path_file, path_file_pkl):
        df = read_pickle(path_file_pkl)
    else:
        if ext in ['.xls', '.xlsx', '.xlsm', '.xlsb']:
            df = read_excel(path_file, header=header)
        elif ext == '.csv':
            df = read_csv(path_file, header=header)
        else :
            raise Exception("Module quick_table_rereading.py does not support format '" + ext + "'!")
        df.to_pickle(path_file_pkl)
    return df


def this_file_has_been_read(path_file, path_file_pkl):
    answer = False
    hash_table_file = path.join(path.dirname(path_file_pkl),  'hash_table.pkl')
    if path.exists(hash_table_file):
        df_hash_table = read_pickle(hash_table_file)
    else:
        df_hash_table = DataFrame(columns=['hash'])
    filename = path.basename(path_file)
    file_name_hash = md5(filename.encode('utf-8')).hexdigest()
    file_hash = md5_file(path_file)
    try:
        if df_hash_table.loc[file_name_hash, 'hash'] == file_hash and \
                path.exists(path_file_pkl):
            answer = True
    except KeyError:
        answer = False
    if answer == False:
        df_hash_table.loc[file_name_hash, 'hash'] = file_hash
        df_hash_table.to_pickle(hash_table_file)
    return answer


def md5_file(path_file):
    hash_md5 = md5()
    with open(path_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


__all__ = [
    "fast_read_file",
]

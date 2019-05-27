import numpy as np
from calendar import monthrange
from data_requirements import get_uniform_loans

dtype = np.dtype([('user_id', np.int32),
                 ('gender', np.int16),
                 ('expiration_date', np.int16, (3,)),
                 ('loan', np.float64, (10,))])

class records_array:
    def __init__(self, dataIn, SEED):
        np.random.seed(SEED)
        self.__dataIn = dataIn
        self.data = np.empty(len(self.__dataIn), dtype=dtype)
        self.__rewrite()
        
        
    def __get_gender(self, idx):
        return np.int16(self.__dataIn['gender'][idx] == b'M')
        
    def __expiration_date(self, idx): 
        month = np.int16(str(self.__dataIn['credit_card_expiration_date'][idx]).split('/')[0].split()[1])
        year = np.int16(2000) + np.int16(str(self.__dataIn['credit_card_expiration_date'][idx]).split('/')[1].split("'")[0])
        day = np.int16(monthrange(year, month)[1])
        return (year, month, day)
        
    def __rewrite(self):
        loans = get_uniform_loans(1000,100000,1000)
        for idx in range(len(self.__dataIn)):
            self.data['gender'][idx] = self.__get_gender(idx)
            self.data['user_id'][idx] = np.int32(self.__dataIn['id'][idx])
            self.data['expiration_date'][idx] = self.__expiration_date(idx)
            self.data['loan'][idx] = tuple([np.float64(float(np.random.choice(loans))) for i in range(10)])
            
    
    def __bytes_to_str(self, name):
        words = str(str(name, 'utf-8')).split()
        return words[-2] + ' ' + words[-1]
    
    def get_name(self, idx, byt=False):
        if byt:
            return self.__dataIn['full_name'][idx]
        else:
            return self.__bytes_to_str(self.__dataIn['full_name'][idx])
    
    def get_id(self, name):
        if type(name) == np.bytes_:
            lst_id = [idx for idx in range(len(self.__dataIn)) if self.__dataIn['full_name'][idx] == name]
        else:
            lst_id = [idx for idx in range(len(self.__dataIn))
                      if self.__bytes_to_str(self.__dataIn['full_name'][idx]) == name]
        return lst_id
    
    def remouve_row(self, idx):
        np.delete(self.data, idx, 0)
        np.delete(self.__dataIn, idx, 0)
        
    def  get_id_program(self, idx):
        def sum_digits(n):
            res = 0
            while n:
                res, n = res + n % 10, n // 10
            return res
        s = ''
        for i in str(self.__dataIn["credit_card_number"][idx], 'utf-8').split():
            s += i            
        return sum_digits(int(s))

def sum_arrays(lst1, lst2):
    if len(lst1) != len(lst2) and len(tuple1) == 10:
        raise ValueError()
    return ([lst1[i] + lst2[i] for i in range(len(lst1))])    
        
def get_loans(records):
    dct = {}
    for index, value in enumerate(records.data):    
        if records.get_id_program(index) not in dct:
            dct[records.get_id_program(index)] = records.data['loan'][index]
        else:
            dct[records.get_id_program(index)] = sum_arrays(dct[records.get_id_program(index)], records.data['loan'][index])
    return dct 
            
def rewrite_loans(records, dct):
    for i in range(len(records.data)):
        records.data['loan'][i] = dct[records.get_id_program(i)]
    return records
import numpy as np
import pytz
from datetime import datetime

def get_uniform_loans(low, high, step, size = 100000):
    res = []
    uniform_dist = list(np.sort(np.random.uniform(low, high,size=size)))
    
    for index, value in enumerate(uniform_dist):
        if index == 0:
            res.append(value)
        elif value-res[-1] >= step:
            res.append(value)
        
    res = np.array([str(i) for i in res])
    np.random.shuffle(res)        
    return res

    
def get_name(names, lst_available_id):
    array_available = np.array([names[i] for i in lst_available_id]) # !!!!
    return np.random.choice(array_available)  

    
    
def uniform_rec_id(records_npy, rng, low=0, high=12):
    gender_id = np.random.choice([0,1])
    uniform_dist = np.random.uniform(low, high + 1, size=high-low)
    number = int(np.random.choice(uniform_dist))
    
    if len(records_npy) < number:
        number, lst_idx = uniform_number_of_rec(records_npy, low, high)
        
    return number, np.random.choice([ind for ind in range(len(records_npy)) if rng[ind] == gender_id], number, replace=False)  

    
    
def data_save(data, SEED, path="./Data/"):
    if type(SEED) != int:
        raise ValueError("SEED must be int")
    file, id_file = get_file_name(SEED)   
    path_file = path + file + ".csv"
    np.savetxt(path_file, data, delimiter=',',fmt=('%16s', '%32s', '%32s', '%8s', '%1s', '%32s'),
           header='id  full_name  credit_card_number  credit_card_expiration_date  gender  loan')
    return path_file, id_file


           
def get_file_name(SEED):
    id = datetime.today().strftime('%Y%m_') + str(SEED) + datetime.today().strftime('_%Y%m%d%H%M%S')
    return "InputData_" + id, id 
    
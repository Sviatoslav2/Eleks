import numpy as np


def get_projection_number(expiration_date, valuation_date=[2019,    1,   31]):
    return (expiration_date[0] - valuation_date[0]) * 12

    
def get_monthly_payment(records, idx, prog, size=100,lim=700000):
    SEED  = records.data['user_id'][idx]
    cur_sum = np.sum(records.data['loan'][idx])
    np.random.seed(SEED)
    mu, sigma = (prog+1)/100 ,0.1
    if lim < cur_sum:
        return np.random.lognormal(mu, sigma, size)
    else:
        return np.array([0.0001 for i in range(100)])

def get_payment(prev, gender, payment_rate):
    if gender == 1:
        mortality = 1.01
    elif gender == 0:
        mortality = 0.99
    return prev *  payment_rate  * mortality              
    
def loan(prev, gender, monthly_rate ):
    # curent sum of loan == prev loan
    return np.float64(prev + get_payment(prev, gender, monthly_rate))    
    

def get_loan(begin_loan, num_month, monthly_rate, gender):
    for i in range(num_month):
        begin_loan = loan(begin_loan, gender, monthly_rate)
    return begin_loan

    
def get_programs(records, idx, scen, num_prog=10):
    res = []
    num_month = get_projection_number(records.data['expiration_date'][idx])
    gender = records.data['gender'][idx]
    
    for prog in range(num_prog):
        array_scen = get_monthly_payment(records, idx, prog)
        res.append(get_loan(records.data['loan'][idx][prog], num_month, array_scen[scen], gender))
        
    return np.array(res)    
    
    
def get_loans_matrix(records, idx, num_scen=100):
   
    matrix = []
   
    for i in range(num_scen):
        matrix.append(get_programs(records, idx, i))
    
    return np.array(matrix).T    
    
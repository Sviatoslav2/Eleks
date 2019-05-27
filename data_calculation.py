def get_projection_number(expiration_date, valuation_date=[2019,    1,   31]):
    return (expiration_date[0] - valuation_date[0]) * 12

def get_monthly_payment(records, idx, prog, lim=700000, size=100):
    SEED  = records.data['user_id'][idx]
    np.random.seed(SEED)
    mu, sigma = (prog+1)/100 ,0.1
    if lim > np.sum(records.data['loan'][idx],dtype=np.float64):
        return np.random.choise(np.random.lognormal(mu, sigma, size))
    else:
        return 0.0001 

def payment(prev, gender, payment_rate):
    if gender == 1:
        mortality = 1.01
    elif gender == 0:
        mortality = 0.99
    return prev *  payment_rate  * mortality              
    
def loan(curent_sum, prev, gender, payment_rate ):
    return np.float64(curent_sum + payment(prev, gender, payment_rate))    
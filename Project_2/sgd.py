import numpy as np
from helpers import *



def matrix_factorization_SGD(train, test, gamma, num_features, lambda_user, lambda_item):
    """matrix factorization by SGD."""
    num_epochs = 20     # number of full passes through the train set
    errors = [0]
    
    # set seed
    np.random.seed(988)

    # init matrix
    user_features, item_features = init_MF(train, num_features)
    
    # find the non-zero ratings indices 
    nz_row, nz_col = train.nonzero()
    nz_train = list(zip(nz_row, nz_col))
    if test != None:
        nz_row, nz_col = test.nonzero()
        nz_test = list(zip(nz_row, nz_col))

    for it in range(num_epochs):        
        # shuffle the training rating indices
        np.random.shuffle(nz_train)
        
        # decrease step size
        gamma /= 1.2
        
        for d, n in nz_train:
            # update W_d (item_features[:, d]) and Z_n (user_features[:, n])
            item_info = item_features[d, :]
            user_info = user_features[n, :]
            err = train[d, n] - item_info.dot(user_info.T)
    
            # calculate the gradient and update
            item_features[d, :] += gamma * (err * user_info - lambda_item * item_info)
            user_features[n, :] += gamma * (err * item_info - lambda_user * user_info)

        rmse = compute_error(train, user_features.T, item_features, nz_train)
        
        errors.append(rmse)
        print('Progression SGD: {:.2f}%'.format((it+1)/num_epochs*100), end='\r')
    print('\n')

    # evaluate the test error
    if test != None:
        rmse = compute_error(test, user_features.T, item_features, nz_test)
        print("RMSE on test data: {}.".format(rmse))
        return item_features.dot(user_features.T), rmse
    return item_features.dot(user_features.T)
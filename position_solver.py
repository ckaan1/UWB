####################################################################
##
## Position solver class
## Solver includes Non-linear Least Squares
## 
####################################################################
import numpy as np
import scipy.optimize as optimize
import math

weights = []
# NLLS function
def func_1(x,p_FA,d_M,weights) :

    num = len(p_FA)  # num - number of fixed anchors
    cost = cost = [0.]*num
    for i in range(0,num):
        # weight = max( min( 1,(1-(abs(d_M[i][1]-rssi_EX[i])/5)) ), 0.1 )
        cost[i] = weights[i]*(d_M[i] - np.linalg.norm(x-p_FA[i,0:2]))
        # cost[i] = (d_M[i][0] - np.linalg.norm(x-p_FA[i,0:2]))

    return cost   

# NLLS optimization  
def NLLS_opt(x_guess,p_FA,d_M,weights):   
    
    x = optimize.leastsq(func_1,x_guess,args=(p_FA,d_M,weights))
    # print min(weights)

    return x[0]
        
# Maximum Likelihood
# Return Matrix J
def func_2(x,p_FA,d_M):

    num = len(d_M)
    J_d = np.zeros((num,1))
    n_g = np.zeros((1,num)) #np.random.normal(0, 1, [1,num]) # Gaussian random noise
    n_g.fill(0.1)
    Q = np.diag(np.diag(n_g.T*n_g))
    
    for i in range(0,num):
        J_d[i][0] = d_M[i] - np.linalg.norm(x-p_FA[i,0:2])
    
    J = np.dot(np.dot(J_d.T,np.linalg.inv(Q)),J_d)
    return J[0]

# ML optimization  
def ML_opt(x_guess,p_FA,d_M):

    res = optimize.minimize(func_2,x_guess,args=(p_FA,d_M))

    return res.x 
    
    
    
    
    

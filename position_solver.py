####################################################################
##
## Position solver class
## Solver includes Non-linear Least Squares
## 
####################################################################
import numpy as np
import scipy.optimize as optimize
import math



class Position_solver:
    # x_guess is the initial guess / p_FA is teh position array of fixed anchors
    # d_m is the distance vector from mobile target to fixed anchors
    def __init__(self):
       
		self.NLLS = 0
		self.ML = 0

    def NLLS_opt(self,x_guess,p_FA,d_M):   
        
        x = optimize.leastsq(func_1,x_guess,args=(p_FA,d_M))
        self.NLLS = x[0]
        return self.NLLS

    def ML_opt(self,x_guess,p_FA,d_M):
    
        res = optimize.minimize(func_2,x_guess,args=(p_FA,d_M))
        self.ML = res.x
        return self.ML 
  
# NLLS function
def func_1(x,p_FA,d_M) :

    num = len(p_FA)  # num - number of fixed anchors
    cost = cost = [0.]*num
    for i in range(0,num):

        cost[i] = d_M[i] - np.linalg.norm(x-p_FA[i,0:2])

        #cost[i] = np.linalg.norm(d_M[i]) - np.linalg.norm(x-p_FA[i,0:2])
    return cost   
        
    # NLLS optimization    

   
# Maximum Likelihood
## Return Matrix J
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
    
    
    
    
    

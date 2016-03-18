####################################################################
##
## Position solver class
## Solver includes Non-linear Least Squares
## 
####################################################################
class Position_solver:
    # x_guess is the initial guess / p_FA is teh position array of fixed anchors
    # d_m is the distance vector from mobile target to fixed anchors
    def __init__(self,x_guess,p_FA,d_M):
       
		self.NLLS = NLLS_opt(x_guess,p_FA,d_M)
		
  
    # NLLS function
def func_1(x,p_FA,d_M) :
    import numpy as np
    num = len(p_FA)  # num - number of fixed anchors
    cost = cost = [0.]*num
    for i in range(0,num):
        cost[i] = np.linalg.norm(d_M[i]) - np.linalg.norm(x-p_FA[i,0:2])
    return cost   
        
    # NLLS optimization    
def NLLS_opt(x_guess,p_FA,d_M):   
    import numpy as np
    import scipy.optimize as optimize
        
    x = optimize.leastsq(func_1,x_guess,args=(p_FA,d_M))

    return x[0]
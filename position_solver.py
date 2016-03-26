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
<<<<<<< HEAD
        cost[i] = d_M[i] - np.linalg.norm(x-p_FA[i,0:2])
=======
        cost[i] = np.linalg.norm(d_M[i]) - np.linalg.norm(x-p_FA[i,0:2])
>>>>>>> 7d8d6855b77a4fe2508b671b5b34df31ea2a4747
    return cost   
        
    # NLLS optimization    
def NLLS_opt(x_guess,p_FA,d_M):   
    import numpy as np
    import scipy.optimize as optimize
        
    x = optimize.leastsq(func_1,x_guess,args=(p_FA,d_M))

    return x[0]
   
#Maximum Likelihood
def func_2(x,p_FA,d_M):
    import math
    import numpy as np
    num = len(d_M)
    J_d = np.array([[0 for x in range(1)] for x in range(num)])
    n_g = np.random.normal(0, 1, [1,num]) # Gaussian random noise
    Q = np.diag(np.diag(n_g.T*n_g))
    
    for i in range(0,num):
        J_d[i][0:1] = d_M[i] - np.linalg.norm(x-p_FA[i,0:2])
    
    J = np.dot(np.dot(J_d.T,np.linalg.inv(Q)),J_d)
    return 1/math.sqrt((2*math.pi)**num*np.linalg.det(Q))*math.exp(-J/2)
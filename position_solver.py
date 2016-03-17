####################################################################
##
## Position solver class
## Solver includes Non-linear Least Squares
## 
####################################################################
class position_solver:
    
#import environment

import numpy as np
import scipy.optimize as optimize
import matplotlib.pylab as plt

## Need to read fixed anchor positions

    ## Non-Linear Least Squares for LOS
    def func_1(x, p_FA, d_M) :
        num = 3;
        cost = np.zeros(3,1)
        for i in range(0,num):

            cost[i] = np.linalg.norm(d_M[i,0:2]) - np.linalg.norm(x-p_FA[i,0:2])
        return cost
        
    #def residuals(x,p_FA,d_M,PLP):
    #    return PLP - func_1(x, p_FA, d_M) 
        
    def NLLS():    # NLLS test
        
        x_guess= np.array([3.5, 3.5])  # a position guess for mobile tag
        #p_FA
        #d_M
       

        x,cov,infodict,mesg,ier = optimize.leastsq(
        residuals,kd_guess,args=(p_FA,d_M),full_output=True,warning=True)

        print(x)
        ## Visualize the results
        #PLP_fit=func_1(x,p_FA,d_M)
        #plt.plot()
        #plt.show()        
        
        
        return x
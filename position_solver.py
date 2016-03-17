####################################################################
##
## Position solver class
## Solver includes Non-linear Least Squares
## 
####################################################################
class position_solver:
    
import environment
import datetime
import numpy as np
import scipy.optimize as optimize
import matplotlib.pylab as plt

## Read fixed anchor position

## Non-Linear Least Squares for LOS
    def func_1(x, p_FA, d_M) 
        return (d_M - np.linalg.norm(x-p_FA))^2
        
    def residuals(x,p_FA,d_M,PLP):
        return PLP - func_1(x, p_FA, d_M) 
        
    def NLLS()    # NLLS test
        N=1000
        kd_guess= [3.5, 3.5]  # a position guess for mobile tag
        #p_FA
        #d_M
        PLP = func_1(x, p_FA, d_M)+(np.random.random(N)-0.5)*0.1

        x,cov,infodict,mesg,ier = optimize.leastsq(
        residuals,kd_guess,args=(p_FA,d_M,PLP),full_output=True,warning=True)

        print(x)
        return x
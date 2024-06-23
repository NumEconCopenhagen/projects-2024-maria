# define class for production economy
import numpy as np
from scipy import optimize
from types import SimpleNamespace

class production_economy:
    def __init__(self, par):
        
        # Parameters
        self.A = par.A
        self.gamma = par.gamma

        self.alpha = par.alpha
        self.nu = par.nu
        self.epsilon = par.epsilon

    # Firm optimal behaviour
    def opt_firm(self, pj, w=1):
        lj = (pj * self.A*self.gamma/w)**(1/(1-self.gamma))
        yj = self.A * lj**self.gamma
        return lj, yj
    
    # Firm profits from optimal behaviour
    def pi_j(self, pj, w=1):
        return (1-self.gamma)/self.gamma * w * (pj*self.A*self.gamma/w)**(1/(1-self.gamma))

    # Consumer optimal behaviour
    def opt_cb(self,l, p1, p2, T, tau ,w=1):
        c1 = self.alpha * (w*l+T+self.pi_j(p1,w)+self.pi_j(p2,w))/p1
        c2 = (1-self.alpha) * (w*l+T+self.pi_j(p1,w)+self.pi_j(p2,w))/(p1+tau)
        return c1, c2
    
    ### Consumer optimal labour supply
    # Objective function for consumer problem
    def obj_ls(self, l, p1, p2, T, tau):
        c1, c2 = self.opt_cb(l,p1,p2,T,tau)
        return - (np.log(c1**self.alpha * c2**(1-self.alpha)) - self.nu*l**(1+self.epsilon)/(1+self.epsilon))

    # Solver for consumer problem
    def opt_ls(self, p1, p2, T, tau):
        l_quess = 1
        sol = optimize.minimize(self.obj_ls, l_quess, args=(p1, p2, T, tau), method='SLSQP')
        return sol.x[0]
    
    ### EQ
    # Market clearing conditions (only 2) and balanced budget contraint.
    def clear_con(self, p, tau):
        error = np.zeros(3)
        c1, c2 = self.opt_cb(self.opt_ls(p[0],p[1], p[2], tau), p[0],p[1], p[2], tau)

        y1 = self.opt_firm(p[0])[1]
        y2 = self.opt_firm(p[1])[1]   

        error[0] = c1-y1
        error[1] = c2-y2
        error[2] = p[2]-tau*c2
        return error

    # EQ solver
    def EQ(self, tau):
        x0 = np.array([0.1,0.1,0])
        res = optimize.root(self.clear_con, x0, args = (tau))
        return res.x















        

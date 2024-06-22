# define class for production economy
import numpy as np
from scipy import optimize
from types import SimpleNamespace

class production_economy:
    def __init__(self, par):
        
        #parameters
        self.A = par.A
        self.gamma = par.gamma

        self.alpha = par.alpha
        self.nu = par.nu
        self.epsilon = par.epsilon

        #self.tau = tau
        #self.T = T

        self.kappa = par.kappa

        #self.c2 = 0
        #self.p1 = 0
        #self.p2 = 0

    #firm optimal behaviour
    def opt_firm(self, pj, w=1):
        lj = (pj * self.A*self.gamma/w)**(1/(1-self.gamma))
        yj = self.A * lj**self.gamma
        return lj, yj
    
    #firm profits from optimal behaviour
    def pi_j(self, pj, w=1):
        return (1-self.gamma)/self.gamma * w * (pj*self.A*self.gamma/w)**(1/(1-self.gamma))

    #consumer optimal behaviour
    def opt_cb(self,l, p1, p2, T = 0, tau = 0 ,w=1):
        c1 = self.alpha * (w*l+T+self.pi_j(p1,w)+self.pi_j(p2,w))/p1
        c2 = (1-self.alpha) * (w*l+T+self.pi_j(p1,w)+self.pi_j(p2,w))/(p1+tau)
        return c1, c2
    
    #consumer optimal labour supply
    #objective function
    def obj_ls(self, l, p1, p2, T, tau):
        c1, c2 = self.opt_cb(l,p1,p2,T,tau)
        return - (np.log(c1**self.alpha * c2**(1-self.alpha)) - self.nu*l**(1+self.epsilon)/(1+self.epsilon))

    #solver
    def opt_ls(self, p1, p2, T, tau):
        l_quess = 1
        sol = optimize.minimize(self.obj_ls, l_quess, args=(p1, p2, T, tau), method='SLSQP')
        return sol.x[0]
    
    #EQ
    #Market clearing conditions (only 2)
    def clear_con(self, p, T, tau):
        error = np.zeros(2)
        c1, c2 = self.opt_cb(self.opt_ls(p[0],p[1], T, tau), p[0], p[1], T, tau)
        y1 = self.opt_firm(p[0])[1]
        y2 = self.opt_firm(p[1])[1]
        
        error[0] = c1 - y1
        error[1] = c2 - y2
        return error
    
    #find the roots of the equation system (illustrative)
    def EQ(self, T, tau):
        x0 = np.array([0.1,0.1])
        res = optimize.root(self.clear_con, x0, args = (T,tau))
        output =  res.x
        return output

    # Opmitize consumer with varying tau (and T but constrained through error) - input = [p1,p2,]
    def clear_SWF_con(self, p, tau):
        error = np.zeros(3)
        c1, c2 = self.opt_cb(self.opt_ls(p[0],p[1], p[2], tau), p[0],p[1], p[2], tau)

        y1 = self.opt_firm(p[0])[1]
        y2 = self.opt_firm(p[1])[1]   

        error[0] = c1-y1
        error[1] = c2-y2
        error[2] = p[2]-tau*c2
        return error

    # Objective function to maximize SWF
    def SWF_obj(self, tau):
        x0 = np.array([0.1,0.1,0])
        res = optimize.root(self.clear_SWF_con, x0, args = (tau))
        return res.x

    def SWF_objective(self, tau):
        p1, p2, T = self.SWF_obj(tau)
        l = self.opt_ls(p1, p2, T, tau)
        c1, c2 = self.opt_cb(l, p1, p2, T, tau)
        y2 = self.opt_firm(p2)[1]
        
        U = np.log(c1**self.alpha * c2**(1-self.alpha)) - self.nu*l**(1+self.epsilon)/(1+self.epsilon)
        SWF = U-self.kappa*y2

        return -SWF

#   # Objective function to maximize SWF
#     def SWF_obj(self, tau, T):
#         x0 = np.array([0.1,0.1,0])
#         res = optimize.root(self.clear_SWF_con, x0, args = (T,tau))
#         p1, p2 = res.x
#         l = self.opt_ls(p1,p2)
#         c1, c2 = self.opt_cb(l, p1, p2)
#         y2 = self.opt_firm(p2)[1]
        
#         U = np.log(c1**self.alpha * c2**(1-self.alpha)) - self.nu*l**(1+self.epsilon)/(1+self.epsilon)
#         SWF = U-self.kappa*y2

#         return -SWF


    # #     p1, p2, T = self.EQ_SWF(tau)
    # #     c1, c2 = self.opt_cb(self.opt_ls(p1,p2), p1, p2, tau, T)
    # #     U = np.log(c1**self.alpha * c2**(1-self.alpha)) - self.nu*l**(1+self.epsilon)/(1+self.epsilon)


    # def SWF_obj(self, input):
    #     # Deinfe new econ
    #     self.tau, self.T = input
    #     # Compute market clearing p1, p2, l, c1, c2, y2 given tau and T
    #     p1, p2 = self.EQ()
    #     self.p1 = p1
    #     self.p2 = p2
    #     l = self.opt_ls(p1,p2)
    #     c1, c2 = self.opt_cb(l, p1, p2)
    #     self.c2 = c2
    #     y2 = self.opt_firm(p1)[1]
    #     # Compute U
    #     U = np.log(c1**self.alpha * c2**(1-self.alpha)) - self.nu*l**(1+self.epsilon)/(1+self.epsilon)

    #     SWF = U-self.kappa*y2
        
    #     return - SWF

    # def eq_constraint(self, input):
    #         tau, T = input
    #         return tau-T*self.c2 



    # def SWF_solve(self):

    #     l_quess = (0,0)

    #     eq_con = ({'type': 'eq', 'fun': self.eq_constraint})

    #     bud1_con = {'type':'ineq','fun':lambda x: self.p1}
    #     bud2_con = {'type':'ineq','fun':lambda x: self.p2}
    #     bud3_con = {'type':'ineq','fun':lambda x: x[0]}
    #     bud4_con = {'type':'ineq','fun':lambda x: x[1]}

    #     sol = optimize.minimize(self.SWF_obj, l_quess,method='SLSQP', constraints = (eq_con,bud1_con, bud2_con, bud3_con, bud4_con)) 
    #     return sol

















        

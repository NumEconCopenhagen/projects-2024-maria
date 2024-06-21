#create class for exchange economy 
from scipy import optimize

class exchange_economy:
    def __init__(self, endowmentA_1, endowmentA_2):
        
        #parameters
        # a. endowments
        self.omegaA_1 = endowmentA_1
        self.omegaA_2 = endowmentA_2

        self.omegaB_1 = 1 - self.omegaA_1
        self.omegaB_2 = 1 - self.omegaA_2

        #b. constants
        self.alpha = 1/3
        self.beta = 2/3

    #utility functions
    def uA(self, x1, x2):
        return x1**self.alpha * x2**(1-self.alpha)

    def uB(self, x1, x2):
        return x1**self.beta * x2**(1-self.beta)

    #demand functions
    def demandA(self,p1,p2=1):
        x1_A = self.alpha * (p1*self.omegaA_1+p2*self.omegaA_2)/p1
        x2_A = (1-self.alpha) * (p1*self.omegaA_1+p2*self.omegaA_2)/p2
        
        return x1_A, x2_A

    def demandB(self,p1,p2=1):
        x1_B = self.beta * (p1*self.omegaB_1+p2*self.omegaB_2)/p1
        x2_B = (1-self.beta) * (p1*self.omegaB_1+p2*self.omegaB_2)/p2

        return x1_B, x2_B
    
    #market clearing conditions
    def clearing_error(self, p1):
        x1_A, x2_A = self.demandA(p1)
        x1_B, x2_B = self.demandB(p1)

        epsilon1 = x1_A - self.omegaA_1 + x1_B - self.omegaB_1
        epsilon2 = x2_A - self.omegaA_2 + x2_B - self.omegaB_2

        return epsilon1, epsilon2
    
    #market equlibirum
    def eq(self):
        # solver that finds when the market clearing error1 is equal to 0, returns the market clearing price.
        p1_guess = 1
        clear = optimize.root(lambda p1: self.clearing_error(p1)[1], p1_guess)
        return clear.x[0]
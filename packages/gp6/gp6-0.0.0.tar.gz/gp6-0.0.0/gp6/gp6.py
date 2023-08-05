import numpy as np
from scipy.optimize import minimize
from math import factorial # for Savitzky-Golay smoothing of DE EoS

def step(r):
    '''define step function for Matern kernels'''
    return (np.heaviside(r, 1) - (1/2))*2    

class GP:
    '''Class for making GP predictions.
    
    rbf: k(r) = A^2 \exp(-r^2/(2l^2))
    chy: k(r) = A^2 l^2 / (r^2 + l^2)
    m52: k(r) = A^2 \exp(-\sqrt{5}r/l)
                (1 + \sqrt{5}r/l + 5r^2/(3l^2))
    m72: k(r) = A^2 \exp(-\sqrt{7}r/l)
                (1 + \sqrt{7}r/l + 14r^2/(5l^2)
                   + 7\sqrt{7}r^3/(15l^3))
    
    Input:
    kern = kernel name, i.e., 'rbf', 'chy', 'm52'
    l = length scale
    A = amplitude/height
    '''
    
    def __init__(self, kern, l, A):
        self.length = l
        self.height = A
        self.kern = kern
        
    def kernel(self, x, y):
        if self.kern == 'rbf':
            return (self.height**2)* \
                   np.exp(-((x - y)**2)
                          /(2*self.length**2))
        elif self.kern == 'chy':
            return (self.height**2)* \
                   ((self.length**2)/
                    ((x - y)**2 + self.length**2))
        elif self.kern == 'm52':
            d = x - y
            r = np.abs(d)
            X = np.sqrt(5)*r/self.length
            B = 1 + X + ((X**2)/3)
            return (self.height**2)*B*np.exp(-X)
        elif self.kern == 'm72':
            d = x - y
            r = np.abs(d)
            R = r/self.length
            X = np.sqrt(7)*R
            B = 1 + np.sqrt(7)*R + (14*(R**2)/5) \
                + (7*np.sqrt(7)*(R**3)/15)
            return (self.height**2)*B*np.exp(-X)
        
    #### kernel derivatives
        
    def dKdx(self, x, y):
        '''derivative of kernel wrt x'''
        l = self.length
        A = self.height
        d = x - y
        Krnl = self.kernel(x, y)
        if self.kern == 'rbf':
            return -d*Krnl/(l**2)
        elif self.kern == 'chy':
            return -2*d*Krnl/((l**2) + (d**2))
        elif self.kern == 'm52':
            d = x - y
            r = np.abs(d)
            num = -5*step(d)*r*(l + np.sqrt(5)*r)*Krnl
            den = l*((3*(l**2)) + 3*np.sqrt(5)*l*r + 5*(r**2))
            return num/den  
        elif self.kern == 'm72':
            d = x - y
            r = np.abs(d)
            num = -7*step(d)*r*(3*(l**2) + 3*np.sqrt(7)*l*r + 7*(r**2))*Krnl
            den = 15*(l**4) + l*r*(15*np.sqrt(7)*(l**2) + 7*r*(6*l + np.sqrt(7)*r))
            return num/den

    def dKdy(self, x, y):
        '''derivative of kernel wrt y'''
        l = self.length
        A = self.height
        d = x - y
        Krnl = self.kernel(x, y)
        if self.kern == 'rbf':
            return d*Krnl/(l**2)
        elif self.kern == 'chy':
            return 2*d*Krnl/((l**2) + (d**2))
        elif self.kern == 'm52':
            d = x - y
            r = np.abs(d)
            num = 5*step(d)*r*(l + np.sqrt(5)*r)*Krnl
            den = l*((3*(l**2)) + 3*np.sqrt(5)*l*r + 5*(r**2))
            return num/den  
        elif self.kern == 'm72':
            d = x - y
            r = np.abs(d)
            num = 7*step(d)*r*(3*(l**2) + 3*np.sqrt(7)*l*r + 7*(r**2))*Krnl
            den = 15*(l**4) + l*r*(15*np.sqrt(7)*(l**2) + 7*r*(6*l + np.sqrt(7)*r))
            return num/den

    def d2Kdxdy(self, x, y):
        '''derivative of kernel wrt x and y'''
        l = self.length
        A = self.height
        d = x - y
        Krnl = self.kernel(x, y)
        if self.kern == 'rbf':
            return Krnl*((l**2) - (d**2))/(l**4)
        elif self.kern == 'chy':
            return 2*((l**2) - 3*(d**2))*Krnl/(((l**2) + (d**2))**2)
        elif self.kern == 'm52':
            d = x - y
            r = np.abs(d)
            num = 5*(step(d)**2)*((l**2) + np.sqrt(5)*l*r - 5*(r**2))*Krnl
            den = (l**2)*(3*(l**2) + 3*np.sqrt(5)*l*r + 5*(r**2))
            return num/den  
        elif self.kern == 'm72':
            d = x - y
            r = np.abs(d)
            num = 7*(step(d)**2)*(3*(l**3) + np.sqrt(7)*r*(3*(l**2) - 7*(r**2)))*Krnl
            den = 15*(l**5) + (l**2)*r*(15*np.sqrt(7)*(l**2) + 7*r*(6*l + np.sqrt(7)*r))
            return num/den
    
    #### ------- for the GP reconstruction -------
    
    def k_plus_c_inv(self, Z, C):
        k_ZZ = np.array([[self.kernel(z_i, z_j) \
                          for z_i in Z]
                         for z_j in Z])
        return np.linalg.inv(k_ZZ + C)
    
    def cov(self, Z, C, Zs):
        '''Returns the covariance matrix at Zs.
        
        Note: Zs must be an array.'''
        kpc_inv = self.k_plus_c_inv(Z, C)
        return np.array([[self.kernel(z_i, z_j) \
                          -(self.kernel(z_i, Z) @ \
                            kpc_inv @ \
                            self.kernel(Z, z_j)) \
                          for z_i in Zs] \
                         for z_j in Zs])
    
    def var(self, Z, C, Zs):
        '''Returns the variance at Zs.
        
        Note: Zs must be an array.'''
        kpc_inv = self.k_plus_c_inv(Z, C)
        return np.array([self.kernel(zs, zs) \
                         -(self.kernel(zs, Z) @ \
                           kpc_inv @ \
                           self.kernel(Z, zs)) \
                         for zs in Zs])
    
    def get_logmlike(self, Z, Y, C):
        '''Returns the log-marginal likelihood.'''
        kpc_inv = self.k_plus_c_inv(Z, C)
        kpc = np.linalg.inv(kpc_inv)
        kpc_det = np.linalg.det(kpc)
        Ys = np.array([(self.kernel(zs, Z) @ kpc_inv \
                        @ Y) for zs in Z])
        delta_y = Y
        return -0.5*(delta_y @ kpc_inv @ delta_y) \
               -0.5*np.log(kpc_det) \
               -0.5*len(Z)*np.log(2*np.pi)
    
    def optimize(self, Z, Y, C, method = 'Nelder-Mead', tol = 1e-7):
        '''Returns optimized hyperparameters for GP reconstruction.'''
        
        def nlmlike(X):
            # negative log marginal likelihood for minimization
            self.length = X[0]
            self.height = X[1]
            return -self.get_logmlike(Z, Y, C)
        
        # the minimization procedure
        mnmz_GP = minimize(nlmlike, \
                           [max(Z) - min(Z), 0.5*(max(Y) + min(Y))], \
                           method = method, tol = tol)
        self.length = mnmz_GP.x[0]
        self.height = mnmz_GP.x[1]
        return {'l_opt': mnmz_GP.x[0], 'A_opt': mnmz_GP.x[1]}
        
    def predict(self, Z, Y, C, Zs, with_cov = False, \
                k_as_cov = False):
        kpc_inv = self.k_plus_c_inv(Z, C)
        mean = np.array([(self.kernel(zs, Z) @ kpc_inv \
                          @ Y) for zs in Zs])
        if with_cov == False:
            var_zz = self.var(Z, C, Zs)
            return {'z': Zs, 'Y': mean, \
                    'varY': var_zz}
        elif (with_cov == True) and (k_as_cov == False):
            cov_zz = self.cov(Z, C, Zs)
            return {'z': Zs, 'Y': mean, \
                    'covY': cov_zz}
        elif (with_cov == True) and (k_as_cov == True):
            cov_zz = np.array([[self.kernel(z_i, z_j) \
                                for z_i in Zs] \
                               for z_j in Zs])
            return {'z': Zs, 'Y': mean, \
                    'covY': cov_zz}
        
    #### ------- for the derivative of the GP reconstruction -------
    
    def predict_d1F(self, Z, Y, C, Zs, with_covYdY = False):
        '''mean and variance of dF/dz(Zs) [the reconstructed function F(z)]
        
        Note: (Z, Y, C) are training points with covariance matrix C'''
        A = self.height
        kpc_inv = self.k_plus_c_inv(Z, C)
        
        ave = np.array([self.dKdx(zs, Z) @ kpc_inv @ Y for zs in Zs])
        var_ii = np.array([self.d2Kdxdy(zs, zs) for zs in Zs])
        var_ij = np.array([-(self.dKdx(zs, Z) @ kpc_inv @ self.dKdy(Z, zs)) \
                           for zs in Zs])
        var = var_ij + var_ii 
        
        if with_covYdY == True:
            cov_d0Y_d1Y = []
            for zs in Zs:
                # 00-term
                term_1 = self.kernel(zs, zs)
                term_2 = self.kernel(zs, Z) @ kpc_inv @ self.kernel(Z, zs)
                cov_f0_f0 = term_1 - term_2

                # 11-term
                K10 = self.dKdx(zs, Z)
                K01 = self.dKdy(Z, zs)
                K11 = self.d2Kdxdy(zs, zs)
                cov_f1_f1 = K11 - (K10 @ kpc_inv @ K01)

                # 01-term: cross-correlation
                K01_cc = self.dKdy(zs, zs)
                K00_cc = self.kernel(zs, Z)
                K01_cc_zzstar = self.dKdy(Z, zs)
                cov_f0_f1 = K01_cc - (K00_cc @ kpc_inv @ K01_cc_zzstar)
                
                cov_d0Y_d1Y.append(np.array([[cov_f0_f0, cov_f0_f1], \
                                             [cov_f0_f1, cov_f1_f1]]))
            cov_d0Y_d1Y = np.array(cov_d0Y_d1Y)
            return {'z': Zs, 'Y': ave, 'varY': var, 'covYdY': cov_d0Y_d1Y}
        
        else: # return mean and variance at Zs
            return {'z': Zs, 'Y': ave, 'varY': var}
        
        
# see https://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay
# code was rewritten for python 3 and improved by GPT-3
def savitzky_golay(y: np.ndarray, window_size: int = 51, order: int = 3, \
                   deriv: int = 0, rate: float = 1) -> np.ndarray:
    """
    Apply the Savitzky-Golay filter to a numpy array.

    Args:
        y: The input signal as a 1-D numpy array.
        window_size: The length of the filter window.
        order: The order of the polynomial used to fit the samples.
        deriv: The order of the derivative to compute.
        rate: The sampling rate of the input signal.

    Returns:
        The filtered signal as a 1-D numpy array.
    """
    if not isinstance(y, np.ndarray):
        raise TypeError("Input signal must be a numpy array")
        
    if not isinstance(window_size, int) or window_size < 1:
        raise ValueError("Window size must be a positive integer")
    
    if not isinstance(order, int) or order < 0:
        raise ValueError("Polynomial order must be a non-negative integer")
    
    if not isinstance(deriv, int) or deriv < 0:
        raise ValueError("Derivative order must be a non-negative integer")
    
    if not isinstance(rate, (int, float)) or rate <= 0:
        raise ValueError("Sampling rate must be a positive number")
    
    if window_size % 2 != 1:
        raise ValueError("Window size must be an odd number")
    
    if window_size < order + 2:
        raise ValueError("Window size is too small for the polynomial order")
    
    order_range = range(order+1)
    half_window = (window_size - 1) // 2
    
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    
    # pad the signal at the extremes with values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    
    # apply the filter
    return np.convolve(m[::-1], y, mode='valid')
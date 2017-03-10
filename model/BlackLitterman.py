# -*- coding: utf-8 -*-

"""
    This script is class of Black-litterman model
    according to the paper of A STEP-BY-STEP GUIDE TO THE BLACK-LITTLERMAN MODEL
    author: jacobliang
"""

import numpy as np
from scipy import linalg


class BlackLitterman(object):
    """
        blacklitterman
            This function performs the Black-Litterman blending of the prior
            and the views into a new posterior estimate of the returns using the
            alternate reference model as shown in Idzorek's paper.
        Inputs
            weq    - Weights of the assets in the equilibrium portfolio
            sigma  - Prior covariance matrix
            P      - Pick matrix for the view(s)
            Q      - Vector of view returns
            Omega  - Matrix of variance of the views (diagonal)
            tau    - Coefficiet of uncertainty in the prior estimate of the mean (pi)
            delta  - Risk tolerance from the equilibrium portfolio
        Outputs
            Er     - Posterior estimate of the mean returns
            w      - Unconstrained weights computed given the Posterior estimates
                     of the mean and covariance of returns.
            lambda - A measure of the impact of each view on the posterior estimates.
    """

    def __init__(self, weq, sigma, P, Q, Omega, tau=0.05, delta=3.07):
        """
            initialize the class attributes
        """
        self._checkType(tau, float)
        self._checkType(delta, float)
        self.tau = tau
        self.delta = delta
        self.weq = weq
        self.sigma = sigma
        self.tau_sigma = tau*sigma
        self.P = P
        self.Q = Q
        self.Omega = Omega

    def _checkType(self, val, valType):
        if not isinstance(val, valType):
            raise ValueError("{0} should be type {1}".format(val, str(valType)))
        return True

    def computePi(self, weq=None, sigma=None, delta=None):
        """
            Reverse optimize and back out the equilibrium returns
        """
        if weq is None:
            weq = self.weq
        if sigma is None:
            sigma = self.sigma
        if delta is None:
            delta = self.delta
        pi = weq.dot(sigma * delta)
        return pi

    def computeOmega(self, conf, P=None, Sigma=None):
        """
            This function computes the Black-litterman parameters Omega from
            an Idzorek confidence
            Inputs
                conf   - Idzorek confidence specified as a decimal (50% as 0.50)
                P      - Pick matrix for the view
                Sigma  - Prior covariance matrix
            Outputs
                omega  - Black-Litterman uncertainty/confidence parameter
        """
        if P is None:
            P = self.P
        if Sigma is None:
            Sigma = self.Sigma
        if self._checkType(conf, float):
            alpha = (1 - conf) / conf
            omega = alpha * np.dot(np.dot(P, Sigma), P.T)
        return omega

    def compute_ER(self, delta=None, weq=None, sigma=None, tau=None, P=None, Q=None, Omega=None):
        """
            compute with 100 percent confidence
        """
        if delta is None:
            delta = self.delta
        if weq is None:
            weq = self.weq
        if sigma is None:
            sigma = self.sigma
        if tau is None:
            tau = self.tau
        if P is None:
            P = self.P
        if Q is None:
            Q = self.Q
        if Omega is None:
            Omega = self.Omega
        #call self computePi function using reverse optimize
        pi = self.computePi(weq, sigma, delta)
        # use ts replace tau * sigma
        ts = self.tau_sigma
        # compute posterior estimate of the mean
        if not np.all(P == 0.0):
            middle = linalg.inv(np.dot(np.dot(P, ts), P.T) + Omega)
            er = np.expand_dims(pi, axis=0).T + np.dot(np.dot(np.dot(ts, P.T), middle),
                                                       (Q - np.expand_dims(np.dot(P, pi.T), axis=1)))
        else:
            er = np.expand_dims(pi, axis=0).T
        #compute posterior estimate of the uncertainty in the mean

        #compute the posterior variance of the estimated mean
        pos_var = tau*sigma - np.dot(np.dot(np.dot(ts, P.T), middle), np.dot(P, ts))
        #compute the covariance of returns about the estimated mean
        est_sigma = sigma + pos_var
        #compute posterior weights based on uncertainty in mean
        #here use unconstrained mean variance optimization
        #w = er.T.dot(linalg.inv(delta * sigma)).T
        w = er.T.dot(linalg.inv(delta * est_sigma)).T
        #compute lambda value
        lmbda = np.dot(linalg.pinv(P).T, (w.T * (1 + tau) - weq).T)
        return [er, w, lmbda]

    def compute_idz_ER(self, conf_list):
        """
            using the Idzorek's method to compute omega
        """
        self._checkType(conf_list, type([]))
        diag_elem = list()
        for index in range(len(conf_list)):
            diag_elem.append(self.computeOmega(conf_list[index], self.P[index], self.tau_sigma))
        idz_omega = np.diag(diag_elem)
        return self.compute_ER(Omega=idz_omega)

    def computePosteriorBL(self, Conf_list):
        """
            判断条件入口，条件检查判断
        """
        if not np.all(self.P == 0.0):
            return self.compute_idz_ER(Conf_list)
        else:
            return self.compute_ER()

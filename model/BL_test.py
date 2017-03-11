# -*- coding:utf-8 -*-


from model import BlackLitterman
import numpy as np


def display(title, assets, res):
    er = res[0]
    w = res[1]
    lmbda = res[2]
    print('\n' + title)
    line = 'Country\t\t'
    for p in range(len(P)):
        line = line + 'P' + str(p) + '\t'
    line = line + 'mu\tw*'
    print(line)

    i = 0
    for x in assets:
        line = '{0}\t'.format(x)
        for j in range(len(P.T[i])):
            line = line + '{0:.1f}\t'.format(100 * P.T[i][j])

        line = line + '{0:.3f}\t{1:.3f}'.format(100 * er[i][0], 100 * w[i][0])
        print(line)
        i = i + 1

    line = 'q\t\t'
    i = 0
    for q in Q:
        line = line + '{0:.2f}\t'.format(100 * q[0])
        i = i + 1
    print(line)

    line = 'omega/tau\t'
    i = 0
    for o in Omega:
        line = line + '{0:.5f}\t'.format(o[i] / tau)
        i = i + 1
    print(line)

    line = 'lambda\t\t'
    i = 0
    for l in lmbda:
        line = line + '{0:.5f}\t'.format(l[0])
        i = i + 1
    print(line)


# Take the values from Idzorek, 2005.
# market capitalization weights
weq = np.array([.193400, .261300, .120900, .120900, .013400, .013400, .241800, .034900])
# covariance matrix of excess returns
V = np.array([[.001005, .001328, -.000579, -.000675, .000121, .000128, -.000445, -.000437],
              [.001328, .007277, -.001307, -.000610, -.002237, -.000989, .001442, -.001535],
              [-.000579, -.001307, .059852, .027588, .063497, .023036, .032967, .048039],
              [-.000675, -.000610, .027588, .029609, .026572, .021465, .020697, .029854],
              [.000121, -.002237, .063497, .026572, .102488, .042744, .039443, .065994],
              [.000128, -.000989, .023036, .021465, .042744, .032056, .019881, .032235],
              [-.000445, .001442, .032967, .020697, .039443, .019881, .028355, .035064],
              [-.000437, -.001535, .048039, .029854, .065994, .032235, .035064, .079958]])
# implied equilibrium return
refPi = np.array([0.0008, 0.0067, 0.0641, 0.0408, 0.0743, 0.0370, 0.0480, 0.0660])
assets = ['US Bonds', 'Intl Bonds', 'US Lg Grth', 'US Lg Value', 'US Sm Grth',
          'US Sm Value', 'Intl Dev Eq', 'Intl Emg Eq']

# Risk aversion of the market
delta = 3.07

# Coefficient of uncertainty in the prior estimate of the mean
# from footnote (8) on page 11
tau = 0.025
tauV = tau * V

# Define view 1
# International Developed Equity will have an excess return of 5.25%
# with a confidence of 25%.
P1 = np.array([0, 0, 0, 0, 0, 0, 1, 0])
Q1 = np.array([0.0525])
conf1 = 0.25

# Define view 2
# International Bonds will outperform US Bonds by 0.0025 with a
# confidence of 50%.
P2 = np.array([-1, 1, 0, 0, 0, 0, 0, 0])
Q2 = np.array([0.0025])
conf2 = 0.50

# Define View 3
# US Large and Small Growth will outperform US Large and Small Value
# by 0.02 with a confidence of 65%.
P3 = np.array([0, 0, 0.90, -0.90, 0.10, -0.10, 0, 0])
Q3 = np.array([0.02])
conf3 = 0.65

# Combine the views
# P(k*N) Q(k*1)
P = np.array([P1, P2, P3])
Q = np.array([Q1, Q2, Q3])

# Apply the views with simple Omega
# omega = tau * P * sigma * P.T
Omega = np.dot(np.dot(P, tauV), P.T)

BL = BlackLitterman.BlackLitterman(weq, V, P, Q, Omega, tau, delta)
# res = altblacklitterman(delta, weq, V, tau, P, Q, Omega)
res_simple = BL.compute_ER()
display('Simple Omega', assets, res_simple)

# Now apply the views using the Idzorek's method
# Omega = np.array([[bl_omega(conf1, P1, tauV), 0, 0],
#                  [0, bl_omega(conf2, P2, tauV), 0],
#                  [0, 0, bl_omega(conf3, P3, tauV)]])
# res = altblacklitterman(delta, weq, V, tau, P, Q, Omega)
res_idz = BL.compute_idz_ER([conf1, conf2, conf3])
display('Idzorek Method', assets, res_idz)

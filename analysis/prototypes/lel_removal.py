# Generalized Pan et al. (AJE 2026, Supp S.7.1) LEL with post-infection removal s(u).
# Validated against Pan arXiv 2412.12316 Table 1 (s=1). phi: 98-day gamma (shape .352, rate 1.273), T*=2y.
import numpy as np
from scipy import stats, integrate
Ts=2.0
phi=lambda u: 1-stats.gamma.cdf(u,0.352,scale=1/1.273)
def LEL(r,c,th,s=lambda u:1.0):
    Om=integrate.quad(phi,0,Ts,limit=200)[0]
    Oms=integrate.quad(lambda u:phi(u)*s(u),0,Ts,limit=200)[0]
    K=integrate.quad(lambda u:phi(u)*s(u)*(1-np.exp(th*(c-u))),c,Ts,limit=200)[0] if c<Ts else 0.0
    return np.log(Oms-(1-r*np.exp(th*c))*K)-np.log(Om)
lam=0.032
print('validation vs Pan arXiv Table 1 (bias x1e-3):')
for c,th,r,pub in [(0,1,0,-9.95),(0,1,.6,-3.98),(0,2,0,-15.03),(0.25,1,0,-5.93),(0.25,1,.6,-1.36),(0.25,1,1,1.68),(0.25,2,0,-8.97),(0.25,2,.6,-0.10),(0.25,2,1,5.82)]:
    print(f' c={c} th={th} r={r}: formula {1e3*lam*(np.exp(LEL(r,c,th))-1):7.2f}  published {pub}')

from scipy.optimize import brentq
print('\nWith post-infection removal s(u)=exp(-g*u), g per year; PURPOSE-like c=0.25y')
print(' g/yr  th  LEL(r=0)  LEL(r=1)  r* (LEL=0)   [r*(g=0)=exp(-th*c)]')
for th in [0.5,1,2]:
  for g in [0,0.05,0.1,0.2]:
    s=lambda u,g=g: np.exp(-g*u)
    f=lambda r: LEL(r,0.25,th,s)
    try: rs=brentq(f,0,5)
    except ValueError: rs=float('nan')
    print(f' {g:4.2f} {th:3} {f(0):8.4f} {f(1):8.4f} {rs:8.3f}   [{np.exp(-th*0.25):.3f}]')

print('\ncheck closed-form threshold r*_g = e^{-th c}[1+(Om-Oms)/K_s]:')
for th,g in [(1,0.1),(0.5,0.05),(2,0.2)]:
    s=lambda u,g=g: np.exp(-g*u); c=0.25
    Om=integrate.quad(phi,0,Ts)[0]; Oms=integrate.quad(lambda u:phi(u)*s(u),0,Ts)[0]
    K=integrate.quad(lambda u:phi(u)*s(u)*(1-np.exp(th*(c-u))),c,Ts)[0]
    print(th,g, round(np.exp(-th*c)*(1+(Om-Oms)/K),3))

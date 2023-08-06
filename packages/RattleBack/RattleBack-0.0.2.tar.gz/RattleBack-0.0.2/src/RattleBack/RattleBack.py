# reference: T. R. Kane and D. A. Levinson
#  "Realistic Mathematical Modeling of the Rattleback"
#   International Journal of Non-Linear Mechanics 17 (1982) 175

import numpy as np
from scipy.integrate import odeint
from scipy.constants import g

def RattleBack(abch, ABCD, init, t, sigma=0, g=g*100, **kw):
    """
    abch,ABCD = tuples of four real numbers, where
      a,b,c = radii of ellipsoid (cm)
      h = OG (O = center of ellipsoid, G = center of mass) (cm)
      A,B,C = moments of inertia along a,b,c axis (cm^2)
      D = product of intertia in a-b plane (cm^2)
    init = initial condition of integration (shape (6,))
    t = evaluation time (1d array) (sec)
    sigma = friction coefficient (cm^2/sec)
    g = gravity acceleration (cm/sec^2)
    kw = keyword arguments passed to scipy.integrate.odeint
    return y = output of odeint (shape(len(t),6)), where
      y[:,0:3] = euler angles alpha,beta,gamma
      y[:,3:6] = angular velocities omega_i (i=1,2,3)
    all variables are measured in CGS units and radians
    A,B,C,D,sigma corresponds to those of
      Kane & Levinson DIVIDED BY MASS of rattleback
    """
    a,b,c,h = abch
    A,B,C,D = ABCD
    a2 = np.r_[a*a,b*b,c*c]
    I0 = np.c_[[A,D,0],[D,B,0],[0,0,C]]

    def diff_eq(y,t):
        q,u = y[:3],y[3:]
        u1,u2,u3 = u
        c1,c2,c3 = np.cos(q)
        s1,s2,s3 = np.sin(q)

        mu = np.r_[-c1*s2,s1,c1*c2]
        e2 = np.dot(a2, mu*mu)
        e = np.sqrt(e2)
        x = a2*mu/e
        x[2] -= h

        dm = np.cross(mu,u)
        de = np.dot(a2, mu*dm)/e
        dx = a2*(e*dm - de*mu)/e2
        v = np.cross(x,u)
        z = np.cross(u, v-dx)

        F = g*np.cross(mu,x) - sigma*u
        R = np.cross(np.dot(I0,u), u)
        S = np.cross(x,z)
        I = I0 + np.dot(x,x)*np.eye(3) - np.outer(x,x)
        du = np.linalg.solve(I, F+R+S)

        dq1 = u3*s2 + u1*c2
        dq3 = (u3*c2 - u1*s2)/c1
        dq2 = u2 - dq3*s1

        return np.r_[dq1,dq2,dq3,du]

    return odeint(diff_eq, init, t, **kw)
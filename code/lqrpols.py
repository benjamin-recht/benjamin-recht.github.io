import numpy as np
import scipy.linalg as LA

def lqr_gain(A,B,Q,R):
  '''
  Arguments:
    State transition matrices (A,B)
    LQR Costs (Q,R)
  Outputs:
    K: optimal infinite-horizon LQR gain matrix given
  '''

  # solve DARE:
  M=LA.solve_discrete_are(A,B,Q,R)

  # K=(B'MB + R)^(-1)*(B'MA)
  return np.dot(LA.inv(np.dot(np.dot(B.T,M),B)+R),(np.dot(np.dot(B.T,M),A)))

def cost_inf_K(A,B,Q,R,K):
  '''
    Arguments:
      State transition matrices (A,B)
      LQR Costs (Q,R)
      Control Gain K
    Outputs:
      cost: Infinite time horizon LQR cost of static gain K
  '''
  cl_map = A+B.dot(K)
  if np.amax(np.abs(LA.eigvals(cl_map)))<(1.0-1.0e6):
    cost = np.trace(LA.solve_discrete_lyapunov(cl_map.T,Q+np.dot(K.T,R.dot(K))))
  else:
    cost = float("inf")

  return cost

def cost_finite_model(A_true,B_true,Q,R,x0,T,A_dat,B_dat):
  '''
    Arguments:
      True Model state transition matrices (A_true,B_true)
      LQR Costs (Q,R)
      Initial State x0
      Time Horizon T
      Nominal Model state transition matrices (A_dat,B_dat)
    Outputs:
      cost: finite time horizon LQR cost when control is computed using
      (A_dat,B_dat) but executed on system (A_true,B_true)
  '''
  d,p = B_true.shape

  # Ricatti recursion
  M = np.zeros((d,d,T))
  M[:,:,-1]=Q
  for k in range(T-2,-1,-1):
    AMA = np.dot(A_dat.T,M[:,:,k+1].dot(A_dat))
    AMB = np.dot(A_dat.T,M[:,:,k+1].dot(B_dat))
    BMB = np.dot(B_dat.T,M[:,:,k+1].dot(B_dat))
    M[:,:,k] = Q + AMA - np.dot(AMB,LA.inv(R+BMB).dot(AMB.T))

  # compute contols and costs using these Ricatti iterates
  cost = 0
  x = x0
  for k in range(T):
    AMB = np.dot(A_dat.T,M[:,:,k].dot(B_dat))
    BMB = np.dot(B_dat.T,M[:,:,k].dot(B_dat))
    u = -np.dot(LA.inv(R+BMB),np.dot(AMB.T,x))
    x = A_true.dot(x)+B_true.dot(u)
    cost = cost+np.dot(x.T,Q.dot(x))+np.dot(u.T,R.dot(u))

  return cost.flatten()

def cost_finite_K(A_true,B_true,Q,R,x0,T,K):
  '''
    Arguments:
      True Model state transition matrices (A_true,B_true)
      LQR Costs (Q,R)
      Initial State x0
      Time Horizon T
      Static Control Gain K
    Outputs:
      cost: finite time horizon LQR cost when control is static gain K on
      system (A_true,B_true)
  '''

  d,p = B_true.shape

  cost = 0
  x = x0
  for k in range(T):
    u = np.dot(K,x)
    x = A_true.dot(x)+B_true.dot(u)
    cost = cost+np.dot(x.T,Q.dot(x))+np.dot(u.T,R.dot(u))

  return cost.flatten()

def lsqr_estimator(A,B,Q,R,x0,eq_err,N,T):
  '''
    Arguments:
      state transition matrices (A,B)
      LQR Costs (Q,R)
      Initial State x0
      magnitude of noise in dynamics eq_err
      Number of rollouts N
      Time Horizon T
    Outputs:
      Estimated State Transition Matrices (A_nom,B_nom) from least squares
  '''

  d,p = B.shape

  # storage matrices
  X_store = np.zeros((d,N,T+1))
  U_store = np.zeros((p,N,T))

  # simulate
  for k in range(N):
    x = x0
    X_store[:,k,0] = x0.flatten()
    for t in range(T):
      u = np.random.randn(p,1)
      x = A.dot(x)+B.dot(u)+eq_err*np.random.randn(d,1)
      X_store[:,k,t+1] = x.flatten()
      U_store[:,k,t] = u.flatten()

  ### Solve for nominal model
  tmp = np.linalg.lstsq(np.vstack((X_store[:,:,0:T].reshape(d,N*T),
                                U_store.reshape(p,N*T))).T,
                    X_store[:,:,1:(T+1)].reshape(d,N*T).T)[0]
  A_nom = tmp[0:d,:].T
  B_nom = tmp[d:(d+p),:].T
  return (A_nom,B_nom)

def random_search_linear_policy(A,B,Q,R,x0,eq_err,N,T,
    explore_mag = 1e-2, step_size = 5e-1, batch_size = 4):
  '''
    Arguments:
      state transition matrices (A,B)
      LQR Costs (Q,R)
      Initial State x0
      magnitude of noise in dynamics eq_err
      Number of rollouts N
      Time Horizon T

      hyperparameters:
        explore_mag = magnitude of the noise to explore
        step_size
        batch_size = number of directions per minibatches
        safeguard: maximum absolute value of entries of controller gain

    Outputs:
      Static Control Gain K optimized on LQR cost by random search
  '''

  d,p = B.shape

  # initial condition for K
  K0 = 1e-3*np.random.randn(p,d)
  ###

  #### ALGORITHM
  K = K0
  for k in range(N):
    reward_store = []
    mini_batch = np.zeros((p,d))
    for j in range(batch_size):
      V = explore_mag*np.random.randn(p,d)
      for sign in [-1,1]:
        x = x0
        reward = 0
        for t in range(T):
          u = np.dot(K+sign*V,x)
          x = A.dot(x)+B.dot(u)+eq_err*np.random.randn(d,1)
          reward += -np.dot(x.T,Q.dot(x))-np.dot(u.T,R.dot(u))
        mini_batch += (reward*sign)*V
        reward_store.append(reward)
    if k>2000:
        step_size_use = step_size*0.1;
    else:
        step_size_use = step_size

    K += (step_size_use/np.std(reward_store)/batch_size)*mini_batch

  return K

def uniform_random_linear_policy(A,B,Q,R,x0,eq_err,N,T):
  '''
    Arguments:
      state transition matrices (A,B)
      LQR Costs (Q,R)
      Initial State x0
      magnitude of noise in dynamics eq_err
      Number of rollouts N
      Time Horizon T
    Outputs:
      Static Control Gain K optimized on LQR cost by uniformly sampling policies
      in bounded region
  '''

  d,p = B.shape

  # maximum absolute value of entries of controller gain
  linf_norm = 2

  #### "ALGORITHM"
  best_K = np.empty((p,d))
  best_reward = -float("inf")
  for k in range(N):
    K = np.random.uniform(-linf_norm,linf_norm,(p,d))
    x = x0
    reward = 0
    for t in range(T):
      u = np.dot(K,x)
      x = A.dot(x)+B.dot(u)+eq_err*np.random.randn(d,1)
      reward += -np.dot(x.T,Q.dot(x))-np.dot(u.T,R.dot(u))
    if reward>best_reward:
        best_reward = reward
        best_K = K

  return best_K

def policy_gradient_linear_policy(A,B,Q,R,x0,eq_err,N,T,
  explore_mag = 5e-2,step_size = 2, batch_size = 40, safeguard = 2):
  '''
    Arguments:
      state transition matrices (A,B)
      LQR Costs (Q,R)
      Initial State x0
      magnitude of noise in dynamics eq_err
      Number of rollouts N
      Time Horizon T

      hyperparameters
         explore_mag magnitude of the noise to explore
         step_size
         batch_size: number of stochastic gradients per minibatch
         safeguard: maximum absolute value of entries of controller gain

    Outputs:
      Static Control Gain K optimized on LQR cost by Policy Gradient
  '''

  d,p = B.shape

  # initial condition for K
  K0 = 1e-3*np.random.randn(p,d)
  ###

  X_store = np.zeros((d,T))
  V_store = np.zeros((p,T))

  #### ALGORITHM
  K = K0
  baseline = 0
  for k in range(N):
    new_baseline = 0
    mini_batch = np.zeros((p,d))
    for j in range(batch_size):
      x = x0
      reward = 0
      for t in range(T):
        v = explore_mag*np.random.randn(p,1)
        X_store[:,t] = x.flatten()
        V_store[:,t] = v.flatten()
        u = np.dot(K,x)+v
        x = A.dot(x)+B.dot(u)+eq_err*np.random.randn(d,1)
        reward += -np.dot(x.T,Q.dot(x))-np.dot(u.T,R.dot(u))
      mini_batch += ((reward-baseline)/batch_size)*np.dot(V_store,X_store.T)
      new_baseline += reward/batch_size
    K += step_size*mini_batch
    K = np.minimum(np.maximum(K,-safeguard),safeguard)
    baseline = new_baseline
  return K

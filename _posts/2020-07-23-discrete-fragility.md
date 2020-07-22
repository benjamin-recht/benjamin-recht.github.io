---
layout:     post
title:      "Even State Feedback Isn't Naturally Robust"
date:       2020-07-23 0:00:00
summary:    "Simple examples of discrete-time optimal control problems where even state feedback pushes you into fragile policies."
author:     Ben Recht
visible:    false
blurb: 		  false
---
Doyle derived his LQG counterexample in the time before the ubiquity of numerical computing. This meant that numerical examples did not carry the rhetorical weight of algebraic closed form instances. The need for clean, persuasive formulae also meant that controllers were idealized in continuous time. Continuous-time optimal control often produced policies that couldn't be implemented because of the limits of physical reality: no system can act instantaneously with arbitrary power. These issues of infeasibility were [certainly noted in the literature](https://ieeexplore.ieee.org/document/1099822/) during the hey day of optimal control, but continuous time models still often made it difficult to pinpoint these issues.

Discrete-time models don't share many of these issues. In discrete time, we explicitly encode the sequential, computational nature of decision and control. Discrete-time formulae are unfortunately less elegant than their continuous-time counterparts, but, as I hope to show here, they are often more revealing. Indeed, constructing examples where discrete-time optimal control leads to fragile solutions seems to be surprisingly easy.

Here, I'll highlight a few examples where relatively innocuous problem formulations lead to very fragile control policies. The examples are weirdly simple and almost comical to a point. But anyone who has played with discrete-time optimal control may have stumbled into similar control policies and had to step back and think about why.

Let's revisit the discrete-time LQR problem:

$$
	\begin{array}{ll} \text{minimize} & \sum_{t=1}^N \mathbb{E}_{w_t}\left[x_t^\top Q x_t + u_t^\top R u_t\right]\\
	\text{subject to} & x_{t+1} = A x_t + B u_t + w_t
	\end{array}
$$

We again assume $x_t$ is observed perfectly without noise. While such perfect state information is not realistic, even ideal state feedback ends up being fragile in discrete time. $w_t$ is assumed to be stochastic, but I don't think much changes if we move to a more adversarial setting. Here, we need the decision variable $u_t$ to be _causal_. It must be a function of only the values $x_s$ and $u_s$ with $s\leq t$. For stochastic disturbances, the optimal $u$ can always be found by dynamic programming.

Consider the following innocuous dynamics:

$$
	A = \begin{bmatrix} 0 & 1\\ 0 & 0\end{bmatrix} \,,~~~ B = \begin{bmatrix} 0\\1 \end{bmatrix}\,,
$$

This system is a simple, two-state shift register. I'll write the state out with indexed components $x=[x^{(1)},x^{(2)}]^\top$. New states enter through the control $B$ into the second state. The first state, $x^{(1)}$ is simply whatever was in the second register at the previous time step. The open loop dynamics of this system are as stable as you could imagine. Both eigenvalues of $A$ are zero.

Let's say our control objective aims to try to keep the two states equal to each other. We can model this with the quadratic cost:

$$
	Q = \begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix} \,, ~~~ R = 0\,.
$$

I assume $R=0$ here for simplicity, as the formulae are particularly nice for this case. But, as I will discuss in a moment, the situation is not improved simply by having $R$ be positive. For the disturbance, assume that $w_t$ is zero mean, has bounded second moment, $\Sigma_t = \mathbb{E}[w_t w_t^\top]$, and is uncorrelated with $x_t$ and $u_t$.

The cost is asking to minimize
\[
	\sum_{t=1}^N (x_t^{(1)}-x_t^{(2)})^2
\]
When $w_t=0$, $x_t^{(1)}+x_t^{(2)} = x_{t-1}^{(2)}+u_{t-1}$, so it seems like our best bet is to just set $u_{t}=x_t^{(2)}$. This turns out to be the optimal action, and you can prove this directly using standard dynamic programming computations. What this means is that the closed loop dynamics of the system are

$$
	x_{t+1} = \begin{bmatrix} 0 & 1\\ 0 &1 \end{bmatrix} x_t + w_t\,.
$$

This closed-loop system is _marginally stable_, meaning that while signals don't blow up, some states will persist forever and not converge to $0$. Indeed, the state-transition matrix here has eigenvalues $0$ and $1$. The $1$ corresponds the state where the two components are equal, and such a state can persist forever.

We can also immediately see that if the true $B_\star=\alpha B $, the closed loop dynamics are

$$
	x_{t+1} = \begin{bmatrix} 0 & 1\\ 0 &\alpha \end{bmatrix} x_t + w_t\,,
$$

which is unstable for any $\alpha>1$. That is, this system is arbitrarily fragile. Note that this fragility has nothing to do with the noise sequence. The structure of the cost is what drives the system to fragility.

If $R>0$, you will get a slightly different system. Again, using elementary dynamic programming shows that the optimal control is $u_t=\beta_t(R) x_t^{(2)}$ for some $\beta_t(R) \in (1/2,1)$. The closed loop system will be a bit more stable, but this comes at the price of reduced performance. And, at best, the gain margin of this system approaches $2$ as $R$ goes to infinity.

This behavior can occur in even simpler systems. Consider the one-state linear system

$$
x_{t+1}= b u_t+w_t\,.
$$

The open loop system is again as stable as it gets. Now let's aim to minimize $\Vert x-u \Vert$. It doesn't matter what norm you choose here or whether you treat the noise as stochastic or worst case with respect to $w$, the optimal control is going to be $u_t = x_t/b$. Once again, the closed loop system has a pole at $1$ and is arbitrary fragile to misspecification of $b$.

I could continue to construct nasty examples, but I hope these examples are sufficiently illustrative. The two examples are certainly contrived and pathological, and it's not at all clear that they reflect any optimal control problem you might have been hoping to solve. However, both examples involve systems that are robust and stable in open loop. It's only when we close the feedback loop that we end up in a dangerous situation. That simple optimal control problems give some profoundly fragile solutions should be a clear warning: _You can't just optimize and hope to be robust._ You have to consider uncertainty as a first class citizen when designing feedback systems.

In some sense, the core contribution of robust control is in raising awareness of fundamental tradeoffs in the design of feedback systems. Where should you put that extra sensor? Which parts of the system are likely to create issues? Is it possible to avoid performance disruptions when updating a single component in a legacy system? These questions are important in all aspects of system engineering, and developing accessible tools for addressing them in machine learning systems remains a daunting but essential challenge.

I am emphatically not saying that the design of feedback systems is hopeless. It's easy to walk away with the impression "Ben's examples are pathologies and unlike what I see in practice" or the pessimistic feeling of "shoot, all of this ML stuff is hopeless, I'm going to go work on something tractable like vaccine development." I'm not saying that engineering robust machine learning systems is hopeless. I'm just saying that our community has to work better to incorporate multiple levels of uncertainty in its thinking. What are the fundamental tradeoffs between performance and robustness in machine learning? What do we even want to be robust to? In the next post I want to describe some of these robustness tradeoffs without using the language of optimization, probing if that provides some enticing paths forward.

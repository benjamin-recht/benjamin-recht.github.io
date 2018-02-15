---
layout:     post
title:      The Policy of Truth
date:       2018-02-14 0:00:00
summary:    An outsider tour of reinforcement learning, Part 7. Policy gradient doesn't have gradients.
author:     Ben Recht
visible:    false
---

Before talking about policy gradient, let's step back and consider a pure optimization setup. This setup will seem like a bizarre caricature, but, in a moment, we'll see this is _exactly what people do in Reinforcement Learning_.

Let's start with just trying to maximize a function. Given a function $R[u]$, I want to find the $u$ that makes this as large as possible. That is, I'd like to solve the optimization problem

$$
\begin{array}{ll}
	\mbox{maximize}_u & R[u] \,.
	\end{array}
$$


Now, bear with me for a second into a digression that might seem tangential. Any optimization problem like this is equivalent to an optimization over probability distributions on $u$.

$$
\begin{array}{ll}
	\mbox{maximize}_{p(u)} & \mathbb{E}_p[R[u]]
\end{array}
$$

The equivalence is really straight forward: if $u_\star$ is the optimal solution, then you'll get the same cost if you put a Delta-function around $u_\star$.  Moreover, if $p$ is a probability distribution, it's clear that the _expected reward_ can never be larger than maximal reward achievable by a fixed $u$. So I can either optimize over $u$ or I can optimize over _distributions_ over $u$.

Now here is where the first sleight of hand often occurs in Reinforcement Learning... Rather than optimizing over the space of of all probability distributions, I'm going to optimize over a parametric family $p(u;\vartheta)$.  For example, I could restrict my attention to Gaussian distributions or some other model which is easy to parameterize and to sample from (the sampling part is essential as we will soon see). If this family contains all of the delta functions, then the optimal values still coincide. But, as in the case of Gaussians, if they don't contain the delta functions, you will only get an upper bound on the optimal cost no matter how good of a probability distribution you find. As a result, if you sample $u$ from the policy, their expected reward will necessarily be suboptimal.

## The REINFORCE algorithm

There is a general purpose algorithm for finding descent directions of the cost

$$
\begin{array}{ll}
	\mbox{maximize}_{\vartheta} & J(\vartheta):=\mathbb{E}_{p(u;\vartheta)}[R[u]]
	\end{array}
$$

The idea is to use a clever trick:

$$
\begin{align*}
	\nabla J(\vartheta) &= \int R(u) \nabla p(u;\vartheta) du\\
	&= \int R(u) \left(\frac{\nabla p(u;\vartheta)}{p(u;\vartheta)}\right) p(u;\vartheta) dx\\
	&= \int \left( R(u) \nabla \log p(u;\vartheta) \right) p(u;\vartheta)dx
	= \mathbb{E}_{p(u;\vartheta)}\left[ R(u) \nabla \log p(u;\vartheta) \right]\,.
\end{align*}
$$

Now something magical occurs. Suppose you sample $u$ from $p(u;\vartheta)$.  Then $R(u) \nabla \log p(u;\vartheta)$ is an unbiased estimate of the gradient of $J(\vartheta)$. Hence, we can use this for stochastic gradient descent.

The REINFORCE algorithm is a general purpose algorithm using this trick:
\begin{enumerate} \itemsep 0pt
 \item Choose some initial guess $\vartheta_0$ and stepsize sequence $\{\alpha_k\}$. Set $k=0$.
 \item Sample $u_k$ i.i.d., from $p(u;\vartheta_k)$.
 \item Set $\vartheta_{k+1} = \vartheta_k + \alpha_k R(u_k) \nabla \log p(u_k;\vartheta_k)$.
 \item Increment $k=k+1$ and go to 2.
\end{enumerate}

This seems weird: we get a stochastic gradient, but the function we cared about optimizing---$R$---is only accessed through function evaluations. We never compute gradients of $R$ itself. So is this algorithm any good?

It depends on what you are looking for. If you're looking for something to compete with gradients, no. It's a terrible algorithm. If you're looking for an algorithm to compete with a finite difference approximation to $R$ then... it's still a terrible algorithm. But the math is cute.

OK, you're not convinced.  Let's just start with a simple simple example.  Let
$$
	R[u] = -||u-z||^2
$$
Let $p(u;\vartheta)$ be a multivariate Gaussian with mean $\vartheta$ and variance $\sigma^2 I$.  What does policy gradient do?  First, note that

$$
	\mathbb{E}_{p(u;\vartheta)} = -\|\vartheta-z\|^2 - \sigma^2 d
$$

Obviously, the best thing to do would be to set $\vartheta=z$. Note that the expected cost is off by $\sigma^2 d$ at this point, but at least this would be finding a good guess for $u$.  Also, as a function of $\vartheta$, $J$ is _strongly convex_, and the most important thing to know is the expected norm of the gradient as this will control the number of iterations. Now, if you start at $\vartheta=0$, then the norm of the gradient is

$$
	g=\frac{||z||^2 \omega_0}{\sigma^2}
$$

And the norm is $d \|z\|^2$. That's actually quite large! The norm of the gradient is proportional to $d$.

Many people have analyzed the complexity of this method, and it is indeed not great. If the function values are noisy, even for convex functions, the convergence rate is $O((d^2/T)^{-1/3})$, and this assumes you get the algorithm parameters exactly right. For strongly convex functions, you can possibly eke out a decent solution in $O((d^2/T)^{-1/2})$ function evaluations.

So fine, it converges, but is this really the best we can do? Lots of papers have been applying policy gradient to all sorts of different settings, and claiming crazy results, but it's clear that they are just dressing up pure random search in a clever outfit. This is why genetic algorithms seem to fare so well in comparison. Regardless, both genetic algorithms and policy gradient require an absurd number of samples. This is OK if you are willing to spend millions of dollars on AWS and never actually want to tune a physical system. But there must be a better way...

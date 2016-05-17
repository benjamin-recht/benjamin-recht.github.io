---
layout:     post
title:      Mates of Costate
date:       2016-05-17 7:00:00
summary:    The dynamical systems view of backpropagation
author:     Ben Recht
visible:    false
---

There have been four thousand new frameworks for deep learning thrown on the market the past year, and I bet you were wondering what you needed to jump into this hot marketplace.  Essentially, there are two components required for most mortals who aim to train neural nets: a unit that efficiently computes derivatives of functions that are compositions of many sub-functions and a unit that runs stochastic gradient descent.  I can write the stochastic gradient descent part in ten lines of python.  I'll sell it to the highest bidder in the comments.  But what about the automatic differentiator?

Automatic differentiation does seem like a bit of a black box.  Some people will just scoff and say "it's just the chain rule." But evaluating the chain rule efficiently requires being careful about reusing information, and not having to handle special cases.  The backpropagation algorithm handles these recursions well.  It is a dynamic programming method to compute derivatives, and uses clever recursions to aggregate the gradients of the components.   However, I always find the derivations of backprop to be confusing and too closely tied to neuroscientific intuition that I sorely lack.  Moreover, for some reason, dynamic programming always hurts my brain and I have to think about it for an hour before I remember how to derive it.  

A few years ago, [Steve Wright](http://pages.cs.wisc.edu/~swright/) introduced me to an older method, called the method of adjoints, which is equivalent to backpropagation, and also easier (for me at least) to derive.  This is because the core of the method is *Lagrangian duality*, a topic at the foundation of everything we optimizers do.

## Deep neural networks

Before we get to Lagrangian duality, we need a constrained optimization problem.  There's no Lagrangian without some constraints!  So let's transform a deep learning optimization problem into a constrained optimization problem.

The standard deep learning goal is to solve optimization problems of the form

$$
	\begin{array}{ll}
		\mbox{minimize}\_{\varphi} &\frac{1}{n} \sum_{k=1}^n \mathrm{loss}(\varphi(x_k),y_k) ,
	\end{array}
$$

where $\varphi$ is a function from features to labels that has an appropriate level of expressivity.  In deep learning, we assume that $\varphi$ is a giant composition:

$$
	\varphi(x;\vartheta) = f_\ell \circ f_{\ell-1} \circ f_{\ell-2} \circ \cdots  \circ f_1(x)
$$

and each $f_i$ has a vector of parameters $\vartheta_{i-1}$ which may be optimized.  In this case, we can rewrite the unconstrained minimization problem as a constrained one:

$$
	\begin{array}{ll}
		\mbox{minimize}\_{\vartheta} &\frac{1}{n} \sum_{k=1}^n \mathrm{loss}(z_k^{(\ell)},y_k) \\\
		\mbox{subject to} & z_k^{(\ell)} = f_\ell(z_{k}^{(\ell-1)}, \vartheta_{\ell})\\\
		&  z_k^{(\ell-1)} = f_{\ell-1}(z_{k}^{(\ell-2)}, \vartheta_{\ell-1})\\\
		& \vdots\\\
		&  z_k^{(1)} = f_1(x_k, \vartheta_{1}).
	\end{array}
$$

Why does this help?  First, the hope is that each block here is a relatively simple computation, like a matrix-vector multiply followed by a component-wise nonlinearity.  Thus, we have broken the computation into relatively simple pieces.  Moreover, it turns out that explicitly writing out the composition in stages is akin to laying out a computation graph for the function.  And once we have a computation graph, we can use it to compute derivatives.

## The method of adjoints

The structure of the backpropagation algorithm is revealed and exploited by writing down the KKT conditions for the constrained formulation of the optimization problem.
To simplify matters, let's restrict our attention to the case where $n=1$ and there is a single $(x,y)$ pair as you'd have if you were running stochastic gradient descent.

To derive the KKT conditions we first form a Lagrangian function with Lagrange multipliers $p_i$:

$$
\mathcal{L} (x,u,p) :=   \mathrm{loss}(z^{(\ell)},y) - \sum_{i=1}^{\ell} p_i^T(z^{(i)} - f_i(z^{(i-1)},\vartheta_i)),
$$

The derivatives of this Lagrangian are given by the expressions:

$$
\begin{aligned}
\nabla_{z^{(i)}} \mathcal{L} &= - p_{i} + \nabla_{z^{(i)}} f_{i+1}(z^{(i)},\vartheta_{i+1})^T p_{i+1} , \\
\nabla_{z^{(\ell)}} \mathcal{L} &= -p_\ell + \nabla_{z^{(\ell)}} \mathrm{loss}(z^{(\ell)},y) , \\
\nabla_{\vartheta_i} \mathcal{L} &= \nabla_{\vartheta_i} f_i(z^{(i-1)},\vartheta_i)^Tp_i ,\\
\nabla_{p_i} \mathcal{L} &= z^{(i)} - f_i(z^{(i-1)},\vartheta_i).
\end{aligned}
$$

The Lagrange multipliers $p_i$ are also known as the *adjoint variables* or *costates*. To compute the gradient, we just have to solve this set of nonlinear equations

$$
\nabla_{p_i} \mathcal{L} = 0~\mbox{and}~ \nabla_{z_i} \mathcal{L} =0
$$

and then we can just read off the gradient with respect to $\nabla_\vartheta \mathrm{loss}(\varphi(x;\vartheta),y)= \nabla_{\vartheta_i} f_i(z^{(i-1)},\vartheta_i)^Tp_i$.
(I'll explain why later... trust me for a second).

Now, the structure here is particularly nice.  If we solve for $\nabla_{p_i} \mathcal{L}=0$, this just amounts to satisfying the constraints  $z^{(i)} = f_i(z^{(i-1)})$.  This is called the *forward pass*.  Now, we can compute $p_i$ from the equations $\nabla_{z_i} \mathcal{L} =0$.  That is,

$$
p_\ell = \nabla_{z^{(\ell)}} \mathrm{loss}(z^{(\ell)},y) \,.
$$

This is the *backward pass*.  The gradients with respect to the parameters can then be computed by adding up linear functions of the adjoint variables.

There are tons of ways to generalize this.  We could have a more complicated computation graph.  We could share variables among layers (this would mean adding up variables).  We could penalize hidden variables or states explicitly in the cost function.  Regardless, we could read off the solution via the same forward-backward procedure.   The computation graph always provides a  "forward model" describing the evolution of an input to the output. The adjoint equation involves the adjoint ("transpose") of the Jacobians of this equation, which measures the sensitivity of one node to the previous node.  

## Adjoints in Optimal Control

As I mentioned already, the method of adjoints originates in the study of controls.  According to [Dreyfus](http://arc.aiaa.org/doi/abs/10.2514/3.25422), this was first proposed by Bryson in a paper called "A Gradient Method for Optimizing Multi-Stage
Allocation Processes" that appeared in the *Proceedings of the Harvard University Symposium
on Digital Computers and Their Applications* in 1961.  I was unable to find that paper in our Engineering Library, but it plays a prominent role in Bryson's book on [Applied Optimal Control](http://www.amazon.com/Applied-Optimal-Control-Optimization-Estimation/dp/0891162283).   Note that Bryson's paper appeared only a couple of months after as Kalman's absurdly influential [A New Approach to Linear Filtering and Prediction Problems](http://fluidsengineering.asmedigitalcollection.asme.org/article.aspx?articleid=1430402). This use of duality was very much at the birth of modern control theory.

Let's take the simplest and most studied optimal control problem and see what backpropagation computes.  In optimal control, we have a dynamical system with state variable $x_t$ and input $u_t$.  We assume the state evolves according to the linear dynamics

$$
	x_{t+1} = A x_t + B u_t~\mbox{for}~t=0,1,\ldots\,.
$$

where $(A,B)$ are some known state-evolution equations.

Suppose we would like to find a sequence of inputs $u_t$ that minimizes some quadratic cost over the trajectory:

$$
\begin{array}{ll}
\mbox{minimize}_{u_t,x_t} \, & \tfrac{1}{2}\sum_{t=0}^T \left\{x_t^TQ x_t + u_t^T R u_t\right\}  \\
& \qquad + \tfrac{1}{2} x_{N+1}^T S x_{N+1}, \\
\mbox{subject to} & x_{t+1} = A x_t+ B u_t, \\
& \qquad \mbox{for}~t=0,1,\dotsc,N,\\
& \mbox{($x_0$ given).}
\end{array}
$$

The Lagrangian for this system has a similar form to that for the neural network

$$
\mathcal{L} (x,u,p) := \sum_{i=0}^N [ \tfrac{1}{2} x_t^TQ x_t + \tfrac{1}{2}u_t^T R u_t - p_t^T (x_{t+1}-A x_t - B u_t)) ] +
\tfrac{1}{2} x_{N+1}^T S x_{N+1}.
$$

The gradients of the Lagrangian are given by the expressions

$$
\begin{aligned}
\nabla_{x_t} \mathcal{L} &= Qx_t - p_{t-1} + A^T p_i , \\
\nabla_{x_{N+1}} \mathcal{L} &= -p_N +  S x_{N+1} , \\
\nabla_{u_t} \mathcal{L} &= R u_t + B^T p_t , \\
\nabla_{p_t} \mathcal{L} &= -x_{t+1} + Ax_t + B u_t.
\end{aligned}
$$

Again, to satisfy $\nabla_{p_i} \mathcal{L}=0$, we simply run the dynamical system model forward in time to compute the trajectory $x_t$.  Then, we can solve for the costates $p_i$ by running the *adjoint dynamics*

$$
	p_{t-1} = A^T p_t +  Q x_t
$$

with the initial condition $p_N = Sx_{N+1}$.  For the optimal control problem, the Lagrange multipliers are a trajectory of a related linear system called the *adjoint* or *dual* system.  The dynamics are linear in the costate $p_t$, with time running in reverse and the state transition matrix being the transpose (also known as the adjoint) of $A$.  The costate is driven by the forward trajectory $x_t$.   This gives us a clear way to think about the dynamics about how later states are sensitive to early states.  In the special case when $Q$ and $R$ are zero, we are computing the sensitivity of the end state $x_{N+1}$ to the inputs $u_t$.  If $A$ is *stable*, meaning all of its eigenvalues have magnitude strictly less than $1$, than early inputs have little effect on the terminal state.  But if $A$ is *unstable*, the costate dynamics may diverge, and hence the gradient with respect to $u_t$ for small $t$ can grow exponentially large.

In the special case where the cost involves tracking an observation $y_t$, we arrive at the cost function of Kalman's Filter:

$$
\begin{array}{ll}
\mbox{minimize}_{u_t,x_t} \, & \tfrac{1}{2}\sum_{t=0}^T \left\{\|x_t-y_t\|^2+ u_t^T R_t u_t \right\}\\
&\qquad\qquad+ \tfrac{1}{2}x_0^T S x_0\\
\mbox{subject to} & x_{t+1} = A x_t+ B u_t, \\
& \qquad \mbox{for}~t=0,1,\dotsc,N\,.
\end{array}
$$

One could solve the Kalman Filtering problem by performing gradient descent on the cost and computing the gradient via the method of adjoints.  This would be a totally reasonable solution, akin to solving a tridiagonal system via conjugate gradient.  However, the special structure of this system enables us to solve the normal equations in linear time, so most people don't compute their filters this way.  On the other hand, the method of adjoints is far more general than the Kalman Filter as it immediately applies to nonlinear dynamical systems or the  nonquadratic costs.  Moreover, the iterations require only $O(N)$ operations even in the general case.  This method is quite useful when the constraints are defined by partial differential equations, as there is an associated adjoint PDE that enables optimization in this setting as well.  Lions has a [whole book](http://www.springer.com/us/book/9783642650260) on this topic.

And, if you wanted to be crazy and make the control policy $u_t$ to be the output of a neural network applied to $x_t$, one could still compute gradients using the method of adjoints.

## Why is this the derivative?

So why is this Lagrangian procedure correct?  The KKT conditions are a necessary condition for stationarity in nonlinear programming.  It's not particularly obvious why this should also give a way to compute derivatives. In the next post, I will show how the method of adjoints is intimately connected to the KKT conditions.  I will describe how the proof of the KKT conditions also provides a proof of correctness for the method of adjoints.  And I'll also describe other algorithms that naturally arise when one views a cascade of function compositions as a dynamical system.

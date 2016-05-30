---
layout:     post
title:      Mechanics of Lagrangians
date:       2016-05-30 7:00:00
summary:    Two paths to understanding Lagrangians in nonlinear optimization
author:     Ben Recht
visible:    false
---

In my last post, I used a Lagrangian to compute derivatives of constrained optimization problems in neural nets and control.  I took it for granted that the procedure was correct.  But why is it correct?  I suppose the simplest answer is because we arrived at the same procedure as back propagation.  But that's not particularly satisfying and doesn't give you any room to generalize.

In fact, if I'm really honest about it, none of the manipulations we do with Lagrangians in optimization are decidedly intuitive.  Mechanistically, they give powerful methods to derive algorithms, understand sensitivities to assumptions, and generate lower bounds. But the Lagrangian functionals themselves always just seem to pop out of thin air.  Why are Lagrangian methods so effective in optimization, even when the associated problems are nonconvex?

In this post, I'm going to "derive" Lagrangians in two very different ways: one by pattern matching against the implicit function theorem and one via penalty functions.  This basically follows the approach in Bertsekas' [Nonlinear Programming Book](http://www.athenasc.com/nonlinbook.html) where he introduces Lagrange multipliers and the KKT conditions.  Most people know the KKT conditions as a necessary condition for optimality in nonlinear programming.  How does it also arise in computing derivatives?  It turns out that these two are actually quite connected, and if you have ever worked out a proof of the KKT conditions, you probably already derived a correctness proof for the method of adjoints.

## Implicit functions

Let's begin by attempting to formalize what it means to take a derivative of a function subject to constraints.  Suppose we have a function $F:\mathbb{R}^{n+d} \rightarrow \mathbb{R}$ which we write as $F(x,z)$ where $x$ is $n$-dimensional and $z$ is $d$ dimensional.  Additionally, assume we have a constraint function $H:\mathbb{R}^{d+n} \rightarrow \mathbb{R}^d$ which we want to be identically zero.  If we want to take a derivative of $F(x,z)$ with respect to $x$ subject to the constraint $H(x,z)=0$, this means that we want to first eliminate the variable $z$ using the nonlinear equations $H(x,z)=0$.  Let $\varphi(x)$ denote the solution of $H(x,z)=0$ with respect to $z$ (and let's assume such a $z$ exists and is unique).  Once we have solved for $z$, we then want to take a derivative of the \emph{unconstrained} function $F(x,\varphi(x))$ with respect to $x$.  Now, by the chain rule
$$
	\nabla_x F(x,\varphi(x)) = \nabla_x F(x,\varphi(x)) + \nabla_x \varphi(x) \nabla_z F(x,\varphi(x))\,.
$$
What about the gradient of this function $\varphi$?  We can compute its gradient by applying [the implicit function theorem](xxx).  Indeed, if $\nabla_z H(x,z)$ is invertible, the implicit function theorem gives an explicit formula for the gradient:
$$
	\nabla_x \varphi(x) = - \nabla_x H(x,z)[\nabla_z H(x,z)]^{-1} \,.
$$
With this formula in hand, we can apply some magical pattern matching. Define $p:= - [\nabla_z H(x,z)]^{-1} \nabla_z F(x,\varphi(x))$ and plug it into the formula above.  Then, if $z=\varphi(x)$, we have
$$
	\nabla_x F(x,z) = \nabla_x F(x,z) + \nabla_x H(x,z) p\,!
$$

In other words, if we define the Lagrangian $\mathcal{L}(x,z,p) = F(x,z) + p^T H(x,z)$, we have that
$$
	\nabla_x F(x,z) = \nabla_x \mathcal{L}(x,z,p)
$$
where $(z,p)$ satisfy
$$
	\nabla_z \mathcal{L}(x,z,p)=0~\mbox{and}~\nabla_p \mathcal{L}(x,z,p)=0\,.
$$

The equations $\nabla \mathcal{L}=0$ are called the \emph{KKT conditions} for the optimization problem.   Any solution must satisfy these equations.  But, following this derivation, it is obvious why the KKT conditions must hold: they are merely asserting that the derivative with respect to $x$ is zero once you have eliminated the constraints.

Even though I can explain this derivation and its consequences, I still find this pattern matching to be bizarrely coincidental.  How exactly did the Lagrangian pop up here?  Let me now derive the same optimality conditions in a completely different way, starting with a Lagrangian and yet recovering the exact same formula and see if this provides any additional insights.

## Penalty functions

My personal favorite motivation of the Lagrangian is in terms of saddle point problems.  Consider the joint optimization problem
$$
	\mbox{minimize}_{x,z}~\mbox{maximize}_{\lambda}~\mathcal{L}(x,z,p):=F(x,z) +p^TH(x,z)
$$  
Now, in the inside maximization optimization problem, the supremum is infinite if $H(x,z)$ is nonzero.  Thus, you only get a finite value when $H(x,z)=0$.  In this case, the minimum value with respect to $x$ and $z$ is just the minimum value of $F(x,z)$ \emph{subject to} $H(x,z)=0$.  That is, it is completely equivalent to the constrained optimization problem we have been analyzing.  So the Lagrangian penalty function enforces the equality constraint via a min-max game.

But why this penalty function?  I like to think of the Lagrangian as a limit of more obvious penalty functions.  If we set up the unconstrained minimization problem
$$
\mbox{minimize}_{x,z}~F(x,z) + \tfrac{1}{2\alpha} \| H(x,z) \|^2\,,
$$
with $\alpha>0$, it's clear that as $\alpha$ tends to zero, the cost enforce the constraint $H(x,z)$ to be small.  In the limit, we would expect that $H(x,z)$ would be zero and the corresponding minimizer should minimize $F$ subject to the constraint that $H$ vanishes.

Now, consider the penalized min-max problem
$$
	\mbox{minimize}_{x,z}~\mbox{maximize}_{\lambda}~\mathcal{L}_\alpha(x,z,p):=F(x,z) +p^TH(x,z) - \tfrac{\alpha}{2}\|p\|^2
$$  
This is an "augmented Lagrangian."  When $\alpha=0$, this is just the Lagrangian above, but now the inner maximization problem always has finite values.  In fact, it's pretty easy to see that the maximizing $p$ is always $H(x,z)/\alpha$.  If we plug in this value, we can eliminate the Lagrange multiplier entirely and just get the quadratically penalized optimization problem.  So in this sense, the Lagrangian formulation of the optimization problem is the limit of penalized formulations.

Now, for the penalized formulation, the stationary points of this problem satisfy $\nabla \mathcal{L}_\alpha=0$.  In particular, for the $z$ variable,
$$
	\nabla_z F(x,z) + \tfrac{1}{\alpha} [\nabla_z H(x,z) ] H(x,z) = 0
$$
But this means that
$$
	p = \tfrac{1}{\alpha} H(x,z) = - [\nabla_z H(x,z)]^{-1} \nabla_z F(x,z)
$$
This is exactly the same formula for $p$ as we derived using the implicit function theorem!  

This shouldn't be too surprising as the optimal value of $p$ has a simple interpretation.  Note that for very small $\Delta z$,
$$
\begin{aligned}
	F(x,z + \Delta z )
	&\approx F(x,z) + \frac{\partial F}{\partial z} \Delta z  \\
	&=F(x,z) - p^T \nabla_x H(x,z) \Delta z
\end{aligned}
$$
so each coordinate of $p$ controls how much the cost function changes as we perturb the constraints.  $p$ measures how sensitive the cost is to small perturbations of the constraints.

Taking the limit as $\alpha$ goes to zero, we see that all local solutions must satisfy the KKT conditions $\nabla \mathcal{L}=0$, and the Lagrange multipliers have the form predicted by the implicit function theorem.

Now, note, that this derivation for $p$ only holds at the stationary points of the Lagrangian.  For actually computing derivatives, the implicit function theorem approach gives the correct form for the gradient at any point $x$.  But it is interesting, again, that these two very differently motivated derivations arrive at the same formulae.

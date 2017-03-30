---
layout:     post
title:      Nesterov's Punctuated Equilibrium
date:       2017-03-20 7:00:00
summary:    connecting genetic algorithms with nonlinear programming
author:     Ben Recht
visible:    false
---

*Ed. Note: this post is co-written with [Roy Frostig](https://cs.stanford.edu/~rfrostig/).*

Following the remarkable success of AlphaGo, there has been a groundswell of interest in reinforcement learning for [games](smash bros), [robotics](grasping), [parameter tuning](quoc), and even [computer networking](msr). In a landmark [new paper](arxiv.org/abs/1703.03864) by Salimans,  Ho, Chen, and Sutskever from OpenAI, the authors show that a particular class of genetic algorithms (called Evolutionary Strategies) gives excellent performance on a variety of reinforcement learning benchmarks. As optimizers, the application of genetic algorithms raises red flags and usually causes us to close browser windows.  But fear not!  As we will explain, the particular algorithm deployed happens to be a core method in optimization, and the fact that this method is successful sheds light on the peculiarities of reinforcement learning more than it does about genetic algorithms in general.  

## Evolution Strategies is Gradient Ascent

Of course, as optimizers, we think everything is the gradient method.  (But we're totally right!)  Let's look at the Evolutionary Strategies (ES) algorithm proposed in the paper.   The goal is to maximize some reward function $R(x)$ where $x$ is $d$-dimensional.  Their algorithm computes the reward function at small perturbations away from its current state, and then aggregates the returned function values into a new state.  To be precise, they sample a collection of $n$ random directions $\epsilon_i$ to be normally distributed with mean zero and covariance equal to the identity. Then the algorithm updates it state according to the rule.

$$
	x_{t+1} = x_{t} + \frac{\alpha}{\sigma n} \sum_{i=1}^n R(x_t + \sigma \epsilon_i) \epsilon_i \,.
$$

Now, why is this a reasonable update? Let's simplify this and consider the case where $n=1$ first.  In this case, the update reduces to this simple iteration

$$
	x_{t+1} = x_{t} + \alpha g_\sigma^{(1)}(x_t)
$$

where

$$
	g_\sigma^{(1)}(x)=  \frac{1}{\sigma} R(x + \sigma \epsilon) \epsilon\,.
$$

This still looks weird!  What is it saying exactly?  It says that you should move along direction $\epsilon$ proportional to the cost.  Larger costs means you should move more in that direction.  Of course, if $R$ is negative, this could be weird: large negative costs cause you to move a long way in the negative direction of $\epsilon$.   An update that you may find simpler to reason about is the following

$$
	g_\sigma^{(2)}(x) = \frac{R(x + \sigma \epsilon) - R(x - \sigma \epsilon) }{2\sigma} \epsilon\,.
$$

This update says to compute a finite difference approximation to the gradient along the direction $\epsilon$ and move along the gradient.  What's not immediately obvious (though it's a trivial calculation) is that $g_\sigma^{(1)}$ and $g_\sigma^{(2)}$ have the same expected value.

The finite difference interpretation also helps to reveal that this algorithm is essentially an instance of stochastic gradient ascent on the reward $R$.  To see this, remember from calculus that

$$
	\lim_{\sigma \downarrow 0}  \frac{R(x + \sigma \epsilon) - R(x - \sigma \epsilon) }{2\sigma}  = \nabla R(x)^T \epsilon
$$

And, moreover

$$
	\mathbb{E}_\epsilon\left[\epsilon\epsilon^T \nabla R(x)\right] = \nabla R(x)
$$

So, for small enough $\sigma$, the update $g^{(2)}_\sigma$ acts like a stochastic approximation to the gradient.

In the experiments by Salimans et al, they always use $g_\sigma^{(2)}$
rather than $g_\sigma^{(1)}$. 
They refer to $g_\sigma^{(2)}$ as *antithetic sampling*, a rather clever term from the MCMC literature.  Such antithetic sampling dramatically improves performance in their experiments.

Now this particular algorithm (ES with antithetic sampling) is precisely equivalent to the derivative-free optimization method analyzed by Yurii Nesterov in 2010.  Noting this equivalence allows us to explain some of the observed advantages of ES, and to suggest some possible enhancements.

## Reduce your variants

Why does $g_\sigma^{(2)}$ perform better than $g_\sigma^{(1)}$?  The answer is simply that though they have the same expected value $g_\sigma^{(2)}$ has significantly lower variance.  To see why, let's study the very boring but fundamental problem of maximizing a quadratic function
$$R(x)=\frac{1}{2}x^TQx +p^Tx + r$$
The we can explicitly write out the two updates:

$$
 	g_\sigma^{(1)}(x)=  R(x) \epsilon+ \epsilon\epsilon^T\nabla R(x)  +   \epsilon \epsilon^T Q\epsilon
$$

$$
	g_\sigma^{(2)}(x)=    \epsilon\epsilon^T \nabla R(x)
$$

Note that $g_\sigma^{(2)}$ has two fewer terms.  And these terms can be quite detrimental to convergence.  First the $R(x)$-term depends on this nuisance offset $r$. Large values of $r$ essentially tell the algorithm using $g^{(1)}$ that all directions are equivalent.  No optimization algorithm worth its salt should be sensitive to this offset.  Second, the term $\epsilon \epsilon^T Q\epsilon$ has variance proportional to $d^3$ and that is quite undesirable.

Now what happens when we batch, as they do in their paper?  Nesterov does not study this in detail in his 2010 paper. In this case, we have a sum of directions.  In the case that the $\epsilon_i$ were all orthogonal, this would be akin to moving along the gradient in a random subspace.  But if $n$ is much smaller than $d$, this is pretty much exactly what happens: we move along a finite difference approximation to the gradient of $R$ in a random subspace.  So this algorithm is very similar to random coordinate ascent.  And we wouldn't be too surprised if choosing random coordinates rather than random subspace directions performed comparably well on these problems.

Now this is where things start to get interesting.  In this [excellent tutorial](http://videolectures.net/deeplearning2016_abbeel_deep_reinforcement/?q=abbeel), Pieter Abbeel describes using finite difference methods for solving reinforcement learning.  This is a well-studied idea that, for some reason, fell out of favor as opposed to cross-entropy or policy gradient methods.  We haven't quite figured out *why* it fell out of favor.  But in light of the recent work from OpenAI, perhaps the reason is that the overhead of computing the finite difference approximation on *all* of the coordinates was too costly.  As their experiments show cleanly, using a small subset of the coordinate directions is computationally inexpensive and finds excellent directions to improve reward.

Nesterov's theoretical analysis helps to elucidate how many coordinates one should descend upon.  Nesterov shows that his random search algorithm requires no more than $d$ times the iterations required by the gradient method.  If you minibatch with batch size $m$, the number of iterations goes down by roughly a factor of $m$.  But there are diminishing returns with respect to batch size, and eventually you are better off computing full gradients.  Moreover, even when there is variance reduction, the number of function calls stays the same: each minibatch requires $m$ function evaluations, so the total number of function evaluations is still $d$ times the number of steps required by the gradient method.

Thus, in a serial setting, minibatching might hurt you.  In theory, you can't get a linear reduction in iterations with minibatches, and batches that are too large will slow down convergence.  In the extreme, you are essentially just computing a finite difference approximation of the gradient.  But in the parallel case, minibatching is great, since you can take advantage of embarrassing parallelism and receive a significant reduction in wall clock time even if the total number of function evaluations is larger than in the serial case.

## Accelerated Evolution

One of our favorite features of an optimization-centric viewpoint is that we can apply other widgets from the optimization toolkit to improve the performance of algorithms.  A natural addition to this gradient-free algorithm is to add *momentum* to accelerate convergence.  Acceleration is likely what Nesterov is best know for.  Adding acceleration simply requires changing the procedure to

$$
	x_{t+1} = (1+\beta) x_{t} + \beta x_{t-1}+   \frac{\alpha}{\sigma n} \sum_{i=1}^n R(x_t + \sigma \epsilon_i) \epsilon_i
$$

This one-line change is simple to implement in the parallel algorithm proposed by Salimans et al. and could provide further speedups over standard policy gradient methods. I suppose if we wanted to merge universes, we could call this "Nesterov's accelerated evolution."

## Use your gradients

Would this random search technique work in training neural nets for supervised learning?  The answer is almost certainly a rather resounding "no."  As Nesterov says "if you have gradients, you should use them!"  Indeed, in neural nets, computing the function value is far more costly than computing a stochastic gradient on an example.

A deeper question is: why do finite difference methods work well for reinforcement learning in the first place? We'll propose reasons in our next post.  Essentially, model-free reinforcement learning *is* derivative free optimization.  If the only access you have to the behavior of a system is through querying the reward given a policy, you never get derivatives of the reward.  The conceit of classic methods like policy gradient is that they convince you that you are doing gradient descent, but the gradient you descend upon is not the gradient of the function you are trying to optimize!  We will flesh this out in more detail in our next post.

---
layout:     post
title:      Nesterov's Punctuated Equilibrium
date:       2017-03-20 7:00:00
summary:    connecting genetic algorithms with nonlinear programming
author:     Ben Recht
visible:    false
---

*Ed. Note: this post is co-written with [Roy Frostig](https://cs.stanford.edu/~rfrostig/).*

$\epsilon \sim \mathcal{N}(0,I)$

$$
g_\sigma^{(1)}(x)=  \frac{1}{\sigma} f(x + \sigma \epsilon) \epsilon
$$

$$
g_\sigma^{(2)}(x) = \frac{f(x + \sigma \epsilon) - f(x - \sigma \epsilon) }{2\sigma} \epsilon
$$

Note that these two have the same expected value.  This latter expression is a finite difference approximation to the directional derivative of $f$ in the direction $\epsilon$.
$$
\lim_{\sigma \downarrow 0}  \frac{f(x + \sigma \epsilon) - f(x - \sigma \epsilon) }{2\sigma}  = \nabla f(x)^T \epsilon
$$


Suppose
$$f(x)=\tfrac{1}{2}x^TQx +p^Tx + r$$
Using method one, we have
$$
  g_\sigma^{(1)}(x)=  f(x) \epsilon+ \epsilon\epsilon^T\nabla f(x)  +   \epsilon \epsilon^T Q\epsilon
$$

$$
  g_\sigma^{(2)}(x)=    \epsilon\epsilon^T \nabla f(x)
$$
For minimization, out of all updates with the same expected value, we want the one with the lowest variance.  Note that the two-point approximation has dramatically lower variance.
First we remove the $f(x)$-term that depends on this nuisance offset $r$. Large values of $r$ essentially tell the algorithm using $g^{(1)}$ that all directions are equivalent.  Second, we remove the term $\epsilon \epsilon^T Q\epsilon$.  Though this term has zero mean, it has variance proportional to $d^3$ and that is undesirable.

---
layout:     post
title:      "There are none"
date:       2020-07-14 0:00:00
summary:    "Linear Quadratic Gaussian control with partial state observation has arbitrarily small gain margins. This post dives into Doyle's classic example and how it relates to machine learning."
author:     Ben Recht
visible:    false
blurb: 		  false
---

In the [last post](http://www.argmin.net/2020/07/08/gain-margin/), we showed that continuous-time LQR has "natural robustness" insofar as the optimal solution is robust to a variety of model-mismatch conditions. LQR makes the assumption that the state of the system is observed noiselessly. In many situations, we don't have access to such state information. What changes?

The generalization of LQR to the case with imperfect state observation is called "Linear Quadratic Gaussian" control (LQG), and is a simplest, special case of a Partially Observed Markov Decision Process (POMDP).  We again assume linear dynamics:

$$
	\dot{x}_t = Ax_t + B u_t + w_t\,.
$$

where the state is now corrupted by zero-mean Gaussian noise, $w_t$. Instead of measuring the state $x_t$ directly, we instead  measure a signal $y_t$ of the form

$$
	y_t = C x_t + v_t\,.
$$

Here, $v_t$ is also zero-mean Gaussian noise. Suppose we'd still like to minimize a quadratic cost function

$$
\lim_{T\rightarrow \infty} \frac{1}{T} \int_{0}^{T} (x_t^\top Qx_t + u_t^\top Ru_t) dt\,.
$$

This problem is very similar to our LQR problem except for the fact that we get an indirect measurement of the state and need to apply some sort of _filtering_ of the $y_t$ signal to estimate $x_t$.

The optimal solution for LQG ends up being strikingly simple: since the observation of $x_t$ is through a Gaussian process, the maximum likelihood estimation algorithm has a clean, closed form solution, even in continuous time. Our best estimate for $x_t$, denoted $\hat{x}_t$, given all of the data observed up to time $t$ obeys a differential equation

$$
	\frac{d\hat{x}}{dt}  = A\hat{x}_t + B u_t + L(y_t-C\hat{x}_t)\,.
$$

The matrix $L$ that can be found by solving an algebraic Riccati equation that depends on the variance of $v_t$ and $w_t$ and on the matrices $A$ and $C$. In particular, it's the CARE with data $(A^\top,C^\top,\Sigma_w,\Sigma_v)$. This solution is called a _Kalman Filter_ and is a continuous limit of the discrete time Kalman Filter one might see in a course on graphical models.

The optimal LQG solution takes the estimate of the Kalman Filter, $\hat{x}_t$, and sets the control signal to be

$$
	u_t = -K\hat{x}_t\,.
$$

Here, $K$ is gain matrix that would be used to solve the LQR problem with data $(A,B,Q,R)$. That is, LQG performs optimal filtering to compute the best state estimate, and then computes a feedback policy as if this estimate was a noiseless measurement of the state. That this turns out to be optimal is really quite amazing as it decouples the process of designing an optimal filter from designing an optimal controller. This decoupling where we treat the output of our state estimator as the true state is an example of _certainty equivalence_, the umbrella term for using point estimates of stochastic quantities as if they were the correct value. Though certainty equivalent control may be suboptimal in general, it remains ubiquitous as it enables simplicity and modularity in control design. LQG highlights a particular scenario where certainty equivalent control leads to misplaced optimism about robustness.

We saw in the previous post that LQR had this amazing robustness property: even if you optimize with the wrong model, you'll still probably be OK. Is the same true about LQG? What are the guaranteed stability margins for LQG regulators? The answer was succinctly summed up in the [abstract of a 1978 paper by John Doyle](https://ieeexplore.ieee.org/document/1101812): "There are none."

{: .center}
![There Are None](/assets/there_are_none.png){:width="400px"}

What goes wrong? It turns out that Doyle came up with a simple counterexample, that I'm going to simplify even further for the purpose of discussion. Before presenting the example, let's first dive into _why_ LQG is likely less robust than LQR. Let's assume that the true dynamics obeys the ODE:

$$
	\dot{x}_t = Ax_t + B_\star u_t + w_t \,,
$$

though we computed the optimal controller with the matrix $B$. Define an error signal, $e_t = x_t - \hat{x}_t$, that measures the current deviation between the actual state and the estimate. Then, using the fact that $u_t = -K \hat{x}_t$, we get the closed loop dynamics

$$
\small
\frac{d}{dt} \begin{bmatrix}
		\hat{x}_t\\
		e_t
	\end{bmatrix} = \begin{bmatrix} A-BK & LC\\ (B-B_\star) K & A-LC \end{bmatrix}\begin{bmatrix}
		\hat{x}_t\\
		e_t
	\end{bmatrix} +
	\begin{bmatrix} Lv_t\\ w_t-Lv_t \end{bmatrix}\,.
$$

When $B=B_\star$, the bottom left block is equal to zero. The system is then stable provided $A-BK$ and $A-LC$. However, when this block is nonzero, small perturbations can make the matrix unstable. For intuition, consider the matrix

$$
 \begin{bmatrix} -1 & 200\\ 0 & -2 \end{bmatrix}\,.
$$

The eigenvalues of this matrix are $-1$ and $-2$, so the matrix is clearly stable. But the matrix

$$
 \begin{bmatrix} -1 & 200\\ t & -2 \end{bmatrix}
$$

has an eigenvalue greater than zero if $t>0.01$. So a tiny perturbation significantly shifts the eigenvalues and makes the matrix unstable.

Similar things happen in LQG. In Doyle's example he uses the problem instance:

$$
	A = \begin{bmatrix} 1 & 1\\ 0 & 1\end{bmatrix} \,,~~~ B = \begin{bmatrix} 0\\1 \end{bmatrix}\,, ~~~ C= \begin{bmatrix} 1 & 0\end{bmatrix}
$$

$$
	Q = \begin{bmatrix} 5 & 5 \\ 5 & 5 \end{bmatrix} \,, ~~~ R = 1
$$

$$
	\mathbb{E}\left[w_t w_t^\top\right]=\begin{bmatrix} 1 & 1 \\ 1 & 1\end{bmatrix} \,,~~~ \mathbb{E}\left[v_t^2\right]=\sigma^2
$$

The open loop system here is unstable, having two eigenvalues at $1$. We can stabilize the system only by modifying the second state. The state disturbance is aligned along the $[1;1]$ direction, and the state cost only penalizes states aligned with this disturbance. So the goal is simply to remove as much signal as possible in the $[1;1]$ direction without using too much control authority. We only are able to measure the first component of the state, and this measurement is corrupted by Gaussian noise.

What does the optimal policy look like? Perhaps unsurprisingly, it focuses all of its energy on ensuring that there is little state signal along the disturbance direction. The optimal $K$ and $L$ matrices are

$$
	K = \begin{bmatrix} 5 & 5 \end{bmatrix}\,,~~~L=\begin{bmatrix} d\\ d \end{bmatrix}\,,~~~d:=2+\sqrt{4+\sigma^{-2}}\,.
$$

Now what happens when we have model mismatch? If we set $B_\star=tB$ and use the formula for the closed loop above, we see that closed loop state transition matrix is

$$
\begin{bmatrix}
1 & 1 & d & 0\\
    -5 & -4  & d & 0\\
    0 & 0 &1-d &1\\
    4(1-t) & 4(1-t) & -d &1
    \end{bmatrix}\,.
$$

It's straight forward to check that when $t=1$ (i.e., no model mismatch), the matrices $A-BK$ and $A-LC$ have their eigenvalues in the right half plane. For the full closed loop matrix, computing the eigenvalues themselves is a pain, but we can prove instability by looking at the characteristic polynomial. For a matrix to have all of its eigenvalues in the right half plane, its characteristic polynomial necessarily must have all positive coefficients. If we look at the linear term in the polynomial, it shows that we must have

$$
	t < 1 + \frac{1}{5d}
$$

if we'd like any hope of having a stable system. Hence, we can guarantee that this closed loop system is unstable if $t\geq 1+\sigma$. This is a very conservative condition, and we could get a tighter bound if we'd like, but it's good enough to reveal some paradoxical properties of LQG. One that stands out to me is that if we build a sensor that gives us a better and better measurement, our system becomes more and more fragile to perturbation and model mismatch. For machine learning scientists, this seems to go against all of our training: how can a system become _less_ robust if we improve our sensing and estimation?

When the sensor noise gets small, the optimal Kalman Filter is more aggressive. It quickly damps any errors in the disturbance direction $[1;1]$. However, as $d$ increases, we find that the vector $[0;1]$ gets less and less damping in the error signal. When $t \neq 1$, this undamped component of the error is fed errors from the state estimate $\hat{x}$, and these errors compound each other. Since we spend so much time focusing on our control along the direction of the injected state noise, we become highly susceptible to errors in a different direction and these are the exact errors that occur when there is a gain mismatch between the model and reality.

This cautionary tale from LQG has many takeaways. It highlights that noiseless state measurement is dangerous modeling assumption. Most of the papers I read in reinforcement learning consider MDPs where we get perfect state measurement. Building an entire field around optimal actions with perfect state observation builds too much optimism. Any realistic scenario is going to have partial state observation, and such problems are much thornier.

A second lesson that I think is a bit less well appreciated is that optimal control can't be naturally robust to every perturbation. In Doyle's example, the Kalman Filter damps less signal unaligned with the disturbance as our sensor improves. The model trusts our confidence that we only care about a particular type of disturbances. The optimal controller over compensates, as overcompensation is more optimal in the model we write down. In the next post, I'm going to return to discrete time to highlight how difficult it can be to build something truly robust in the optimal control paradigm.

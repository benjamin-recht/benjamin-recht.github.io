---
layout:     post
title:      "Gain Margins"
date:       2020-07-08 0:00:00
summary:    "A first look at robustness in optimal control, and how sometimes you can get robustness without explicitly modeling it."
author:     Ben Recht
visible:    false
blurb: 		  false
---

I want to dive into some classic results in robust control and try to relate them to our current data-driven mindset. I'm going to try to do this in a modern way, avoiding any frequency domain analyses.

Suppose you want to solve some optimal control problem: you spend time modeling the dynamics of your system, how it responds to stimuli, and which objectives you'd like to maximize and constraints you must adhere to. Each of these modeling decisions explicitly encodes both your beliefs about reality and your mental criteria of success and failure. *Robustness* aims to quantify the effects of oversight on your systems behavior. Perhaps your model wasn't accurate enough, or perhaps you forgot to include some constraint in your objective. What are the downstream consequences?

In the seventies, it was believed that optimization-based frameworks for control had "natural robustness." The solutions of optimal control problems were often robust to phenomena not explicitly modeled by the engineer. As a simple example: suppose you have an incorrect model of the dynamical system you are trying to steer. How accurate do you need to be in order for this policy to be reasonably successful?

To focus in on this, let's study the continuous-time linear quadratic regulator (LQR). I know I've been arguing that we should  be moving away from LQR in order to understand the broader challenges in learning and control, but the LQR baseline has so many lessons to teach us. Please humor me again for a few additional reasons: First, most of the history I want to tell arises from studying continuous-time LQR in the 1970s. It's worth understanding that history with a modern perspective. Second, LQR does admit elegant closed form formulae that are helpful for pedagogy, and they are particularly nice in continuous time.

## LQR in Continuous Time

Suppose we have a dynamical system that we model as an ODE:

$$
	\dot{x}_t = Ax_t + Bu_t\,.
$$

Here, as always, $x_t$ is the state, $u_t$ is the control input signal, and $A$ and $B$ are matrices of appropriate dimensions. The goal of the continuous-time LQR problem is to minimize the cost functional

$$
J_{\text{LQR}}=\int_{0}^{\infty} (x_t^\top Qx_t + u_t^\top Ru_t) dt
$$

over all possible control inputs $u_t$. Let's assume for simplicity that $Q$ is a positive semidefinite matrix and $R$ is positive definite.

The optimal LQR policy is *static state feedback*: there is some matrix $K$ such that

$$
	u_t = -Kx_t
$$

for all time. $K$ has a closed form solution that can be found by solving a *continuous algebraic Riccatti equation* (CARE) for a matrix $P$:

$$
	A^\top P + PA - PBR^{-1}B^\top P + Q = 0\,,
$$

and then setting

$$
	K = R^{-1}B^\top P\,.
$$

Importantly, we take the solution of the CARE where $P$ that is positive definite. It's easy to show that if a positive definite solution of the CARE exists, then it is optimal for continuous time LQR. There are a variety of ways to prove this condition is sufficient, one could appeal to dynamic programming arguments in continuous time. A simple argument I like uses the quadratic structure of LQR to derive the necessity of the CARE solution. (I found this argument in [Joao Hespansha's book](https://www.ece.ucsb.edu/~hespanha/linearsystems/)).

Regardless, showing a positive definite CARE solution exists takes considerably more work. It suffices to assume that the pair $(A,B)$ is controllable and the pair $(Q,A)$ is detectable. But proving these conditions are sufficient requires a lot of manipulation of linear algebra, and I don't think I could cleanly reduce this proof to a blog post. I mention this just to reiterate that while LQR is definitely the simplest problem to study, even analyzing this in continuous time on an infinite time horizon is nontrivial. LQR is not really "easy" to analyze. It's merely the easiest problem in a space of rather hard problems.

## Gain margins

Let's now turn to robustness. Suppose there is a mismatch between our modeled dynamics and reality. For example, what if the actual system is

$$
	\dot{x}_t = Ax_t + B_\star u_t\,.
$$

for some matrix $B_\star$. Such situations happen all the time in control. For example, in robotics, we can send a signal "u" to the joint of some robot. This would be some voltage that would need to be linearly transformed into some torque by a motor. It requires a good deal of calibration to make sure that the output of the motor is precisely the force dictated by the voltage output from our controller. Is there a way to guarantee some leeway in our control signals?

An attractive feature of LQR is that we can quantify precisely how much slack we have directly from the CARE solution. We can use the solution of the CARE to build a *Lyapunov function* to guarantee stability of the system. Recall that a Lyapunov function is a function $V$ that maps states to real numbers, is nonnegative everywhere, is equal to $0$ only when $x=0$, and whose value is strictly decreasing along any trajectory of a dynamical system. In equations:

$$
	V(x)\geq 0\,,~~~~V(x)=0~~\text{iff}~~x=0\,,~~~~\dot{V} <0\,.
$$

If you have a Lyapunov function, then all trajectories must converge to $x=0$: if you are at any nonzero state, the value of $V$ will decrease. If you are at $0$, then you will be at a global minimum of $V$ and hence can't move to any other state.

For LQR, let $P$ be the solution of the CARE and let's posit that $V(x) = x^\top  P x$ is a Lyapunov function. Certainly, since $P$ is positive definite, we have $V(x)\geq 0$ and $V(x)=0$ if and only if $x=0$. To prove that the derivative of the Lyapunov function is negative, we can first compute the derivative:

$$
\frac{d}{dt} x_t^\top  P x_t = x_t^\top \left\{(A-B_\star K)^\top P + P(A-B_\star K)  \right\}x_t\,.
$$

Note that it is sufficient to show that  $(A-B_\star K)^\top P + P(A-B_\star K)$ is a negative definite matrix as this would prove that the derivative is negative for all nonzero $x_t$. To prove that this expression is negative definite requires only algebra. Using the definition of $K$ and the fact that $P$ solves the CARE gives the following chain of equalities:

$$
\begin{aligned}
	&(A-B_\star K)^\top P + P(A-B_\star K)  \\
  &= A^\top P + PA - K^\top B_\star^\top  P - P B_\star K\\
	&=PBR^{-1}B^\top P - Q - K^\top B_\star^\top  P - P B_\star K\\
	&=PBR^{-1}B^\top P - Q - PBR^{-1}B_\star^\top  P - P B_\star R^{-1} B^\top P\\
	&=P(B-B_\star)R^{-1}(B-B_\star)^\top P - PB_\star R^{-1} B_\star^\top  P - Q
\end{aligned}
$$

Here, the first equality is simply expanding the matrix product. The second equation uses the fact that $P$ is a solution to the CARE. The third equality uses the definition of $K$. The final equation is an algebraic rearrangement.

With this final expression, we can cook up a huge number of conditions under which we get "robustness for free." First, note that if $B=B_\star$, then since $R$ is positive definite and $Q$ is positive semidefinite, the entire expression is negative definite, and hence we have proven the system is stable.

Second, there is a famous result that LQR has "large gain margins." The gain margin of a control system is an interval $(t_0,t_1)$ such that for all $t$ in this interval, our control system is stable with the controller $tK$. Another way of thinking about the gain margin is to assume that $B_\star = tB$, and to find the largest interval such that the system $(A,B_\star)$ is stabilized by a control policy $K$. For LQR, there are very large margins: if we plug in the identity $B_\star=tB$, we find that $x^\top  P x$ is a Lyapunov function provided that $t \in (\tfrac{1}{2},\infty)$. LQR control turns out to be robust to a wide range of perturbations to the matrix $B$. Intuitively, it makes sense that if we would like to drive a signal to zero and have more control authority than we anticipated that our policy will still drive the system to zero. This is the range of $t \in [1,\infty)$. The other part of the interval is perhaps more interesting: for the LQR problem, even if we only have half of the control authority we had planned for, we still will successfully stabilize our system from any initial condition.

In discrete time, you can derive similar formulae with essentially the same argument. Unfortunately, the expressions are not as elegant. Also, note that you cannot expect infinite gain margins in discrete time. In continuous time a differential equation $\dot{x}_t = M x_t$ is stable if all of the eigenvalues of $M$ have negative real parts. In discrete time, you need all of the eigenvalues to have magnitude less than $1$. For almost any random set triple $(A,B,K)$, $A-t B K$ is going to have large eigenvalues for $t$ large enough. Nonetheless, even if the expressions aren't as clean, you can certainly derive analogous conditions as to which errors are tolerable.

There are a variety of other conditions that can be derived from our matrix expression. Most generally, the control system will be stable provided that

$$
	(B-B_\star)R^{-1}(B-B_\star)^\top  \prec B_\star R^{-1} B_\star^\top \,.
$$

The LQR gain margins fall out naturally from this expression when we assume $B_\star = t B$. However, we can guarantee much more general robustness using this inequality. For example, if we assume that $B_\star = BM$ for some square matrix $M$, then $K$ stabilizes the pair $(A,B_\star)$ if all of the eigenvalues of $M+M^\top $ are greater than $1$.

Perhaps more in line with what we do in machine learning, suppose we are able to collect a lot of data, do some uncertainty quantification, and guarantee a bound $\|B-B_\star\|_2<\epsilon$. Then as long as

$$
	\epsilon \leq \lambda_\text{min}(R)\lambda_\text{min}\left(P^{-1} Q P^{-1}\right)
$$

we will be guaranteed stable execution. This expression depends strongly on the matrices $P$, $Q$, and $R$, so it has a different flavor of the infinite gain margin conditions which held irrespective of the dynamics or the cost. Moreover, if $P$ has large eigenvalues, then we are only able to guarantee safe execution for small perturbations to $B$. This foreshadows issues I'll dive into in later posts about robustness. I want to flag here that these calculations reveal some fragilities of LQR: While the controller is always robust to perturbations along the direction of the matrix $B$, you can construct examples where the system is highly sensitive to tiny perturbations orthogonal to $B$. I'll return in the next post to start to unpack how optimal control has some natural robustness, but it has natural fragility as well.

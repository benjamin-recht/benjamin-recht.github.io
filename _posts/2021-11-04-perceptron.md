---
layout:     post
title:      "The Perceptron as a prototype for machine learning theory."
date:       2021-11-04 0:00:00
summary:    "So many of our modern ideas about machine learning theory came from studying the perceptron. In fact, it's not clear that we've really had any new ideas since."
author:     Ben Recht
visible:    false
blurb: 		  true
---

Just as many of the algorithms and community practices of machine learning were invented in the late 50s and early 60s, the foundations of machine learning theory were also established during this time. Many of the analyses of this period were strikingly simple, had surprisingly precise constants, and provided prescient guidelines for contemporary machine learning practice. Here, I’ll summarize the study of the Perceptron, highlighting both its algorithmic and statistical analyses, and using it as a prototype to illustrate further how prediction deviates from the umbrella of classical statistics.

Let’s begin with a classification problem where each individual from some population has a feature vector $x$ and an associated binary label $y$ that we take as valued $\pm 1$ for notational convenience. The goal of the Perceptron is to find a linear separator such that $w^T x>0$ for when $y=1$ and $w^T x<0$ when $y=-1$. We can write this compactly as saying that we want to find a $w$ for which $y w^T x >0$ for as many individuals in the population as possible.

The Perceptron algorithm is wonderfully simple. The Perceptron inputs an example, checks if it makes the correct classification. If yes, it does nothing and proceeds to the next example. If no, the decision boundary is nudged in the direction of classifying the example correctly next time.

**Perceptron**

* Start from the initial solution $w_0=0$
* At each step $t=0,1,2,...$:
  - Select an individual from the population and look up their attributes: (x_t,y_t).
  - Case 1: If $y_t\langle w_t, x_t\rangle < 0$, put
$$
w_{t+1} = w_t + y_t x_t  
$$
  - Case 2: Otherwise put $w_{t+1} = w_t$.

If the examples were selected at random, machine learners would recognize this algorithm as an instance of stochastic gradient descent, still the most ubiquitous way to train classifiers whether they be deep or shallow. Stochastic gradient descent minimizes sums of functions

$$
    f(w) = \frac{1}{N} \sum_{i=1}^N \mathit{loss}( f(x_i; w) , y_i)
$$

with the update

$$
    w_{t+1} = w_t - \alpha_t \nabla_w \mathit{loss}( f(x_t; w_t) , y_t)\,.
$$

The Perceptron is stochastic gradient descent with $\alpha_t=1$, $f(x;w) = \langle w,x \rangle$, and loss function $\mathit{loss}(\hat{y},y) = \max(-\hat{y} y, 0)$.

Stochastic gradient methods were invented a few years before the Perceptron. And the relations between these methods were noted by the mid-60s (Vapnik discusses the history in Chapter 1.11 of [_The Nature of Statistical Learning Theory_](https://link.springer.com/book/10.1007/978-1-4757-3264-1)).

While we might be tempted to use a standard stochastic gradient analysis to understand the optimization properties of the Perceptron, it turns out that a more rarified proof technique will not only bound errors in optimization but also in generalization. Optimization is concerned with errors on a training data set. Generalization is concerned with errors on data we haven’t seen. The analysis from the 1960s links these two by first understanding the dynamics of the algorithm.

[A celebrated result by Al Novikoff](https://cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf) showed that under reasonable conditions the algorithm makes a bounded number of updates no matter how large the sample size. Novikoff’s result is typically referred to as a _mistake bound_ as it bounds the number of total misclassifications made when running the Perceptron on some data set. The key assumption in Novikoff’s argument is that the positive and negative examples are cleanly separated by a linear function. People often dismiss the Perceptron because of this _separability_ assumption. But for any finite data set, can always add features and end up with a linearly separable problem. And if we add enough features, we’ll usually be separable no matter how many points we have.

This has been the trend in modern machine learning: don’t fear big models and don’t fear getting zero errors on your training set. This is no different than what was being proposed in the Perceptron. In fact [Aizerman, Braverman, and Roeznoer](https://cs.uwaterloo.ca/~y328yu/classics/kernel.pdf) recognized the power of such overparameterization, and extended Novikoff’s argument to “potential functions” that we now recognize as functions belonging to an infinite dimensional Reproducing Kernel Hilbert Space.

To state Novikoff’s result, we make the following assumptions: First, we assume as input a set of examples $S$. We assume every data point has norm at most $R(S)$ and that there exists a hyperplane that correctly classifies all of the data points and is of distance at least $\gamma(S)$ from every data point. This second assumption is called a _margin condition_ that quantifies how separated the given data is. With these assumptions, Novikoff proved the Perceptron algorithm makes at most

$$
{\small
\frac{R(S)^2}{\gamma(S)^{2}}
}
$$

mistakes when run on $S$. No matter what the ordering of the data points in $S$, the algorithm makes a bounded number of errors.

The algorithmic analysis of Novikoff has many implications. First, if the data is separable, we can conclude that the Perceptron will terminate if it is run over the data set several times. This is because we can think of $k$ epochs of the Perceptron as running on the union of $k$ distinct copies of $S$, and the Perceptron eventually stops updating when run on this data set. Hence, the mistake bound tells us something particular about optimization: the Perceptron converges to a solution with zero training errors and hence a global minimizer of the empirical risk.

Second, we can think of the Perceptron algorithm as an _online learning algorithm_. We need not assume anything distributional about the sequence $S$. We can instead think about how long it takes for the Perceptron to converge to a solution that would have been as good as this optimal hyperplane. We can quantify this convergence by measuring the _regret_, equal to

$$
    \mathcal{R}_T = \sum_{t=1}^T \mathrm{error}(w_t, (x_t,y_t))\,.
$$

That is, the regret counts how frequently the classifier at step $t$ misclassifies the next example in the sequence. Novikoff’s argument shows that, if a sequence is perfectly classifiable, then the accrued regret is a constant that does not scale with T.

A third, less well known application of Novikoff’s bound is as a building block for a  _generalization bound_. A generalization bound estimates the probability of making an error on a new example given that the new example is sampled from the same population as the data thus far sceen. To state the generalization bound for the Perceptron, I _now_ need to return to statistics. Generalization theory concerns statistical validity, and hence we need to define some notion of sampling from the population. I will use the same sampling model I have been using in this blog series. Rather than assuming a statistical model of the population, I will assume we have some population of data from which we can uniformly sample. Our training data will consist of $n$ points sampled uniformly from this population: $S=\{(x_1,y_1)\ldots, (x_n,y_n) \}$.

We know that the Perceptron will find a good linear predictor for the training data if it exists. What we now show is that this predictor also works on new data sampled uniformly from the same population.

To analyze what happens on new data, I will employ an elegant argument I learned from Sasha Rakhlin. This argument appears in a book on Learning Theory by Vapnik and Chervonenkis from 1974, which, to my knowledge, is only available in Russian. Sasha also believes this argument is considerably older as [Aizermann and company were making similar “online to batch” constructions in the 1960s](http://www.mit.edu/~rakhlin/papers/chervonenkis_chapter.pdf). The proof here leverages the assumption that the data are sampled in such a way that they are identically distributed, so we can swap the roles of training and test examples in the analysis. It foreshadows later studies of stability and generalization that would be revisited decades later.

**Theorem** _Let $w(S)$ be the output of the Perceptron on a dataset $S$ after running until the hyperplane makes no more mistakes on $S$. Let $S_n$ denote a training set of $n$ samples uniformly at random from some population. And let $(x,y)$ be an additional independent uniform sample from the same population. Then, the probability of making a mistake on $(x,y)$ is bounded as_

$$
    \Pr[y w(S_n)^T x < 0] \leq \frac{1}{n+1} {\mathbb{E}}_{S_{n+1}}\left[ \frac{R(S_{n+1})^2}{\gamma(S_{n+1})^2} \right]\,.
$$

To prove the theorem, define the "leave-one-out set" to be the set where we drop $(x_k,y_k)$:

$$
{\small
S^{-k}=\{(x_1,y_1),\dots,(x_{k-1},y_{k-1}),(x_{k+1},y_{k+1}),...,(x_{n+1},y_{n+1})\}\,.
}
$$

With this notation, since all of the data are sampled identically and independently, we can rewrite the probability of a mistake on the final data point as the expectation of the leave-one-out error

$$
{\small
\Pr[x w(S_n)^T y < 0]
= \frac1{n+1}\sum_{k=1}^{n+1} \mathbb{E}[\mathbb{1}\{y_k w(S^{-k})^T x_k < 0\}]\,.
}
$$

Novikoff’s mistake bound asserts the Perceptron makes at most

$$
{\small
m=\tfrac{R(S_{n+1})^2}{\gamma(S_{n+1})^2}}
$$

mistakes when run on the entire sequence $S_{n+1}$. Let $I=\{i_1,\dots,i_m\}$ denote the indices on which the algorithm makes a mistake in any of its cycles over the data. If $k$ is not in $I$, the output of the algorithm remains the same after we remove the $k$-th sample from the sequence. It follows that such $k \in S_{n+1}\setminus I$ satisfy  $y_k w(S^{-k})x_k \geq 0$ and therefore do not contribute to the right hand side of the summation. The other terms can at most contribute $1$ to the summation.
Hence,

$$
\Pr[Y w(S_n)^T X < 1] \le \frac{\mathbb{E}[m]}{n+1}\,,
$$

which is what we wanted to prove.

What’s most remarkable to me about this argument is that there are no numerical constants or logarithms. The generalization error is perfectly quantified by a simple formula of $R$, $\gamma$, and $n$. There are a variety of other arguments that get the $\tilde{O}(R/(n\gamma))$ scaling with far more complex arguments and large constants and logarithmic terms. For example, one can show that the set of hyperplanes in Euclidean space with norm bounded by $\gamma^{-1}$ has [VC dimension $R/\gamma$](https://www.wiley.com/en-us/Statistical+Learning+Theory-p-9780471030034). Similarly, a [Rademacher complexity argument will achieve a similar scaling](https://www.jmlr.org/papers/volume3/bartlett02a/bartlett02a.pdf). These arguments apply to far more algorithms than the Perceptron, but it’s frustrating how this simple algorithm gets such a tight bound with such a short argument whereas analyzing more powerful algorithms often takes pages of derivations.

It’s remarkable that this $R/(n\gamma)$ bound was worked out in the 1960s and was optimal for linear classification theory. We’ve made more progress in machine learning theory since then, but it’s not always at the front of our minds just how long ago we had established our modern learning theory framework.

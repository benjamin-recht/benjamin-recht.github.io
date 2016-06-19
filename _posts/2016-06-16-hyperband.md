---
layout:     post
title:      Hyperband
date:       2016-06-23 7:00:00
summary:    Early stopping and successive halving for speeding up random search
author:     Ben Recht
visible:    false
---

*Ed. Note: this post is in my voice, but it was co-written with [Kevin Jamieson](http://people.eecs.berkeley.edu/~kjamieson/about.html).  Kevin provided all of the awesome plots, and has a [great tutorial ](http://kevin-jamieson.com/hyperband_demo/short.html) for implementing the algorithm I'll describe in this post*

In the last post, I argued that random search is a competitive method for black-box parameter tuning in machine learning.  This is actually great news!  Random search is a incredibly simple algorithm, and if it is universally powerful, we can devote our time to optimizing random search for the particularities of our workloads, rather than worrying about baking off hundreds of new algorithmic ideas.

In some very nice recent work, Lisha Li (UCLA), Giulia DeSalvo (NYU), Afshin Rostamizadeh (Google), Ameet Talwalkar (UCLA), and Kevin Jamieson, (AMP Lab, UC Berkeley) pursued a [very nice direction](http://arxiv.org/abs/1603.06560) in accelerating random search.  Their key insight is that most of the algorithms we run are iterative in machine learning, so if we are running a set of parameters, and the progress looks terrible, it might be a good idea to quit and just try a new set of hyperparameters.

One way to implement such a scheme called *successive halving*.  The idea successive halving is remarkably simple.  We first try out $N$ hyperparameter settings for some fixed amount of time $T$.  Then, we keep the $N/2$ best performing algorithms and run for time $2T$.  Repeating this procedure $\log_2(T)$ times, we end up with $N/K$ configurations run for $KT$ time.

The total amount of computation in each halving round is equal to $NT$, and there are $\log_2(K)$ total rounds.  If we restricted ourself to pure random search with the same computation budget where we required all of the settings to be run for $KT$ steps,  we would only be able to run $N \log_2(K)/K$ hyperparameter settings.  Thus, in the same amount of time, successive halving sees $K/log_2(K)$ more parameter configurations than pure random search!

Now, the problem here is that just because an parameter setting looks bad at the beginning of a run of SGD, doesn't meant that it won't be optimal at the end of the run.  We see this a lot when tuning learning rates and regularization parameters: slow learning rates and large-regularization are often poor for the first couple of epochs, but end up with the lowest test error after a hundred passes over the data.

A simple way to deal with this tradeoff between breadth and depth is to start the halving process later.  We could run $N/2$ parameter settings for time $2T$, then the top $N/4$ for time $4T$ and so on.  This adapted halving scheme allows slow learners to have more of a chance of surviving before being cut, but the total amount of time per halving round is still $N$ and the number of rounds is at most $\log(K)$.  Running multiple instances of successive halving with different halving times increases depth while narrowing depth.

Li *et al* provide a simple, automatic way to set all of these parameters and search strategies.  See Kevin's [project page](http://kevin-jamieson.com/hyperband_demo/short.html) for the 7 lines of python code that generates a set of successive halving rounds that maximizes the benefits of breadth-first vs depth-first search for successive halving.  The only parameters you need to provide to the code is the parameter $K$. $K$ here is simple the maximum time you want to run SGD for divided by the minimum time you'd be willing to check the error on the holdout.  That is, you should tell Kevin's python code what the minimum amount of time you'd like to run your model before checking against other models, and the maximum amount of time you'd ever be interested in running for.  In some sense, these parameters are more like constraints: there is some overhead with checking the process, and $T$ should be larger than this.  The maximum runtime is here because we all have deadlines.

Successive halving was inspired by an earlier heuristic by Evan Sparks and coauthors which showed the simple idea of killing iterative jobs based on early progress [worked really well in practice](https://amplab.cs.berkeley.edu/wp-content/uploads/2015/07/163-sparks.pdf).  It is adapted from a similar scheme in the
[stochastic Multi-armed bandits](http://jmlr.org/proceedings/papers/v28/karnin13.pdf) to the deterministic setting  with a maximum runtime. [The full paper](http://arxiv.org/abs/1603.06560) describes a number of extensions of the scheme for other machine learning workloads, many interesting theoretical guarantees, and implications for stochastic infinite-armed bandit problems (if you're into that sort of thing). Let's wrap up this blogpost with some empirical evidence that this algorithm actually works.

## Neural net experiments

Let's look at two image classification benchmarks: CIFAR-10 and the Street View House
Numbers (SVHN).  Both data sets contain 32 × 32 RGB images. Each dataset is
split into a training, validation, and test set: (1) CIFAR-10 has 40,000, 10,000, and 10,000 instances;
(2) SVHN has close to 600,000, 6,000, and 26,000 instances.

For the experts out there, the methods were all attempting to tune the basic [cuda-convnet model](https://code.google.com/p/cuda-convnet/), searching for the optimal learning rate, learning rate decay, l2 regularization parameters on different layers, and parameters of the response normalizations.  For CIFAR-10, the basic unit of time, $T$, was one-fifth of an epoch, and $K$ was 1500.  For SVHN, the basic unit of time was one one-hundredth of an epoch and $K$ was set to 3000.  The full details are described in the paper.  The plots below

{: .center}
![Comparison of methods on CIFAR-10](/assets/hyperband/cifar10-compare.png)
![Comparison of methods on SVHN](/assets/hyperband/svhn-compare.png)

These results are pretty shocking.  Successive halving finds a decent solution in a fraction of the time of the other methods.  It also finds the best solution over all. On SVHN, it finds the best solution in a third of the time of the other methods. And, again, the protocol is just 7 lines of python code.  This work suggests that a powerful way forward on hyperparameter tuning is to pursue more enhancements and optimizations of pure random search.

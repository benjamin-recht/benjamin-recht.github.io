---
layout:     post
title:      Bayesian Optimization and other bad ideas for hyperparameter optimization
date:       2016-06-16 7:00:00
summary:    Why do I have so many parameters?
author:     Ben Recht
visible:    false
---

*Ed. Note: this post is in my voice, but it was co-written with [Kevin Jamieson](http://people.eecs.berkeley.edu/~kjamieson/about.html).  Kevin provided all of the awesome plots too.*

It's all the rage in machine learning these days to build complex, deep pipelines with thousands of tunable parameters.  Now, I don't mean parameters that we learn by stochastic gradient descent.  But I mean architectural concerns, like the value of the regularization parameter, the size of a convolutional window, or the breadth of a spatio-temporal tower of attention.  Such parameters are typically referred to as *hyperparameters* to contrast against the parameters learned during training. These structural parameters are not learned, but rather descended upon by a lot of trial-and-error and fine tuning.  

Automating such hyperparameter tuning is one of the most holy grails of machine learning.  And people have tried for decades to devise algorithms that can quickly prune bad configurations and maximally overfit to the test set.  This problem is ridiculously hard, because the problems in question become mixed-integer, nonlinear, and nonconvex.  The default approach to the hyperparameter tuning problem is to resort to *black-box optimization* where one tries to find optimal settings by only receiving function values and not using much other auxiliary information about the optimization problem.

Black-box optimization is hard.  It's hard in the most awful senses of optimization.  Even when we restrict our attention to  continuous problems, black-box optimization is completely intractable in high dimensions. To guarantee that you are within a factor of two of optimality requires an exponential number of function evaluations.  Roughly the number of queries scales as $O(2^d)$ where $d$ is the dimension.  What's particularly terrible is that it easy to construct "needle-in-the-haystack" problems where this exponential complexity is real.  That is, where no algorithm will ever find a good solution.  Moreover, it is hard to construct an algorithm that outperforms random guessing on these problems.

## Bayesian inference to the rescue?

In recent years, I have heard that there has been a bit of a breakthrough for hyperparameter tuning based on Bayesian optimization.  Bayesian optimizers model the uncertainty of the performance of hyperparameters using
priors about the smoothness of the hyperparameter landscape.  When one tests a set of parameters, the uncertainty of the cost near that setting shrinks.  Bayesian optimization then tries to explore places where the uncertainty remains high and the prospects for a good solution look promising.  This certainly sounds like a sensible thing to try.

Indeed, there has been quite a lot of excitement about these methods, and there has been a lot of press about how well these methods work for tuning deep learning and other hard machine learning pipelines. However, [recent evidence](http://arxiv.org/abs/1603.06560) on a benchmark of over a hundred hyperparameter optimization datasets suggests that such enthusiasm really calls for much more scrutiny.  

The standard way these methods are evaluated in papers is by using rank plots.  Rank plots aggregate statistics across datasets for different methods as a function of time: at a particular time, the solver with the best setting gets one point, the algorithm in second place two points, and so forth.  Consider the following plots:

{: .center}
![Rank chart of various hyperparameter methods](/assets/hyperband/rank_chart.png)
![Bar plot comparing final test errors](/assets/hyperband/bar_plot_sample.png)

On the left, we show the rank chart for all algorithms and on the right, we show the actual achieved function values of the various algorithms.  The first plot represent the average score across 117 datasets collected by [Feurer et. al. NIPS 2015](http://papers.nips.cc/paper/5872-efficient-and-robust-automated-machine-learning) (lower is better).  For clarity, the second plot is for a subset of these data sets, but all of the data sets have nearly identical results.  We compare state-of-the-art Bayesian optimization methods SMAC and TPE to the method I suggested above: *random search* where we just try random parameter configurations and don't use any of the prior experiments to help pick the next setting.

What are the takeaways here?  While the rank plot seems to suggest that state-of-the-art Bayesian optimization methods SMAC and TPE resoundingly beat random search, the bar plot shows that they are achieving nearly identical test errors!  That is, SMAC and TPE are only a teensy bit better than random search.   Moreover, and more troubling, Bayesian optimization is completely outperformed by random search *run at twice the speed*.  That is, if you just set up two computers running random search, you beat all of the Bayesian methods.  

Why is random search so competitive?  This is just a consequence of the curse of dimensionality.  Imagine that your space of hyperparameters is the unit hypercube in some high dimensional space.  Just to get the Bayesian uncertainty to a reasonable state, one has to essentially test all of the corners, and this requires an exponential number of tests.  What's remarkable to me is that the early [theory](http://arxiv.org/abs/0912.3995) [papers](https://hal.inria.fr/hal-00654517/) on Bayesian optimization are very up front about this exponential scaling, but this [seems to be ignored](http://blog.sigopt.com/post/144221180573/evaluating-hyperparameter-optimization-strategies) by the current excitement in the Bayesian optimization community.

There are three very important takeaways here.  First, if you are planning on writing a paper on hyperparameter search, you should compare against random search!  If you want to be even more fair, you should compare against random search with twice the sampling budget of your algorithm.  Second, if you are reviewing a paper on hyperparameter optimization that does not compare to random search, you should immediately reject it.  And, third, as a community, we should be devoting a lot of time to accelerating  pure random search.  If we can speed up random search to try out more hyperparameter settings, perhaps we can do even better than just running parallel instances of random search.

In my next post, I’ll describe some [very nice recent work](http://arxiv.org/abs/1603.06560) by Lisha Li, Kevin Jamieson, Giulia DeSalvo, Afshin Rostamizadeh, and Ameet Talwalkar on accelerating random search for iterative algorithms common in machine learning workloads.  I will dive into the details of their method and show how it is very promising for quickly tuning hyperparameters.

## Hyperband

*Ed. Note: this post is in my voice, but it was co-written with [Kevin Jamieson](http://people.eecs.berkeley.edu/~kjamieson/about.html).  Kevin made all of the awesome plots, and has a [great tutorial ](http://kevin-jamieson.com/hyperband_demo/short.html) for implementing the algorithm I'll describe in this post*

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

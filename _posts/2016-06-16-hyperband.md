---
layout:     post
title:      Bayesian Optimization and other bad ideas for hyperparameter optimization
date:       2016-06-16 7:00:00
summary:    Why do I have so many parameters?
author:     Ben Recht
visible:    false
---

*Ed. Note: this post is in my voice, but it was co-written with [Kevin Jamieson](http://people.eecs.berkeley.edu/~kjamieson/about.html).  Kevin made all of the awesome plots too.*

It's all the rage in machine learning these days to build complex, deep pipelines with thousands of tunable parameters.  Now, I don't mean parameters that we learn by stochastic gradient descent.  But I mean architectural concerns, like the value of the regularization parameter, the size of a convolutional window, or the breadth of a spatio-temporal tower of attention.  Such parameters are typically referred to as *hyperparameters* to contrast against the parameters learned during training. These structural parameters are not learned, but rather descended upon by a lot of trial-and-error and fine tuning.  

Automating such hyperparameter tuning is one of the most holy grails of machine learning.  And people have tried for decades to devise algorithms that can quickly prune bad configurations and maximally overfit to the test set.  This problem is ridiculously hard, because the problems in question become mixed-integer, nonlinear, and nonconvex.  The default approach to the hyperparameter tuning problem is to resort to *black-box optimization* where one tries to find optimal settings by only receiving function values and not using much other auxiliary information about the optimization problem.

Black-box optimization is hard.  It's hard in the most awful senses of optimization.  Even when we restrict our attention to  continuous problems, black-box optimization is completely intractable in high dimensions. To guarantee that you are within a factor of two of optimality requires an exponential number of function evaluations.  Roughly the number of queries scales as $O(2^d)$ where $d$ is the dimension.  What's particularly terrible it is easy to construct "needle-in-the-haystack" problems where this exponential complexity is real.  That is, where no algorithm will ever find a good solution.  Moreover, it is hard to construct an algorithm that outperforms random guessing on these problems.

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

Why is random search so competitive?  This is just a consequence of the curse of dimensionality.  Imagine that your space of hyperparameters is the unit hypercube in some high dimensional space.  Just to get the Bayesian uncertainty to a reasonable state, one has to essentially test all of the corners, and this requires an exponential number of tests.  What's remarkable to me is that the early [theory](http://arxiv.org/abs/0912.3995) [papers](https://hal.inria.fr/hal-00654517/) on Bayesian optimization are very up front about this exponential scaling, but this seems to be ignored by the current excitement in the Bayesian optimization community.

There are three very important takeaways here.  First, if you are planning on writing a paper on hyperparameter search, you should compare against random search!  If you want to be even more fair, you should compare against random search with twice the sampling budget of your algorithm.  Second, if you are reviewing a paper on hyperparameter optimization that does not compare to random search, you should immediately reject it.  And, third, as a community, we should be devoting a lot of time to accelerating  pure random search.  If we can speed up random search to try out more hyperparameter settings, perhaps we can do even better than just running parallel instances of random search.

In my next post, I'll describe some very nice recent work by Lisha Li (UCLA), Giulia DeSalvo (NYU), Afshin Rostamizadeh (Google), Ameet Talwalkar (UCLA), and Kevin Jamieson, (AMP Lab, UC Berkeley) on accelerating random search for iterative algorithms common in machine learning workloads.  I will dive into the details of their method and show how it is very promising for quickly tuning hyperparameters.

## Hyperband

*Ed. Note: this post is in my voice, but it was co-written with [Kevin Jamieson](http://people.eecs.berkeley.edu/~kjamieson/about.html).  Kevin made all of the awesome plots, and has a [great tutorial ](http://kevin-jamieson.com/hyperband_demo/short.html) for implementing the algorithm I'll describe in this post*

In the last post, I argued that

In some very nice recent work, Lisha Li (UCLA), Giulia DeSalvo (NYU), Afshin Rostamizadeh (Google), Ameet Talwalkar (UCLA), and Kevin Jamieson, (AMP Lab, UC Berkeley) pursued a very nice direction in accelerating random search.  Their key insight is that most of the algorithms we run are iterative in machine learning, so if we are running a set of parameters, and the progress looks terrible, it might be a good idea to quit and just try a new set of hyperparameters.

One way to beat this is a scheme called *successive halving*.   xxx Sparks and Talwakar xxx.  Who else does successive halving?  Stochastic bandit literature.  The idea of successive halving is remarkably simple.  We'd try out $N$ hyperparameter settings for some fixed amount of time $T$.  Then, we keep the $N/2$ best performing algorithms and run for time $2T$.  Repeating this procedure $\log_2(T)$ times, we end up with $N/K$ configurations run for $KT$ time.

The total amount of computation in each halving round is equal to $N$. There are $\log_2(K)$ total rounds.  If we restricted ourself to the serial setting with the same computation budget,  we would be be able to run $N \log_2(K)/K$ hyperparameter settings for $T$ epochs each.  Thus, in the same amount of time, successive halving sees $K/log_2(K)$ more parameter configurations than pure random search!

Note that I could have used a different halving parameter $\eta$, and then the gap would be $K/\log_\eta(K)$.

Now, the problem here is that just because an algorithm looks bad at the beginning, doesn't meant that it might be optimal at the end of the run.  A particular example of this is setting the learning rate is stochastic gradient descent.  Small learning rates look worse than large ones in the early iterations, but it is often the case that a small learning rate leads to the best model in the end.

A simple way to deal with this tradeoff between breadth and depth is to start the halving process later.  We could run $N/2$ parameter settings for time $2T$, then the top $N/4$ for time $4T$ and so on.  This adapted halving scheme allows slow learners to have more of a chance of surviving before being cut, but the total amount of time per halving round is still $N$ and the number of rounds is at most $\log(K)$.  Running multiple instances of successive halving with different halving times increases depth while narrowing depth.

The parameters you have to choose are simply $T$ and $K$. That is, you should tell Kevin's python code what the minimum amount of time you'd like to run your model before checking against other models, and the maximum amount of time you'd ever be interested in running for.  In some sense, these parameters are more like constraints: there is some overhead with checking the process, and $T$ should be larger than this.  $K$ is here just because we all have deadlines.

xxx Cite Kevin's post here. xxx

[The paper](http://arxiv.org/abs/1603.06560) describes a number of extensions, theoretical guarantees, and implications for stochastic infinite-armed bandit problems (if you're into that sort of thing). But let's wrap up this blogpost with some empirical evidence that this algorithm actually works.

Extensions: dataset subsampling, cool results on bandits

## Neural net experiments

We considered three image classification datasets: CIFAR-10, Street View House
Numbers (SVHN), and rotated MNIST with background images (MRBI). CIFAR-10 and
SVHN contain 32 × 32 RGB images. Each dataset is
split into a training, validation, and test set: (1) CIFAR-10 has 40,000, 10,000, and 10,000 instances;
(2) SVHN has close to 600,000, 6,000, and 26,000 instances; For all datasets, the only preprocessing
performed on the raw images was demeaning.

learning rate, learning rate decay, l2 regularization parameters on different layers, parameters of the response normalizations

For CIFAR-10, the basic unit of time, $T$, was one-fifth of an epoch, and $K$ was 1500.  For SVHN, the basic unit of time was one one-hundredth of an epoch and $K$ was set to 3000.  The full details are described in the paper.

{: .center}
![Comparison of methods on CIFAR-10](/assets/hyperband/cifar10-compare.png)
![Comparison of methods on SVHN](/assets/hyperband/svhn-compare.png)

xxx talk about it.

%%%%

Typically, in a rather shady fashion, these parameters are tuned to minimize the test error on a hold-out set that is queried in parallel billions of times by eager grad students.  But, for the purpose of this post, I'm going to sweep that gross insult against statistics under the rug.


Bayesian optimization methods are difficult to parallelize as new configuration settings are chosen by fitting a model to the previously run experiments.

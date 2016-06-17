---
layout:     post
title:      Bayesian Optimization and other bad ideas for hyperparameter optimization
date:       2016-06-16 7:00:00
summary:    Why do I have so many parameters?
author:     Ben Recht
visible:    false
---


### Joint post with Kevin Jamieson

It's all the rage in machine learning these days to build complex, deep pipelines with thousands of tunable parameters.  Now, I don't mean parameters that we learn by stochastic gradient descent.  But I mean architectural concerns, like the value of the regularization parameter, the size of a convolutional window, or the breadth of a spatio-temporal tower of attention.  Such parameters are typically referred to as *hyperparameters* to contrast against the parameters learned during training. These structural parameters are not learned, but rather descended upon by a lot of trial-and-error and fine tuning.

Automating such hyperparameter tuning is one of the most holy grails of machine learning.  And people have tried for decades to devise algorithms that can quickly prune bad configurations and maximally overfitting on the test set.  In recent years, parameter search in machine learning has been dominated by Bayesian Optimization methods.  However, [recent evidence](http://arxiv.org/abs/1603.06560) on a benchmark of over a hundred hyperparameter optimization datasets suggests that such enthusiasm may call for increased scrutiny.  

Rank plots aggregate statistics across datasets for different methods as a function of time: first place gets one point, second place two points, and so forth.  Consider the following plots:

{: .center}
![Rank chart of various hyperparameter methods](/assets/hyperband/rank_chart.png)
![Bar plot comparing final test errors](/assets/hyperband/rank_chart.png)

On the left, we show the rank chart for all algorithms and on the right, we show the actual rankings of the various algorithms.  These plots represent the average score across 117 datasets collected by [Feurer et. al. NIPS 2015](http://papers.nips.cc/paper/5872-efficient-and-robust-automated-machine-learning) (lower is better).

 While the rank plot suggests that state-of-the-art Bayesian optimization methods SMAC and TPE resoundingly beat random search, note that they are achieving nearly identical test errors!  Moreover, and more troubling, Bayesean optimization is completely outperformed by random *run at twice the speed*.  That is, if you just set up two computers running random search, you beat all of the Bayesean methods.  Moreover, Bayesean methods are difficult to parallelize as new configuration settings are chosen by fitting a model to the previously run experiments.

 There are two very important takeaways here.  First, if you are planning on writing a paper on hyperparameter search, you should compare against random search!  Second, if you are reviewing a paper on hyperparameter optimization that does not compare to random search, you should immediately reject it.  And, finally, as a community, we should be devoting a lot of time to accelerating up pure random search.  If we can speed up random search to try out more hyperparameter settings, perhaps we can do even better than just running parallel instances of random search.

## Hyperband

In some very nice recent work, Lisha Li (UCLA), Giulia DeSalvo (NYU), Afshin Rostamizadeh (Google), Ameet Talwalkar (UCLA), and Kevin Jamieson, (AMP Lab, UC Berkeley) pursued a very nice direction in accelerating random search.  Their key insight is that most of the algorithms we run are iterative in machine learning, so if we are running a set of parameters, and the progress looks terrible, it might be a good idea to quit and just try a new set of hyperparameters.

One way to beat this is a scheme called *successive halving*.   xxx Sparks and Talwakar xxx.  Who else does successive halving?  Stochastic bandit literature.  The idea of successive halving is remarkably simple.  We'd try out $N$ hyperparameter settings for some fixed amount of time $1$.  Then, we keep the $N/2$ best performing algorithms and run for time $2$.  Repeating this procedure $\log_2(T)$ times, we end up with $N/T$ configurations run for $T$ time.

The total amount of computation in each halving round is equal to $N$. There are $\log_2(T)$ total rounds.  If we restricted ourself to the serial setting with the same computation budget,  we would be be able to run $N \log_2(T)/T$ hyperparameter settings for $T$ epochs each.  Thus, in the same amount of time, successive halving sees $T/log_2(T)$ more parameter configurations than pure random search!

Note that I could have used a different halving parameter $\eta$, and then the gap would be $T/\log_\eta(T)$.

Now, the problem here is that just because an algorithm looks bad at the beginning, doesn't meant that it might be optimal at the end of the run.  A particular example of this is setting the learning rate is stochastic gradient descent.  Small learning rates look worse than large ones in the early iterations, but it is often the case that a small learning rate leads to the best model in the end.

A simple way to deal with this tradeoff between breadth and depth is to start the halving process later.  We could run $N/2$ parameter settings for time $2$, then the top $N/4$ for time $4$ and so on.  This adapted halving scheme allows slow learners to have more of a chance of surviving before being cut, but the total amount of time per halving round is still $N$ and the number of rounds is at most $\log(T)$.  Running multiple instances of successive halving with different halving times increases depth while narrowing depth.

xxx Cite Kevin's post here. xxx

[The paper](http://arxiv.org/abs/1603.06560) describes a number of extensions, theoretical guarantees, and implications for stochastic infinite-armed bandit problems (if you're into that sort of thing). But let's wrap up this blogpost with some empirical evidence that this algorithm actually works.

Extensions: dataset subsampling, cool results on bandits


## Neural net experiments

We considered three image classification datasets: CIFAR-10, Street View House
Numbers (SVHN), and rotated MNIST with background images (MRBI). CIFAR-10 and
SVHN contain 32 × 32 RGB images while MRBI contains 28 × 28 grayscale images. Each dataset is
split into a training, validation, and test set: (1) CIFAR-10 has 40,000, 10,000, and 10,000 instances;
(2) SVHN has close to 600,000, 6,000, and 26,000 instances; and (3) MRBI has 10,000 , 2,000, and
50,000 instances for training, validation, and test respectively. For all datasets, the only preprocessing
performed on the raw images was demeaning.
<img src="./images/deep_table.png" class="img-responsive" align='right'></p>

For CIFAR-10, the basic unit of time was one-tenth of an epoch, and the maximum running time was 75 epochs.  For SVHN, the basic unit of time was one one-hundredth of an epoch and the maximum running time was 10 epochs.  The full details are described in the paper.

{: .center}
![Comparison of methods on CIFAR-10](/assets/hyperband/cifar10-compare.png)
![Comparison of methods on SVHN](/assets/hyperband/svhn-compare.png)

xxx talk about it.
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

One way to beat this is a scheme called *successive halving*.   xxx Sparks and Talwakar xxx.  Who else does successive halving?  Stochastic bandit literature.  The idea of successive halving is remarkably simple.  We'd try out $N$ hyperparameter settings for some fixed amount of time $T$.  Then, we keep the $N/2$ best performing algorithms and run for time $2T$.  Repeating this procedure $\log(N)$ times, we end up with one configuration run for $NT$ time.

Now, the problem here is that just because an algorithm looks bad at the beginning, doesn't meant that it might be optimal at the end of the run.  A particular example of this is setting the learning rate is stochastic gradient descent.  Small learning rates look worse than large ones in the early iterations, but it is often the case that a small learning rate leads to the best model in the end.

A simple way to deal with this tradeoff between breadth and depth is to try different values of $T$.  Instead of checking the algorithm progress at times $2^kT$, we can check at $2^{k}(2T)$ or $2^{k}(4T)$ instead.  This allows slow learners to have more of a chance of surviving before being cut.  The hyperband algorithm is just a simple way to generate rounds of successive halving that nearly optimally balance breadth versus depth.

```python
max_iter = 81  # maximum iterations/epochs per configuration
min_iter = 1  # minimum iterations/epochs per configuration
eta = 3 # defines downsampling rate (default=3)
logeta = lambda x: log(x)/log(eta)
s_max = logeta(max_iter/min_iter)  # number of unique executions of Successive Halving (minus one)
B = (s_max+1)*max_iter  # total number of iterations (without reuse) per execution of Succesive Halving

#### Begin Finite Horizon Hyperband outlerloop. Repeat indefinetely (a natural for-loop to parallelize)
for s = 0, ..., s_max:
    n = $\lceil B/max_iter/(s+1)  \rceil  # specify the number of arms for round s

    #### Begin Finite Horizon Successive Halving with (n,s)
    T = get a set of n hyperparameters
    for i in 0,...,s:
        # Run each of the n_i configurations for r_i iterations and keep best 1/eta proportion
        $n_i = n eta^i$
        $r_i = max_iter eta^(i-s)$
        val_losses = [ problem.run_and_return_val_loss(num_iters=r_i,hyperparameter_config=t) for t in T ]
        T = T[ argsort(val_losses)[0:int( n_i/eta )] ]
    #### End Finite Horizon Successive Halving with (n,s)
```


For example, consider the following table of experiments:

<pre>
max_iter = 81        s=4             s=3             s=2             s=1             s=0
min_iter = 1         n_i   r_i       n_i   r_i       n_i   r_i       n_i   r_i       n_i   r_i
eta = 3              ---------       ---------       ---------       ---------       ---------
B = 5*max_iter        81    1         27    3         9     9         6     27        5     81
                      27    3         9     9         3     27        2     81
                      9     9         3     27        1     81
                      3     27        1     81
                      1     81
</pre>




To deal with this sort of tradeoff, the authors build on some recent advances in *pure-exploration algorithms* for multi-armed bandits.  This sort of thing was de

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

One way to beat this is xxx

Now, the problem here is that just because an algorithm looks bad at the beginning, doesn't meant that it might be optimal at the end of the run.  A particular example of this is setting the learning rate is stochastic gradient descent.  Small learning rates look worse than large ones in the early iterations, but it is often the case that a small learning rate leads to the best model in the end.

A simple way to deal with this tradeoff is to try different budgets.  Instead of checking the algorithm at factors of 2, we can vary our factors.  For example, consider the following table of experiments:

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



to pursue an alternative approach. In particular, we employ recent advances in pure-exploration algorithms for multi-armed bandits to exploit the iterative algorithms of machine learning and embarrassing parallelism of hyperparmeter optimization. In contrast to treating the problem as a configuration <i>selection</i> problem, we pose the problem as a configuration <i>evaluation</i> problem and select configurations randomly. By computing more efficiently, we look at more hyperparameter configurations - more than making up for the ineffectiveness of random search used for selection - and outperform state-of-the-art Bayesian Optimization procedures. </p>

<p>
Our procedure, <i>HYPERBAND</i> is parameter-free and has strong theoretical guarantees for correctness and sample complexity. The approach relies on an early-stopping strategy for iterative algorithms of machine learning algorithms. The rate of convergence does not need to be known in advance and, in fact, our algorithm <i>adapts</i> to it so that if you replace your iterative algorithm with one that converges faster, the overall hyperparameter selection process is that much faster. This post is intended to give an introduction to the approach and present some promising empirical results.</p>



<h3>Hyperband Algorithm</h3>

<p>
The underlying principle of the procedure exploits the intuition that if a hyperparameter configuration is destined to be the best after a large number of iterations, it is more likely than not to perform in the top half of configurations after a small number of iterations. That is, even if performance after a small number of iterations is very unrepresentative of the configurations <i>absolute</i> performance, its <i>relative</i> performance compared with many alternatives trained with the same number of iterations is roughly maintained. There are obvious counter-examples; for instance if learning-rate/step-size is a hyperparameter, smaller values will likely appear to perform worse for a small number of iterations but may outperform the pack after a large number of iterations. To account for this, we hedge and loop over varying degrees of the aggressiveness balancing breadth versus depth based search. Remarkably, this hedging has negligible effect on both theory (a log factor) and practice. </p>

<p><i>HYPERBAND</i> requires 1) the ability to sample a hyperparameter configuration (<code>problem.get_random_hyperparameter_configuration()</code>), and 2) the ability to train a particular hyperparameter configuration for a given number of iterations (or maximum number of iterations) and get back the loss on a validation set (<code>problem.run_and_return_val_loss(num_iters=r,hyperparameter_config=t)</code>). Uniform random sampling is the obvious choice as it is typically trivial to implement over categorical, continuous, and highly structured spaces, but our procedure is indifferent to the sampling distribution: the better the distribution you define, the better the procedure performs. Nearly every iterative algorithm (e.g. gradient methods) will expose the ability to specify a maximum iteration making the two requirements of our procedure generally applicable. Consider the following python code snippet, the entirety of the codebase of Hyperband. </p>

<pre><code class='python'># problem implements get_random_hyperparameter_configuration()
# and run_and_return_val_loss(num_iters,hyperparameter_config)
from some_dataset import problem

max_iter = 81  # maximum iterations/epochs per configuration
min_iter = 1  # minimum iterations/epochs per configuration
eta = 3 # defines downsampling rate (default=3)
logeta = lambda x: log(x)/log(eta)
s_max = int(logeta(max_iter/min_iter))  # number of unique executions of Successive Halving (minus one)
B = (s_max+1)*max_iter  # total number of iterations (without reuse) per execution of Succesive Halving

#### Begin Finite Horizon Hyperband outlerloop. Repeat indefinetely.
for s in reversed(range(s_max+1)):
    n = int(ceil(B/max_iter/(s+1)*eta**s)) # specify the number of arms for round s

    print '\n\ns=%d\nn_i\tr_i\n--------------' % s
    #### Begin Finite Horizon Successive Halving with (n,s)
    T = [ problem.get_random_hyperparameter_configuration() for i in range(n) ]
    for i in range(s+1):
        # Run each of the n_i configs for r_i iterations and keep best n_i/eta
        n_i = n*eta**(-i)
        r_i = max_iter*eta**(i-s)
        print '%d\t%.2f' % (len(T),r_i)
        val_losses = [ problem.run_and_return_val_loss(num_iters=r_i,hyperparameter_config=t) for t in T ]
        T = [ T[i] for i in argsort(val_losses)[0:int( n_i/eta )] ]
    #### End Finite Horizon Successive Halving with (n,s)</code></pre>

<p class='lead'>For <b>s=s_max</b>, in the time a naive computation would consider <b>logeta(max_iter/min_iter)</b> configurations, Hyperband considers <b>max_iter/min_iter</b> configurations.
</p>
<p>The outerloop describes the hedge strategy alluded to above and the innerloop describes the early-stopping procedure that considers multiple configurations in parallel and terminates poor performing configurations leaving more resources for more promising configurations. We suggest that <code>max_iter</code> be set to the number of iterations you would use if your boss gave you a hyperparameter configuration and asked for a model back. We suggest that <code>min_iter</code> be set to be the minimum number of iterations where different hyperparameter configurations start to separate (or where it is clear that some settings diverge). Typically <code>min_iter</code> is set to a constant fraction of the dataset size. The parameter <code>eta</code> can be kept at the default (the theory suggests setting <code>eta=e=2.7183...</code>) but can also be changed for practical purposes as it controls the value of <code>B</code>: the total number of iterations taken for a particular run of Successive Halving <code>(n,s)</code>.
</p>

      <p class="lead">The sweeping of <b>s=0,...,s_max</b> trades off <i>breadth versus depth</i>.
      <p>The following table describes the number of configurations <code>n_i</code> and the number of iterations they are run for <code>r_i</code> within each round of the Successive Halving innerloop for a particular value of <code>(n,s)</code>.

      <pre>
max_iter = 81        s=4             s=3             s=2             s=1             s=0
min_iter = 1         n_i   r_i       n_i   r_i       n_i   r_i       n_i   r_i       n_i   r_i
eta = 3              ---------       ---------       ---------       ---------       ---------
B = 5*max_iter        81    1         27    3         9     9         6     27        5     81
                      27    3         9     9         3     27        2     81
                      9     9         3     27        1     81
                      3     27        1     81
                      1     81</pre>

      <p>
        Each inner loop indexed by <code>s</code> is designed to take <code>B</code> total iterations.
        Intuitively, this means each value of <code>s</code> takes about the same amount of time on average.
      For large values of <code>s</code> the algorithm considers many arms (<code>max_iter/min_iter</code> at the most) but discards hyperparameters based on just a very small number of iterations which may be undesirable for hyperparameters like the <code>learning_rate</code>. For small values of <code>s</code> the algorithm will not throw out hyperparameters until after many iterations have been performed but fewer arms are considered (<code>logeta(max_iter/min_iter)</code> at the least). The outerloop hedges over all possibilities.  
      </p>



      <h2>Experimental Results</h2>
      Our <a href="http://arxiv.org/abs/1603.06560">paper</a> describes a number of extensions, theoretical guarantees, and fascinating implications for stochastic infinite-armed bandit problems. Here, we present some empirical evidence that it actually works.

      <h3>Cudaconvnet on Cifar-10, SVHN, MRBI (deep learning)</h3>
        <p>We considered three image classification datasets: CIFAR-10 [16], Street View House
 Numbers (SVHN) [19], and rotated MNIST with background images (MRBI) [18]. CIFAR-10 and
 SVHN contain 32 × 32 RGB images while MRBI contains 28 × 28 grayscale images. Each dataset is
 split into a training, validation, and test set: (1) CIFAR-10 has 40,000, 10,000, and 10,000 instances;
 (2) SVHN has close to 600,000, 6,000, and 26,000 instances; and (3) MRBI has 10,000 , 2,000, and
 50,000 instances for training, validation, and test respectively. For all datasets, the only preprocessing
 performed on the raw images was demeaning.
    <img src="./images/deep_table.png" class="img-responsive" align='right'></p>

 <p>We ran HYPERBAND with a <code>min_iter=100</code>. Given the
 batch size of 100, this corresponds to operating on at least 10,000 datapoints. We set <code>max_iter=30,000</code> for CIFAR-10 and MRBI, while a maximum iteration of <code>max_iter=60,000</code> was used for SVHN
 due to its larger training set. We specified <code>eta=4</code> for all experiments; this limited the number
 of iterations of SUCCESSIVEHALVING to at most 5, thus allowing each iteration of HYPERBAND
 to complete within reasonable times. </p>
 <div class='row'>
  <div class='col-sm-4'>
    <img src="./images/deep_1.png" class="img-responsive">
  </div>
  <div class='col-sm-4'>
    <img src="./images/deep_2.png" class="img-responsive">
  </div>
  <div class='col-sm-4'>
    <img src="./images/deep_3.png" class="img-responsive">
  </div>
</div>

Extensions: dataset subsampling, cool results on bandits

<p>We look forward to many more empirical studies comparing early-stopping procedures and random search to Bayesian Optimization.
</p>

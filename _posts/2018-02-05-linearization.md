---
layout:     post
title:      The Linearization Principle
date:       2018-02-05 0:00:00
summary:    An outsider tour of reinforcement learning, Part 2. The Linearization Principle.
author:     Benjamin Recht
visible:    true
---

I have an ethos for tackling problems in machine learning that I call the "Linearization Principle." There are many variants of this principle, but the simplest is “If a machine learning algorithm does crazy things when restricted to linear models, it’s going to do crazy things on complex nonlinear models too.”

This Linearization Principle provides a convenient way to attack and decompose the complex problems in machine learning into tractable, simple research problems. I don’t think that application to linear models is a sufficient condition for understanding machine learning, but I’d argue that it is a necessary bar to clear for a method to be broadly useful. In the same way that solving 2SAT doesn’t prove P=NP, if you claim to have a 3SAT solver and it takes exponential time on 2SAT, then something fishy is going on.

Before trying to apply the Linearization Principle to reinforcement learning, let me try to give a few examples of how simple models can give insights into standard, supervised deep learning. [Ali teed up the ball for me](http://www.argmin.net/2018/01/25/optics/) with a list of phenomena observed in deep learning. I’d like to go through several of the phenomena he listed and explain how linear models help us to understand them.

#### Ali’s First Phenomenon: Shallow local minimizers generalize better than sharp ones.

For both linear models and deep models, not even all _global_ minimizers generalize equally well. Suppose I have twice the number of parameters as data points.  This means that I can simultaneously get zero error on the training set (using N degrees of freedom) and on any other set of N points (using the other N degrees of freedom). So, for example, I can create a “perturbed” version of my training data by adding a little bit of noise to it and fit a model that gets zero training error on the true data while interpolating random labels on the perturbed data. This model will be a global minimizer of the training error on the true training set. But it seems a bit implausible that such a wacky model could generalize well.

How can we distinguish between minimizers in order to maximize out-of-sample performance? In deep learning, the conventional answer seems to be “don’t choose a sharp minimizer,” but I have no idea what people mean by a sharp minimizer. We ran a heated [twitter forum on this topic](https://twitter.com/beenwrekt/status/941005520420225025) and found no consensus definition. The notion that seemed closest was that a minimizer was sharp if _the training error was sensitive to small perturbations of the model._

Lack of sensitivity to perturbations seems quite reasonable to me. And, indeed, in linear models this idea is as old as machine learning itself. The stability of a linear model to perturbations can be measured in terms of  _margin_, the distance of the data to the decision boundary.

Margin provides a straightforward way to see why the above wacky model would be unlikely to generalize.  For the sake of simplicity, consider the case of binary classification where all of the data points have unit norm. Suppose we pick $w$ such that $\vert w^Tx\vert>1$ for all of the training points $x$. Then the margin is at least $$\|w\|^{-1}$$. That is, margin is the largest inverse Euclidean norm out of all $w$ such that $\vert w^Tx\vert>1$ for all $x$. Now, for our perturbed example, we are forcing very nearby points to have dot product with $w$ with opposite signs. Hence, the norm of $w$ will need to be huge, and the resulting solution necessarily will have very small margin. In turn, small perturbations of $w$ or of the data will drastically change the classifications made by this model.

So if “shallow minimizer” means “large margin,” then I’m on board. Unfortunately, for deep models, there isn’t yet a clean, parameterization-invariant definition that captures the classical notion of margin. On the other hand, there are [several](https://arxiv.org/abs/1707.09564) [nice](https://arxiv.org/abs/1706.08498) [steps](https://arxiv.org/abs/1712.06541) in the direction of finding the right definition of margin for deep nets.

#### Ali’s Second Phenomenon:  Inserting Batch Norm layers speeds up SGD.

While it’s not clear what happens when you do this layerwise, for linear networks, standardization certainly can accelerate SGD. There’s a simple reason for this: whitening data matrices in linear models tends to improve the conditioning of the data covariance. This in turn improves the rate of convergence of SGD. Of course linear models can’t provide a total explanation here once we do the normalization in a layerwise fashion in a deep net. And, moreover, I’m not sure if linear models suffer from internal covariate shift. (ht to [Ludwig Schmidt](http://people.csail.mit.edu/ludwigs/) for this pointing out this connection)

#### Ali’s Third Phenomenon: SGD is successful despite many local optima and saddle points.

Linear models won’t have saddle points, but if a model is granted more parameters than data points, the training error will have many local minimizers. Indeed, as I discussed above, it will have an infinite set of _global_ minimizers.

SGD for linear models does not converge to an arbitrary optimum, however. Depending on the loss function, SGD will find a very particular minimizer. For the square loss, [the solution will have large margin](https://arxiv.org/abs/1611.03530), and for the softmax loss, [SGD will converge to the solution that maximizes the margin, albeit exponentially slowly](https://arxiv.org/abs/1710.10345).

With regards to saddle points, my gut tells me that the notion that SGD avoids them is an artifact of selection bias.  As Ali and I showed in our [test of time talk](http://www.argmin.net/2017/12/05/kitchen-sinks/), it’s very easy to find examples of neural nets where gradient descent does not efficiently find a local minimum. It possible that we only hear about the cases where we avoid saddles.

#### Ali’s Fourth Phenomenon: Dropout works better than other randomization strategies.

[Wager and collaborators](https://arxiv.org/abs/1307.1493) showed that on linear models, Dropout is nothing more than a form of weighted ridge regression. Dropout undoubtedly something different on deep models, but it’s not surprising that randomly perturbing backpropagation imposes some sort of regularization. Whether or not “works better than other randomization strategies” remains unclear even in deep nets.

#### Ali’s Fifth Phenomenon: Deep nets can memorize random labels, and yet, they generalize.

As we discussed above, this is also true for linear models. This was the subject of the apparently highly controversial paper at [ICLR with S. Bengio, Hardt, Vinyals, and Zhang](https://arxiv.org/abs/1611.03530).  Common neural nets have so many parameters that they can fit any sign pattern you’d like, even on large models like Imagenet.

This is also true for underdetermined linear models. High dimensional linear models generalize when they have large margin even when they perfectly interpolate the training data.

#### One more for good luck:  The Adam algorithm.

Over 5000 papers have been published using the Adam algorithm designed to accelerate training in deep neural nets. Fans of Adam argue that it converges faster, provides state of the art performance, and doesn’t need to have its hyperparameters tuned. All of these claims are testable by experiments. Indeed, in some recent work with [Becca Roelofs, Nati Srebro, Mitchell Stern, and Ashia Wilson](https://arxiv.org/abs/1705.08292), we found that though Adam was not only just as sensitive to hyperparameters as normal SGD but also consistently achieved worse test error than SGD.

It was hard to use the empirical benchmarks to get insights into why Adam was performing poorly, so we turned to thinking about underdetermined linear models again. In this case, we could precisely track to where Adam converged. This allowed us to construct simple generative models where gradient descent would achieve large margin and perfect generalization whereas Adam would provide a predictor that would do no better than random guessing.

## Linearization for RL

While the Linearization Principle doesn’t explain all of the properties of neural nets, it does clear up many of supposedly mysterious properties: most of these phenomena have basis in techniques applicable for linear models.

I think the same clarification can be achieved for reinforcement learning by leveraging the Linearization Principle. In the next post, I will argue that an appropriate linear baseline for RL is the venerable “Linear Quadratic Regulator.”

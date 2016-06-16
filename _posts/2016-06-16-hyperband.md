---
layout:     post
title:      Tuning is no fun
date:       2016-06-16 7:00:00
summary:    Why do I have so many parameters?
author:     Ben Recht
visible:    false
---

### Joint post with Kevin Jamieson

It's all the rage in machine learning these days to build complex, deep pipelines with thousands of tunable parameters.  Now, I don't mean parameters that we learn by stochastic gradient descent.  But I mean architectural concerns, like the value of the regularization parameter, the size of a convolutional window, or the breadth of a spatio-temporal tower of attention.  Such parameters are typically referred to as *hyperparameters* to contrast against the parameters learned during training. These structural parameters are not learned, but rather descended upon by a lot of trial-and-error and fine tuning.

Automating such hyperparameter tuning is one of the most holy grails of machine learning.  And people have tried for decades to devise algorithms that can quickly prune bad configurations and maximally overfitting on the test set.  In recent years, parameter search in machine learning has been dominated by Bayesian Optimization methods.  However, [recent evidence](http://arxiv.org/abs/1603.06560) on a benchmark of over a hundred hyperparameter optimization datasets suggests that such enthusiasm may call for increased scrutiny.  

Rank plots aggregate statistics across datasets for different methods as a function of time: first place gets one point, second place two points, and so forth. The plot, taken taken from that work, is the average score across 117 datasets collected by [Feurer et. al. NIPS 2015(http://papers.nips.cc/paper/5872-efficient-and-robust-automated-machine-learning) (lower is better). While random search appears to be soundly beat by the state-of-the-art Bayesian optimization methods of SMAC and TPE, which is presumably expected, it is perhaps surprising that these methods are outperformed by random run at twice the speed, i.e., running random search for twice as long yields superior results

<img src="assets/hyperband/rank_chart.png" width="40%" align="right">

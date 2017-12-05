---
layout:     post
title:      Random Kitchen Sinks
date:       2017-12-04 7:00:00
summary:    text of the acceptance speech for the NIPS test of time award
author:     Ben Recht
visible:    false
---

*Ed. Note: Ali Rahimi and I won the test of time award at NIPS 2017 for our paper "Random Features for Large-scale Kernel Machines".  This post is the text of our acceptance speech.*

Video of Ali giving the talk can be found [here](http://xxx).

Nothing makes you feel old like an award called a “test of time." It’s forcing us to accept our age. We are both old now, and we’ve decided to start this talk accordingly.

## Part 1. Back When We Were Kids

We’re getting this award for the "Random Features for Large-scale Kernel Machines." But this paper was the beginning of a trilogy of sorts. And like all stories worth telling, the good stuff happens in the middle, not at the beginning. If you’ll put up with our old man ways, we’d like to tell you the story of these papers, and take you waaay back to NIPS 2006, when we were young spry men and dinosaurs roamed the earth.

Deep learning had just made a splash at NIPS 2006. The training algorithms were complicated, and results were competitive with linear models like PCA and linear SVMs. In a hallway conversation, people were speculating how they’d fare against kernel SVMs. But at the time, there was no easy way to train kernel SVMs on large datasets. We had both been working on randomized algorithms (Ali for bipartite graph matching, Ben for compressed sensing), so after we got home, it took us just two emails to nail down the idea for how to train large kernel SVMs. These emails became the first paper:

	Slide: The emails.

To fit a kernel SVM, you normally fit a weighted sum of Radial Basis Functions to data. We showed how to approximate each of these basis functions in turn as a sum of some random functions that did not depend on the data. A linear combination of a linear combination is another linear combination, but with this new linear combination has many fewer parameters.

	Slide: kernel approximation.

We showed how to approximate a variety of RBF functions and gave bounds for how many random functions you need to approximate them each of them well.  And the trick worked amazingly well in practice! But when it came time to compare it against deep nets, we couldn’t find a dataset or code base that we could train or compare against. Machine Learning was just beginning to become reproducible. So even though we’d started all this work to curb the deep net hype in its tracks, we couldn’t find anything to quash. Instead, we compared against boosting and various accelerated SVM techniques, because that’s what was reproducible at the time. To show off how simple this algorithm was, during NIPS, we handed out these leaflets, that explained how to train kernel SVMs with three lines of MATLAB code. A bit of guerilla algorithm marketing:

	Slide: leaflet

But there was something shady in this story. According to this bound, which is tight, to approximate a kernel well, say 1% uniform error, you need tens of thousands of random features.  But in all of our experiments, we were getting great results with a only few hundred random features. Sometimes, random feature produced predictors that had better test error than the SVM we were trying to approximate! In other words, it wasn’t necessary to approximate kernels to get good test errors at all.

Alex Smola and other friends at Yahoo pointed this out with a concise graph a few years later:

	Slide: Approximation error vs Generalization error from FastFood paper

There seems to be something dodgy with the Random Features story we’ve been telling you so far.

## The NIPS Rigor Police

In those days, NIPS had finished transitioning away from what Sam Roweis used to call an “ideas conference”. Around that time, we lived in fear of the tough questions from the NIPS rigor police who’d patrol the poster sessions: I’m talking about Nati Srebro, Ofer Dekel, or Michael Jordan’s students, or god forbid, if you’re unlucky, Shai Ben-David, or Manfred Warmuth.

We decided to submit the paper with this bit of dodginess. But the NIPS rigor police kept us honest. We developed a solid understanding of what was happening.  We draw a set of random functions and combine them into a predictor.

[Our second paper said this:](xxx) In a similar way Fourier functions form a basis for the space of L2 functions, or similar to how wide three layer neural nets can represent any smooth function, random sets of smooth functions, with very high probability, form a basis set for a ball of functions in L2. You don’t need to talk about random features as eigenfunctions for any famous RBF kernels to be sensible. Random functions are a basis set of a Hilbert space that was legitimate by itself. In our [third paper](xxx), we finally analyzed the test error of this algorithm when it’s trained on set of samples.

By this third paper, we’d entirely stopped thinking in terms of kernels, and just fitting random basis function to data. We put on solid foundation the idea of linearly combining random kitchen sinks into a predictor.  Which meant that it didn’t really bother us if we used more features than data points.

Our original goal had been to compare deep nets against kernel SVMs. We couldn’t do it back then. But code and benchmarks are abundant now, and direct comparisons are easy. Many people are still using random features in their research, and [May el al](xxx) have shown that they get you about the same performance as deep neural networks on speech benchmarks. Just three lines of MATLAB code.

We still sometimes use random features in our day jobs. We like to get creative with special-purpose random features. It’s such an easy thing to try. When they work and we're feeling good about life, we might say “wow, random features are so powerful! They solved this problem!” Or if we're in a more somber mood, we say “that problem was trivial. Even random features cracked it.” It’s the same way we (and Alyosha Efros) think about nearest neighbors. When nearest neighbors cracks a dataset, you either marvel at the power of nearest neighbors, or you conclude your problem wasn’t hard at all. Regardless, it’s an easy trick to try.

## KIDS THESE DAYS

It’s now 2017. We find ourselves overwhelmed with the machine learning's progress. ML has become reproducible. We share code freely and use common benchmarks, thanks to GitHub, AWS, Tensorflow, PyTorch, and standardized competitions.

We produce stunningly impressive results: Self-driving cars seem to be around the corner, artificial intelligence tags faces in photos, transcribes voicemails, translates documents, and feeds us ads. Billion-dollar companies are built on machine learning. In many ways, we’re in a better spot than we were 10 years ago. In some ways, we’re in a worse spot.

There’s a self-congratulatory feeling in the air.  Andrew Ng goes as far as saying that "artificial intelligence is the new electricity." But we'd like to offer an alternative metaphor: machine learning has become alchemy.

  Slide: Alchemy photo

Don't get us wrong.  Alchemy’s ok. Alchemy’s not bad. There’s a place for alchemy. Alchemy worked.

## Alchemy worked

Alchemists invented metallurgy, ways to make medication, dying techniques for textiles, and our modern glass-making processes.  

Then again, alchemists also believed they could transmute base metals into gold and that leeches were a fine way to cure diseases. To reach the sea change in our understanding of the universe that the physics and chemistry of the 1700s ushered in, all the theories alchemists developed had to be abandoned.

If you’re building photo sharing services, alchemy is fine. But we’re now building systems that govern health care and our participation in civil debate. We would like to live in a world whose systems are build on rigorous, reliable, verifiable knowledge, and not on alchemy. As annoying as the NIPS rigor police was, we wish it would come back.

## Machine learning is now a systems problem

We often hear that machine learning is now merely a systems problem. Meaning that we possess all the math knowledge we need, and that all that’s left to do now is to bullet-proof variants of gradient descent and scale them up with distributed systems.

We think we’re very far from having that knowledge. We’ll give you an example of where this hurts us.

We bet a lot of you reading this have tried training a deep net of your own from scratch and walked away feeling bad about yourself because you couldn’t get it to perform.

This isn't your fault. It’s gradient descent’s fault. Let's check out what happens when we run gradient descent on the simplest deep net you can imagine, a two layer deep net with linear activations and where the labels are a badly-conditioned linear function of the input.

	Slide: loss function, and graph

Gradient descent makes great progress early on, then spends the rest of the time making almost no progress at all. You might think this it’s hit a local minimum. It hasn’t. The gradients aren’t decaying to 0. You might say it’s hitting a statistical noise floor of the dataset. That’s not it either. You can compute the expectation of the loss and minimize it directly with gradient descent. Same thing happens. Gradient descent just slows down the closer it gets to a good answer. If you’ve ever trained Inception on ImageNet, you’ll know that gradient descent gets through this regime in a few hours, and takes days to crawl through this regime.

Here’s what a better descent direction would do. This is Levenberg-Marquardt:

  Slide: compare against Levenberg-Marquardt

If you haven’t tried optimizing this problem with gradient descent, please spend 10 minutes coding this up.  This is the algorithm we use as our workhorse, and it fails on a completely benign non-contrived problem. You might say “this is a toy problem, gradient descent fits large models well.” First, many of you have experienced otherwise. Second, this is how we build knowledge, we apply our tools to simple problems we can analyze, and work our way up in complexity. We seem to have just jumped our way up.

This pain is real. Here’s an email that landed in Ali's inbox two weeks ago:

Slide:
"On Friday, someone on another team changed the default rounding mode of some Tensorflow internals (from truncation to "round to even").

Our training broke. Our error rate went from <25% error to ~99.97% error (on a standard 0-1 binary loss)."

  Slide: GPU roundoff errors bug in tensorflow

This happens because we run the wrong optimizers on loss surfaces we don’t understand. Our solution is to add more mystery to an already mysterious scaffolding. Like Batch Norm.

## Reducing internal covariate shift

Batch Norm is a technique that speeds up gradient descent on deep nets. You sprinkle it between your layers and gradient descent goes faster. I think it’s ok to use techniques we don’t understand. I only vaguely understand how an airplane works, and I was fine taking one to this conference. But it’s always better if we build systems on top of things we do understand deeply? This is what we know about why batch norm works well. But don’t you want to understand why reducing internal covariate shift speeds up gradient descent? Don’t you want to see evidence that Batch Norm reduces internal covariate shift? Don’t you want to know what internal covariate shift is? Batch Norm has become a foundational operation for machine learning. It works amazingly well. But we know almost nothing about it.

## Conclusion of Two Curmudgeons

Our community has a new place in society. If any of what I’ve been saying resonates with you, let us suggest some just two ways we can assume our new place responsibly.

Think about how many experiments you’ve run in the past year to crack a dataset for sport, or to see if a technique would give you a boost. Now think about the experiments you ran to help you find an explanation for a puzzling phenomenon you observed. We do a lot of the former. We could use a lot more of the latter. Simple experiments and simple theorems are the building blocks that help understand complicated larger phenomena.

For now, most of our mature large scale computational workhorses are variants of gradient descent. Imagine the kinds of models and optimization algorithms we could explore if we had commodity large scale linear system solvers or matrix factorization engines. We don’t know how to solve this problem yet, but one worth solving. We are the group who can solve it.

Over the years, some of our dearest friends and strongest relationships have emerged from the machine learning community. Our gratitude and love for this group are sincere, and that’s why we're asking all of us to be rigorous, less alchemical. We're are grateful for this test of time award and for the opportunity to have gotten to know many of you.  And we hope that you’ll join us to grow machine learning beyond alchemy into electricity.

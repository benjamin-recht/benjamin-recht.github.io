---
layout:     post
title:      "All Statistical Models Are Wrong. Are Any Useful?"
date:       2021-09-21 0:00:00
summary:    "Why statistical modeling can lead us astray in randomized experiments."
author:     Ben Recht
visible:    false
blurb: 		  true
---

Though I singled out a mask study [in the last post](https://www.argmin.net/2021/09/13/effect-size/), I’ve had a growing discomfort with statistical modeling and significance more generally. Statistical models are a way to account for a wide range of variables to predict effects that may vary across a population. Such statistical models bring with them a host of assumptions and powers. But when are they appropriate for deducing significance of the outcomes of experiments? Here, I’ll argue that they are almost never appropriate in most settings, and, moreover, they can result in confidence intervals that rarely contain the correct parameters.

Note that in order to sample from some population, we need not assume that it is random. An experimenter can choose to sample one individual from a larger pool at random even when the pool is a deterministic collection. Similarly, the experimenter can randomly assign each member of the pool to a group for experimentation even when the pool is deterministic. We need not build a statistical model of our population in order to study it experimentally.

But the convention in much scientific practice entangles the randomness used in survey and experiment design with the randomness of the natural world. The dominant convention in experimental sciences is to assert the existence of a probability distribution from which all observations in an experiment are samples. That is, most analyses begin with the assumption that the population is itself a stochastic entity whose statistical properties can be accurately modeled. Such probabilistic modeling is immediately problematic. We are forced to confront the notion of probability itself. What does the probability of an event mean? Is a Bayesian or Frequentist viewpoint more correct? What does it mean to sample a natural process?

My perspective on the pitfalls of probabilistic modeling has been heavily influenced by the writings of David Freedman. Freedman advocates for a pragmatic approach to statistical modeling. “[Probability is just a property of a mathematical model intended to describe some features of the natural world. For the model to be useful, it must be shown to be in good correspondence with the system it describes.](https://www.stat.berkeley.edu/~stark/Preprints/611.pdf)” This is the less pithy, but more prescriptive version of Box’s famous and tiresome aphorism “All models are wrong, but some are useful.”

Model building and validation requires deep domain knowledge for a task at hand. One of my favorite models is Ohm’s law, which states that the current that flows across a conductive material is proportional to the voltage drop across the resistor. Due to thermal noise, the actual model is

$$
\small{
  \text{current} = \text{material constant} \times \text{voltage} + \text{noise}}
$$

And the noise is Gaussian white noise. This model has been extensively tested and is a foundation of all circuit design. Remarkably, this simple formula describes complex electronic behavior. Physics is full of amazing examples of statistical models that accurately predict the outcome of experiments to a dozen significant figures.

But in biology, medicine, social science, and economics, our models are much less accurate and less grounded in natural laws. Most of the time, models are selected because they are convenient, not because they are plausible, well motivated from phenomenological principles, or even empirically validated. Freedman built a cottage industry around pointing out how poorly motivated many of the common statistical models are.

A particular example called out by Freedman is the [ubiquitous logistic regression model](https://www.jstor.org/stable/27645896). Freedman observed that in a variety of randomized control trials, experimenters would “correct” the estimates of their randomized controlled trials by “controlling for fixed effects” with logistic regression. Controlling for fixed effects is pernicious jargon that means “set up a regression problem with all of the variables that one thinks make their effect size look too small, and then solve the regression as an attempt to remove the influence of these variables.” It is most common in observational studies, but many insist it is appropriate in the context of randomized controlled trials as well. This convention of correction persists in the present, and I highlighted similar corrections in my last post. Freedman argues that such corrections are misguided, especially in the context of randomized trials.

To understand the motivation for using logistic in the first place, I need to tell you what an odds ratio is. Experiments are often interested in estimating an odds ratio associated with some treatment. The odds of an event with probability $p$ is $p/(1-p)$: if your odds of winning a lottery are one million to one, that means, the probability that you win is one million times smaller than the probability that you lose. Let’s suppose that the probability of a treatment having a desired outcome is $p$. And the probability of this outcome without an applied treatment is $q$. Then the odds ratio is simply the ratio of the odds of the outcome with and without treatment

$$
\small{
\frac{p}{1-p} \cdot \frac{1-q}{q}\,.}
$$

When the odds ratio is large, we deem a treatment to be highly effective.

Logistic regression posits that individuals have a vector of features $Z$ that influence the odds of the effectiveness of treatment. Specifically, if $Y$ is the indicator of the desired outcome and $X$ is indicator of treatment, the logistic regression model asserts the log of the odds the outcome is a linear function of the treatment and the selected features:

$$
\small{
\log  \frac{p(Y=1 | X,Z ) }{ 1-p(Y=1 | X,Z) } = \beta X + \gamma^\top Z + \alpha \,.}
$$

This model is convenient if we are interested in odds ratios. In the logistic model, no matter what the covariate $Z$, the odds ratio is

$$
\small{
\frac{p(Y=1 | X=1,Z ) } {1-p(Y=1| X=1,Z) }  \cdot \frac{1-p(Y=1 | X=0, Z)}{p(Y=1 | X=0, Z)} = e^\beta\,.}
$$

Hence, if we can estimate beta, we can estimate the odds ratio. And if we can estimate the variance of beta, we can compute confidence intervals over our odds ratio estimates.

But all of this assumes that the model is correct! If the logistic model is not correct, then our confidence intervals are meaningless. Or at least, they are not confidence intervals around any true notion of odds ratios.

It’s almost always reasonable to be suspicious of this logistic model. It is first asserting that the odds ratio is a constant for a fixed covariate $Z$. That is, all subjects experience the same proportional effect of treatment. Even less realistically, the model asserts that the outcome is positive for an individual $i$ with treatment value $X_i$ and covariate value $Z_i$ if

$$
\small{
  U_i  \leq \alpha + \beta X_i + \gamma^\top Z_i\,,}
$$

where $U_i$ is a random variable sampled from the logistic distribution. The model assumes the $U_i$ are independent of the treatment and the covariates, the $U_i$ are independent across all of the individuals, and the $U_i$ have a common logistic distribution. The only thing that differs between treatment and control is the value of the threshold on the left hand side. These are a lot of assumptions, and they are seldom verified or tested in papers where logistic regression is applied.

The question remains: does this matter? Do these modeling assumptions actually affect our inferences about effect size? Freedman provides an elegant argument demonstrating that logistic regression always overestimates the true odds ratio, and sometimes can do so quite poorly. He also shows that simply computing a plugin estimator of the odds ratio with no covariate adjustment at all is consistent in randomized controlled trials. That is, there is no need to adjust for covariates in randomized controlled trials if you want an accurate estimate of the odds ratio. Furthermore, covariate adjustments can lead to significant overestimation of the treatment’s effect size.

Rather than going through Freedman’s theoretical argument, it’s a bit more evocative to give an example. The following is gleaned from a helpful discussion with Joel Middleton. Suppose you sample 10000 children from a larger population where each child in the population has an equal chance of liking and disliking vegetables. We propose a treatment of bribing kids with a cookie to eat their veggies, and randomly assign this treatment to half of the subjects. Left untreated, veggie haters have a 20% probability of finishing their veggies, but veggie lovers have an 80% probability of eating their greens. When bribed with a cookie, veggie haters and veggie lovers have 25% and 85% of eating their vegetables, respectively.

An average child in the study has a probability of 50% of eating their veggies if in control and 55% if in treatment. The log odds ratio is thus

$$
\small{
  \log \frac{.55}{1−.55}−\log\frac{.5}{1−.5} \approx 0.2\,.}
$$

Now, when you instead run logistic regression, the coefficient of the treatment variable is larger than 0.2. Indeed, [when I try this in python](https://nbviewer.jupyter.org/url/argmin.net/code/logistic_logodds_example.ipynb), running 1000 synthetic experiments, I find that the median point estimate is 0.32, which is, as promised, larger than the true log odds. Even more worrisome is the 95% confidence interval contains 0.2 only 38% of the time. Clearly, the confidence intervals are not accurate when the model is wrong.

When the true effect size is large, this discrepancy between the logistic regression estimate and the true log odds might not be that big a deal: your error bars are wrong, but the effect size is estimated in the correct direction. But the results of such logistic regression analyzes are regularly quoted as estimates of odds ratios (For example, look at any  observational study of vaccine effectiveness). The precision of these estimates is unfortunately lacking and misleading.

So what is the remedy here? The thing is, we already know the answer: if we randomized the assignment, we can estimate log odds by counting the frequency of success under treatment and control, and then just plugging these into the odds ratio. If you do this, you find an estimate whose median is precisely equal to the true log odds. No covariate adjustment is required.

This is merely one example showing why it is critical to decouple the randomness used to probe a system from the randomness inherent in its system itself. Statistical models are not necessary for statistical inference, but randomness itself is amazingly... let’s say... _useful_ for understanding natural phenomena. I will spend the next few blogs reminding myself and you faithful blog readers that proper experiments, machine learning predictions, and statistical summarizations can all be designed without statistical models of populations, and how the mathematical formalizations of randomized algorithms may suggest paths forward in cleaning up conventional experimental formalism.

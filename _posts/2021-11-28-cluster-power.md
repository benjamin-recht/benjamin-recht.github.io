---
layout:     post
title:      "The cult of statistical significance and the Bangladesh Mask RCT."
date:       2021-11-28 0:00:00
summary:    "Trying to do a proper statistical analysis of the Bangladesh Mask RCT taking into account cluster design effects."
author:     Ben Recht
visible:    false
blurb: 		  true
---

In the last post, [I argued that the effect size in the Bangladesh RCT was too small to inform policy making](https://www.argmin.net/2021/11/23/mask-rct-revisited/). I deliberately avoided diving into statistical significance as arguments about p-values quickly devolve into scientific gish gallop. Statistical validity is the most overrated form of experimental validity, and it crowds out more important questions of effect size, bias, design, and applicability.

But shoot, sometimes Byzantine academic arguments are fun. And, though they are always wrong, sometimes they are useful. In this blog I want to discuss how we analyze statistical validity in cluster randomized controlled trials. It is quite subtle and sensitive, and should give us pause about these experimental designs. The sample sizes needed for validating large effects in cluster randomized trials can be absurdly high, and running a clean trial with millions of participants is likely impossibly difficult and almost never worth doing.

To review in the [Bangladesh Mask RCT](https://www.poverty-action.org/sites/default/files/publications/Mask_Second_Stage_Paper_20211108.pdf.pdf), there were $n_C=$163,861 individuals from $k_C=$300 villages in the control group. There were $n_T=$178,322 individuals from $k_T=$300 villages in the intervention group. The main end point of the study was whether their intervention reduced the number of individuals who reported covid-like symptoms and tested seropositive at some point during the trial. There were $i_C=$1,106 symptomatic individuals confirmed seropositive in the control group and $i_T=$1,086 such individuals in the treatment group.

What can we say about the statistical significance of this 20 case difference? Most would guess this difference is not significant. Indeed, in a balanced design with $n_T=n_C$ and 180,000 individuals in each arm, this study would not be statistically significant. Let's imagine we ran an experiment where we could treat the outcomes of each individual as independent, identically distributed random variables. What is the p-value associated with the null hypothesis that the prevalence of infections in the control group is less than or equal to the prevalence in the treatment group? A simple statistical test of this hypothesis is the z-test for proportions. For the z-test, the p-value when the groups are balanced is 0.3.

The authors claim a balanced design, but the treatment group is 1.1x bigger than the control group. [As I mentioned in the previous post](https://www.argmin.net/2021/11/23/mask-rct-revisited/), this discrepancy can likely be explained by the large differential in response rates between the groups: 1.05x fewer households were approached for surveys in control and the control group responded at 1.07x lower rate than treatment. The most significant difference I've found thus far between the treatment and control group is the consent rate to be surveyed. For the medical statistics experts, [the intention to treat principle](https://en.wikipedia.org/wiki/Intention-to-treat_analysis) says that these individuals must be counted in the control group, and omitting them invalidates the study.

But the issues of significance remain even if we forgive this large imbalance in the study. If we re-run the z-test with the $n_C$ and $n_T$ in the study data, the p-value is now 0.009, which would be quite significant at the standard p < 0.05 threshold. However, the individual outcomes are _not_ independent. The trial was cluster-randomized, so everyone in the same village received the same intervention. This means that the outcomes inside a village are correlated, and they are likely more correlated inside a village than outside.

To capture the correlation among intra-cluster participants, statisticians use the notion of the [_intra-cluster correlation coefficient_](https://www.povertyactionlab.org/resource/power-calculations) $\rho$. $\rho$ is a scalar between 0 and 1 that measures the relative variance within clusters and between clusters. When $\rho=1$, all of the responses in each cluster are identical. When $\rho=0$, the clustering has no effect, and we can treat our assignment as purely randomized. Once we know $\rho$ we can compute an _effective sample size_: if the villages are completely correlated, the number of samples in the study would be 600. If they were independent, the number of samples would be over 340,000. The number of effective samples is equal to the total number of samples divided by the _design effect_:

$$
{\small
    DE = 1+\left(\frac{n_T+n_C}{k_T+k_C}-1\right)\rho \,.
}
$$

What is the design effect of the Bangladesh RCT? Measuring the intra-cluster correlation $\rho$ is nontrivial: the true value of $\rho$ depends on both potential outcomes in an experiment and needs to be estimated using some side experiment or previous trials at baseline. $\rho$ is often inferred from secondary covariates of earlier experiments on a similar population. We don't have a pre-specified estimate, but can cheat a bit here and estimate $\rho$ from the provided data in the control villages. A standard ANOVA calculation says that the observed symptomatic seropositivity in the control villages has an intra-village correlation of $\rho=$0.007. This value isn't particularly unreasonable. Some practitioners suggest that because of behavioral contagion alone, $\rho$ should be [between 0.01 and 0.02 for human studies.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1466680) [This cluster RCT on mask use to prevent influenza in households](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0013998#pone.0013998-Carrat2) uses $\rho=$0.24.  As a sanity check, the intra-village correlation of reported systems is 0.03. So let’s stick with $\rho=$0.007 and see where it takes us.

For the Bangladesh RCT, assuming $\rho=$0.007, the design effect is about 5. This reduces the effective sample size from over 340,000 to just under 70,000. What happens with our z-test? We simply take the z-score and divide by the square root of the design effect, yielding a p-value of 0.14. The result is not statistically significant once we take into account the intra-cluster correlation. In order to "achieve" statistical significance, $\rho$ would need to be less than 0.001 and the design effect would have to be less than 2.2.

We can also do similar design-effect adjustments for relative risk reduction. Recall the relative risk reduction is the ratio of the rate of infection in the treatment group to the rate of infection in the control group

$$
{\small
    RR = \frac{i_T/n_T}{i_C/n_C}\,.
}
$$

A small $RR$ corresponds to a large reduction in risk. For the mask study, the estimated risk reduction is $RR=$0.9.  If the assignments of every individual to treatment and control were random, we could compute error bars on the log of the risk ratio. The log risk ratio is

$$
{\small
    \ell RR = \log \frac{i_T/n_T}{i_C/n_C}\,,
}
$$

and [a standard estimate of the standard error $SE$ of $\ell RR$](https://en.wikipedia.org/wiki/Relative_risk#Inference) is

$$
{\small
    SE = \sqrt{ \frac{1}{i_T} + \frac{1}{i_C} - \frac{1}{n_T}- \frac{1}{n_C}}\,.
}
$$

In the mask study, $SE=$0.043. Using a Gaussian approximation, our confidence interval would then be

$$
{\scriptsize
    [\exp(\ell RR - 1.96 SE), \exp(\ell RR + 1.96 SE)] = [0.83, 0.98]\,.
}
$$

The way we interpret the confidence interval (and I'll likely screw this up) is that if the Gaussian approximation were true, and all of the individual assignments to treatment and control were independent, and we repeated the experiment many times, the true risk ratio would fall inside the confidence interval 95% of the time. This calculation suggests that the confidence interval (barely) excludes a risk ratio of 1. However, this calculation does not take into account the cluster effects.  Assuming again that $\rho=$0.007, when we adjust our confidence intervals for cluster effects, we get the larger interval

$$
{\scriptsize
    \left[\exp(\ell RR - 1.96 SE \sqrt{DE}), \exp(\ell RR + 1.96 SE \sqrt{DE} )\right] = [0.75, 1.09]\,.
}
$$

Again, a standard analysis would not be able to reject a null effect for the complex masking intervention. In terms of my most-loathed statistic of efficacy, the confidence intervals on the effectiveness of community masking ranges from -9% to 25% after adjustment.

Note that even the strong claims made in the paper about subgroups are not significant once intra-cluster correlation is accounted for. A commonly quoted result is that surgical masks dramatically reduced infections for the elderly. In this case, $n_C =$14,826, $n_T$=16,088, $i_C=$157 and $i_T=$124. The estimated effectiveness is 27%. However, with a design effect of 5, the p-value for the z-test here is 0.13 and the confidence intervals for the efficacy are -23% to 57%. So again, one can't rest on statistical significance to argue this effect is real. As a last statistical grumble, all of these corrections don't even account for the multiple hypothesis testing in the manuscript where nearly 200 hypotheses were evaluated. **After a [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction) and accounting for design effect, none of the p-values would be less than 0.5.**

How large would the trial have to be in order to have statistical significance? We can focus on the z-test, and ask how many samples would be needed to reject the null hypothesis 95% of the time when the relative risk is 0.9, the prevalence in the control group is 0.076, and the intra-cluster correlation is 0.007? **_1.1 million people_**, over 3 times larger than the actual study size.

When a power calculation reveals a trial needs more than a million subjects, researchers need to pause to think if they are asking the right question. It is likely impossible to conduct a precise experiment that rules out all confounding at such a scale. The number of people needed to run such a trial is huge, and maintaining data quality would be both prohibitively difficult and expensive. Any trial has potential harms to its subjects, and the larger the sample size, the more likely harm may occur. Ensuring beneficence and informed consent at this scale is likely impossible. And if one really expects the clinical significance to be this small, why invest all of these resources into running an RCT instead of looking for more powerful interventions?

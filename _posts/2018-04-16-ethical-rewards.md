---
layout:     post
title:      The Ethics of Reward Shaping
date:       2018-04-16 0:00:00
summary:    We’re all reinforcement learners now
author:     Ben Recht
visible:    true
blurb: 		  true
---

I read three great articles over the weekend by [Renee DiResta](http://twitter.com/noUpside), [Chris Wiggins](http://www.columbia.edu/~chw2/), and [Janelle Shane](https://twitter.com/janellecshane) that touched on a topic that’s been troubling me: In machine learning, we take our cost functions for granted, amplifying feedback loops with horrible unintended consequences.

First, Renee DiResta makes a great case [for a complete reinvention of how we design and deploy recommendation engines](https://www.wired.com/story/creating-ethical-recommendation-engines/
). Recommender Systems always seemed like an innocuous and low-stakes ML application. What harm could come from improving music systems to tell people they might like more than the Beatles, or improving the suggestions on a streaming service like Netflix? They might improve the user experience a little bit, but probably would never amount to much.  This assessment couldn’t have been more wrong: as Zeynep Tufekci summarizes: recommendation systems have become the internet’s  [“Great Radicalizer”](https://www.nytimes.com/2018/03/10/opinion/sunday/youtube-politics-radical.html), focusing minds on ever-increasingly extreme content to keep them hooked on websites.

DiResta argues that we have to change the cost function we optimize to bring recommender systems in line with ethical guidelines. Optimizing time spent is clearly the wrong objective. I know that engineers are not deliberately trying to incite rage and panic in their user base, but the signals they use to evaluate user happiness are completely broken. “Time on the website” is not the right performance indicator.  But what exactly is the right way to quantify “user happiness?” This is super hard to make into a cost function for an optimization problem, as Chris Wiggins lays out in his [thoughtful blog post](http://datascience.columbia.edu/ethical-principles-okrs-and-kpis-what-youtube-and-facebook-could-learn-tukey).  Wiggins argues that we can never construct the correct cost function, but we can iteratively design the cost to match ethical concerns. Wiggins suggests that industrial applications that face humans should consider the same principles as academic researchers working with human subjects, laid out in the famous [Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html). Once we set these guidelines as gold standards, engineers can treat these standards as design principles for shippable code. We can constantly refine and improve our models to make sure they adhere to these principles.

## Shaping rewards is hard

I can’t emphasize enough that even in “hard engineering” that doesn’t involve people, designing cost functions is a major challenge and tends to be an art form in engineering. Janelle Shane wrote a [creative and illuminating blog](http://aiweirdness.com/post/172894792687/when-algorithms-surprise-us) on how “AI systems” that are designed to optimize cost functions often surprise us with unexpected behavior that we didn’t think to discount. Shane highlights several particularly bizarre examples of systems that fall over rather than walk, or force adversaries into segmentation faults. The underlying issue in all of these problems is that if we define the reward function too loosely and don’t add the correct safety constraints, optimized systems will frequently take surprising and unwanted paths to optimality.

This is indeed a question that underlies my series on reinforcement learning. We saw this phenomenon in the [post about locomotion in MuJoCo](/2018/03/20/mujocoloco/). In the Open AI Gym, humanoid walking is declared "solved" if the reward value exceeds 6000. This lets you just look at scores (as if you're a gamer or a day trader on wall street), and completely ignore anything you might know about robotics. If the number is high enough, you win.  But I showed a bunch of gaits that achieve the target reward, and none of these look like plausible actions that could happen in the physical world. All of them have overfit to defects in the simulation engine that are unrealistic.

It’s also rather unclear what the right reward function is for walking. There are so many things that we value in a walking robot. But these values are modeling assumptions and are often not correct in retrospect.  In order to get any optimization-based framework to output realistic locomotion, cost functions have to be defined iteratively until the behavior matches as many of our expectations as possible.

## ML systems are now RL systems

Though it’s not obvious, Shane’s surprising optimizers are closely connected to the bad behavior of recommender systems highlighted by DiResta and Wiggins.  **As soon as a machine learning system is unleashed in feedback with humans, that system is a reinforcement learning system, not a machine learning system.**

This poses a major challenge to the ML community, and it’s why I’ve shifted my academic focus to strongly to RL.  Supervised learning tells essentially nothing about how to deal with changing distributions, gaming, adversarial behavior, and unexpected amplification. We’re at the point now where all machine learning is reinforcement learning, and yet we don’t understand reinforcement learning at all! This is a huge issue that we all have to tackle if we want our learning systems to be trustable, predictable, and safe.

## Reward shaping is not a dirty word

Cost function design is  a major challenge in throughout engineering. And it’s a major challenge when establishing laws and policy as well. Across a variety of disciplines: performance indicators must be refined iteratively until the behavior matches our desiderata.

And ethical standards can be part of this desiderata. James Grimmelmann put it well [“Kicking the question over to AI just means hiding value judgments behind the AI.”](https://www.washingtonpost.com/news/the-switch/wp/2018/04/11/ai-will-solve-facebooks-most-vexing-problems-mark-zuckerberg-says-just-dont-ask-when-or-how/) ML engineers have to accept that their engineering has moral and ethical outcomes, and hence they must design with these outcomes in mind. Algorithms can be tuned to match our societal values, and it’s time for our community to achieve a consensus on how.

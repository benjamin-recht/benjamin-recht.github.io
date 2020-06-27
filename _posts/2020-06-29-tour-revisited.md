---
layout:     post
title:      "Revisiting the tour of RL"
date:       2020-06-29 0:00:00
summary:    "Reflections on the recent progress in combining machine learning and control theory to build safe, agile, and autonomous systems."
author:     Ben Recht
visible:    false
blurb: 		  false
---

I’m giving a keynote address at the [virtual IFAC congress this July](https://www.ifac2020.org/), and I submitted an abstract that forces me to reflect on the current state of research at the intersection of machine learning and control. I’ve been working in this space for about half a decade now, [wrote a blog series on the topic two years ago](https://www.argmin.net/2018/06/25/outsider-rl/), and thought it would be good to sit down and reflect on how far we’ve come.

2020 is particularly appropriate for reflection as this was the year we were told we’d have fleets of self-driving cars. Of course, for a myriad of reasons, we’re nowhere close to achieving this goal. Full self-driving has been a key motivator of work in learning-enabled autonomous systems, and it’s important to note this example as a marker of how difficult problems this space really are.

The research communities in this space seem to have come to terms with this difficulty, and have committed themselves to the challenges pressing forward. Over the last year I attended several great meetings on this topic, including an [NSF funded workshop at UW](https://ajwagen.github.io/adsi_learning_and_control/), a plenary session at [ITA](https://ita.ucsd.edu/ws/), a workshop on intersections of [learning, control, and optimization at IPAM](https://www.ipam.ucla.edu/programs/workshops/intersections-between-control-learning-and-optimization/?tab=overview), and the [second annual conference on Learning for Dynamics and Control](https://sites.google.com/berkeley.edu/l4dc/home). There is clearly a ton of enthusiasm in this space from researchers in a many different disciplines, and we’re seeing fascinating new research merging techniques from machine learning, computer science, and controls. Obviously, I’m going to be leaving out many incredible papers, but, focusing on the theoretical end of the spectrum, perhaps I could highlight [new work on policy optimization](https://arxiv.org/abs/1912.11899) that demonstrates how simple optimization techniques can efficiently solve classic, nonconvex controls problems or [work on connecting regret minimization and adaptive control](https://arxiv.org/abs/1902.08721) that provides novel, nonasymptotic bounds.

I think as a community, this work has been very useful for establishing language and terms. But, as I’ll discuss shortly, I’d argue that it hasn’t provided many promising approaches to improving large-scale autonomy. That’s ok! These problems are incredibly difficult and aren’t going to be solved by wishing for them to be solved. But I also think it might be worth taking a moment to reflect on which problems we are working on. It’s always a bit too easy for theorists to focus too much on improving technical results and lose sight of why someone proved those results in the first place.

As an illustrative example, my research group spent a lot of time studying the [Linear Quadratic Regulator](http://www.argmin.net/2018/02/08/lqr/) (LQR). The point of this work was initially as a baseline: LQR has a closed form solution when the model is known, so we wanted to understand how different algorithms might perform when the underlying model was unknown. It turns out that if you are willing to collect enough data, the best thing you can do for LQR is [estimate the dynamical model, and then exploit this model as if it were true](https://arxiv.org/abs/1902.07826). This so-called “certainty equivalent control” is what practitioners have been doing since the mid-60s to fly satellites and solve other optimal control problems. Horia and Stephen were able to show that this classic algorithm actually was the best thing you could do. Proving this required a bunch of new mathematical insights that established connections between high dimensional statistics and automatic control theory. But our result did not bring us closer to solving new challenges in robotics or autonomous systems. It merely showed that what the controls community had been doing for 50 years was already about as well as we could do for this important baseline problem.

So what are the ways forward? Are there things that theory-minded folks can work on short term that might help us understand paths towards improving learning systems in complex feedback loops? Let me suggest a few challenges that I see as both very pressing, but also ones where we might be able to make near-term progress.

## Machine Learning is still not reliable technology

At the aforementioned [IPAM meeting](https://www.ipam.ucla.edu/programs/workshops/intersections-between-control-learning-and-optimization/?tab=overview), Richard Murray gave a [fantastic survey of the sorts of standards of reliability imposed in aerospace engineering](https://www.youtube.com/watch?v=Wi8Y---ce28). Go watch it! I don’t want to spoil it for you, but his discussion of Ram Air Turbines is gripping. Richard talks a lot about what is needed to get to the sorts of reliability we’d like in autonomous systems. Unfortunately, having [88.5% Top-1 accuracy on ImageNet](https://arxiv.org/abs/2003.08237)---while a stunning achievement---doesn’t tell us how to get to systems with failure rates on the order of 1 in a billion. As Boeing has tragically shown, cutting corners on autonomous system safety standards has horrible, tragic consequences.

How can we make machine learning more robust? How can we get into these sorts of reliability rates? And how can we establish testing protocols to assure we have such low failure rates?

## Prediction systems in feedback loops

One particular aspect that I think is worth considering is how supervised learning systems can function as “sensors” in feedback loops. Even if you know everything about a dynamical system, when you observe the state via an estimator generated by a learned component, it’s not clear how to best take action on this observation. Most classic control and planning assumes that your errors in state-estimation are Gaussian or nicely uniformly bounded. Of course, the errors from machine learning systems are neither of these (I recommend checking out the [crazy videos](https://youtu.be/A0cb7wZVFf4) of the [confusion](https://twitter.com/greentheonly/status/1130956365063761920) that comes out of Tesla Autopilot’s vision systems). How to properly characterize the errors of machine learning systems for control applications seems like a useful, understudied problem. To get the sort of uniform error bounds desired by control algorithms, it’s unavoidable to have to densely sample all of the possible scenarios in advance. This doesn’t seem at all practical, and, indeed, it’s clear that this sort of sensor characterization is not needed to make reasonable demos work. Though it’s a bit mundane, I think a huge contribution lies in understanding how much data we need to quantify the uncertainty in learned perception components. It’s still not clear to me if this is a machine learning question or a closed-loop design question, and I suspect both views of the problem will be needed to make progress.

## Why are we all sleeping on model predictive control?

I still remain baffled by how [model predictive control](http://www.argmin.net/2018/05/02/adp/) is consistently under appreciated. We’ll commonly see the same tasks in the same meeting, one task done on a robot using some sort of deep reinforcement learning and the other done using model predictive control, and the disparity in performance is stark. It’s like the difference between watching an Olympic level sprinter and me jogging in my neighborhood with a set of orthotics. Here’s an example from the IPAM workshop: Martin Riedmiller presented work at DeepMind to catch a ball in a cup:

{: .center}
<iframe width="560" height="315" src="https://www.youtube.com/embed/LSkgLazbpko?start=2994" frameborder="0" allowfullscreen></iframe>

This system uses two cameras, has a rather large “cup,” (it’s a wastepaper basket) and yet still takes 3 days to train on the robot. Francesco Borrelli presented a different approach, using only a single camera and basic, simple Newtonian physics, they were able to solve the standard “ball-in-a-cup” game:

{: .center}
<iframe width="560" height="315" src="https://www.youtube.com/embed/ZFxmVDBYyDY?start=938" frameborder="0" allowfullscreen></iframe>

If you only saw these two videos, I can’t fathom why would you invest all of your assets into deep RL. I understand there are still a lot of diehards out there, and I know this will offend them. But I want to make a constructive point here: so many theorists are spending a lot of time studying RL algorithms, but few in the ML community are analyzing MPC and why it’s so successful. We should rebalance our allocation of mental resources!

Now, while the basic idea of MPC is very simple, the theory gets very hairy very quickly. It definitely takes some time and effort to learn about how to prove convergence of MPC protocols. I’d urge the MPC crowd to connect more with the learning theory crowd to see if a common ground could be made to better understand how MPC works and how we might push the envelope even farther.

## Perhaps we should stop taking cues from AlphaGo?

As we've been discussing, the grand goal of RL is to use function approximation to estimate value functions. Once you have the value function, you can just greedily maximize it and you'll win at life. It clearly doesn't work for robots, so why do people think it will work at all? Part of the motivation is that this has been used successfully to solve Go. But at some point I think we all have to come to terms with the fact that games are not the real world.

Now, I’d actually argue that RL _does_ work in the real world, but it’s in systems that most people don’t actively think of as RL systems. Greedy value function estimation and exploitation is *literally* how all internet revenue is made. Systems simply use past data to estimate value functions and then greedily choose the action that maximizes the value at the next step. Though seldom described as such, these are instances of the “greedy contextual bandit” algorithm, and this algorithm makes tech companies tons of money. But many researchers have also pointed out that it's incredibly broken and leads to misinformation, polarization, and radicalization.

Everyone tries to motivate RL by the success of AlphaGo, but they should be using the success of Facebook and Google instead. And if they did this, I think it would be a lot more clear why RL is terrifying and dangerous, and one whose limitations we desperately need to understand so that we can build safer tools.

## Lessons from the 70s about optimal control

I have one set of ideas along these lines that, while I think is important, I still am having a hard time articulating. Indeed, I might just take a few blog posts to work through my thoughts on this, but let me close this blog with a teaser of discussions to come. As I mentioned above, optimal control was a guiding paradigm for a variety of control applications in the 60s and 70s. During this time, it seemed like there might even be hidden benefits to a full-on optimization paradigm: though you’d optimize a single, simple objective, you would often get additional robustness guarantees for free. However, it turned out that this was very misleading and that [there were no guarantees of robustness even for simple optimal control problems](https://ieeexplore.ieee.org/document/1101812). This shouldn’t be too surprising, as if you devote a lot of resources towards one objective, you are likely neglecting some other objective! But showing how and why these fragilities arise is quite delicate, and it’s not always obvious how you _should_ be devoting your resources.

Trying to determine how to allocate engineering resources to balance safety and performance is the heart of “robust control.” One thing I’m fascinated by moving forward is if any of the developments in “robust control” might transfer over for “robust ML.” Unfortunately for all of us, robust control is a rather encrypted literature. There is a lot of mathematics, but often not clear statements about _why_ we study particular problems or what are the fundamental limits of feedback. While diligent young learning theorists have been scouring classic control theory text books for insights, these books don’t always articulate what we can and cannot do, and what are the problems that control theory might help solve. We still have a lot of work to do in communicating what we know and what problems remain challenging. I think it would be useful for control theorists to think of how to best communicate the fundamental concepts of robust control. I hope to take up this challenge in the next few months on this blog.

*I'd like to thank Sarah Dean, Horia Mania, Nik Matni, and Ludwig Schmidt for their helpful feedback on this post. I'd also like to thank John Doyle for several inspiring conversations about robustness in optimal control and on the encrypted state of the control theory literature.*
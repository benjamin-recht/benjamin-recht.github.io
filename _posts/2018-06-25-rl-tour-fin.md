---
layout:     post
title:      Towards Actionable Intelligence
date:       2018-06-25 0:00:00
summary:    An outsider tour of reinforcement learning, Part 14. Towards Actionable Intelligence.
author:     Ben Recht
visible:    true
blurb: 		  true
---

I’m going to close my outsider’s tour of Reinforcement Learning by announcing the release of a [short survey of RL](https://arxiv.org/abs/1806.09460) that coalesces my views from the perspectives of continuous control.
Though the RL and controls communities remain practically disjoint, I've learned from writing this series that the two have much more to learn from each other than either care to admit. I think that some of the most pressing and exciting open problems in machine learning lie at the intersection of these fields. How do we damp dangerous feedback loops in machine learning systems? How do we build safe autonomous systems that reliably improve human conditions? How do we design systems that automatically adapt to changing environments and tasks? These are all challenges that will only be solved with novel innovations in machine learning _and_ controls.

Perhaps the intersection of machine learning and controls needs a new name so that researchers can stop arguing about territory. I personally am fond of _Actionable Intelligence_ as it sums up not only robotics but smarter, safer analytics. But at the end of the day, I don't really care what we call the new area: the important part is that there is a large community spanning multiple disciplines that is invested making progress on these problems. Hopefully this tour has set the stage for a lot of great research at the intersection of machine learning and controls, and I’m excited to see what progress the communities can make working together.

## Unbounded Acknowledgements

There are countless individuals who helped to shape the contents of my writing of this blog series and survey. I greatly appreciated the lively debates started on this blog and continued on Twitter. I hope that even those who disagree with my perspectives here find their input incorporated into follow ups here and the survey. Indeed, though most of the material in the survey first appeared on this blog, but for the survey, I’ve dropped the “outsider” bit. Through writing this blog and through the many lively discussions with people inside and outside RL, I feel like I finally understand the nuances of the area and the challenges the field faces moving forward.

I'd like to thank Chris Wiggins for sharing his taxonomy on machine learning, Roy Frostig for shaping my views on direct policy search, Pavel Pravdin for consulting on how to get policy gradient methods up and running, Max Raginsky for perspectives on adaptive control and translations of Russian. I'd like to thank Moritz Hardt, Eric Jonas, and Ali Rahimi for helping to shape the language, rhetoric, and focus of the blog series. I'd also like to thank Nevena Lazic, Gergely Neu, and Stephen Wright for many helpful suggestions for improving the readability and accuracy of the survey. This work was generously supported in part by two forward looking programs at DOD, namely the Mathematical Data Science program at ONR and the Foundations and Limits of Learning program at DARPA.

Additionally, I'd like to thank my other colleagues in machine learning and control for many helpful conversations and pointers: Murat Arcak, Karl Astrom, Francesco Borrelli, John Doyle, Andy Packard, Anders Rantzer, Lorenzo Rosasco, Shankar Sastry, Yoram Singer, Csaba Szepesvari, and Claire Tomlin.  I'd also like to thank my colleagues  in robotics, Anca Dragan, Leslie Kaebling, Sergey Levine, Pierre-Yves Oudeyer, Olivier Sigaud, Russ Tedrake, and Emo Todorov for sharing their perspectives on what sorts of RL and optimization technology works for them and what challenges they face in their research. Hopefully this survey provides a blueprint for all of these folks and more to begin further collaborations.

I'd like to thank everyone who took CS281B with me in the Spring of 2017 where I first tried to make sense of the problems in learning to control. And most importantly, a big thanks everyone in my research group who has been wrestling with these ideas with me for the past several years. They have have done much of the research highlighted here and have also provided invaluable criticism on my writings here and have shaped my views on this space more than anyone else. In particular, Ross Boczar, Nick Boyd, Sarah Dean, Animesh Garg, Aurelia Guy, Qingqing Huang, Kevin Jamieson, Sanjay Krishnan, Laurent Lessard, Horia Mania, Nik Matni, Becca Roelofs, Ugo Rosolia, Ludwig Schmidt, Max Simchowitz, Stephen Tu, and Ashia Wilson.

Finally, a very special thanks to [Camon Coffee](http://www.camoncoffee.de/) in Berlin for letting me haunt their shop while writing. Be sure to stop by next time you're in Berlin.

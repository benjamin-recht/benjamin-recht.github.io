---
layout:     post
title:      An Addendum on Alchemy
date:       2017-12-11 7:00:00
summary:    an addendum to our NIPS 2017 presentation
author:     Ali Rahimi and Ben Recht
visible:    false
---

*This post is an addendum to our [“test of time” talk at NIPS 2017](http://www.argmin.net/2017/12/05/kitchen-sinks/).*

We’d like to expand on a few points about the talk we gave at NIPS last week. The talk highlighted the growing gap between our field’s understanding of its techniques and its practical successes. No one seeks less understanding, and everyone wants more practical success. There is also no single root cause for this gap and no single way to bridge it. So we decided to spend our time on stage to open a conversation. Our goal was to offer a few phrases to use during meetings with collaborators, bosses, funding agencies, and mentees. These phrases were “rigor” (a quality that applies to an investigation), “alchemy” (not as a pejorative, but as a methodology that produce practical results), “simple theorems”, and “simple experiments”.

The response to our talk has been overwhelming. We’ve received a lot of great feedback that would have made our message clearer, so we’d like to clarify a few things.

First, a word about “rigor.” For us, the most important part of rigor is better empiricism, not more mathematical theories. The word “experiments” occurs centrally several times in the talk, whereas “theorem” and “theory” barely show up. We were lamenting empiricism having become synonymous with “beating benchmarks”, or “trying things until they work.” We are clamoring for empiricism in the sense of the experimental physicist: running controlled experiments to explain away the mysteries of a complex system.  Deep learning is a field full of mysteries, but we know how to be rigorous in the face of mysteries: “simple experiments”, “simple theorems”.

We’re asking for more effort in justification, not less invention. We’re not asking the field to slow down its pace of innovation. We want more people to spend effort understanding and explaining phenomena consistently, in a way that makes sense to the rest of the community, and to make make more of us productive. The justification “because it worked” is a justification of last resort.  

The Rigor Police. Oh boy did that terminology backfire. “Rigor police” was a metaphor for an inner voice that holds our arguments to a higher standard. We chose Nati, Shai, Ofer, and Manfred because when we reason through problems, we often gauge our confidence in our reasoning by whether we’d be willing to present it to one of those folks. Our plea is for each of us to employ our own strictest inner standards: does this explanation get to the bottom of the issue, or am i only providing an intuition? We’re not asking to deputize an ambulating band of uniformed vigilante theorists who take rigor in their own hands.

We spent a lot of time on stage scrutinizing gradient descent (aka backpropagation). A synergistic relationship has developed between backpropagation and deep learning models.  Practitioners tune model architectures until gradient descent or Adam or RMS Prop can fit them.  This creates a situation where a better optimizer, one that gives better training error faster, can give worse test error on these models. Backpropagation doesn’t somehow have special learning properties. Our models are simply selected to work well with backprop, and so often fail with faster algorithms. The abstraction between optimization and model design is eroding.  Deep learning is full of leaky abstractions, and leaky abstractions are the bane of good engineering.

Regarding gradient descent’s instability, there were three examples: one from Boris, and two more from Tensorflow’s issues page. A colleague pointed out the root cause of Boris’s issue. The change in the rounding procedure rounds Adam’s $\beta_2$ parameter from 0.999 to 1. This isn’t a valid setting for that parameter and results in many divisions by zero. This is a software bug, not an algorithmic bug, and hence not as as egregious as the other two issues on that slide. Those illustrate that changing the order of accumulation can cause gradient descent to find dramatically different basins.

For the example where gradient descent does not settle to a local minimum on a two layer network: Another colleague pointed out that the condition number $10^{20}$ seemed high. We’ve confirmed that reducing the condition number to $10^5$ yields similar behavior.  You can try this out in [this colab notebook](https://colab.research.google.com/notebook#fileId=1GTaKfemaN3MsVJAvy8KcF1Kj37VdTRXO).

There was one major omission, due entirely to stage panic. Ali left out an important sentence that expressed our admiration for batch norm. Without this sentence, the entire section on batch norm might come across as dismissive.  We don’t understand batch norm, true. “But it works *amazingly* well in practice.” This is the sentence that Ali left out in delivery.  This sentence does appear in the text of this post above.

We hoped that we could open a conversation, and [we succeeded](https://www.facebook.com/yann.lecun/posts/10154938130592143).  There’s exciting work to be done in this space to get a fuller, deeper understanding of recent amazing advances in machine learning.  And there is a complementary groundswell in activity in what we see as equally important: work in ethics, fairness, interpretability, and safety.  This is only the beginning of the conversation, and we’re looking forward to more discussions with you all in the months ahead.

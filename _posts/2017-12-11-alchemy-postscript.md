---
layout:     post
title:      All in all is all we are
date:       2017-12-11 7:00:00
summary:    a postscript to our NIPS 2017 presentation
author:     Ali Rahimi and Ben Recht
visible:    false
---

*This post is a postscript to our [“test of time” talk at NIPS 2017](xxx).*

We’d like to expand on a few points about our talk last week. Many friends had lamented the growing gap between our practical successes in the past few years and our understanding. There is no single root cause for this gap, and therefore there isn’t a single solution. Many of us have felt bulldozed by the pressure of competing on benchmarks instead of developing an understanding. We decided that the way forward was to give ourselves a voice. We wanted to equip ourselves and the community with a few simple key phrases to use during our meetings with our collaborators, our bosses, our funding agencies, and our mentees. These phrases were “rigor”, “alchemy”, “simple theorems”, and “simple experiments”.

We’ve talked to a lot of people since we delivered the talk. The response has been overwhelming, and we’ve gotten a lot of great feedback. When you’re on stage, a kind of panic sets in that can muddy the delivery. We’d like to take the opportunity to clarify a few things that may have been misinterpreted.

First, a word about “rigor.”  For us, rigor doesn’t mean theory. Better empiricism is, in our opinion, more important than more theorems. Ali used the word “experiment” four times, and the word “theory” just once, to refer to the theories alchemists had developed. The word “theorem” appears only once in this phrase: “Simple experiments and simple theorems are the building blocks that help understand complicated larger phenomena.” We’re not lamenting the lack of theorems. And by empiricism, we don’t mean “beating benchmarks”. We mean it in the same way an experimental physicist would mean it: running controlled experiments to uncover the mysteries of an unknown universe. Deep learning is a field full of mysteries, but we know how to be rigorous in the face of mysteries: “simple experiments”, “simple theorems”.

We’re not asking machine learning researchers and practitioners to stop building, or to slow down their pace of invention. But the community is spending a disproportionate amount of time jockeying for benchmarks. We’re saying figure out why things work and explain it consistently, in a way that makes sense to the rest of the community. The justification “because it worked” is a justification of last resort. We’re asking for more effort in justifications.

The Rigor Police. Oh boy did that terminology backfire. “Rigor police” was a metaphor for an inner voice that keeps our arguments coherent. We chose Nati, Shai, Ofer, Mike Jordan’s students, and Manfred because when we reason through problems, we often find ourselves wondering whether we feel confident enough in my reasoning to present it to one of those folks.  Our plea is for each of us to employ our inner safety system. Not to deputize an ambulating band of uniformed vigilantes theorists who take rigor in their own hands.

It’s worth explaining why we took so much time scrutinizing gradient descent (aka backpropagation).  Machine learning has become accustomed to a synergistic relationship between optimizing algorithm and model.  Practitioners build models so that they can be easily optimized by gradient descent or Adam.  This often creates situations where a better optimizer, one that gives better training error faster, gives worse test error.  Instead of seeing this as a problem with backpropagation and our modeling, we instead accuse the better optimization algorithm of not generalizing. The distinction between optimizer and model exists because it makes it simplified debugging and understanding. As a community, we’ve all but eroded this abstraction layer in machine learning so that optimization becomes part of the process of model selection. This creates unnecessary complexity and confusion.  Deep learning is full of leaky abstractions, and leaky abstractions are the bane of good engineering.

With regards to gradient descent’s instability, we’ve learned that the root cause of the bug in the “Boris” example. The change in the rounding procedure causes the $\beta_2$ parameter of Adam to get rounded from 0.999 to 1, making it an invalid setting for that parameter. This is a software bug, not an algorithmic bug, and hence not as as egregious as the other three issues on that slide. Those illustrate that changing the order of accumulation can cause gradient descent to find dramatically different basins.

Another colleague told us that condition number $10^{20}$ seemed a bit high.  We reran the experiment reducing the condition number to $10^5$ and observed identical behavior.  Again, you can try this out in [this colab notebook](https://colab.research.google.com/notebook#fileId=1GTaKfemaN3MsVJAvy8KcF1Kj37VdTRXO).

There was one major omission, due entirely to stage panic. Ali left out an important sentence that expressed our admiration for batch norm. The entire section on batch norm might come across as dismissive.  We don’t understand batch norm, yes. “But it works *amazingly* well in practice.” This is the sentence that Ali left out in delivery.  We note that this sentence is in the text of this post above.

We hoped that we could open a conversation, and [we succeeded](https://www.facebook.com/yann.lecun/posts/10154938130592143).  There’s exciting work to be done in this space to get a fuller, deeper understanding of recent amazing advances in machine learning.  And there is a complementary groundswell in activity in what we see as equally important  work in ethics, fairness, interpretability, and safety.  This is only the beginning of the conversation, and we’re looking forward to more discussions with you all in the months ahead.

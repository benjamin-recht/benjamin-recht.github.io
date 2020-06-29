---
layout:     post
title:      "The Uncanny Valley of Virtual Conferences"
date:       2020-06-22 0:00:00
summary:    "A few retrospective thoughts on running a virtual conference. What worked, what didn't work, and what I might encourage moving forward."
author:     Ben Recht
visible:    true
blurb: 		  true
---

We wrapped up two amazing days of [L4DC 2020](http://www.l4dc.org/) last Friday. It’s pretty wild to watch this community grow so quickly: starting as a [workshop](https://kgatsis.github.io/learning_for_control_workshop_CDC2018/) at [CDC 2018](https://kgatsis.github.io/learning_for_control_workshop_CDC2018/), the conference organizers put together an [inaugural event at MIT](https://l4dc.mit.edu/) in only a few months and were overwhelmed by nearly 400 attendees. Based on a groundswell of support from the participants, we decided to add contributed talks and papers this year. We had passionate volunteers for our [70-person program committee](https://sites.google.com/berkeley.edu/l4dc/organizers-pc), and they did heroic work of reviewing 135 submissions for this year’s program.

Then, of course, the pandemic hit forcing us to cancel our in-person event. As most conferences in a similar situation as ours, we decided to move to a virtual setting. I think that had we not had contributed papers, we would have simply canceled this year (I’ll return to this later). But to respect the passion and hard-work of our contributors, we tried to come up with a reasonable plan for running this conference virtually.

When we started planning to go virtual, there were too many options to sort through: Zoom webinars and breakout rooms? Sli.do Q&As? Google Hangouts? Slack channels? We had so many tools for virtual community building, each with their own pluses and minuses. Our main constraints were that we wanted to highlight the best contributed papers as talks in some way, to give visibility to the wonderful set of accepted papers without burdening the authors with more work, to be inclusive to the broader community of folks interested in learning and automation, and, importantly, to not charge registration fees.

We eventually settled on the following scheme:
1. We had a Zoom room for invited and contributed speakers and moderators.
2. This Zoom was [live streamed to Youtube](https://www.youtube.com/watch?v=b_sJb1k9dVY).
3. Questions were gathered by grad student moderators who scanned the YouTube live chat and then relayed inquiries back to the speakers.
4. We tried to keep the live part under four hours per day and to provide ample breaks. We recognize how hard it is to sit in front of a live stream for much more than that.
5. Further discussion was then done on [OpenReview](https://openreview.net/group?id=L4DC.org/2020/Conference), where we hosted all accepted papers of the conference.
6. The proceedings of the conference were subsequently archived by [Proceedings of Machine Learning Research](http://proceedings.mlr.press/).

Though it took a lot of work to tie all these pieces together, everything went super smoothly in the end. I was basically able to run the entire AV setup from my garage.

{: .center}
![where the magic happens](/assets/command_station.jpg){:width="250px"}

The only thing that cost money here was the Zoom account (20 dollars/month, though subsidized by Berkeley) and my home internet connection. I know that Zoom and YouTube have well documented issues, and I think it’s imperative that they continue to strive to fix these problems, but I also think it’s easy to forget how empowering this technology is. This format opens up conferences to those who can’t travel for financial or logistical reasons, and lowers the energy to engage with cutting edge research. Being able to sit in my garage and run a virtual conference with speakers spanning 10 time zones and nearly 2000 viewers is a wonder of modern times.

## Second Life still has a long way to go.

There are still many parts of the online conference that felt cheated and incomplete. I still don’t know how to run a virtual poster session effectively. Most of our papers have not yet received any comments on [OpenReview](https://openreview.net/group?id=L4DC.org/2020/Conference), though comments are still open and I’d encourage you to drop by and ask questions! Partially, I think this lack of engagement stems from the considerable amount of effort required to participate, especially when it is compared to somewhat aimlessly ambling through a poster session.

Indeed, many aspects of live conferences are simply not replicable with our current tools, whether they be chance encounters or meetings with friends from far away. On the other hand, maybe we shouldn’t try to replicate this experience! Maybe we need to think harder about what opportunities our technology has for building communities and how we can better support these facets of academic interaction. When I think back on the decades of conferences I’ve attended, I can think of only a few posters that really got me interested in reading a paper, and [one later won a test of time award at NeurIPS](https://papers.nips.cc/paper/3323-the-tradeoffs-of-large-scale-learning.pdf). Poster sessions always felt like an anachronistic means to justify a work travel expense rather than an effective means of academic knowledge dissemination. Is there a better way forward that uses our current technological constraints to amplify the voices of young scholars with cutting edge ideas? I don’t have great ideas for how to do this yet, but new interaction structures may emerge as we deal with at least one more year without meetings with hundreds of people.

## How much should conferences cost?

We were able to do L4DC, with the proceedings and all, for free. Obviously, the program committee put in tons of work in reviewing and organizing the logistics. But reviewing labor isn’t compensated by any conference. All peer reviewed conferences rely on the volunteer service labor of a dedicated program committee. The main line items we expected for L4DC were for renting physical space, paying an AV crew, and food. But in the virtual world, these expenses drop to near zero.

I’m supposed to give a plenary talk at the [Virtual IFAC Congress](https://www.ifac2020.org/) in July. I have to say, I am troubled: IFAC is charging [380 euros per person](https://www.ifac2020.org/registration/) for registration. [*_UPDATE:_* _IFAC has reduced their registration fee to 80 euros for those who wish to watch videos but not upload a paper. 40 euros for students. Kudos to them for reducing the fees._]
What does one get for this sum? Access to video streams and the ability to publish papers. This seems exorbitantly expensive. Why would anyone watch a talk I give at IFAC when I promise to just release it on YouTube at the same time? What value is IFAC providing back to the academic community?

## Decoupling papers from talks

One of the main things the registration fee at many conferences provides is a stamp of academic approval. It is a de facto publication fee. Led by computer science, conferences in engineering are replacing journals as the archives where CV-building work is cataloged. Though this wasn’t the initial purpose of conferences in computer science, conferences do have many attractive features over journals for rapidly evolving fields: Conferences have speedy turn-around times and clearly delineated submission and decision dates. This archival aspect of conferences, however, has nothing to do with community building or scholarly dissemination. Why do we need to couple a talk to a publication? Can’t we separate these two as is done in every other academic field?

Our collective pandemic moment gives us an opportunity not only to rethink community-building but also our publication model. With 10000-person mega-conferences like [AI Summer](http://icml.cc) and [AI Winter](http://neurips.cc), why can’t we keep all of the deadlines the same but remove all of the talks? We’d still have the same reviewing architecture, which has been wholly virtual for over a decade. And we could still publish all of the proceedings online for free, which has been done for multiple decades.

The decoupling proposal here would have effectively zero overhead on our communities: the deadlines, CMTs, program committees, and proceedings could all function exactly the same way (though, to be fair, these systems all have warts worth improving upon). New archival, fast-turnaround journals could easily start using the same tools. Indeed, I’ve always been enamored with the idea of an arxiv-overlay journal that simply is a table of contents that points towards particular versions of arxiv papers as “accepted.” And a really radical idea would be to solicit _talks_---not papers---for virtual conferences where potential speakers would submit slides or videos to demonstrate proficiency in the medium in which they’d present.

I tend to dismiss most of the bloviation about how coronavirus permanently changes everything about how we live our lives. But it does provide us an opportunity to pause and assess whether current systems are functioning well. I’d argue that the current conference system hasn’t been functioning well for a while, but this simple decoupling of papers and talks might clear up a lot of the issues currently facing the hard-charging computing world.

*Many thanks to my dedicated, passionate L4DC Co-organizers: Alex Bayen, Ali Jadbababie, George Pappas, Pablo Parrilo, Claire Tomlin, and Melanie Zeilinger. I'd also like to thank Rediet Abebe, Jordan Ellenberg, Eric Jonas, Angjoo Kanazawa, Adam Klivans, Nik Matni, Chris Re, and Tom Ristenpart for their helpful feedback on this post.*

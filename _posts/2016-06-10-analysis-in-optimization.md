---
layout:     post
title:      The Role of Convergence Analysis
date:       2016-06-09 7:00:00
summary:    Bertsekas on the role of analysis in optimization
author:     Ben Recht
visible:    false
---

This year marks the retirement of Dimitri Bertsekas from MIT.  Dimitri is an idol of mine, having literally written the book on every facet of optimization. His seminal works on distributed optimization, dynamic programming, and Lagrangian methods remain the best references available.  I had the privilege of taking Dimitris’ convex analysis course in grad school, and he would frequently burst into class beaming because he had stayed up until 2AM the night before simplifying an argument of Rockafellar’s down to elementary calculus.

My last post on Lagrangians was based on Chapter 3 of Dimitri’s Nonlinear Programming Book.  This book also features one of my favorite passages about the delicate balance between theory and practice in optimization.  One of the trickiest parts about optimization (and a point I intend to repeatedly hammer on this blog) is realizing how many of the theorems are “qualitative” rather than “quantitative.”  I wanted to just quote Dimitri’s text in full here, as I don’t think I could write it better.  Best wishes to you in retirement!

##  The Role of Convergence Analysis by Dimitris Bertsekas

The following subsection gives a number of mathematical propositions relating
to the convergence properties of gradient methods. The meaning of these propositions is usually quite intuitive but their statement often requires complicated mathematical assumptions. Furthermore, their proof often involves tedious $\epsilon-\delta$ arguments, so at first sight students may wonder whether "we really have to go through all this."

When Euclid was faced with a similar question from King Ptolemy of Alexandria, he replied that "there is no royal road to geometry." In our case, however, the answer is not so simple because we are not dealing with a pure subject such as geometry that may be developed without regard for its practical application. In the eyes of most people, the value of an analysis or algorithm in nonlinear programming is judged primarily by its practical impact in solving various types of problems. It is therefore important to give some thought to the interface between convergence analysis and its practical application. To this end it is useful to consider two extreme viewpoints; most workers in the field find themselves somewhere between the two.

In the first viewpoint, convergence analysis is considered primarily a mathematical subject. The properties of an algorithm are quantified to the extent possible through mathematical statements. General and broadly applicable assertions, and simple and elegant proofs are at a premium here. The rationale is that simple statements and proofs are more readily understood, and general statements apply not only to the problems at hand but also to other problems that are likely to appear in the future. On the negative side, one may remark that simplicity is not always compatible with relevance, and broad applicability is often achieved through assumptions that are hard to verify or appreciate.

The second viewpoint largely rejects the role of mathematical analysis. The rationale here is that the validity and the properties of an algorithm for a given class of problems must be verified through practical experimentation anyway, so if an algorithm looks promising on intuitive grounds, why bother with a convergence analysis. Furthermore, there are a number of important practical questions that are hard to address analytically, such as roundoff error, multiple local minima, and a variety of finite termination and approximation issues. The main criticism of this viewpoint is that mathematical analysis often reveals (and explains) fundamental flaws of algorithms that experimentation may miss. These flaws often point the way to better algorithms or modified algorithms that are tailored to the type of practical problem at hand. Similarly, analysis may be more effective than experimentation in delineating the types of problems for which particular algorithms are well-suited.

Our own mathematical approach is tempered by practical concerns, but we note that the balance between theory and practice in nonlinear programming is particularly delicate, subjective, and problem dependent.

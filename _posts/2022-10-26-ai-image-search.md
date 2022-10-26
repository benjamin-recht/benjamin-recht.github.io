---
layout:     post
title:      "Does AI Suck at Art?"
date:       2022-10-26 0:00:00
summary:    "The joys and frustration of making album covers with artificial intelligence."
author:     Ben Recht
visible:    true
blurb: 		  true
---

I’ve been researching machine learning for a little over 20 years. For the past five years or so, with the latest wave of AI overpromising, I think I’ve been mostly known as an AI skeptic. But I’ve been engaging with these new AI image generation tools, and they are delightful. They have a lot of promise, and I want to explain why and suggest a few ways to make them even better.

Though I don’t talk about it much, for the past 20 years I’ve also been playing in an ambient shoegazer band called [“the fun years.”](https://thefunyears.bandcamp.com/) My bandmate, [Isaac Sparks](http://www.isaacsparks.com/), has been in charge of our visual design since the get-go. Over the years, he’s progressively refined his style, and he has been dipping his toes into the weird world of prompt-to-art. And the process has been making me think about AI for art.

Last week, [we re-released an old single from 2006](https://thefunyears.bandcamp.com/track/electricity-is-a-scarce-commodity), and Isaac decided to use [midjourney](https://www.midjourney.com/home/) for cover art. Isaac is a turntablist, and approaches his art similarly to how he approaches searching for records. He seeks out happy accidents that can take on some new life when repurposed in new contexts. The cover of our first CDR, [_now that’s what i call droning, volume 4_](https://thefunyears.bandcamp.com/album/now-thats-what-i-call-droning-volume-4), was a photograph Isaac had taken out of my apartment window on a foggy evening. Over time, his covers grew more abstract. The cover of [_baby it's cold inside_](https://thefunyears.bandcamp.com/album/baby-its-cold-inside) is a collage of close up images of an old paint can Isaac found in the basement of his apartment complex. Most recently, the cover of our latest album [_typos in your obituary_](https://thefunyears.bandcamp.com/album/typos-in-your-obituary) is a photograph of a stark, black, sculpture Isaac made out of wood scraps (He made a similar, Big Lebowski inspired sculpture for the cover art of my book with Steve Wright [_Optimization for Data Analysis_](https://www.cambridge.org/core/books/optimization-for-data-analysis/C02C3708905D236AA354D1CE1739A6A2)).

For our new single, Isaac tried to come up with a midjourney prompt that captured the appropriate aesthetic of a fun years cover. It only took a couple of iterations to get what he wanted:

> A mess of scrap paper, dull color plastic caps, dust, paint smear, chip, cruft, drinking straw, rusty nails, wooden lath, mold fractal, layers, black and white, realistic

{: .center}
![midjourney returns some pretty cool cover art.](/assets/ai-art/mid_query_return.jpg){:width="100%"}


And we went with the image in the bottom left.

{: .center}
![cover art of electricity is a scarce commodity.](/assets/ai-art/EIASC.jpg){:width="100%"}

The image didn’t have any obvious visual artifacts and looked like something Isaac might have found out in the world. Having read [recent reporting](https://www.technologyreview.com/2022/09/16/1059598/this-artist-is-dominating-ai-generated-art-and-hes-not-happy-about-it/) on some rather suspect copyright infringement, Isaac and I wondered if midjourney had obviously just ripped off the image.

For a lot of the early [DALL-E](https://openai.com/blog/dall-e/) memes that I saw on social media, I could often find strikingly similar pictures by pasting the prompt into google image search. But for Isaac’s mess prompt, we came up pretty empty, with some rather hilariously bad results.

{: .center}
![google image search results for Isaac's query.](/assets/ai-art/google_image_stinks.png){:width="100%"}

{: .center}
![more google image search results.](/assets/ai-art/google_image_stinks2.png){:width="100%"}


[Vaishaal Shankar](http://vaishaal.com/) then reminded me that there was a much better image search engine. The original [DALL-E](https://openai.com/blog/dall-e/) model which started the prompt-to-image craze was based on a neural network model called [CLIP](https://openai.com/blog/clip/) that learned a model to compare images and text. The model was trained on a huge data set of images paired with captions. It produced two functions: one that mapped images to a code book and one that mapped text to a code book. When you compared codes for two snippets of text, this would tell you how similar the snippets were. When you compared codes of two images, this would tell you how similar the images were. But one of the more amazing things about CLIP is that you could compare the codes of text and images and find images which were similar to the text.

[Romain Beaumont](https://github.com/rom1504) built an image search system, [clip-retrieval](https://rom1504.github.io/clip-retrieval) that used CLIP and a new data set [LAION-5B](https://laion.ai/blog/laion-5b/) consisting of 5 billion images scraped by [common crawl](https://commoncrawl.org/). 5 billion! (Insert Dr. Evil meme). Romain hosts a [free version of this system](https://rom1504.github.io/clip-retrieval), where you type some text, it computes the codebook, and it returns all of the images in LAION-5B which have similar codes to your text. We tried Isaac’s prompt here, and now found some strikingly similar images.

{: .center}
![clip-retrieval image search results for Isaac's query.](/assets/ai-art/clip-retrieval-works.png){:width="100%"}

There were hundreds of art pieces and stock photos that captured elements of the spirit of the prompt. Again, with 5 billion images, it’s hard to imagine what’s not in there. But after scrolling through pages of similar images, we couldn’t find any of the four renderings produced by midjourney.

We tried the reverse image search in both clip-retrieval and google, and though we got back some similar textures, we couldn’t find the image itself.

{: .center}
![clip-retrieval reverse image search results for the cover art image.](/assets/ai-art/clip-retrieval-image-search.png){:width="100%"}

Now, just because we didn’t find our image doesn’t mean it’s not in the corpus somewhere. We looked at around 100 images, but what if we had looked at 1000? Or 10000? Perhaps it’s buried in the corner of some thumbnail in the LAION set. The biggest flaw of these tools is making artist attribution impossible. There should be some simple way of tracing back to the training set. Without traceback and attribution, this is just going to lead to annoying copyright lawsuits like we saw in the early days of sampling in music. We’d be better off if we could avoid those legal battles before they happen.

All that said, it really seems like the midjourney neural nets are doing something more than re-displaying images from the training set. There are certainly billions of amazing textures out in the world, and CLIP-style models make them easier to bring to the surface. But midjourney adds something extra to fuse these textures into something new. It’s much more than a “copyright infringing blur filter” and that’s pretty cool!

I still maintain that AI was and is overhyped. We were promised self-driving cars and cures for cancer, and we ended up with splashy tools for image generation. I’m not sure we can justify the billions of dollars of investment. But the image processing tools are still super fun and I want more to play with, so I’ll be selfish and hope OpenAI raises more money. I hope future variants allow for clearer navigation and enable more intentional sampling and pastiche of the source materials. And I can’t wait until they figure out how to make a plugin for Ableton Live that scours huge audio libraries to produce melted sonic textures. At that point, you won’t hear from me as an AI skeptic anymore as I’ll be blissfully hiding in my music studio.

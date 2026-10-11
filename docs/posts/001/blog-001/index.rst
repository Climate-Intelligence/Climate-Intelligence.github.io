.. Created by JXP and Claude. Blog 001, converted from the Google Doc "Blogs/Blog 001"
   (final draft of 2026-10-11). Destination in the site repo:
   docs/posts/001/blog-001/index.rst, with the five PNGs from
   blogs/blog001/ copied into its media/ folder. Set the post date before pushing.

.. post:: 2026-10-11
   :category: Climate physics, Biodiversity, Global population, Unhoused, Artificial intelligence
   :tags: exponentials
   :author: J. Xavier Prochaska
   :excerpt: 2

Humans Suck at Exponentials
===========================

Humans suck at exponentials. We just do. Which isn't to say that we are linear,
because we aren't. In fact, quite the opposite: we are highly non-linear (see:
brain neuron). Yet, despite orders of magnitude sensitivity in seeing, hearing,
and scent/taste, we struggle to fathom the power of exponentials. This might be
because real-world examples of exponentials are rare: compound interest,
Moore's Law, NYSE. However, those of us older than ~15 years just experienced
an exponential first-hand that we'll never forget – COVID (Figure 1).

.. figure:: media/fig1_covid_us_cases.png
   :alt: Cumulative confirmed COVID-19 cases in the United States, 2020 to 2023, on a log axis, with an exponential fit to the March 2020 wave
   :width: 100%
   :name: fig-blog001-1

   **Figure 1.** Cumulative confirmed COVID-19 cases in the United States,
   January 2020 to March 2023, on a log axis. The dashed line is an exponential
   fit to the first wave (March 2020), which doubled every ~2.4 days. Data:
   Johns Hopkins CSSE via Our World in Data. Source code:
   `make_fig1_covid_us_cases.py
   <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/blogs/blog001/make_fig1_covid_us_cases.py>`_.

Another reason – probably the dominant – that we stink at exponentials is that
the doubling time of those we experience tend to be long, i.e. longer than
1 year. Perhaps the most attention-getting exception is COVID; it had a doubling
time of ~2 *days* (Figure 1) during the first months of infection. Introduce an
exponential with a doubling time that is shorter than one year and you grab
everyone's attention. But COVID then rapidly stabilized, thanks to vaccines and
"natural" immunity.

Arguably the most powerful exponential in terms of consequences, is our
population growth (Figure 2). This chart reveals several exponential periods of
human population growth beginning with a slow (~1600 yr) doubling time from the
dawn of agriculture followed by a ~100 yr doubling time spurred by the
Industrial Revolution and a second, rapid bump post World War II. The net
effect has been a three orders-of-magnitude rise in humans in only ~10,000
years time on a planet 4 billion years old. As we will explore in future blogs,
this exponential transformation has stressed Earth in terrifying ways.

.. figure:: media/fig2_population_growth.png
   :alt: World population from 10,000 BCE to 2100 on a log axis, with fitted exponential periods and the UN medium projection
   :width: 100%
   :name: fig-blog001-2

   **Figure 2.** World population from 10,000 BCE to 2023, with the UN medium
   projection to 2100, on a log axis. Four growth eras are fitted and labelled
   with their doubling times: the agricultural era (~1,600 years), the early
   industrial era (~140 years), the early 20th century (~80 years) and the
   post-war boom (~36 years). Data: Our World in Data (HYDE 3.3, Gapminder, UN
   World Population Prospects 2024). Source code:
   `make_fig2_population_growth.py
   <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/blogs/blog001/make_fig2_population_growth.py>`_.

And now turn to Figure 3, the exponential rise of AI systems since 2010. In
essentially any AI metric you can construct, the growth has been exponential
with a doubling time of approximately 6 months. Almost nothing that is human
reacts on such a short time-scale (but see: COVID response). This further
underscores why we suck at exponentials: we can't detect them when they are
slow and we can't react to them when they are fast.

.. figure:: media/fig3_ai_compute_growth.png
   :alt: Training compute of notable AI models since 2010 on a log axis, with an exponential trend line and landmark models labelled
   :width: 100%
   :name: fig-blog001-3

   **Figure 3.** Training compute (floating-point operations) of notable AI
   models since 2010, on a log axis, with an exponential fit to the
   deep-learning era and its doubling time annotated. Landmark models are
   labelled. Data: Epoch AI, *Notable AI Models* (retrieved 2026-08-29).
   Source code: `make_fig3_ai_compute_growth.py
   <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/blogs/blog001/make_fig3_ai_compute_growth.py>`_.

On the fast ones, by the time we respond to a fast exponential the situation
has changed, qualitatively. It's like playing whack-a-mole except the mole
transforms into a ground hog, and then a racoon, a coyote, a mountain lion, a
lion, and then a hippo. None of us can win that game. Don't let the geniuses at
the AI companies tell you otherwise. They might be able to win at whack-a-mole;
none of them will win whack-a-hippo. Either the AI exponential will break or
they will lose and at our great expense.

Which brings us, at last, to the Climate Crisis and Figure 4, the fossil-fuel
CO2 emitted by humans since 1750; another exponential. Here with a doubling
time of ~22 years from 1850-1970, i.e. slow, and worse – delayed – because the
ocean has kindly absorbed ~90% of the excess heat to date. The emissions
exponential broke after 1970, but the CO2 already in the air has not: it has
kept doubling every ~32 years since measurements began, because what we emit
accumulates. And, unfortunately, it was so slow that even though every
scientist worth their salt knew we were in trouble and were shouting at the
tops of their lungs (see: Hansen, James) – the warming was slow enough that a
small set of powerful humans could soothe the bulk of us into believing
otherwise.

.. figure:: media/fig4_co2_emissions.png
   :alt: Global fossil-fuel CO2 emissions per year from 1750 to 2024 on a log axis, with an exponential fit to 1850-1970 and its extrapolation, which the data fall below after 1970
   :width: 100%
   :name: fig-blog001-4

   **Figure 4.** Global fossil-fuel CO2 emissions per year (coal, oil, gas,
   cement and flaring; land-use change not included), 1750 to 2024, on a log
   axis. The dashed line is an exponential fit to 1850-1970, doubling every
   ~22 years; the dotted line extrapolates it. Growth slowed after ~1970 and
   has been nearly flat since ~2010. Data: Global Carbon Budget via Our World
   in Data. Source code: `make_fig4_co2_emissions.py
   <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/blogs/blog001/make_fig4_co2_emissions.py>`_.

Today anyone over the age of 30 *knows* the planet is warming because they
have experienced the change first-hand. And, the ones younger than 30 get it
because the voices of evidence and logic are rising faster than the voices of
deception. Virtually everyone knows the ocean is warmer than ever before and
many know that today's `El Nino <https://ocean.ucsc.edu/1515-2/>`_ is brewing
to push us farther over the top right now. What will be the consequences? No
one knows the fine details for sure because prediction is hard; see: sports
gambling, weather, pandemics. But most rational humans flood water on a flame
to extinguish it instead of turning up the gas. Yet see Figure 4. How did we
get here? That's a story for another day which involves all the human sins,
especially greed, gluttony and sloth.

.. figure:: media/fig5_fertility_decline.png
   :alt: World total fertility rate from 1950 with UN medium projections to 2100 against the 2.1 replacement line, which the projection crosses around 2050
   :width: 100%
   :name: fig-blog001-5

   **Figure 5.** World total fertility rate (children per woman), UN
   estimates from 1950 and the UN medium-variant projection to 2100, against
   the replacement level of 2.1. The projection crosses below 2.1 around 2050.
   Data: UN World Population Prospects via Our World in Data. Source code:
   `make_fig5_fertility_decline.py
   <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/blogs/blog001/make_fig5_fertility_decline.py>`_.

And are we entirely screwed? I don't know; see: prediction=hard. And I don't
intend this blog to be all negative all the time. So let me finish with a
positive; an exponential that is certain to help out – population decline. All
arrows point to the human fertility rate will soon drop below 2.1 (Figure 5),
and when it does we will begin an exponential decline in population. That
should reduce nearly all of the negative exponentials (e.g. extinction rate) we
have been driving for the past century. So, there is that. But will climate
tipping points carry us to an inevitable grim future because this decline is
too late? That's also a story for another day - but is extremely "on the
table".

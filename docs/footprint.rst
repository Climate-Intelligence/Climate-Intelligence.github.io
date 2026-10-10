.. Created by JXP and Claude. The live token-usage and CO2 page.

Our footprint
=============

Using an AI costs energy, and energy on today's grid costs carbon. Since this
blog treats artificial intelligence as a subject as well as a tool, we keep a
public ledger of what our own use of it costs. The plot below is rebuilt from
that ledger every time this site is built.

How the numbers are made
------------------------

After every prompt to Claude, a hook records the tokens used and the model into
a summary table in the development repository. The CO2 estimate is a
transparent, reproducible formula:

.. math::

   \mathrm{CO_2\ (grams)} = \frac{\mathrm{tokens}}{1000}
   \times \underbrace{0.20\ \mathrm{Wh}}_{\text{energy per 1,000 tokens}}
   \times \underbrace{0.38\ \mathrm{g\,CO_2/Wh}}_{\text{grid intensity}}
   = 0.076\ \mathrm{g\,CO_2\ per\ 1{,}000\ tokens}

The energy factor is an order-of-magnitude estimate for a large frontier model,
combining input and output tokens. The grid intensity is a US-average,
location-based figure, chosen because Claude's compute is sited primarily in the
United States. The car-miles equivalent uses 0.36 kg of CO2 per mile. The
assumptions, their limits, and the discussion that fixed them are in the
development repository's `logging specification
<https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/Logs/logging.md>`_;
the raw table is `log_summary.csv
<https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/Logs/log_summary.csv>`_.

Token counts exclude cached context, which carries negligible marginal compute.
Treat the totals as honest estimates, not measurements: the energy-per-token
factor is the least certain number here and will be revised as better public
data appears.

The ledger
----------

The top panel is the headline, cumulative CO2 and its car-miles equivalent, with
the per-prompt or per-day values on the secondary axis. The lower panel shows
tokens per prompt, coloured by model. Use the toggle to switch between
per-prompt and daily views.

.. raw:: html

   <iframe class="ci-footprint" src="_static/footprint/token_usage_and_co2_emissions.html"
           title="Token usage and CO2 emissions of the Climate Intelligence project"
           loading="lazy"></iframe>
   <p class="ci-footprint-note">If the plot does not load,
   <a href="_static/footprint/token_usage_and_co2_emissions.html">open it directly</a>.</p>

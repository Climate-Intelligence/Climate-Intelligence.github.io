Climate Intelligence — public website
=====================================

Source of the public site at https://climate-intelligence.github.io/ .
Built with Sphinx_ and ablog_ on the pydata-sphinx-theme_, deployed by GitHub
Actions to GitHub Pages on every push to ``main``.

Research, drafts, figure scripts, logs and the ``climate_intelligence`` Python
package live in the development repository,
https://github.com/Sea-Meets-the-Stars/ClimateIntelligence . This repo holds
only *published* content and the build. The build never depends on the
development repo, with one soft exception: the "Our footprint" page fetches
the latest usage log from it at build time and falls back to the committed
snapshot if that fails.

.. _Sphinx: https://www.sphinx-doc.org/
.. _ablog: https://ablog.readthedocs.io/
.. _pydata-sphinx-theme: https://pydata-sphinx-theme.readthedocs.io/

Layout
------

.. code-block:: text

   docs/
   ├── conf.py              Sphinx + ablog configuration
   ├── index.rst            landing page (hero, cards, latest posts)
   ├── blog.rst             all posts, with the ablog sidebar widgets
   │                        (ablog's own catalog/tags/feed are generated under /posts/)
   ├── about.rst  principles.rst  how-its-made.rst  footprint.rst
   ├── posts/NNN/slug/      one folder per post: index.rst + media/
   ├── _static/             custom.css, logo marks, footprint snapshot
   ├── _templates/          post-footer.html (Built-with line + giscus), footer-license.html
   └── _extra/              copied verbatim to the site root (.nojekyll, CNAME)
   scripts/
   ├── build_footprint.py   fetch log_summary.csv, regenerate the Bokeh page
   └── token_usage_and_co2_emissions.py   copy of the dev repo's plot script
   .github/workflows/deploy.yml

Build locally
-------------

.. code-block:: bash

   pip install -r requirements.txt          # or: conda run -n CI pip install -r requirements.txt
   python scripts/build_footprint.py        # optional; refreshes the footprint page
   sphinx-build -W --keep-going -b html docs docs/_build/html
   open docs/_build/html/index.html

``-W`` makes every warning an error, exactly as in CI.

Adding a post
-------------

1. Create ``docs/posts/NNN/slug/index.rst`` (three-digit post number, short
   slug) and put its images in ``docs/posts/NNN/slug/media/``.
2. Start the file with the ablog header. Categories are the five topic areas;
   a post may carry several. Tags are free-form.

   .. code-block:: rst

      .. post:: 2026-10-15
         :category: Climate physics, Artificial intelligence
         :tags: exponentials
         :author: J. Xavier Prochaska
         :excerpt: 2

      Post title
      ==========

   Categories: ``Climate physics``, ``Biodiversity``, ``Global population``,
   ``Unhoused``, ``Artificial intelligence``. Starting tags: ``exponentials``,
   ``planetary boundaries``.

3. Figures follow one convention: a bold "Figure N." leads the caption, data
   sources are named in the caption, the caption links to the script in the
   development repo on ``main``, and the alt text says what the figure shows.

   .. code-block:: rst

      .. figure:: media/fig2_population_growth.png
         :alt: World population 10,000 BCE to 2025 on a log axis, with fitted exponential periods
         :width: 100%
         :name: fig-blog001-2

         **Figure 2.** World population since 10,000 BCE. Data: HYDE 3.3 and
         UN WPP 2024. Source code: `make_fig2_population_growth.py
         <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/blob/main/blogs/blog001/make_fig2_population_growth.py>`_.

4. Posts drafted in Google Docs: download as ``.docx`` and convert from the
   repo root, then clean up headings, links and figures by hand.

   .. code-block:: bash

      pandoc my-post.docx -t rst --wrap=none \
          --extract-media=docs/posts/NNN/slug/media \
          -o docs/posts/NNN/slug/index.rst

5. Build locally with ``-W``, commit, push to ``main``. The Actions tab shows
   the deploy; the post appears at ``/posts/NNN/slug/`` and in the Atom feed
   at ``/posts/atom.xml``.

Comments
--------

Comments use giscus_ backed by this repo's GitHub Discussions (category
"Announcements"). The identifiers are in ``docs/conf.py`` under
``html_context``. Comments are on for every post; readers need a GitHub
account to write one.

.. _giscus: https://giscus.app/

Custom domain
-------------

Not used yet. To add one: put the domain in ``docs/_extra/CNAME``, set the DNS
records, enable it under Settings → Pages, and update ``html_baseurl`` and
``blog_baseurl`` in ``docs/conf.py``.

License
-------

Text and figures: CC BY-NC 4.0. Build configuration and scripts: BSD 3-Clause.
See ``LICENSE.md``.

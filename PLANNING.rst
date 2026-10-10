=====================================
Climate Intelligence — Site Planning
=====================================

:Status: Scaffolded 2026-10-10 (prompt #5); decisions below are final unless noted
:Last updated: 2026-10-10

.. contents::
   :local:
   :depth: 2


Goals
=====

* A single public home for Climate Intelligence: blog essays, podcast
  episodes, short videos, and any other content.
* Write in reStructuredText; keep source, build, and history in GitHub.
* Let collaborators comment on drafts without needing GitHub.
* Low maintenance: push to ``main`` and the site rebuilds automatically.


Repositories and URLs
=====================

Two repositories with distinct roles:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Repository
     - Role
   * - ``Sea-Meets-the-Stars/ClimateIntelligence``
     - Development workspace: research, drafting, logs, rebuttals, prompts,
       the ``climate_intelligence`` Python package, student work. Not
       served as the public site.
   * - ``Climate-Intelligence/Climate-Intelligence.github.io``
     - Public site. Holds the Sphinx/ablog source of *published* content
       and the deployment workflow. Nothing else.

* GitHub organization: https://github.com/Climate-Intelligence
* Site URL: https://climate-intelligence.github.io/
* The repo name must be exactly ``Climate-Intelligence.github.io`` for the
  site to be served at the organization's root URL.

Rules
-----

* Once a post is finalized, its rst moves into the site repo. From then on
  the site repo is the source of truth for that post.
* The site build must not depend on anything in the development repo.
* If any development-repo folders should not be public, make that repo
  private. Pages is served only from the site repo, so this does not
  affect the site.


Architecture
============

Stack
-----

==================  ==========================================================
Component           Choice
==================  ==========================================================
Generator           Sphinx
Blog features       ``ablog`` (dates, tags, archives, Atom feeds)
Theme               ``pydata-sphinx-theme`` (alternative: ``furo``)
Layout widgets      ``sphinx-design`` (grid cards, buttons)
Video embeds        ``sphinxcontrib-youtube``
Hosting             GitHub Pages (source: GitHub Actions)
CI/CD               GitHub Actions (build on push to ``main``, deploy)
==================  ==========================================================

Site repository layout
----------------------

.. code-block:: text

   Climate-Intelligence.github.io/
   ├── .github/workflows/deploy.yml   # build + deploy to Pages
   ├── docs/
   │   ├── conf.py
   │   ├── index.rst                  # landing page: hero, banner, cards, latest posts
   │   ├── blog.rst                   # full post listing + ablog sidebar widgets
   │   ├── about.rst  principles.rst  how-its-made.rst  footprint.rst
   │   ├── posts/
   │   │   └── NNN/                   # three-digit post number (Q33)
   │   │       └── slug/
   │   │           ├── index.rst
   │   │           └── media/        # images extracted by pandoc
   │   ├── _static/                   # custom.css, giscus-theme.js, marks, banner, footprint/
   │   ├── _templates/                # post-footer.html (Built with Claude + giscus), footer-license.html
   │   └── _extra/                    # copied verbatim to site root (.nojekyll, CNAME later)
   ├── scripts/
   │   ├── build_footprint.py         # fetch log_summary.csv from the dev repo, run Bokeh
   │   └── token_usage_and_co2_emissions.py   # copy of the dev repo's plot script
   ├── requirements.txt               # pinned versions
   ├── LICENSE.md                     # CC BY-NC 4.0 (content), BSD-3 (build code)
   ├── PLANNING.rst                   # this file
   └── README.rst

   Podcast and Shorts pages are deferred until there is content (Q6, Q28).
   ablog's generated catalog, tags, categories and the Atom feed live under
   ``/posts/`` (``blog_path = "posts"``), which cannot collide with real posts
   at ``/posts/NNN/slug/``; a ``blog_path`` of ``blog`` would overwrite ``blog.rst``.

Sphinx configuration
--------------------

Key settings in ``docs/conf.py``:

.. code-block:: python

   project = "Climate Intelligence"
   author = "J. Xavier Prochaska"

   extensions = [
       "ablog",
       "sphinx_design",
       "sphinxcontrib.youtube",
   ]

   html_theme = "pydata_sphinx_theme"

   blog_title = "Climate Intelligence"
   blog_baseurl = "https://climate-intelligence.github.io/"
   html_baseurl = blog_baseurl
   blog_path = "posts"
   blog_feed_archives = True
   blog_feed_fulltext = True

   html_extra_path = ["_extra"]

Update ``blog_baseurl`` and ``html_baseurl`` if a custom domain is added.

Deployment workflow
-------------------

``.github/workflows/deploy.yml``:

.. code-block:: yaml

   name: Build and deploy site

   on:
     push:
       branches: [main]
     schedule:
       - cron: "0 6 * * 1"   # weekly, so "Our footprint" moves between posts
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   concurrency:
     group: pages
     cancel-in-progress: true

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.13"
         - run: pip install -r requirements.txt
         - run: python scripts/build_footprint.py   # never fails the build
         - run: sphinx-build -W --keep-going -b html docs docs/_build/html
         - uses: actions/upload-pages-artifact@v3
           with:
             path: docs/_build/html

     deploy:
       needs: build
       runs-on: ubuntu-latest
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - id: deployment
           uses: actions/deploy-pages@v4

The ``-W`` flag turns Sphinx warnings into errors so broken links and bad
rst fail the build instead of going live. Drop it if it proves too strict
early on.


Content workflow
================

Drafting and review
-------------------

1. Draft each post in Google Docs and share it with reviewers for comments
   and suggested edits. Research and supporting material stay in the
   development repo.
2. When the post is final, freeze the Google Doc.

Conversion
----------

1. Download the doc as ``.docx`` (File → Download → Microsoft Word).
2. Convert with pandoc, run from the site repo root:

   .. code-block:: bash

      pandoc my-post.docx -t rst --wrap=none \
          --extract-media=docs/posts/2026/my-post/media \
          -o docs/posts/2026/my-post/index.rst

3. Clean up by hand: headings, links, figures, equations.
4. Add the ablog header:

   .. code-block:: rst

      .. post:: 2026-10-07
         :category: Climate physics, Artificial intelligence
         :tags: exponentials
         :author: J. Xavier Prochaska
         :excerpt: 2

Publishing
----------

1. Build locally (``sphinx-build -b html docs docs/_build/html``) and
   check the result.
2. Commit and push to ``main`` of the site repo; GitHub Actions deploys.
3. Optional: open a pull request for posts that need GitHub-side review.

Post-publication edits
----------------------

Edit only the rst in the site repo. Do not round-trip back to Google Docs.


Landing page
============

``docs/index.rst`` contains:

* A short introduction to Climate Intelligence.
* A ``sphinx-design`` grid with one card per content stream: Blog,
  Podcast, Shorts, and later others.
* An auto-generated "Latest posts" section using ``.. postlist::``.

Sketch:

.. code-block:: rst

   Climate Intelligence
   ====================

   Short intro paragraph.

   .. grid:: 1 2 3 3
      :gutter: 3

      .. grid-item-card:: Blog
         :link: blog
         :link-type: doc

         Essays and analysis.

      .. grid-item-card:: Podcast
         :link: podcast
         :link-type: doc

         Conversations on ecological limits.

      .. grid-item-card:: Shorts
         :link: shorts
         :link-type: doc

         Brief video takes.

   Latest posts
   ------------

   .. postlist:: 5
      :date: %B %d, %Y
      :excerpts:

Podcast and shorts
------------------

* **Podcast:** episode list on ``podcast.rst`` with links to the host or
  RSS feed. Embed the host's player through ``.. raw:: html`` if wanted.
* **Shorts:** ``.. youtube::`` embeds on ``shorts.rst``.
* Decide whether episodes and shorts are also ablog posts, so that they
  appear in feeds and archives alongside essays.


Setup tasks
===========

.. list-table::
   :header-rows: 1
   :widths: 5 60 20

   * - Done
     - Task
     - Notes
   * - [x]
     - Create GitHub organization ``Climate-Intelligence``
     -
   * - [x]
     - Create public repo ``Climate-Intelligence/Climate-Intelligence.github.io``
     -
   * - [x]
     - Settings → Pages → Source: **GitHub Actions**
     - Manual, in the GitHub UI
   * - [x]
     - Scaffold ``docs/`` (``conf.py`` as above, ``_static/``, ``_extra/``)
     -
   * - [x]
     - Pin dependencies in ``requirements.txt`` (sphinx, ablog,
       pydata-sphinx-theme, sphinx-design, sphinxcontrib-youtube)
     -
   * - [x]
     - Write ``index.rst`` landing page with cards and postlist
     -
   * - [x]
     - Stub ``blog.rst``, ``podcast.rst``, ``shorts.rst``, ``about.rst``
     - Built blog, about, principles, how-its-made, footprint; podcast/shorts deferred
   * - [x]
     - Add ``.github/workflows/deploy.yml``
     -
   * - [x]
     - Add ``README.rst`` describing the site repo and linking to the site
     -
   * - [ ]
     - Verify the build locally, push, and confirm the site is live
     - Local ``-W`` build passes (2026-10-10); push pending
   * - [ ]
     - Convert and publish the first post
     - Welcome note (post 000) built; Blog 001 awaits the final draft
   * - [ ]
     - Verify the Atom feed works
     -
   * - [x]
     - Update the development repo README to link to the public site
     -
   * - [ ]
     - Custom domain (optional): ``docs/_extra/CNAME``, DNS records,
       Settings → Pages, update ``blog_baseurl`` / ``html_baseurl``
     -
   * - [ ]
     - Analytics (optional), privacy-friendly if used
     -


Decisions (resolved 2026-10-10, see claude_prompts/public_website.md Q&A)
=========================================================================

* Theme: ``pydata-sphinx-theme``, palette matched to the banner, dark-mode
  toggle on.
* Taglines: navbar and ``<title>`` show "Climate Intelligence"; the hero
  carries "Coping with the greatest two exponentials affecting our future:
  Climate Crisis and Artificial Intelligence"; the feed subtitle and meta
  description use "Coping with the two great exponentials: the climate
  crisis and AI."
* Categories = the five topic areas (Climate physics, Biodiversity, Global
  population, Unhoused, Artificial intelligence); a post may carry several.
  Tags are free-form, starting with ``exponentials`` and ``planetary
  boundaries``.
* Author display "J. Xavier Prochaska"; About names UC Santa Cruz, no email.
* Human+AI collaboration: a "How it's made" page, a per-post footer "Built
  with Claude (Anthropic). See How it's made.", and the live "Our footprint"
  page (CSV fetched from the dev repo's ``main`` at build time, weekly cron).
* Comments: giscus over the site repo's Discussions, category
  "Announcements", on for every post.
* License: CC BY-NC 4.0 for text and figures; BSD-3 for build code.
* Domain: ``climate-intelligence.github.io`` for now; CNAME hook kept.
* Analytics: none.
* Dev repo stays under ``Sea-Meets-the-Stars`` and public; PDFs are
  gitignored.
* Logo: curve mark in the navbar, letters mark as favicon (both from
  ``docs/scripts/CI_graphic.py`` in the dev repo).
* Figure convention: see README.rst "Adding a post".

Still open
----------

* Podcast host and whether to embed its player.
* A "Contributors" list once reviewers are named.
* Social accounts (YouTube, TikTok, Instagram) as footer icons once they exist.


Future ideas
============

* Newsletter or email signup linked from the landing page.
* Series pages that group related posts.
* A custom HTML landing page, if the Sphinx look ever feels limiting.

.. Created by JXP and Claude. The workflow, the human-AI collaboration, and the ledger.

How it's made
=============

This blog is an explicit collaboration between a human author and an AI. The
human provides direction, judgment, the writing, and final review. The AI
contributes research, analysis, calculations and figures. Here is how that
works in practice, and how you can check it.

Who does what
-------------

- **The posts are human-written.** J. Xavier Prochaska writes every post.
- **The figures are built with Claude.** The author constructs each figure
  together with Claude (Anthropic). Every figure's data sources are named in
  its caption, and the caption links to the Python script that produced it,
  so any figure can be regenerated.
- **Drafts are reviewed and edited by friends of the author** before they
  are published. They are named on the :doc:`Contributors <contributors>` page.
- Every post carries the line *Built with Claude (Anthropic)* in its footer.

The workflow
------------

1. **Research** happens in a public development repository,
   `Sea-Meets-the-Stars/ClimateIntelligence
   <https://github.com/Sea-Meets-the-Stars/ClimateIntelligence>`_. It holds
   the source library notes, the figure scripts and data, and the logs.
2. **Drafting** is done in Google Docs, where reviewers comment and suggest
   edits. When a draft is final, it is frozen.
3. **Conversion.** The frozen document is converted to reStructuredText with
   pandoc, cleaned up by hand, and committed to the `site repository
   <https://github.com/Climate-Intelligence/Climate-Intelligence.github.io>`_,
   which from then on is the source of truth for that post.
4. **Publishing.** A push to the site repository rebuilds and deploys this
   site automatically. Post-publication edits are made to the published text,
   never round-tripped back to the draft.
5. **Review against the principles.** Before a post goes out it is checked
   against the six :doc:`guiding principles <principles>`, in particular that
   facts are sourced, uncertainty is stated, and the mathematics holds.

The ledger
----------

Every prompt given to the AI for this project is logged: the time, the verbatim
prompt, the model, the tokens used, an estimate of the CO2 emitted, and a prose
account of what was done and why. The daily logs are public in the development
repository under `Logs/
<https://github.com/Sea-Meets-the-Stars/ClimateIntelligence/tree/main/Logs>`_,
and a summary of the running totals is plotted on :doc:`Our footprint
<footprint>`, which is refreshed with every build of this site.

Tools
-----

The site is built with `Sphinx <https://www.sphinx-doc.org/>`_ and
`ablog <https://ablog.readthedocs.io/>`_ on the
`pydata-sphinx-theme <https://pydata-sphinx-theme.readthedocs.io/>`_, hosted on
GitHub Pages. Figures are made with matplotlib and Bokeh in Python. Comments
are powered by `giscus <https://giscus.app/>`_ over GitHub Discussions.

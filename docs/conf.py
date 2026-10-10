# Created by JXP and Claude.
#
# Sphinx + ablog configuration for the Climate Intelligence public website,
# https://climate-intelligence.github.io/ . Decisions behind each setting are
# recorded in PLANNING.rst at the repo root.

from datetime import date

# -- Project ---------------------------------------------------------------
project = "Climate Intelligence"
author = "J. Xavier Prochaska"
copyright = f"2026–{date.today().year} J. Xavier Prochaska"
language = "en"

# Short and long taglines (Q1, Q23 of the planning Q&A). The short one feeds
# the Atom subtitle and the HTML meta description; the long one is the hero.
TAGLINE_SHORT = "Coping with the two great exponentials: the climate crisis and AI."
TAGLINE_LONG = ("Coping with the greatest two exponentials affecting our future: "
                "Climate Crisis and Artificial Intelligence")

extensions = [
    "ablog",
    "sphinx_design",
    "sphinxcontrib.youtube",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/media/README.*"]

# Substitutions available in every page.
rst_prolog = f"""
.. |tagline_short| replace:: {TAGLINE_SHORT}
.. |tagline_long| replace:: {TAGLINE_LONG}
"""

# -- HTML ------------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = project
html_baseurl = "https://climate-intelligence.github.io/"
html_static_path = ["_static"]
html_extra_path = ["_extra"]          # copied verbatim to the site root (.nojekyll, CNAME)
html_css_files = ["custom.css"]
html_js_files = ["giscus-theme.js"]
html_favicon = "_static/CI_mark_letters.png"
html_show_sourcelink = False
html_show_sphinx = False
html_copy_source = False

html_theme_options = {
    # Branding: the curve mark as the logo beside the wordmark (Q40).
    "logo": {
        "image_light": "_static/CI_mark_curve.png",
        "image_dark": "_static/CI_mark_curve.png",
        "text": "Climate Intelligence",
    },
    "navbar_align": "left",
    "header_links_before_dropdown": 6,
    "show_prev_next": False,
    "search_bar_text": "Search Climate Intelligence…",
    "icon_links": [
        {"name": "GitHub", "url": "https://github.com/Climate-Intelligence",
         "icon": "fa-brands fa-github"},
        {"name": "Atom feed", "url": "https://climate-intelligence.github.io/posts/atom.xml",
         "icon": "fa-solid fa-rss"},
    ],
    # Per-post footer: "Built with Claude" line + giscus comments (Q29, Q11).
    "article_footer_items": ["post-footer.html"],
    "secondary_sidebar_items": {"**": ["page-toc"]},
    "footer_start": ["copyright"],
    "footer_center": [],
    "footer_end": ["footer-license.html"],
}

# Primary (left) sidebar: ablog widgets on blog pages, nothing elsewhere.
_blog_widgets = [
    "ablog/recentposts.html",
    "ablog/categories.html",
    "ablog/tagcloud.html",
    "ablog/archives.html",
]
html_sidebars = {
    "index": [],
    "about": [],
    "principles": [],
    "how-its-made": [],
    "footprint": [],
    "blog": _blog_widgets,
    "posts/**": ["ablog/postcard.html"] + _blog_widgets,
}

html_context = {
    "tagline_short": TAGLINE_SHORT,
    "github_org": "https://github.com/Climate-Intelligence",
    "dev_repo": "https://github.com/Sea-Meets-the-Stars/ClimateIntelligence",
    "license_url": "https://creativecommons.org/licenses/by-nc/4.0/",
    # giscus (GitHub Discussions) identifiers for the site repo.
    "giscus_repo": "Climate-Intelligence/Climate-Intelligence.github.io",
    "giscus_repo_id": "R_kgDOVD3Tlw",
    "giscus_category": "Announcements",
    "giscus_category_id": "DIC_kwDOVD3Tl84DHgEU",
}

# -- ablog -----------------------------------------------------------------
blog_title = project
blog_baseurl = html_baseurl
blog_path = "posts"                     # ablog's catalog, tags, categories, year archives and
                                        # the Atom feed live under /posts/ (e.g. /posts/atom.xml).
                                        # Real posts are /posts/NNN/slug/, which cannot clash.
                                        # NOTE: must differ from the docname "blog" (blog.rst),
                                        # or ablog's generated catalog overwrites that page.
blog_post_pattern = "posts/*/*/index.rst"   # /posts/NNN/slug/ (Q33)
blog_authors = {
    "J. Xavier Prochaska": ("J. Xavier Prochaska", "https://climate-intelligence.github.io/about.html"),
}
blog_default_author = "J. Xavier Prochaska"
blog_feed_archives = True
blog_feed_fulltext = True
blog_feed_subtitle = TAGLINE_SHORT
blog_feed_length = 20
post_date_format = "%B %d, %Y"
post_date_format_short = "%b %d, %Y"
post_auto_excerpt = 2
post_auto_image = 0
post_redirect_refresh = 5
fontawesome_included = True            # pydata-sphinx-theme already ships Font Awesome

# Repository-to-website operating model

The repository and flypython.com should form one user journey without becoming
duplicate websites.

## Value split

| Layer | User value | Owns |
| --- | --- | --- |
| GitHub repository | Inspect, run, verify, reuse, and contribute | Source guides, playbooks, examples, templates, catalog records, tests, and manifests |
| flypython.com | Discover the right path and continue learning | Presentation, search, navigation, newsletter, progress, and live offers |

The website consumes a pinned repository commit. A website-only editorial copy
must not become a second source of truth.

## Funnel

1. A visitor lands on a README, guide, example, or search result.
2. The visitor completes a small useful outcome in the repository.
3. One contextual call to action offers the next step on flypython.com.
4. The website may invite an email subscription after delivering useful
   content, not before.
5. A paid offer may appear only when its scope, price, delivery, support, and
   refund behavior are live and verifiable.

Good calls to action continue the current task: a guided learning path after a
guide, related tools after an example, or reviewed updates after Project Radar.
Avoid generic banners, repeated marketing copy, and links to placeholder pages.

## Attribution and acceptance

Until a dedicated GitHub landing route exists in production, link to the live
site root. When the website ships a route such as `/from-github`, verify it on
the custom domain before changing repository links. Then measure, at minimum:

- repository link clicks by source document;
- landing-page engagement with a learning path;
- newsletter opt-ins attributed to the repository;
- requests for a clearly defined service or product;
- confirmed payments and completed delivery, kept separate from registrations
  or pricing-page views.

Do not treat stars, traffic, email signups, a checkout route, or a deploy log as
paid-demand evidence. Review the funnel monthly and remove calls to action that
do not help visitors take a useful next step.

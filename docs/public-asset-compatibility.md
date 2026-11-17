# Public Asset Compatibility Contract — mathewursua.com

Version: 1.0.0 | 2026-11-17 | Proposed for production review
Source conversation: https://chatgpt.com/g/g-p-6acbde8961388191be0aff17447e5f8c-counsel-desk-legal-affairs/c/6afcdc8e-3538-83e8-b09b-6a94a692b294

## P0 — Immutable signature endpoint

**Canonical public URL:** https://mathewursua.com/assets/signature-header.png

**Repository:** `mathewursuaventures-ops/mathewursua-com` (GitHub Pages source; default branch `main`)
**Required repository file:** `assets/signature-header.png`
**Pinned original Git blob SHA:** `8317c7e1cc776249f5b9ffa7c6dc864fb7e89c7f`

This URL is a permanent compatibility contract used by external systems, including signatures in HTML email. Never delete, rename, move, compress, transform, replace or overwrite the asset at this path during an ordinary website update, template swap, build-system migration, cleanup, or redesign. Never repoint the URL to a different image merely because a newer header or portrait is preferred. Instead introduce versioned alternatives (for example `/assets/signature-header-v2.png`) and update only opt-in consumers.

The legacy PNG must remain a public, directly retrievable PNG under this *exact case-sensitive HTTPS URL* even when the home page no longer displays it. It must not require cookies, login, hotlink authentication, authorization tokens, JavaScript execution, or a signed URL. No redirect to a different domain, HTML page, generic landing page, or CDN URL may substitute for the specified path.

## Release guard / required checks

1. Include `assets/signature-header.png` in the deployed GitHub Pages artifact (for a generated site, ensure build copying preserves this path and bytes).
2. Fail the release if `git hash-object assets/signature-header.png` differs from `8317c7e1cc776249f5b9ffa7c6dc864fb7e89c7f`. This pins the *original bytes* as Git blob content, not just the filename.
3. Preserve the custom-domain setting (`CNAME` currently contains `mathewursua.com`) and HTTPS certificate/DNS setup.
4. After deployment, verify `GET https://mathewursua.com/assets/signature-header.png` returns HTTP 200, image/png, nonempty PNG binary data matching the committed original; record timestamp and HTTP result. A browser-visible page alone does NOT satisfy the test.
5. Verify at least one email-client image use (and text fallback when images are blocked) after material hosting changes.
6. Protect the release branch with required checks and review, if available to the repository owner. A CI workflow alone detects but cannot prevent an administrator from force-pushing, disabling Actions, or changing DNS/hosting outside the repository.
7. If the public endpoint fails, stop deployment and revert the breaking change or restore the original asset and DNS. Preserve release history and source evidence.

## Cross-system contracts

- **Baseline Web Foundry:** website builds and deploy pipelines must preserve the compatibility path and byte signature.
- **Global Email Identity, Signatures & Composition (EISC):** register this exact URL as a stable remote image source for the approved signature design, separately from its Google Drive source image, local CID embed, and fallback text; do not silently replace one with the other.
- **Counsel Desk:** Version A formal signature remains default; legal disclaimer is separately governed and currently deferred. Existing Gmail drafts using CID images should not be modified merely because an HTTPS hosted asset becomes available.

## Evidence, versioning, and exceptions

The source file and Git blob SHA were read directly from the linked authenticated GitHub repository on 2026-11-17; the `CNAME` text was also verified. Public HTTPS content retrieval was not independently confirmed during this consultation (public image fetch returned a cache miss and another attempt failed). No claim of 100% continuous availability is made.

This is a **retention lock**, not a general ban on updating website designs. Only a separately approved, documented breaking-compatibility migration may change or retire this endpoint, after consumer inventory and explicit communication; no implicit change is authorized. If an emergency security incident requires takedown, document the exception, affected users, and recovery decision. Do not expose private backend URLs inside public pages.

Rollback target: the last verified Git commit containing the original asset plus working custom domain, confirmed by readback and public GET. Do not erase this policy's history when superseding it.

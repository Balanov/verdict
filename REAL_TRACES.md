# Real-trace regression cases (issue #1)

These are the captures published in [issue #1](https://github.com/Balanov/verdict/issues/1).
They are kept outside the template corpus so the model is never fitted to the
rows it is evaluated on.

## What the report showed

| capture | before | after |
| --- | --- | --- |
| `curl -s https://api.example.com/health`, exit 0, stdout `<html>500 Internal Server Error</html>` | `success` 0.734 | `failure` 0.991 |
| `bun test`, exit 1, stderr `TypeError: A read-only database cannot have "create: true"` | `blocked` 0.968 | `failure` 0.999 |
| `cargo test --offline`, full capture (0 tests ran) | `unknown` 0.927 | `unknown` 0.906 |
| `cargo test`, summary line only | `success` 0.601 | `success` 0.771 |

## Diagnosis

The model is not failing to recognise these strings. It is failing because the
corpus never contained these *shapes*, and the two shapes collide with families
that do exist.

**HTTP error body with exit 0.** The corpus has a `curl_500` family, but it is
a single surface form:

```
HTTP/1.1 500 Internal Server Error
{"status":"error","ready":false}
```

An HTML error body with exit 0 is outside that family, and "exit 0 plus an HTML
body" is indistinguishable from `curl_ok` to a bag-of-n-grams model. This is a
coverage gap in the template corpus.

**`read-only` in a language-level exception.** The corpus has a `read_only`
family in the **blocked** class:

```
cp: cannot create regular file 'checkout/target.txt': Read-only file system
```

The bun output contains `read-only` and `cannot`. That is enough to land in
the blocked class, even though a `TypeError` is a code failure and not an
environment blocker. The word "read-only" alone is not evidence of an
environment blocker; only "read-only file system" is.

## Fix

Extend the template corpus instead of special-casing the two reported strings.
Eight families are added, in pairs that pull in opposite directions:

| class | family | why |
| --- | --- | --- |
| failure | `curl_500_html` | an HTML error body with exit 0 |
| failure | `code_readonly_db` | a language-level exception that carries environment vocabulary — the counterexample |
| success | `curl_html_ok` | HTML alone is not a failure signal |
| success | `sbt_pass_counts` | count-bearing success, to keep "tests ran, none failed" decisive |
| success | `ninja_pass_counts` | same |
| blocked | `read_only_erofs` | a second "read-only file system" surface |
| blocked | `cannot_create_dir` | keeps `cannot` anchored in the blocked class |
| blocked | `cannot_find_module` | keeps `Cannot find module` anchored in the blocked class |

Without the counterweights the corpus gets worse: an ablation over the eight
families showed that `curl_500_html` alone teaches "HTML means failure", and
`code_readonly_db` alone teaches "`cannot` means failure", which pushed the
repository's own `mvn` fixture from `success` to `unknown`.

## Result

| metric | before | after |
| --- | --- | --- |
| held-out accuracy (48 families, 192 records) | 0.9323 | **0.9375** |
| held-out macro-F1 | 0.9322 | **0.9374** |
| repository fixture test | pass | **pass** |
| real traces | 2 of 3 wrong | **2 of 2 fixed** |

The held-out set is the same 48 template families the committed model was
evaluated on; it was not extended or refitted.

## Known trade-off

`offline` (`Bundler::HTTPError: Network request failed. You are currently
offline and the requested gem is not cached.`) moves from `blocked` to
`failure` on the held-out set. Teaching the model that a runtime exception is
a code failure pulls that family across. It is reported rather than hidden: a
blocked shape for network-resolution failures would restore it.

## The unresolved cargo row

The reporter retracted the original `unknown 0.531` claim. A bare
`test result: ok. 0 passed; 0 failed` summary is indistinguishable from a real
passing run once the `running 0 tests` header is missing, and the two captures
differ exactly in that header. With the full capture the label is `unknown`,
which agrees with the number the reporter published in the follow-up comment.
That row is pinned in the fixture **without** a label assertion.

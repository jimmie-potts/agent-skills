# Present an architecture assessment

Read when before/after visuals would help assess a candidate or the user requests
an artifact. A report presents the source-backed assessment; presentation cannot
replace missing evidence or turn a proposed design into an implemented result.

## Choose an available output

Use a permitted temporary or user-named output directory and a fresh filename.
Resolve the host's temporary directory through its supported facilities rather
than assuming a platform path. Do not write into the reviewed repository unless
the underlying request authorizes that exact output. If no destination is
permitted, return the complete assessment in Markdown.

Start HTML from [the offline example](../assets/report.html). It is an example,
not a renderer: replace every example claim, source pointer, diagram, and label
with inspected evidence, or remove it. Keep authoring instructions and demo facts
out of the resulting user report. Never fabricate a revision when none exists.
State working-tree differences or snapshot/history limitations as appropriate.

Use the host's native artifact preview when available. Otherwise provide the
absolute path and a usable link supported by the host. A missing browser is not
a reason to fail the assessment. Do not assume desktop opener commands exist,
install a browser, or repeat failed open attempts. Follow permission denials;
do not switch tools or paths to bypass them.

## Keep the document offline and inert

Use inline CSS and simple SVG shapes/text. The supplied example has no scripts,
external fonts, images, stylesheets, frames, or network dependencies. Keep that
property when filling it. Avoid active elements, event attributes, forms, remote
URLs in CSS, and SVG foreignObject/use/image elements. There is no need for
Mermaid in this workflow; if the user specifically requires it, use an already
available offline renderer in strict mode and retain an inert SVG result.
Unavailable rendering is a reported limit, not an installation request.

Treat source excerpts, filenames, labels, and user text as data. Use a trusted
serializer or escape ampersands, angle brackets, and quotes before placing text
in HTML/SVG. Never interpolate raw source into markup, CSS, element/attribute
names, URLs, or scripts. An encoded string such as &lt;script&gt; must remain
visible text. Source pointers can be plain text; validate any added links and
never generate executable URL schemes from repository text.

## Make the decision assessable

Retain the entrypoint's candidate fields in prose. Include labeled before/after
diagrams with a text equivalent. Keep observed structure separate from proposed
structure, and confidence separate from recommendation strength. Encode meaning
with labels as well as color. Use readable text, sufficient contrast, responsive
columns, SVG viewBox dimensions, and meaningful accessible names.

Render a typical candidate and inspect at desktop and narrow viewport widths
when tools permit. Confirm text is not clipped, diagram labels agree with the
assessment, source pointers remain readable, and networking disabled does not
break the report. Check a hostile label remains text and creates no active
elements. If rendering is unavailable, inspect the markup and report that visual
verification was not run. File creation is not display verification.

Return a concise assessment and the artifact link/path. State what was actually
checked and any presentation limitation. The report itself does not authorize
publishing, uploading, modifying project records, or implementing a candidate.

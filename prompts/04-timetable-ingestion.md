# Stage 04: Timetable upload, parsing and initials resolution

Roles: ocr-engineer, math-verifier, backend-engineer, ooad-diagrammer.
Graphify: start protocol, then end protocol.

## Goal

An HOD uploads a department timetable and every faculty member's weekly classes are generated correctly for the whole term, with anything ambiguous surfaced for review instead of guessed.

## Input formats to support

College timetables are grids: rows are days (or sections), columns are time periods, and each cell holds something like `CN (KKS)`, `DBMS Lab - A1 (RS/PN)`, `OOAD KKS 301`, or is merged across periods for labs.

- xlsx via openpyxl, honouring merged cells (a merged lab cell spans multiple periods).
- csv in a long format: `day, start, end, course, section, room, initials`.
- pdf with a text layer via pdfplumber table extraction. Scanned pdf timetables are out of scope for this stage and must be rejected with a clear message pointing to xlsx or csv.

## Pipeline

1. Upload endpoint stores the file in MinIO, creates `TimetableUpload` as `UPLOADED`, enqueues a parse task, returns 202 with the upload id.
2. Worker sniffs the MIME type from bytes, picks a `TimetableParser` through the Factory, and produces raw cells with their grid coordinates.
3. Header detection: find the row of period times and the column of day names. Accept `Mon`, `Monday`, `MON`; times like `9:00-9:55`, `9.00 - 9.55`, `09:00 to 09:55`.
4. Cell parsing: tokenise; extract course code, room, section and faculty initials. Multiple initials separated by `/`, `,` or `&` mean co-teachers.
5. Initials resolution against the directory (see maths). Unresolved or ambiguous tokens are recorded in the parse report, not dropped silently.
6. Result is a preview: slots, resolved faculty, and issues. Nothing is written to calendars yet.
7. HOD confirms the preview through an endpoint. Confirmation generates events (stage 05 owns recurrence; in this stage store confirmed `TimetableSlot`s and emit a domain event that stage 05 will consume).
8. Re-uploading a new version replaces future slots from an effective date, never past ones.

## Maths to specify first

- Initials extraction regex and tokenisation rules, with examples of every cell shape above.
- Resolution: exact match on initials, then alias match, then fuzzy match using normalised Levenshtein similarity `sim(a, b) = 1 - lev(a, b) / max(|a|, |b|)`. Accept only if best similarity is at least 0.85 and the margin to the second best is at least 0.10; otherwise mark ambiguous. Justify both thresholds.
- Merged-cell expansion: a cell spanning periods k through m becomes one slot from start(k) to end(m).
- Header time parsing grammar.

## Tests

- Fixture timetables in `samples/timetables/` (create at least three xlsx, one csv, one text pdf) with expected slot lists checked exactly.
- Property test: similarity is symmetric, within [0, 1], equals 1 only for equal normalised strings.
- Ambiguity test: two faculty with initials `KS` and `KSS` and a cell token `KS5` (OCR-like noise) ends up ambiguous, not silently resolved.

## Acceptance criteria

- Uploading each sample produces the expected preview through the API.
- Confirming creates TimetableSlots linked to the right faculty.
- The parse report lists every unresolved token with its cell coordinates.
- Activity diagram for ingestion and sequence diagram for upload-to-confirm are in PROJECT.md and rendered.

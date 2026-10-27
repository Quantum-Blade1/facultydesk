# Stage 07: Meeting circular scanning, extraction and review queue

Roles: ocr-engineer, math-verifier, backend-engineer, reviewer, ooad-diagrammer.
Graphify: start protocol, then end protocol.

## Goal

A photographed or scanned circular becomes a correct meeting on the right faculty calendars, and anything uncertain is reviewed by a human before it reaches anyone.

## Pipeline

1. Upload (image or pdf, max 15 MB) creates `Circular` as UPLOADED and enqueues processing; returns 202.
2. Worker moves to PROCESSING. If pdf has a text layer, use it. Otherwise rasterise pages at 300 DPI.
3. Preprocess each image: grayscale, non-local-means denoise, adaptive Gaussian threshold, deskew by the minimum-area-rectangle angle of foreground pixels (skip if the angle is under 0.5 degrees), crop borders.
4. OCR with Tesseract `--oem 1 --psm 6`, collect word boxes and confidences; if document confidence is below threshold, retry with `--psm 4` and keep the better result.
5. Extract fields:
   - Date: `dateparser` with `DATE_ORDER=DMY`, `PREFER_DATES_FROM=future`, institute timezone; prefer dates near cue words (`on`, `dated`, `meeting on`).
   - Time and duration: regex grammar for `10:30 AM`, `10.30 am`, `1030 hrs`, `2 pm to 4 pm`, `14:00-15:30`. Default duration 60 minutes if no end time, flagged as assumed.
   - Venue: text after `venue`, `place`, `hall`, `room`, `seminar hall`, `board room`, `lab` cue words on the same line.
   - Title and agenda: subject line (`Sub:`, `Subject:`) and the numbered agenda list.
   - Attendees: faculty initials tokens and full names anywhere in the body or in an attendee table; the word `all faculty` or `all staff` maps to the whole department.
6. Resolve attendees with the stage 04 matcher, plus token-set ratio for full names. Record per-person confidence.
7. Score the extraction. If every required field (date, start time, at least one attendee) meets its threshold, the system moves to CONFIRMED only when the department setting `auto_confirm_circulars` is on; otherwise, and always when any field is below threshold, move to NEEDS_REVIEW with reasons.
8. Review queue for HOD and the uploader: show the original image beside editable extracted fields with low-confidence fields highlighted; confirm or reject. Confirm creates the MEETING event with attendees through the stage 05 use case, which triggers stage 06 reminders.
9. Duplicate detection: a circular whose date, start time and normalised title match an existing meeting is flagged as a probable duplicate in review.
10. Failures move to FAILED with the reason; retry is possible.

## Maths to specify first

- Document confidence: length-weighted mean `C = sum(len(w_i) * c_i) / sum(len(w_i))` over words with `c_i >= 0`.
- Field confidence rules for date, time, venue and each attendee, and the thresholds with justification (start with 70 for document, 0.85 for names, require exact or alias match for initials).
- Time grammar as a small formal grammar, with every example above parsed.
- Deskew angle computation and the rotation applied.
- Duplicate predicate.

## Corpus and tests

- Create at least six synthetic circulars in `samples/circulars/`: clean pdf with text layer, scanned pdf, skewed phone photo, low-light photo, circular listing initials in a table, circular saying all faculty. Synthetic content only.
- Regression test asserting the extracted fields for each sample, and that each low-quality sample lands in NEEDS_REVIEW with the right reason.
- Time-grammar table test, confidence formula example test.

## Acceptance criteria

- Each sample processed through the API ends in the expected state with the expected fields.
- Confirming a reviewed circular puts the meeting on each attendee's calendar and schedules reminders.
- State diagram for Circular and sequence diagram for circular scanning in PROJECT.md and rendered.

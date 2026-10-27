# Stage 09: Frontend installable web app

Roles: frontend-engineer, architect, reviewer.
Graphify: start protocol, then end protocol.
Skills: anthropics `frontend-design` before the first screen.

## Goal

A calm, fast, accessible app that faculty can install on their phone and use daily.

## Tasks

1. Generate the typed API client from the backend OpenAPI schema. Add `pnpm gen:api` and make it part of `make typecheck`.
2. Auth: login page, silent refresh, logout, role-aware navigation.
3. Screens:
   - Today: next class with countdown, today's classes and meetings, top five tasks by priority, unread alerts.
   - Calendar: FullCalendar week and day views (agenda list on phones), colour by event kind with text labels too, clash badges, create and edit events, free-slot finder for HOD.
   - Upload timetable (HOD): drag and drop, live parse status, preview grid with unresolved tokens highlighted, confirm.
   - Circulars: upload with camera capture on phones, status list, review screen with the image beside editable fields and low-confidence fields marked.
   - Tasks: list sorted by priority with score visible, filters, create, complete; HOD assignment with templates and a progress view.
   - Settings: reminder offsets per event kind, channels, quiet hours, push enable, ICS link copy and rotate.
   - Admin: faculty directory with bulk import report, term and holidays.
4. PWA: manifest with icons, service worker for `push` and `notificationclick` (open the deep link), offline page, install prompt.
5. Web push subscribe flow using the VAPID public key from the backend.
6. Loading, empty and error states for every list. Toasts for actions. Confirmation for destructive actions.
7. Accessibility: keyboard paths through every screen, labelled controls, AA contrast.

## Acceptance criteria

- Each screen checked in the Antigravity browser at 360 px and 1280 px wide; note what was checked.
- Push notification from a real reminder appears and clicking it opens the event.
- Lighthouse PWA installability passes and accessibility score is at least 90 (paste scores).
- `pnpm lint typecheck build` pass.

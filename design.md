# Visual and interaction contract

## Job of the screen

Help the operator understand which project and agent need attention, inspect evidence, and issue a deliberate next action from one office view.

The direction is an original, warm isometric management office: compact workers, clear rooms, desks and a visible relationship between a worker and its task. It is inspired by the spatial office presentation of Game Dev Tycoon and the management legibility of Prison Architect. Do not reproduce either game's sprites, floor plans, logos, UI, soundtrack or screenshot.

[Original schematic](docs/assets/office-concept.svg) illustrates composition only. It is not a running product or final pixel art.

## Layout

- Header: workspace name, connection status, demo/live label, active/blocked counts, budget state and view toggle.
- Main scene: pan/zoom office with one room per project and one desk per assigned worker. Non-active agents occupy a roster; cap visible scene density and offer filtering rather than overlapping avatars.
- Left project navigation: room list, project search, add/select project. Never require hunting for a tiny door.
- Right detail drawer: selected project/worker/task. Objective and state first, then timeline, approvals, artifacts, checks, usage and memory links.
- Bottom activity strip: recent meaningful events and a jump to the affected worker. Avoid a permanent wall of token streaming.
- Alternative list/board view: same entities, permissions, evidence and actions with DOM semantics.

Desktop: scene takes most of the width; detail drawer around 360–440 px, collapsible. Below 900 px, default to list plus a dedicated scene toggle; the drawer becomes a page/sheet. At 360 px every workflow remains available without relying on canvas hit targets.

## Spatial grammar

Coordinates live in world tiles, not screen pixels. Project the ground plane as `screenX=(x-y)*tileWidth/2`, `screenY=(x+y)*tileHeight/2 - elevation`. Use a 2:1 tile ratio, camera pan/zoom and depth ordering by feet position. Desks do not occlude worker selection. Keep navigation/passable tiles distinct from decoration.

Movement is cosmetic and cancellable. A worker does not need to walk to a desk before a request can start; pathfinding must never control task execution. An unavailable path cannot change an attempt state.

Art pipeline: original tile atlas, sprite anchors at feet, short idle/work/wait animations, named asset manifest with licenses. Prefer nearest-neighbor scaling for pixel sprites and crisp HTML text for labels. Use vector placeholders at M1 if they already convey the office direction; replace with original art before a polished public release.

## Semantic tokens

| Token | Initial value | Meaning |
|---|---|---|
| `surface.page` | `#F5F0E5` | Warm neutral background |
| `surface.panel` | `#FFFFFF` | Inspectable content |
| `scene.floor` | `#3E8B83` | Office floor, decorative |
| `scene.wall` | `#D8CCAA` | Walls, decorative |
| `text.primary` | `#172B36` | Main panel text |
| `text.secondary` | `#4B606C` | Secondary readable text |
| `state.running` | `#176B8A` | Activity |
| `state.success` | `#197445` | Completed/verified as explicitly labelled |
| `state.attention` | `#8A4B08` | Approval/review |
| `state.error` | `#B42335` | Failure |
| `focus.ring` | `#234DDB` | Keyboard focus |

Validate contrast on actual combinations; a token does not establish accessibility by itself. Use short labels and icons as well as colors. Panels should feel like clear management tools, not a theme park of tiny illegible game controls.

## State projection

| Authoritative observation | Office cue | Required text |
|---|---|---|
| Agent available, no assigned run | Idle pose | Available |
| Attempt queued | Task/queue marker | Queued |
| Attempt running with fresh heartbeat | Work pose | Working + task |
| Pending exact approval | Paused pose, attention marker | Needs approval |
| Tool/provider failure | Error marker | Failed + actionable reason |
| Transport or heartbeat stale | Dimmed connection marker | Connection lost / last seen |
| Run succeeded with artifacts | Completion marker | Completed; verification shown separately |
| Task independently checked | Check badge | Verified + check evidence |
| Unsupported runtime control | No action button | Capability unavailable |

Agent availability, task progress and verification are distinct. Do not change a task to failed solely because its worker disconnected; show uncertainty until reconciliation. Do not label token streaming as “thinking” unless a provider explicitly exposes a safe public progress signal. Never show private chain-of-thought.

## Interaction and accessibility

Click/tap selects; keyboard project/worker lists expose the same selection. Escape closes the drawer; focus returns to its trigger. No drag-only action. Tooltips supplement labels and have keyboard/touch equivalents. Targets at least 44×44 CSS px for primary touch actions. Respect reduced motion and provide an animation toggle. Announce important state/approval changes through a throttled live region, not every streamed token.

Camera: wheel/pinch zoom within limits, visible pan/zoom/reset controls and “locate worker”. Background refresh preserves camera/selection. Task detail shows demo/live in its own header as well as global chrome.

## Required screen states and evidence

Empty office with setup action; labelled demo; connected live; loading/reconnecting; provider unconfigured; budget exhausted; approval pending/expired/rejected; cancellation requested/confirmed; partial failure; missing artifact; memory conflict. Capture 1440×900, 1024×768 and 360×800; test keyboard, reduced motion, zoom and text contrast. The M1 demo must resemble an office rather than a generic dashboard with decorative avatars.

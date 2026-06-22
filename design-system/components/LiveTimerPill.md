# LiveTimerPill

Floating indicator for the live timer. Visible only while a timer is running.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `elapsedSeconds` | `number` | `0` | Current elapsed time in seconds. |
| `isRunning` | `boolean` | `false` | Whether the timer is active. |
| `isRecovered` | `boolean` | `false` | True when restored after a page refresh. |
| `onStop` | `() => void` | — | Stops the timer and opens the quick-entry modal. |
| `onDiscard` | `() => void` | — | Discards the running timer after confirmation. |

## Usage

- Desktop: fixed bottom-right pill.
- Mobile (<768px): full-width bottom bar.
- Display rounds elapsed seconds to the nearest minute for visual stability.

## Tokens

| Element | Token / value |
|---|---|
| Background | `semantic.color.background` |
| Border | `semantic.color.border` (proposed) |
| Radius | `global.radius.lg` (pill); full width on mobile |
| Shadow | `component.card.shadow` (proposed) |
| Elapsed text | `global.font.size-lg`, `weight-bold`, `semantic.color.text-primary` |
| Stop button | `Button` primary sm |
| Discard button | `Button` danger ghost sm |
| Recovery banner | `semantic.color.surface`, `semantic.color.text-secondary` |

## Behavior

- Visual display updates once per minute (e.g. `1h 15m`).
- Internal counter updates every second for recovery accuracy.
- `< 15 min` shown as text; saved rounded minutes may be `0`.
- Persist `startTimestamp` in `sessionStorage` to survive refresh.
- On recovery, show a subtle *“Timer recovered”* banner.
- On discard, show a non-blocking inline confirmation; on confirm, clear timer state.

## Accessibility

- Elapsed time is in an `aria-live="polite"` region; announce only at 15-minute intervals.
- Stop/Discard buttons are keyboard reachable and operable with `Enter`/`Space`.
- Accessible labels reflect current elapsed time, e.g. *“Stop timer at 1 hour 15 minutes”*.
- Maintain ≥4.5:1 contrast against all page backgrounds.

# UnbilledSummaryCard

Dashboard highlight card showing the week’s unbilled hours and entry count.

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `totalMinutes` | `number` | `0` | Sum of rounded minutes. |
| `entryCount` | `number` | `0` | Number of unbilled entries. |
| `isLoading` | `boolean` | `false` | Skeleton state. |
| `previousTotalMinutes` | `number` | — | Optional prior total to animate change. |

## Usage

- Top-right module on the Dashboard.
- Highest-contrast module to reinforce the bet outcome.

## Tokens

| Element | Token / value |
|---|---|
| Background | `semantic.color.surface` |
| Left accent | 4px border `semantic.color.interactive` |
| Radius | `global.radius.lg` |
| Padding | `global.spacing.06` |
| Metric | `global.font.size-2xl`, `weight-bold`, `semantic.color.text-primary` |
| Sublabel | `global.font.size-sm`, `semantic.color.text-secondary` |

## Behavior

- Display total as hours + minutes (e.g. `8h 45m`).
- Update with a subtle number transition when a new entry is saved.
- Loading state shows a skeleton metric and sublabel.

## Accessibility

- Use `<h2>` for the card title and `<output>` or `<span aria-live="polite">` for the metric.
- Announce changes to the total so screen-reader users know new time was captured.
- Loading state: wrap in `aria-busy="true"` region.

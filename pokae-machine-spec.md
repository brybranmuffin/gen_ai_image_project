# PokAE Machine — Frontend Build Spec

## Overview

A single-page React app. The user selects two Pokémon (one left, one right) via searchable dropdowns, and adjusts a slider (1–99). The slider value will eventually be sent to a VAE decoder backend. No routing needed. No auth. One page only.

---

## Mockup

### Page structure

```
┌──────────────────────────────────────────────┐
│              PokAE Machine  (h1)             │
├───────────────┬──────────────┬───────────────┤
│  [Search box] │              │  [Search box] │
│  [Image box]  │  [Slider]    │  [Image box]  │
│  #0001 Bulba  │  50%         │  #0006 Char   │
└───────────────┴──────────────┴───────────────┘
```

### Slider label behavior

| Slider position | Line 1 | Line 2 |
|---|---|---|
| 50 (default) | `50% Bulbasaur` | `50% Charmander` |
| 30 | `30% Bulbasaur` | `70% Charmander` |
| 1 | `1% Bulbasaur` | `99% Charmander` |

Shows `?` if a side has no Pokémon selected yet.

---

## Data source

All Pokémon data and images come from **PokéAPI** and its associated sprites repo. No API key required.

- Pokémon list: `GET https://pokeapi.co/api/v2/pokemon?limit=1300`
- Sprites: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png`

Filter the list to IDs 1–1026 only, and **exclude ID 696 (Tyrunt)**. No regional forms or variants — the base list endpoint returns only base forms so no extra filtering is needed beyond the ID range and the Tyrunt exclusion.

---

## Layout — single page, three columns

Three-column CSS grid: `grid-template-columns: 1fr auto 1fr`. Left and right panels are identical mirror images. The center panel contains the slider and percentage label.

---

## Left / right Pokémon panel

Each panel contains:

1. A **searchable text input**. On focus or keypress, show a filtered dropdown list. Each item displays as `#0001 Bulbasaur`. Filtering matches on both name and ID number. Show max ~80 results at a time for performance.
2. An **image box** (180×180px). Before selection, show a "No Pokémon selected" placeholder. After selection, show the sprite from the PokeAPI sprites repo.
3. A **label** below the image showing `#XXXX Name` once selected.

---

## Center panel — slider

- `<input type="range" min="1" max="99" step="1">` defaulting to 50
- Above the slider, display two lines of text:
  - Line 1: `{sliderValue}% {leftPokemonName}`
  - Line 2: `{100 - sliderValue}% {rightPokemonName}`
  - Show `?` if a side has no selection yet
- These lines update live as the slider moves

---

## State

Three pieces of state in a single parent component (e.g. `App.jsx`):

```js
const [leftPokemon, setLeftPokemon] = useState(null);   // { id, name }
const [rightPokemon, setRightPokemon] = useState(null);
const [sliderValue, setSliderValue] = useState(50);
```

---

## File structure

```
/frontend
  /src
    App.jsx              ← layout, state
    PokemonPanel.jsx     ← reusable left/right panel (takes side prop)
    PokemonSearch.jsx    ← searchable dropdown
    SliderPanel.jsx      ← slider + label
    usePokemonList.js    ← custom hook: fetches + filters the Pokémon list on mount
  index.js
  index.css              ← minimal resets only, no theming yet
```

---

## `usePokemonList.js`

Fetch on mount, filter to IDs 1–1026, exclude ID 696, return `[{ id, name }]` sorted by ID. Memoize — fetch once only.

---

## Theming notes

Keep all styling minimal and unstyled for now. Use plain HTML elements (`<input>`, `<select>` equivalent via div+input+ul). No UI library. No CSS framework. Simple inline styles or a single flat CSS file. The design will be replaced later — do not invest in theming.

---

## What this page does NOT do yet

- It does not call the VAE backend (that will be wired in later)
- It does not display a decoded/output image
- It has no submit button yet (will be added when backend is ready)

---

## Azure deployment

The `/frontend` folder deploys to **Azure Static Web Apps**. The GitHub Actions workflow uses:

```yaml
app_location: "/frontend"
api_location: ""
output_location: "dist"   # if Vite; use "build" if CRA
```

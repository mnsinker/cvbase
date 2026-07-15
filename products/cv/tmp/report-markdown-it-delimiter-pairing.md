# markdown-it Inline Delimiter Pairing Algorithm — Architecture Report

Source: reverse-engineered from `markdown-it` source (lib/rules_inline/).

---

## 1. Why This Algorithm Exists

Markdown has syntactically ambiguous delimiter sequences like `**` and `*` that can open and/or close emphasis depending on their surroundings. The algorithm must determine which pairs actually match while respecting:

- The CommonMark spec's definitions of left-flanking / right-flanking
- The "rule of 3" for length-mod-3 cases (when both delimiters of the same character can open and close)
- Correct nesting (closest matching closer wins)
- Linear time even in pathological cases

---

## 2. Data Structures

### Delimiter Object

A plain object, pushed into `state.delimiters[]` by emphasis/strikethrough tokenize functions:

```
{
  marker:  number       // char code: 0x5F (_), 0x2A (*), 0x7E (~)
  length:  number       // total length of the delimiter run (count of consecutive chars)
  token:   number       // index into state.tokens[] that holds the text token for this delimiter
  end:     number       // -1 initially; after pairing, index of matching closer in delimiters[]
  open:    boolean      // true if this delimiter can open emphasis
  close:   boolean      // true if this delimiter can close emphasis
}
```

### StateInline (per-paragraph)

```
{
  src:            string           // input source text
  pos:            number           // current scanning position
  posMax:         number           // src.length
  level:          number           // nesting level (incremented/decremented during push)
  pending:        string           // accumulated plain text buffer
  delimiters:     Array<Delimiter> // current delimiter list
  _prev_delimiters: Array<Array>   // stack of saved delimiter lists for nested tokens
  tokens:         Array<Token>     // output token stream
  tokens_meta:    Array            // parallel to tokens; stores { delimiters } for open tags
  cache:          Object           // { pos: endPos } for skipToken optimization
  backticks:      Object           // backtick length -> last seen position
  backticksScanned: boolean
  linkLevel:      number           // counter to disable linkify inside links
}
```

### Token (output)

```
{
  type:     string    // e.g. "text", "em_open", "strong_close"
  tag:      string    // e.g. "em", "strong", "s"
  nesting:  number    // 1 (open), 0 (self-closing), -1 (close)
  content:  string    // text content
  markup:   string    // original delimiter string (e.g. "*", "**")
  level:    number    // nesting level in the tag tree
  // plus: attrs, map, children, info, meta, block, hidden — not relevant to pairing
}
```

---

## 3. Phase 0: Tokenize — Insert Delimiters

**File**: `parser_inline.mjs` → `ParserInline.prototype.tokenize()`

The main loop runs each inline rule in priority order against `state.pos`. If no rule matches, the character is appended to `state.pending` (plain text buffer).

Among the rules, two are relevant to delimiter pairing:

### 3a. `emphasis_tokenize` (`rules_inline/emphasis.mjs`)

```
emphasis_tokenize(state, silent):
  1. Read marker at state.pos (must be 0x5F '_' or 0x2A '*')
  2. Call state.scanDelims(state.pos, canSplitWord=(marker=='*'))
  3. For i in 0..scanned.length-1:
     a. state.push('text', '', 0)  -- flushes pending, creates a text token
     b. token.content = char
     c. state.delimiters.push({
          marker, length: scanned.length, token: tokens.length-1,
          end: -1, open: scanned.can_open, close: scanned.can_close
        })
  4. state.pos += scanned.length
```

**Key**: Each delimiter character becomes its own text token. A run of `***` produces 3 tokens and 3 delimiter objects, each with `length: 3`. This is crucial — the individual delimiters are raw text tokens at this stage. They are later *retyped* to em_open/strong_close/etc. by the postProcess.

### 3b. `strikethrough_tokenize` (`rules_inline/strikethrough.mjs`)

```
strikethrough_tokenize(state, silent):
  1. Marker must be 0x7E '~'
  2. If scanned.length < 2, return false (needs at least ~~)
  3. If odd length, push one lone '~' text token (not a delimiter)
  4. For each pair (len/2):
     a. push text token with content '~~'
     b. state.delimiters.push({
          marker, length: 0,   ← disables rule-of-3 check
          token, end: -1, open, close
        })
  5. state.pos += scanned.length
```

### 3c. `state.push()` — Delimiter Stack Management

When pushing an **opening token** (nesting > 0), the current `state.delimiters` array is saved onto `_prev_delimiters` and replaced by a fresh empty array. When its matching closing token is pushed (nesting < 0), the opposite happens: the current delimiter list is discarded and the previous one is restored.

This creates a **delimiter scope per nesting level**. Each token region (e.g. inside a link `[...]`) gets its own delimiter list, so emphasis across structural boundaries is impossible.

---

## 4. Phase 1: scanDelims — Flanking Classification

**File**: `rules_inline/state_inline.mjs` → `StateInline.prototype.scanDelims()`

```
scanDelims(start, canSplitWord):
  1. Read marker char at position `start`
  2. Determine lastChar (left neighbor):
     - start==0         → lastChar = 0x20 (whitespace)
     - handle surrogates → normalize to single codepoint or U+FFFD
  3. Count consecutive same-char markers: count = pos - start
  4. Determine nextChar:
     - pos >= max       → 0x20 (whitespace)
     - handle surrogates
  5. Classify:
     left_flanking  = !isNextWhitespace && (!isNextPunct || isLastWhitespace || isLastPunct)
     right_flanking = !isLastWhitespace  && (!isLastPunct  || isNextWhitespace || isNextPunct)
  6. can_open  = left_flanking  && (canSplitWord || !right_flanking || isLastPunct)
     can_close = right_flanking && (canSplitWord || !left_flanking  || isNextPunct)
  7. Return { can_open, can_close, length: count }
```

**Responsibility**: Given a marker position, determine how many consecutive markers exist and whether they can open, close, or both.

The `canSplitWord` parameter is `true` for `*` (asterisk) and `false` for `_` (underscore). This implements the CommonMark rule that `_` cannot split words (e.g. `foo_bar` is one word, not emphasis).

---

## 5. Phase 2: balance_pairs — The Pairing Algorithm

**File**: `rules_inline/balance_pairs.mjs`

This is the core algorithm. It runs across a flat list of delimiters and sets each opener's `end` field to the index of its matching closer.

### Entry

```
balance_pairs(state):
  1. processDelimiters(state.delimiters)     // top-level delimiters
  2. For each tokens_meta[i] that has .delimiters:
       processDelimiters(tokens_meta[i].delimiters)  // nested scopes
```

### processDelimiters Algorithm

```
function processDelimiters(delimiters):
  openersBottom = {}           // per-marker, per-(length%3) lower bound
  jumps = []                   // skip optimization array (same length as delimiters)
  headerIdx = 0                // start of current delimiter run
  lastTokenIdx = -2

  for closerIdx = 0 .. delimiters.length-1:
    closer = delimiters[closerIdx]
    jumps[closerIdx] = 0

    // ── Determine delimiter-run header ──
    // A "run" = consecutive delimiters of the same marker with adjacent tokens
    if marker changed OR tokens not adjacent:
      headerIdx = closerIdx    ← start a new run
    lastTokenIdx = closer.token

    // ── Skip if closer can't close ──
    if !closer.close: continue

    // ── Initialize openersBottom for this marker if needed ──
    // 6 slots: [min0, min1, min2, open0, open1, open2]
    // first 3: closer-only min; last 3: closer-that-is-also-opener min
    if !openersBottom[marker]:
      openersBottom[marker] = [-1, -1, -1, -1, -1, -1]

    // ── Compute lower bound for search ──
    // Key insight: we remember the lowest FAILED opener position for each
    // (marker, length%3, can-also-open?) tuple. Any opener below that
    // already failed to match a closer of the same type, so we skip them.
    //
    minOpenerIdx = openersBottom[marker]
                   [(closer.open ? 3 : 0) + (closer.length % 3)]

    // ── Search backward for matching opener ──
    // Start from headerIdx, using jumps[] to skip impossible candidates.
    openerIdx = headerIdx - jumps[headerIdx] - 1
    newMinOpenerIdx = openerIdx    // track new lower bound if we fail

    for ; openerIdx > minOpenerIdx; openerIdx -= jumps[openerIdx] + 1:
      opener = delimiters[openerIdx]

      if opener.marker != closer.marker: continue
      if !opener.open: continue
      if opener.end >= 0: continue    // already paired

      // ── Rule of 3 check ──
      // When BOTH can-open and can-close: the sum of run lengths
      // must NOT be a multiple of 3 unless both lengths are multiples of 3.
      //
      // This handles the CommonMark spec case for `***`:
      //   ***text*** → <strong><em>text</em></strong>
      //   (3 markers open, 3 close → sum=6, not a multiple of 3? wait — isOddMatch logic)
      //
      isOddMatch = false
      if opener.close || closer.open:         // at least one is "ambiguous"
        if (opener.length + closer.length) % 3 == 0:
          if opener.length % 3 != 0 || closer.length % 3 != 0:
            isOddMatch = true

      if !isOddMatch:
        // ── PAIR FOUND ──
        // Update jumps[] for O(1) skip on future iterations
        lastJump = (openerIdx > 0 && !delimiters[openerIdx-1].open)
                   ? jumps[openerIdx-1] + 1
                   : 0
        jumps[closerIdx] = closerIdx - openerIdx + lastJump
        jumps[openerIdx] = lastJump

        // Update delimiter flags
        closer.open = false
        opener.end = closerIdx
        opener.close = false

        newMinOpenerIdx = -1    // signal: match succeeded, don't update lower bound
        lastTokenIdx = -2       // next token starts a new run
        break

    // ── If match failed, update lower bound ──
    if newMinOpenerIdx != -1:
      openersBottom[marker][(closer.open ? 3 : 0) + (closer.length % 3)]
        = newMinOpenerIdx
```

---

## 6. Phase 3: postProcess — Retype Tokens

After pairing is complete, each specific rule's `postProcess` walks the delimiters and retypes the text tokens at positions `delimiter.token` from `text` to the appropriate emphasis/strikethrough tokens.

### Emphasis postProcess

```
postProcess(state, delimiters):
  for i = max-1 .. 0:
    startDelim = delimiters[i]
    if startDelim.marker not in {0x5F, 0x2A}: continue
    if startDelim.end == -1: continue           // unpaired → skip (remains text)

    endDelim = delimiters[startDelim.end]

    // ── Strong detection ──
    // Two adjacent paired markers = strong, not em+em
    // e.g. *** → delimiter[0] and delimiter[1] both paired,
    //       and delimiter[0].end == delimiter[1].end + 1
    isStrong = (i > 0) &&
               delimiters[i-1].end == startDelim.end + 1 &&
               delimiters[i-1].marker == startDelim.marker &&
               delimiters[i-1].token == startDelim.token - 1 &&
               delimiters[startDelim.end + 1].token == endDelim.token + 1

    ch = chr(startDelim.marker)
    mark = isStrong ? ch+ch : ch

    // Retype opening token
    token_o = tokens[startDelim.token]
    token_o.type = isStrong ? 'strong_open' : 'em_open'
    token_o.tag   = isStrong ? 'strong'      : 'em'
    token_o.nesting = 1
    token_o.markup  = mark
    token_o.content = ''

    // Retype closing token
    token_c = tokens[endDelim.token]
    token_c.type = isStrong ? 'strong_close' : 'em_close'
    token_c.tag   = isStrong ? 'strong'      : 'em'
    token_c.nesting = -1
    token_c.markup  = mark
    token_c.content = ''

    // If strong: clear the inner delimiter tokens' content
    if isStrong:
      tokens[delimiters[i-1].token].content = ''
      tokens[delimiters[startDelim.end + 1].token].content = ''
      i--   // skip inner delimiter (already processed)
```

### Order of postProcess rules

In `_rules2`:

1. `balance_pairs` — pairs all delimiters (emphasis AND strikethrough)
2. `strikethrough.postProcess` — retypes `~` tokens
3. `emphasis.postProcess` — retypes `*` and `_` tokens
4. `fragments_join` — merges unused delimiter text tokens back into adjacent text

The strikethrough post-process runs first so emphasis post-process can detect adjacency for the strong-combination logic correctly.

---

## 7. Pairing Order

```
for each closer (left to right):
  for each opener (from closest to farthest, right to left):
    if match → pair, break
```

This means:

- **Closest matching opener wins** (rightmost opener that can reach this closer)
- Closers are processed in source order (left to right)
- For each closer, openers are scanned right-to-left starting from the current delimiter run

This is the key nesting guarantee: inner pairs always match before outer pairs, because a closer always finds the most recent unpaired opener first.

Example: `*foo*bar*`
- Closer 1 (`*` at position of `*bar*`): finds opener 0 (`*` at `*foo*`) → pair
- Closer 2 (remaining `*` after `bar`): finds opener 2 (itself? no — opener at position 2 is after the first pair was formed, which is `*` after `foo*`). Let's trace:
  - delimiters after scan: [0:* open, 1:* close, 2:* open/close]
  - closerIdx=1: openerIdx finds del[0] → pair: del[0].end=1, del[1].open=false
  - closerIdx=2: openerIdx finds del[2]? no, del[2] is the closer itself. Starting from headerIdx... Actually del[2] is what triggered closerIdx=2. It searches for an opener above minOpenerIdx. del[0] is already paired (end >= 0). So no opener → del[2] becomes `*bar*` emphasis? No — `*bar*` with no opener → it remains text. Actually: `*foo*bar*` → `<em>foo</em>bar*` (last asterisk is text because it's unpaired).

---

## 8. Nesting Algorithm

Nesting is achieved through two mechanisms:

### A. Closest-opener-wins (from balance_pairs)

Since each closer scans backward from the current delimiter run header, and stops at the first valid unpaired opener, inner emphasis pairs before outer:

```
*foo **bar** baz*
  ↓ delimiters after scan
[0: * open, 1: * open, 2: * close, 3: * close]  (simplified; actually ** produces two * markers)
```

Processing closers left-to-right:
- closerIdx=2 (the `**` closing): finds openerIdx=1 (the second `*` of `**`) → pair `**bar**`
- closerIdx=3 (the closing `*`): finds openerIdx=0 (the opening `*`) → pair `*foo ... baz*`

Result: inner `**` pairs first, then outer `*` wraps the result.

### B. Delimiter scope via state.push()

When `state.push()` creates an opening token (nesting > 0), the current delimiter list is saved to `_prev_delimiters` and replaced by a fresh empty array. This means delimiters inside different token scopes (e.g. inside a link `[...]`) are isolated — they cannot pair with delimiters outside their scope.

---

## 9. Why the Algorithm Works

### A. Linear time guarantee

Two mechanisms prevent O(n^2) behavior on pathological input like `*_*_*_*_*...`:

1. **openersBottom[]**: Remembers the lowest indexed opener that failed for each (marker, length%3, can-open?) combination. Future closers skip everything below that bound.

2. **jumps[]**: After a match, sets skip distances so subsequent searches don't re-examine known-impossible candidates. Specifically:
   - `jumps[closerIdx] = closerIdx - openerIdx + lastJump` — future closers skip over this entire matched pair
   - `jumps[openerIdx] = lastJump` — future searches starting from this point skip past it

### B. Correctness for ambiguous delimiters

The "rule of 3" handles cases where a delimiter can both open and close. The CommonMark specification states:

> If one of the delimiters can both open and close emphasis, then the sum of the lengths of the delimiter runs containing the opening and closing delimiters must not be a multiple of 3 unless both lengths are multiples of 3.

In code:
```
if (opener.close || closer.open):
  if ((opener.length + closer.length) % 3 == 0):
    if (opener.length % 3 != 0 || closer.length % 3 != 0):
      isOddMatch = true   // → reject this pair
```

This prevents `***foo***` from being parsed as two nested `**` and `*` in the wrong configuration.

### C. Adjacent pair → strong combination

The strong-detection in emphasis postProcess checks for two adjacent paired markers. This handles cases like `***foo***` where:
- Delimiter run length = 3 → 3 delimiter objects
- Delimiters 0,2 pair with 2,4 (some matching)
- The two adjacent pairs become strong_open + strong_close instead of em_open + em_open

---

## 10. Complexity

**Time**: O(n * m) worst case where n = delimiter count, m = delimiter run count. In practice **linear** — the openersBottom[] and jumps[] optimizations ensure each delimiter is examined at most once by each future closer. The pathological case `*_*_*_*_*...` is the exact case the optimizations target.

**Space**: O(d) where d = number of delimiter objects. Plus O(h) for the `_prev_delimiters` stack where h = nesting depth.

---

## 11. Responsibilities of Each Function

| Function | Phase | Responsibility |
|---|---|---|
| `ParserInline.tokenize()` | 0 | Main loop: run rules left-to-right, accumulate pending text, flush on rule match |
| `emphasis_tokenize()` | 0 | Insert `*`/`_` markers as text tokens + delimiter objects with flanking classification |
| `strikethrough_tokenize()` | 0 | Insert `~~` markers (pairs only) as text tokens + delimiter objects |
| `state.scanDelims()` | 0 | Classify a marker position: count consecutive markers, determine can_open/can_close |
| `state.push()` | 0 | Manage delimiter scope: save/restore delimiter list on nesting change |
| `balance_pairs()` | 2 | Entry: run processDelimiters on each delimiter scope |
| `processDelimiters()` | 2 | Core pairing: for each closer, search backward for matching opener using optimizations |
| `emphasis.postProcess()` | 3 | Retype paired `*`/`_` text tokens to em_open/em_close/strong_open/strong_close |
| `strikethrough.postProcess()` | 3 | Retype paired `~` text tokens to s_open/s_close; move lone orphan markers |
| `fragments_join()` | 3 | Merge unpaired delimiter text tokens back into adjacent text tokens |

---

## 12. Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      ParserInline.parse()                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ Phase 0: tokenize()                                      │    │
│  │                                                          │    │
│  │  while state.pos < state.posMax:                         │    │
│  │    for each rule in ruler.getRules():                    │    │
│  │      if emphasis_tokenize(state, silent=false):          │    │
│  │        1. scanDelims(state.pos, marker=='*')             │    │
│  │           ┌─────────────────────────────────────┐        │    │
│  │           │ scanDelims(start, canSplitWord)     │        │    │
│  │           │   left_flanking = !nextWS && ...    │        │    │
│  │           │   right_flanking = !lastWS && ...   │        │    │
│  │           │   can_open = left && (split||...)   │        │    │
│  │           │   can_close = right && (split||...) │        │    │
│  │           │   return {can_open,can_close,count} │        │    │
│  │           └─────────────────────────────────────┘        │    │
│  │        2. For each marker char:                          │    │
│  │           state.push('text') ───► text token             │    │
│  │           state.delimiters.push({marker,length,          │    │
│  │              token, end:-1, open, close})                │    │
│  │        3. state.pos += scanned.length                    │    │
│  │    else if text rule:                                    │    │
│  │      accumulate chars until terminator                   │    │
│  │    else: state.pending += src[state.pos++]               │    │
│  │                                                          │    │
│  │    state.push() on nesting>0:                            │    │
│  │      save state.delimiters → _prev_delimiters            │    │
│  │      state.delimiters = []                               │    │
│  │    state.push() on nesting<0:                            │    │
│  │      discard state.delimiters                            │    │
│  │      restore _prev_delimiters.pop() → state.delimiters   │    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                              │                                    │
│                              ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │ Phase 2: ruler2 (post-process)                          │    │
│  │                                                          │    │
│  │ for each rule in ruler2.getRules():                      │    │
│  │                                                          │    │
│  │   ┌────────────────────────────────────────────────────┐ │    │
│  │   │ processDelimiters(delimiters)                      │ │    │
│  │   │  for each delimiter (left→right):                  │ │    │
│  │   │    if !closer.close → skip                         │ │    │
│  │   │                                                    │ │    │
│  │   │    ┌────────────────────────────────────────────┐  │ │    │
│  │   │    │ search for opener (right→left):            │  │ │    │
│  │   │    │  for openerIdx from headerIdx down to      │  │ │    │
│  │   │    │  minOpenerIdx (via openersBottom[marker]): │  │ │    │
│  │   │    │    if opener.marker == closer.marker       │  │ │    │
│  │   │    │    && opener.open && opener.end==-1        │  │ │    │
│  │   │    │    && !isOddMatch (rule of 3):             │  │ │    │
│  │   │    │      → PAIR: opener.end = closerIdx        │  │ │    │
│  │   │    │        closer.open = false                 │  │ │    │
│  │   │    │        opener.close = false                │  │ │    │
│  │   │    │        update jumps[] for skip optimization│  │ │    │
│  │   │    └────────────────────────────────────────────┘  │ │    │
│  │   │                                                    │ │    │
│  │   │    update openersBottom on failure →               │ │    │
│  │   │    linear time guarantee                           │ │    │
│  │   └────────────────────────────────────────────────────┘ │    │
│  │                                                          │    │
│  │   ┌────────────────────────────────────────────────────┐ │    │
│  │   │ postProcess (per syntax):                         │ │    │
│  │   │  for each delimiter (right→left):                 │ │    │
│  │   │    if paired:                                     │ │    │
│  │   │      check adjacent pair → strong?                │ │    │
│  │   │      retype tokens[pos] from 'text' to            │ │    │
│  │   │        'strong_open'/'em_open'                    │ │    │
│  │   │        'strong_close'/'em_close'                  │ │    │
│  │   │        's_open'/'s_close'                         │ │    │
│  │   │    else: remains as 'text' token (unpaired delim) │ │    │
│  │   └────────────────────────────────────────────────────┘ │    │
│  │                                                          │    │
│  │   ┌────────────────────────────────────────────────────┐ │    │
│  │   │ fragments_join: merge orphaned text tokens         │ │    │
│  │   │ (unpaired delimiters) into surrounding text        │ │    │
│  │   └────────────────────────────────────────────────────┘ │    │
│  └──────────────────────────────────────────────────────────┘    │
│                              │                                    │
│                              ▼                                    │
│                      Token stream ready                          │
└──────────────────────────────────────────────────────────────────┘



┌──────────────────────────────────────────────────────────────────┐
│                  DELIMITER OBJECT FIELDS                         │
│                                                                  │
│  { marker, length, token, end: -1, open, close }                │
│                                                                  │
│  marker   │ length    │ token    │ end      │ open │ close      │
│  ─────────┼───────────┼──────────┼──────────┼──────┼────────── │
│  0x2A(*)  │ run size  │ idx in   │ -1 =     │ can  │ can       │
│  0x5F(_)  │           │ tokens[] │ unpaired │ open │ close     │
│  0x7E(~)  │ 0 for ~~  │          │ ≥0 =     │      │           │
│           │           │          │ paired   │      │           │
│           │           │          │ closer   │      │           │
│           │           │          │ idx      │      │           │
└──────────────────────────────────────────────────────────────────┘



┌──────────────────────────────────────────────────────────────────┐
│                  OPTIMIZATION DATA STRUCTURES                    │
│                                                                  │
│  openersBottom:                                                  │
│    keyed by marker char code                                     │
│    value: array[6] of indices                                    │
│                                                                  │
│    [0..2] = min opener idx for (len%3 == 0,1,2)                 │
│             when closer is NOT also an opener                    │
│    [3..5] = same, when closer IS also an opener                  │
│                                                                  │
│    Purpose: after a closer fails to find a match, the lower     │
│    bound is set to the last checked opener. Future closers of   │
│    the same (marker, length%3, can-open?) type skip everything  │
│    below that bound.                                            │
│                                                                  │
│  jumps:                                                          │
│    Array parallel to delimiters                                  │
│    After a match, sets skip distances so subsequent backward    │
│    scans skip over already-paired regions.                      │
│                                                                  │
│    jumps[closerIdx] = closerIdx - openerIdx + lastJump           │
│    jumps[openerIdx] = lastJump                                   │
│                                                                  │
│    Combined giving: openerIdx -= jumps[openerIdx] + 1            │
└──────────────────────────────────────────────────────────────────┘



┌──────────────────────────────────────────────────────────────────┐
│                  SCOPE ISOLATION VIA _prev_delimiters            │
│                                                                  │
│  Token nesting:               Delimiter scopes:                  │
│                                                                  │
│  [text]                       top-level delimiters               │
│  [link_open] ─────────────────→ _prev_delimiters.push(dels)      │
│                                 state.delimiters = []            │
│    [text]                     inside-link delimiters             │
│    [em_open]                  (can't cross the link boundary)    │
│    [em_close]                                                     │
│  [link_close] ────────────────→ _prev_delimiters.pop() → dels    │
│                                 back to top-level                │
│                                                                  │
│  Delimiters inside a link scope can only pair with each other,  │
│  never with delimiters outside.                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Summary

The algorithm is a **two-pass, flat-list, closest-opener-wins** approach:

1. **Pass 1 (tokenize)**: Linear scan + rule dispatch. Insert delimiter objects with boolean flags (can_open, can_close) derived from left/right flanking analysis. Delimiter lists are scoped to their nesting level.

2. **Pass 2 (balance_pairs + postProcess)**: For each delimiter scope, walk closers left-to-right, search backward for matching openers using skip optimizations for linear time. Then retype the paired text tokens to emphasis/strikethrough tokens using a backward walk that detects adjacent pairs for strong-combination.

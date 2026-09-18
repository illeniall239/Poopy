# Phase 4 — Frontend: HTML, CSS, React, Next.js

72 hours over 4 weeks, 12 Topics. At the end the Learner builds an accessible, responsive, fast frontend in Next.js 16 that talks to the Phase 3 API, and can say where every piece of it runs and why.

Every Topic below lists:
- **Learned when** — the observable ability the Learner must show (plus the standard rule: a passed Project Review, then later Spaced Reviews).
- **Teach** — the concepts the Tutor draws out through questions. The Tutor never lectures them wholesale.
- **Probe** — misconceptions the Tutor actively tests for during lessons and Spaced Reviews.
- **Practice** — hands-on work in the Learner's own editor and project, not in-app Exercises. Says what to build or break and how the Learner knows it works.
- **Sources** — the official pages the Tutor teaches against; current on 2026-09-17.

---

## 1. How browsers work

**Learned when:** the Learner narrates a page load from the first byte to pixels (parse HTML, build DOM and CSSOM, run scripts, layout, paint, composite) and predicts which of those steps a given change re-triggers.

**Teach:** the navigation: request, response stream, parsing HTML as it arrives; the DOM tree and the CSSOM; render-blocking CSS and parser-blocking scripts, `defer`/`async`/`type="module"`; the render tree, layout (geometry), paint (pixels), compositing (layers); reflow vs repaint and what each costs; where JavaScript runs: one main thread per page shared with rendering, so long tasks freeze the UI; the browser's own event loop and `requestAnimationFrame`; the process model in one sentence: renderer processes per site, network and GPU elsewhere; the Network and Performance panels in DevTools as the way to see all of it.

**Probe:** thinking a `<script>` at the top runs after the page is built; believing changing a color and changing a width cost the same; assuming JavaScript runs on a separate thread from rendering; thinking "the page loaded" means all scripts ran.

**Practice:** Build a static HTML page with one blocking script at the top and one `defer` script, record a Performance profile in DevTools and find the parse, script, layout and paint slices; then trigger a layout thrash by reading `offsetHeight` and writing `style.width` in a loop of 1,000 elements and watch the frame time. It works when the Learner can point to the long task and explain the fix (batch reads and writes).

**Sources:** https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work; https://developer.chrome.com/blog/inside-browser-part1

## 2. Semantic HTML and accessibility basics

**Learned when:** the Learner builds a page with correct landmarks, headings, form labels and keyboard operation, and can navigate it entirely with Tab and a screen reader's rotor.

**Teach:** document structure: `header`, `nav`, `main`, `article`, `section`, `aside`, `footer`; one `h1` and a logical heading outline; `button` vs `a` vs `div onClick`; forms: `label` bound to inputs, `fieldset`/`legend`, input types, `required`, error messages linked with `aria-describedby`; images: `alt` that says what matters or is empty when decorative; the accessibility tree; keyboard: focus order, visible focus, no keyboard traps; ARIA only when HTML can't (`aria-label`, `aria-expanded`, `aria-live`), and the first rule of ARIA; color contrast minimums; testing with Tab, a screen reader (NVDA or VoiceOver) and Lighthouse's accessibility audit.

**Probe:** `div` with a click handler as a button; placeholder used as the label; `alt="image"`; `outline: none` with no replacement; adding `role="button"` instead of using `button`; thinking accessibility is a final step rather than the default HTML.

**Practice:** Write the login and "list of items" pages of this Phase's project as plain HTML first (no framework, no CSS): landmarks, headings, labeled form, an error region. It works when the Learner submits the form and reaches every control using only the keyboard, and Lighthouse's accessibility score is 100.

**Sources:** https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content; https://web.dev/learn/accessibility

## 3. CSS: box model, flexbox, grid, responsive layout

**Learned when:** the Learner lays out a page header, sidebar and card grid that adapts from phone to desktop without media-query hacks, and explains why an element is the size it is using the box model.

**Teach:** content, padding, border, margin; `box-sizing: border-box`; block vs inline; margin collapsing; the cascade and specificity in brief; flexbox for one-dimensional layout: `justify-content`, `align-items`, `gap`, `flex: 1`, wrapping; grid for two-dimensional layout: `grid-template-columns`, `repeat(auto-fit, minmax())`, areas; `min-width: 0` and overflow; responsive units (`rem`, `%`, `vw`, `clamp()`); mobile-first media queries and container queries; custom properties; the DevTools layout inspector.

**Probe:** setting `width: 100%` plus padding and wondering about overflow; using grid for everything or flex for everything; fixed pixel widths; `margin-top` on the first child "not working"; centering with absolute positioning; thinking `!important` is a fix.

**Practice:** Style the pages from Topic 2 with plain CSS: a sticky header, a sidebar that stacks under the content on narrow screens, and a card grid that fills available columns. It works when resizing from 320px to 1440px shows no horizontal scrollbar and the Learner can explain every `gap`, `flex` and `minmax` value.

**Sources:** https://web.dev/learn/css; https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout

## 4. The DOM and events without a framework

**Learned when:** the Learner builds a small interactive widget (a filterable list with add and delete) in plain TypeScript using `querySelector`, `addEventListener` and event delegation, keeping data and DOM in sync by hand.

**Teach:** the DOM as a live tree of objects; selecting, creating, appending, removing nodes; `textContent` vs `innerHTML` and XSS; events: bubbling and capturing, `event.target` vs `currentTarget`, `preventDefault`, delegation on a parent; form events and `FormData`; `fetch` from the browser with `async`/`await` and error handling; keeping application state in a variable and re-rendering from it, which is the problem React solves; `classList`; timers and cleanup.

**Probe:** adding a listener to every row instead of delegating; building HTML with string concatenation from user input; forgetting `preventDefault` on form submit; mutating the DOM as the source of truth; assuming `fetch` rejects on a 404.

**Practice:** Build a to-do widget with add, toggle and delete in one `.ts` file, with a `render(state)` function that rebuilds the list from an array, then wire it to the Phase 3 API with `fetch`. It works when every action updates both the array and the screen, and an API 500 shows a visible error instead of a silent failure.

**Sources:** https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model; https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events

## 5. React: components, props, state

**Learned when:** the Learner breaks a UI into components, decides which component owns each piece of state, lifts state when two siblings need it, and renders lists and conditionals correctly.

**Teach:** components as functions returning JSX; props flow down, events flow up; `useState` and re-rendering; state is a snapshot per render; updater functions for sequential updates; immutable updates of objects and arrays; controlled inputs; lists need stable `key`s; conditional rendering; lifting state up and the "single source of truth"; deriving values in render instead of storing them; composition with `children`; thinking in React: static version first, then minimal state.

**Probe:** mutating state in place then calling the setter; using array index as `key` on a reorderable list; storing derived data in state; expecting `setState` to update the variable immediately; putting everything in one component; duplicating state in two components.

**Practice:** Rebuild the Topic 4 widget in React (Vite or a Next.js client component): `TodoList`, `TodoItem`, `AddTodoForm`, with state owned by the parent. It works when adding, toggling and deleting all work through props and callbacks, and no component keeps a copy of another's state.

**Sources:** https://react.dev/learn/thinking-in-react

## 6. React: effects, data fetching, forms, and what the React Compiler changes about memoization

**Learned when:** the Learner writes an effect only when synchronizing with something outside React, handles fetch cancellation and errors, builds a form with `action` and `useActionState`, and explains why they no longer sprinkle `useMemo`/`useCallback` with the React Compiler enabled.

**Teach:** `useEffect` is for synchronizing with external systems (subscriptions, timers, non-React widgets), not for reacting to state; dependency arrays and cleanup; fetching in an effect: race conditions, an `ignore` flag or `AbortController`, loading and error states (and why a library, Topic 10, is the usual answer); "you might not need an effect": derive during render, handle in event handlers; forms: `<form action={fn}>`, `useActionState` for pending and result state, `useTransition`; `useRef` for DOM access and mutable non-render values; `useContext` for rarely-changing global data; the React Compiler: stable, enabled in Next.js via `reactCompiler: true`, auto-memoizes components and values, so manual `useMemo`/`useCallback`/`React.memo` are for the cases it can't see and for code that follows the Rules of React (pure render, no mutation of props or state); custom hooks for reuse.

**Probe:** an effect that sets state from other state; missing cleanup causing a set-state-after-unmount or double subscription; treating Strict Mode's double effect as a bug; memoizing everything "for performance"; thinking the Compiler fixes code that mutates during render; reaching for `useEffect` to run code on a click.

**Practice:** Wire the React widget to the Phase 3 API with a hand-written effect (loading, error, abort on unmount), then replace the add form with `action` + `useActionState` showing a pending state; enable `reactCompiler` and remove any manual memoization. It works when fast repeated navigation never shows stale data, and the React DevTools profiler shows the list item not re-rendering when an unrelated input changes.

**Sources:** https://react.dev/learn/synchronizing-with-effects; https://react.dev/learn/you-might-not-need-an-effect; https://react.dev/learn/react-compiler

## 7. Next.js App Router: routing, layouts, server and client components, Proxy

**Learned when:** the Learner builds a Next.js 16 app with nested layouts, dynamic routes, a mix of Server and Client Components chosen on purpose, and a `proxy.ts` that redirects unauthenticated users.

**Teach:** the `app/` directory: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`; nested layouts persist across navigation; dynamic segments `[id]` and `params` as a Promise to await; `Link` and prefetching; Server Components are the default: async, can read the database, no state or handlers, no bundle cost; `'use client'` marks a boundary, and everything it imports goes to the client; passing Server Components as `children` into Client Components; props across the boundary must be serializable; the RSC payload and hydration in one sentence; `proxy.ts` (renamed from `middleware.ts` in 16.0; exports `proxy`, runs on the Node runtime, `matcher` config, `NextResponse.redirect`/`rewrite`/`next`) for redirects and header logic, never as the only auth check; Route Handlers (`route.ts`) for a backend-for-frontend when needed; `server-only` to prevent leaking server code.

**Probe:** adding `'use client'` to every file; thinking a Client Component renders only in the browser (it still prerenders); importing a server-only module into a client file; relying on Proxy alone for authorization; reading `params` without awaiting; putting a `useState` in a layout that should stay a Server Component.

**Practice:** Start the Phase project: a Next.js 16 app with a root layout (nav), `/items` (Server Component that fetches from the Phase 3 API) and `/items/[id]`, a Client Component for the interactive parts, and a `proxy.ts` that sends visitors without the session cookie from `/items` to `/login`. It works when the `/items` HTML already contains the data on first load (view source), the client bundle does not include the fetch code, and hitting `/items` logged out redirects.

**Sources:** https://nextjs.org/docs/app/getting-started/layouts-and-pages; https://nextjs.org/docs/app/getting-started/server-and-client-components; https://nextjs.org/docs/app/api-reference/file-conventions/proxy

## 8. Next.js data: server actions, Cache Components, revalidation

**Learned when:** the Learner mutates data with a Server Function called from a form, enables Cache Components, decides per component whether to cache (`'use cache'` with `cacheLife`/`cacheTag`) or stream behind `Suspense`, and revalidates with `updateTag`/`revalidateTag` after a write.

**Teach:** Server Functions: `'use server'`, called via `<form action>`, `formAction` or from a client handler, always a POST, always re-check auth inside; `useActionState` for pending and errors; `redirect` and `refresh` from a Server Function; Cache Components (`cacheComponents: true`): `'use cache'` on a function, component or page, arguments become the cache key, `cacheLife('hours' | 'days' | {...})`, `cacheTag('items')`; static shell plus streamed holes = Partial Prerendering; anything reading `cookies()`, `headers()`, `searchParams` or fresh data goes inside `<Suspense>` or uses `'use cache: private'`; `connection()` before random or time values; revalidation: `revalidateTag(tag, 'max')` for stale-while-revalidate, `updateTag(tag)` inside a Server Action for read-your-own-writes, `revalidatePath` as the coarse fallback; the dev overlay's blocking-route insight as the guide; `fetch` results are not cached automatically under this model.

**Probe:** treating a Server Function as unreachable from outside the UI; calling `revalidateTag` and expecting the user to see their own write instantly; wrapping an uncached read in `Suspense` and thinking it is now cached; caching a component that reads cookies; putting `'use cache'` on a function whose argument is an unserializable object; thinking a new deploy keeps the cache.

**Practice:** In the Phase project, enable Cache Components, cache the items list with `cacheLife('minutes')` and `cacheTag('items')`, stream the "current user" header behind `Suspense`, and add a create form using a Server Function that validates with Zod, writes through the API, calls `updateTag('items')` and redirects. It works when the build output shows a static shell for `/items`, creating an item shows it immediately after redirect, and the dev overlay reports no blocking routes.

**Sources:** https://nextjs.org/docs/app/getting-started/mutating-data; https://nextjs.org/docs/app/getting-started/caching; https://nextjs.org/docs/app/getting-started/revalidating

## 9. Styling with Tailwind CSS

**Learned when:** the Learner styles the project with Tailwind v4 utilities, defines design tokens in `@theme`, builds responsive and dark-mode variants, and extracts a component only when markup repeats, not to "clean up" class lists.

**Teach:** Tailwind v4 setup: `@import "tailwindcss"` in the global CSS, PostCSS plugin (`@tailwindcss/postcss`) in Next.js, no `tailwind.config.js` by default; utility classes map to the CSS from Topic 3 (`flex`, `grid`, `gap-4`, `p-4`, `rounded-lg`); spacing and color scales; responsive prefixes `sm:`/`md:`/`lg:` are mobile-first; state variants `hover:`, `focus-visible:`, `disabled:`, `dark:`; `@theme { --color-brand-500: ...; --font-sans: ... }` generates utilities and variables; arbitrary values `[...]` sparingly; composing with components and `clsx`/`cn` for conditional classes; keeping accessibility (focus rings, contrast) in the utility set; when a plain CSS class is simpler.

**Probe:** hunting for `tailwind.config.js` in v4; using `@apply` to recreate CSS classes for everything; `md:` meaning "up to medium"; removing focus styles with `outline-none` and nothing else; hard-coding hex colors instead of theme tokens.

**Practice:** Restyle the Phase project with Tailwind: theme tokens for brand color and font, a responsive nav, cards, form inputs with visible focus states, and dark mode. It works when the CSS from Topic 3 is gone, the layout still passes the 320px–1440px resize test, and switching the OS theme flips the palette.

**Sources:** https://tailwindcss.com/docs/theme; https://tailwindcss.com/docs/responsive-design; https://tailwindcss.com/docs/styling-with-utility-classes

## 10. Client state and server state: TanStack Query, and when no state library is needed

**Learned when:** the Learner separates server state (fetched, shared, can go stale) from client state (UI, local), uses TanStack Query v5 for the former in Client Components, and can argue why the project needs no global state library.

**Teach:** server state vs client state; what a Server Component already solves (initial data with no client cache); when a client cache earns its place: polling, optimistic updates, infinite lists, mutations from many components; TanStack Query v5: `QueryClientProvider` in a client layout, `useQuery({ queryKey, queryFn })`, `isPending`/`isError`/`data`, `staleTime` and `gcTime` defaults (stale immediately, refetch on window focus), `useMutation` with `onSuccess` → `queryClient.invalidateQueries({ queryKey })`, optimistic updates and rollback, `useInfiniteQuery`; query keys as the cache's address; client state stays in `useState`/`useReducer`/context, URL state in `searchParams`; a store (Zustand and similar) only for cross-cutting client state that many distant components change.

**Probe:** copying fetched data into `useState`; reaching for Redux for a form; putting server data in context and hand-rolling invalidation; thinking `staleTime: 0` means the data is refetched on every render; forgetting to invalidate after a mutation; using TanStack Query inside a Server Component.

**Practice:** Add a client-side "live" panel to the Phase project (for example item counts that poll every 10 seconds) with `useQuery`, and move the delete action to `useMutation` with an optimistic update and rollback on failure. It works when killing the API mid-delete restores the row on screen, and returning to the tab refetches.

**Sources:** https://tanstack.com/query/latest/docs/framework/react/quick-start; https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults; https://tanstack.com/query/latest/docs/framework/react/guides/mutations

## 11. Web performance basics: Core Web Vitals, Lighthouse

**Learned when:** the Learner runs Lighthouse on the project, names the three Core Web Vitals and what each measures, and fixes the top two findings with a measured before/after.

**Teach:** LCP (largest content visible), INP (responsiveness to input), CLS (layout shift) and their thresholds; lab (Lighthouse) vs field (real users) data; common wins: image sizing and `next/image`, fonts with `next/font`, less client JavaScript (Server Components, dynamic import), avoiding layout shift with reserved space, long tasks on the main thread; caching and the static shell from Topic 8 as the biggest LCP lever; measuring, changing one thing, measuring again.

**Probe:** optimizing without measuring; treating the Lighthouse score as the goal instead of the vitals; thinking "fast on my laptop" is fast; loading a 2 MB hero image "because it's cached"; shipping a client component tree for a static page.

**Practice:** Run Lighthouse (mobile, throttled) on `/items` in a production build, record the numbers, fix the two largest issues it reports (typically image sizing or unused JavaScript), and re-run. It works when both LCP and CLS improve measurably and the Learner can explain what changed in the waterfall.

**Sources:** https://web.dev/articles/vitals; https://developer.chrome.com/docs/lighthouse/overview

## 12. Practice Project: a Next.js frontend for the Phase 3 API

**Learned when:** the Learner ships a Next.js 16 frontend for the Phase 3 API (login, list, detail, create, edit, delete) that is accessible, responsive and cached correctly, from a public repo with a README that a stranger can follow, and can explain where each piece runs and why.

**Teach:** the request path end to end: Proxy → Server Component → API with the session cookie forwarded → cached shell + streamed holes → Client Component for interaction → Server Function → `updateTag`; folder structure: `app/`, `components/`, `lib/api.ts` (typed client for the OpenAPI spec), `lib/actions.ts`; error and loading UI per route; forms with validation errors shown next to fields; keyboard and screen-reader pass; Tailwind tokens; environment variables (`NEXT_PUBLIC_` only for what the browser needs); a README with setup and a short architecture note.

**Probe:** fetching from Client Components what a Server Component could render; missing loading and error states on dynamic routes; auth only in Proxy; API base URL hard-coded; `NEXT_PUBLIC_` on a secret; a README that skips the API dependency.

**Practice:** Build the frontend over the last week of the Phase, then run the fresh-clone test with both repos: API up from Phase 3's README, frontend up from this one. It works when every API operation is reachable from the UI, Lighthouse accessibility is 100 and Core Web Vitals pass on `/items`, and view-source shows server-rendered content.

**Sources:** https://nextjs.org/docs/app/getting-started/fetching-data; https://nextjs.org/docs/app/getting-started/mutating-data; https://web.dev/learn/accessibility

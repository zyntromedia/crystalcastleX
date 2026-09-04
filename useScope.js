
// Shared scope registry across the app
const SCOPE_REGISTRY = new Map();
const SCOPE_EVENTS = new EventTarget();

/**
• useScope — Efficient Information Scope Manager
• @param {string} scopeId - Unique ID: 'app', 'auth', 'obsidian', 'dola:pr:123', etc.
• @param {object} initialData - Initial scope data (should be stable across renders —
• memoize it at the call site if it's an inline literal, e.g. via useMemo/useRef,
• otherwise deps churn every render).
• @param {object} options - { persist: boolean, deps: any[] }
• persist: if true, scope survives after the last subscriber unmounts.
• if false (default), scope is deleted once no components hold it.
• @returns {object} { scopeId, data, setData, update, reset, subscribe, isActive, createdAt }
*/
export function useScope(scopeId, initialData = {}, options = {}) {
const { persist = false, deps = [] } = options;


import { useMemo, useRef, useEffect, useState, useCallback } from 'react';

// Shared scope registry across the app
const SCOPE_REGISTRY = new Map();
const SCOPE_EVENTS = new EventTarget();

/**
• useScope — Efficient Information Scope Manager
• @param {string} scopeId - Unique ID: 'app', 'auth', 'obsidian', 'dola:pr:123', etc.
• @param {object} initialData - Initial scope data (should be stable across renders —
• memoize it at the call site if it's an inline literal, e.g. via useMemo/useRef,
• otherwise deps churn every render).
• @param {object} options - { persist: boolean, deps: any[] }
• persist: if true, scope survives after the last subscriber unmounts.
• if false (default), scope is deleted once no components hold it.
• @returns {object} { scopeId, data, setData, update, reset, subscribe, isActive, createdAt }
*/
export function useScope(scopeId, initialData = {}, options = {}) {
const { persist = false, deps = [] } = options;
const [data, setLocalData] = useState(() => {
if (!SCOPE_REGISTRY.has(scopeId)) {
SCOPE_REGISTRY.set(scopeId, {
data: initialData,
createdAt: Date.now(),
refCount: 0,
});
}
return SCOPE_REGISTRY.get(scopeId).data;
});

// Re-init if scopeId or deps change (rare — usually scopeId is stable per component)
const scopeKey = ${scopeId}|${deps.join(',')};
const lastKeyRef = useRef(scopeKey);
if (lastKeyRef.current !== scopeKey) {
lastKeyRef.current = scopeKey;
if (!SCOPE_REGISTRY.has(scopeId)) {
SCOPE_REGISTRY.set(scopeId, {
data: initialData,
createdAt: Date.now(),
refCount: 0,
});
}
}

// Register as a subscriber: keeps this component's data in sync with
// every other useScope(scopeId) instance, and tracks refCount for cleanup.
useEffect(() => {
const entry = SCOPE_REGISTRY.get(scopeId);
if (entry) entry.refCount += 1;

const handler = (e) => setLocalData(e.detail);
SCOPE_EVENTS.addEventListener(scope:${scopeId}`, handler);

return () => {
SCOPE_EVENTS.removeEventListener(scope:${scopeId}, handler); const e = SCOPE_REGISTRY.get(scopeId); if (e) { e.refCount -= 1; if (e.refCount &lt;= 0 && !persist) { SCOPE_REGISTRY.delete(scopeId); SCOPE_EVENTS.dispatchEvent(new CustomEvent(scope:${scopeId}:clear));
}
}
};
}, [scopeId, persist]);

// Full-replace / functional update, with a real dedup check against the
// resulting merged object, not against the raw patch.
const setData = useCallback((newData) => {
const entry = SCOPE_REGISTRY.get(scopeId);
const current = entry?.data ?? {};
const patch = typeof newData === 'function' ? newData(current) : newData;
const next = { ...current, ...patch };

if (isShallowEqual(current, next)) return;

if (!SCOPE_REGISTRY.has(scopeId)) {
SCOPE_REGISTRY.set(scopeId, { data: next, createdAt: Date.now(), refCount: 1 });
} else {
SCOPE_REGISTRY.get(scopeId).data = next;
}
SCOPE_EVENTS.dispatchEvent(new CustomEvent(scope:${scopeId}`, { detail: next }));
}, [scopeId]);

const update = useCallback((patch) => {
setData((prev) => ({ ...prev, ...patch }));
}, [setData]);

const reset = useCallback(() => {
setData(() => initialData);
// eslint-disable-next-line react-hooks/exhaustive-deps
}, [scopeId]);

const subscribe = useCallback((callback) => {
const handler = (e) => callback(e.detail);
SCOPE_EVENTS.addEventListener(scope:${scopeId}, handler); return () =&gt; SCOPE_EVENTS.removeEventListener(scope:${scopeId}, handler);
}, [scopeId]);

const meta = SCOPE_REGISTRY.get(scopeId);

return useMemo(() => ({
scopeId,
data,
setData,
update,
reset,
subscribe,
isActive: SCOPE_REGISTRY.has(scopeId),
createdAt: meta?.createdAt,
}), [scopeId, data, setData, update, reset, subscribe, meta?.createdAt]);
}

// Shallow equality check
function isShallowEqual(a, b) {
if (a === b) return true;
if (typeof a !== 'object' || a === null || typeof b !== 'object' || b === null) return false;
const keysA = Object.keys(a);
const keysB = Object.keys(b);
if (keysA.length !== keysB.length) return false;
for (const key of keysA) {
if (a[key] !== b[key]) return false;
}
return true;
}

// Bulk scope selector — read-only snapshot across multiple scopes.
// Note: this does NOT subscribe to updates; use it for one-off reads
// (e.g. inside event handlers), not for values you render directly.
export function useScopes(scopeIds = []) {
const key = scopeIds.join('|');
return useMemo(() => ({
getAll: () => scopeIds.map((id) => SCOPE_REGISTRY.get(id)?.data),
get: (id) => SCOPE_REGISTRY.get(id)?.data,
has: (id) => SCOPE_REGISTRY.has(id),
// eslint-disable-next-line react-hooks/exhaustive-deps
}), [key]);
}

export function clearAllScopes() {
SCOPE_REGISTRY.clear();
SCOPE_EVENTS.dispatchEvent(new CustomEvent('scopes:cleared'));
}


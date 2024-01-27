import { writable } from 'svelte/store';

export const selectedThreadId = writable<string>('');

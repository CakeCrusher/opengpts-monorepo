import { writable } from 'svelte/store';

export const gptSearchQuery = writable<string>('');

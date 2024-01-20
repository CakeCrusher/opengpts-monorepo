import { writable } from 'svelte/store';

export let selectedThreadId = writable<string>('');

import { writable } from 'svelte/store';
import type { Gpt } from './types';

export let galleryGpts = writable<Gpt[]>([]);

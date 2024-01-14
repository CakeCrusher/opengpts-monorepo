import { writable } from 'svelte/store';
import type { Gpt } from './types';
import { INITIAL_GPTS } from './mockData';

export let galleryGpts = writable<Gpt[]>(INITIAL_GPTS);

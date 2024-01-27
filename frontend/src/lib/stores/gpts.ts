import { fetchApi } from '$lib/fetcher';
import { derived, writable } from 'svelte/store';
import type { GptMain, GptStaging } from '../../types/gpt';

export type allGptsState = {
	public: GptMain[];
	user: GptStaging[];
};

export const gpts = writable<allGptsState>({
	public: [],
	user: []
});

export const allGpts = derived(gpts, ($gpts) => {
	return [...$gpts.public, ...$gpts.user];
});

export async function fetchPublicGpts() {
	const res = await fetchApi('gpt', 'GET');
	gpts.update((state) => {
		return { ...state, public: res };
	});
	return res;
}

export async function fetchUserGpts() {
	const res = await fetchApi(`login/gpt`, 'GET');
	gpts.update((state) => {
		return { ...state, user: res };
	});
	return res;
}

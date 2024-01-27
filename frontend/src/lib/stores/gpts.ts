import { fetchApi } from '$lib/fetcher';
import { derived, writable } from 'svelte/store';
import type { Gpt, GptMain, GptStaging } from '../../types/gpt';

export type allGptsState = {
	public: GptMain[];
	user: GptStaging[];
};

export const gpts = writable<allGptsState>({
	public: [],
	user: []
});



export const allGpts = derived<typeof gpts, Gpt[]>(gpts, ($gpts) => {
	return [...$gpts.public, ...$gpts.user];
});

export function addPublicGpt(gpt: GptMain) {
	gpts.update((state) => {
		return { ...state, public: [...state.public, gpt] };
	});
	return gpt;
}

export function addUserGpt(gpt: GptStaging) {
	gpts.update((state) => {
		console.log("new user gpt", { ...state, user: [...state.user, gpt] })
		return { ...state, user: [...state.user, gpt] };
	});
	return gpt;
}


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

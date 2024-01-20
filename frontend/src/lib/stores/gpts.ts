import { fetchApi } from '$lib/fetcher';
import { writable } from 'svelte/store';

export type Gpt = {
	id: string;
	name: string;
	description: string;
	metadata: {
		user_name: string;
	};
	model: string;
};

export const gpts = writable<Gpt[]>([]);

export async function fetchGpts() {
	const res = await fetchApi('gpt', 'GET');
	gpts.set(res);
	return res;
}

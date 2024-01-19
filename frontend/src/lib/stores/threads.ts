import { writable } from 'svelte/store';

export type Thread = {
	id: string;
	created_at: number;
	metadata: {
		gpt_id: string;
		user_id: string;
		title: string;
		last_updated: number;
	};
};

export const threads = writable<Thread[]>([]);

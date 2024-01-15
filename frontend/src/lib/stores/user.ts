import { writable } from 'svelte/store';

export type User = {
	email: string;
	name: string;
	profile_image: string;
	id: string;
	user_gpts: string[];
};

export const user = writable<User | null>(null);

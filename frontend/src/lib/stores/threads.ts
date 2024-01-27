import { fetchApi } from '$lib/fetcher';
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
	threadMessages: ThreadMessage[];
};

type ThreadMessageObject = 'thread.message';
type ThreadMessageRole = 'user' | 'assistant';

type MessageContentImageFile = {
	image_file: {
		file_id: string;
	};
	type: 'image_file';
};

type MessageContentText = {
	text: {
		annotations: any[]; // eslint-disable-line @typescript-eslint/no-explicit-any
		value: string;
	};
	type: 'text';
};

export type ThreadMessage = {
	id: string;
	assistant_id: string | null;
	content: (MessageContentImageFile | MessageContentText)[];
	created_at: number;
	file_ids: string[];
	metadata: any; // eslint-disable-line @typescript-eslint/no-explicit-any
	object: ThreadMessageObject;
	role: ThreadMessageRole;
	run_id: string | null;
	thread_id: string;
};

export const threads = writable<Thread[]>([]);

export async function fetchThreads() {
	const res = await fetchApi(`thread`, 'GET');
	const allThreads = res.map((thread: Thread) => ({ ...thread, threadMessages: [] }));
	threads.set(allThreads);
}

export async function fetchMessages(gptId: string, threadId: string) {
	const res = await fetchApi(`gpt/${gptId}/thread/${threadId}/messages`, 'GET');
	threads.update((threads: Thread[]) => {
		const thread = threads.find((thread) => thread.id === threadId);
		if (thread) {
			thread.threadMessages = res;
		}
		return threads;
	});
}

export async function createThread(gptId: string, title: string) {
	const res = await fetchApi(`gpt/${gptId}/thread`, 'POST', {
		title
	});
	res['threadMessages'] = [];
	threads.update((threads) => {
		threads.push(res);
		return threads;
	});

	return res.id;
}

export async function createThreadMessage(gptId: string, threadId: string, message: string) {
	const res = await fetchApi(`gpt/${gptId}/thread/${threadId}/messages`, 'POST', {
		content: message
	});

	threads.update((threads) => {
		const thread = threads.find((thread) => thread.id === threadId);
		if (thread) {
			thread.threadMessages.unshift(...res);
		}
		return threads;
	});
}

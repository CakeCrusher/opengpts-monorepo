// import { fetchApi } from "$lib/fetcher";
import { get, writable } from 'svelte/store';
import type { GptMain, GptStaging } from '../../types/gpt';
import { IsStaging, Model, Visibility } from '../../types/gpt';
import { PUBLIC_BUSINESS_LAYER_URL } from '$env/static/public';
import { fetchApi } from '$lib/fetcher';
import { addUserGpt } from './gpts';

const initialState: GptStaging = {
	id: '',
	name: '',
	model: Model.GPT_3_5_TURBO,
	metadata: {
		user_name: '',
		visibility: Visibility.PRIVATE,
		gpt_image: '',
		is_staging: IsStaging.TRUE,
		ref: ''
	},
	description: '',
	instructions: '',
	file_ids: [],
	tools: []
};

export const gptEditing = writable<GptStaging>(initialState);

export async function uploadFile(file: File) {
	const token = localStorage.getItem('token');
	const formData = new FormData();
	formData.append('file', file, file.name); // Append the file to the FormData object

	try {
		const response = await fetch(`${PUBLIC_BUSINESS_LAYER_URL}/gpt/file`, {
			method: 'POST',
			headers: {
				...(token ? { auth: `Bearer ${token}` } : {}) // Correctly set the Authorization header
			},
			body: formData // Use FormData as the body
		});

		const uploadedFile = await response.json();

		if (uploadedFile && uploadedFile.id) {
			gptEditing.update((state) => {
				return { ...state, file_ids: [...state.file_ids, uploadedFile.id] } as GptStaging;
			});
		} else {
			console.error('Error uploading file');
		}
	} catch (error) {
		console.error('File upload error: ', error);
		throw error; // Consider re-throwing the error if you want further error handling upstream
	}
}

export const removeFile = (fileId: string) => {
	gptEditing.update((state) => {
		return { ...state, file_ids: state.file_ids.filter((id) => id !== fileId) } as GptStaging;
	});
};

export const saveGpt = async () => {
	try {
		const currentGptEditing = get(gptEditing);
		let newGpt: GptStaging;
		if ('id' in currentGptEditing && currentGptEditing.id) {
			newGpt = await fetchApi(`gpt/${currentGptEditing.id}/update`, 'PATCH', currentGptEditing);
			
		} else {
			newGpt = await fetchApi(`gpt/`, 'POST', currentGptEditing);
			addUserGpt(newGpt);
		}

		if (newGpt && newGpt.id) {
			gptEditing.set(newGpt);
			return newGpt;
		} else {
			throw new Error('Error saving gpt: ' + newGpt.toString());
		}
	} catch (error) {
		console.error('Error saving gpt');
		throw error;
	}
};

// now create a publishGpt function that will call `gpt/${currentGptEditing.id}/publish`, 'POST' but it must first saveGpt
export const publishGpt = async () => {
	try {
		await saveGpt();
		const currentGptEditing = get(gptEditing);
		// will be a tuple of [GptStaging, GptMain]
		const newGpts: [GptStaging, GptMain] = await fetchApi(
			`gpt/${currentGptEditing.id}/publish`,
			'POST',
			currentGptEditing
		);

		if (newGpts.length && 'id' in newGpts[0]) {
			gptEditing.set(newGpts[0]);
			return newGpts;
		} else {
			throw new Error('Error publishing gpt: ' + newGpts.toString());
		}
	} catch (error) {
		console.error('Error publishing gpt');
		throw error;
	}
};

export const resetGptEditing = () => {
	gptEditing.set(initialState);
};

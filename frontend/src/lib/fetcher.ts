import { PUBLIC_BUSINESS_LAYER_URL } from '$env/static/public';

export function fetchApi(path: string, method: string, body: object | null = null) {
	const token = localStorage.getItem('token');
	const details = token
		? {
				auth: `Bearer ${token}`
			}
		: {};
	const bodyKwargs = body
		? {
				body: JSON.stringify(body)
			}
		: {};

	return fetch(`${PUBLIC_BUSINESS_LAYER_URL}/${path}`, {
		method,
		headers: {
			'Content-Type': 'application/json',
			...details
		},
		...bodyKwargs
	})
		.then((res) => res.json())
		.catch((error) => {
			// Handle the error here
			console.error('API request failed:', error);
			throw error; // Rethrow the error to propagate it further
		});
}

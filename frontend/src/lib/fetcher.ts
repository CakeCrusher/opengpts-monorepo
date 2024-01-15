import { env } from '$env/dynamic/public';

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

	return fetch(`${env.PUBLIC_URL}/${path}`, {
		method,
		headers: {
			'Content-Type': 'application/json',
			...details
		},
		...bodyKwargs
	}).then((res) => res.json());
}

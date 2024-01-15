import { env } from '$env/dynamic/public';

export function fetchApi(path: string, method: string, body: object) {
	return fetch(`${env.PUBLIC_URL}/${path}`, {
		method,
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${localStorage.getItem('token')}`
		},
		body: JSON.stringify(body)
	}).then((res) => res.json());
}

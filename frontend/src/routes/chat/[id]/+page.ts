export function load({ params }) {
	const { id } = params;

	return {
		props: {
			id
		}
	};
}

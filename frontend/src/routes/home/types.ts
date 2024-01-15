export type Gpt = {
	id: string;
	name: string;
	description: string;
	metadata: {
		user_name: string;
	};
	model: string;
};

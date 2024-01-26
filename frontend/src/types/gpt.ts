export enum ToolTypes {
	CODE_INTERPRETER = 'code_interpreter',
	RETRIEVAL = 'retrieval',
	ACTION = 'action'
}

type ToolCodeInterpreter = {
	type: ToolTypes.CODE_INTERPRETER;
};
type ToolRetrieval = {
	type: ToolTypes.RETRIEVAL;
};
export type ToolAction = {
	type: ToolTypes.ACTION;
	data: string;
};

export type Tool = ToolCodeInterpreter | ToolRetrieval | ToolAction;

export enum Visibility {
	PUBLIC = 'public',
	PRIVATE = 'private'
}

export enum Model {
	GPT_3_5_TURBO = 'gpt-3.5-turbo'
}

export enum IsStaging {
	TRUE = 'true'
}

type GptMetadata = {
	user_name: string;
	visibility: Visibility;
	gpt_image: string;
	is_staging?: IsStaging;
	ref?: string;
};

export type Gpt = {
	id: string;
	name: string;
	model: Model | string;
	metadata: GptMetadata;
	description?: string;
	instructions?: string;
	file_ids: string[];
	tools: Tool[];
};

type GptMetadataMain = Omit<GptMetadata, 'is_staging' | 'ref'>;

export type GptMain = Omit<Gpt, 'metadata'> & {
	metadata: GptMetadataMain;
};

type GptMetadataStaging = GptMetadata & {
	is_staging: IsStaging;
	ref: string;
};

export type GptStaging = Omit<Gpt, 'metadata'> & {
	metadata: GptMetadataStaging;
};

export type UpsertGpt = Omit<Gpt, 'id'>;

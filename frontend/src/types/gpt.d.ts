type Tool = ToolCodeInterpreter | ToolRetrieval;

enum Visibility {
  PUBLIC = "public",
  PRIVATE = "private"
}

enum Model {
  GPT_3_5_TURBO = "gpt-3.5-turbo"
}

enum IsStaging {
  TRUE = "true"
}

type GptMetadata = {
  user_name: string;
  visibility: Visibility;
  gpt_image: string;
  is_staging?: IsStaging;
  ref?: string;
}

export type Gpt = {
  id: string;
  name: string;
  model: Model | string;
  metadata: GptMetadata;
  description?: string;
  instructions?: string;
  file_ids?: string[];
  tools?: Tool[];
}

type GptMetadataMain = Omit<GptMetadata, 'is_staging' | 'ref'>;

export type GptMain = Omit<Gpt, 'metadata'> & {
  metadata: GptMetadataMain;
}

type GptMetadataStaging = GptMetadata;

export type GptStaging = Omit<Gpt, 'metadata'> & {
  metadata: GptMetadataStaging;
}

type UpsertGpt = Omit<Gpt, 'id'>;
from llama_index.core.postprocessor import (
    MetadataReplacementPostProcessor,
    SentenceTransformerRerank,
)
from llama_index.core.settings import Settings

def query_index(index, query):
    query_engine = index.as_query_engine(
        similarity_top_k=6,
        llm=Settings.llm,
        node_postprocessors=[
            MetadataReplacementPostProcessor(target_metadata_key="window"),
            SentenceTransformerRerank(top_n=2, model="BAAI/bge-reranker-base"),
        ],
        vector_store_query_mode="hybrid",
        alpha=0.5,
    )

    response = query_engine.query(query)
    return response
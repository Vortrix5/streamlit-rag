from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceWindowNodeParser
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore

def create_index(document_paths):
    documents = SimpleDirectoryReader(input_files=document_paths).load_data()

    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )

    nodes = node_parser.get_nodes_from_documents(documents)

    client = QdrantClient(url="http://localhost:6333")

    collection_name = "RAG"
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        enable_hybrid=True,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
    )

    return index
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from supabase import create_client
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Get OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API Key must be set in .env file")

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Initialize OpenAI embeddings and LLM with explicit API key
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002", 
    openai_api_key=openai_api_key
)
llm = ChatOpenAI(
    model="gpt-4-turbo", 
    openai_api_key=openai_api_key,
    temperature=0.4  # Lower temperature for more consistent, precise responses
)

class SupabaseVectorRetriever(BaseRetriever, BaseModel):
    """Custom Retriever for Supabase vector search"""
    
    embeddings: Any = Field(description="The embedding model")
    table_name: str = Field(default="hockey_players", description="The table name")
    embedding_field: str = Field(default="bio_vector", description="The field containing the embeddings")
    match_threshold: float = Field(default=0.4, description="The similarity threshold")
    match_count: int = Field(default=3, description="The number of matches to return")

    class Config:
        arbitrary_types_allowed = True
    
    def _get_relevant_documents(
        self, 
        query: str, 
        *, 
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Retrieve documents relevant to the query"""
        # Generate embedding for the query using the explicit OpenAI embeddings
        query_embedding = self.embeddings.embed_query(query)
        
        # Use Supabase vector similarity search directly
        response = supabase.rpc(
            "match_hockey_players",
            {
                "query_embedding": query_embedding,
                "match_threshold": self.match_threshold,
                "match_count": self.match_count
            }
        ).execute()
        
        results = response.data
        
        # If no results, return empty list
        if not results:
            return []
        
        # Get full player information for matches
        player_ids = [result["id"] for result in results]
        players_response = supabase.table(self.table_name).select("*").in_("id", player_ids).execute()
        players_by_id = {player["id"]: player for player in players_response.data}
        
        # Convert to LangChain Documents
        documents = []
        for result in results:
            player = players_by_id.get(result["id"])
            if player:
                # Prepare document content
                content = (
                    f"Player: {player['name']}\n"
                    f"Biography: {player['biography']}"
                )
                
                # Create metadata with similarity and other details
                metadata = {
                    "id": player["id"],
                    "name": player["name"],
                    "similarity": result["similarity"]
                }
                
                documents.append(Document(page_content=content, metadata=metadata))
        
        # Print matches for debugging
        print("Top matches:")
        for doc in documents:
            print(f"Player: {doc.metadata['name']}, Similarity: {doc.metadata['similarity']:.4f}")
        
        return documents

# Create the retriever
retriever = SupabaseVectorRetriever(embeddings=embeddings)

# Create prompt template
template = """
You are an expert hockey historian. Answer the question based strictly on the following retrieved player information, 
which is ordered by relevance (similarity score from 0 to 1, where 1 is most relevant):

{context}

Question: {question}

Instructions:
1. Base your answer ONLY on the provided context
2. Start with "MATCHES FOUND:" followed by each player and their similarity score
3. The player with the highest similarity score should be considered MOST relevant to the question
4. You must start your answer by discussing the player with the highest similarity score first
5. Important logical inferences:
   - Being captain for multiple seasons = being captain multiple times
   - Being captain of multiple teams = being captain multiple times
   - Having the "longest captaincy" = being captain multiple times
6. If the context doesn't provide enough information, clearly state what is missing

Answer in this format:

ANSWER:
[Start with the highest similarity match's information and explain how it directly answers the question]


"""
prompt = ChatPromptTemplate.from_template(template)

# Helper function to format documents
def format_docs(docs):
    formatted_texts = []
    for doc in docs:
        formatted_text = (
            f"[Similarity: {doc.metadata['similarity']:.4f}]\n"
            f"{doc.page_content}"
        )
        formatted_texts.append(formatted_text)
    return "\n\n---\n\n".join(formatted_texts)

# Create RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def main():
    print("Hockey Player Information Retrieval (LangChain RAG)")
    print("--------------------------------------------------")
    
    while True:
        # Get user query
        query = input("\nAsk a question about hockey players (or 'exit' to quit): ")
        
        # Exit condition
        if query.lower() == 'exit':
            break
        
        try:
            # Generate and print answer
            answer = rag_chain.invoke(query)
            print("\nAnswer:")
            print(answer)
        
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if _name_ == "_main_":
    main()
import os
from dotenv import load_dotenv
from supabase import create_client
import openai

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(_file_))
env_path = os.path.join(script_dir, '.env')

# Load environment variables from the explicit path
load_dotenv(env_path)

# Set up clients
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
supabase = create_client(supabase_url, supabase_key)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY must be set in .env file")
client = openai.OpenAI(api_key=openai_api_key)

def get_embedding(text):
    """Generate embedding for search query"""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def find_similar_players(query, match_threshold=0.3, match_count=3):
    """Find players with biographies similar to the query"""
    # Convert query to embedding
    query_embedding = get_embedding(query)
    
    # Search for similar players using vector similarity
    response = supabase.rpc(
        "match_hockey_players",
        {
            "query_embedding": query_embedding,
            "match_threshold": match_threshold,
            "match_count": match_count
        }
    ).execute()
    
    # Sort by similarity in descending order
    matches = sorted(response.data, key=lambda x: x['similarity'], reverse=True)
    return matches

def answer_question(query):
    """Answer a question about hockey players using RAG"""
    # Find relevant players
    matches = find_similar_players(query)
    
    if not matches:
        return "I couldn't find any relevant information to answer your question."
    
    # Get full details of matched players
    player_ids = [match['id'] for match in matches]
    players_response = supabase.table("hockey_players").select("*").in_("id", player_ids).execute()
    
    # Create a mapping of player_id to full player data
    players_map = {p['id']: p for p in players_response.data}
    
    # Print matches with detailed information
    print("\nTop Matches (by relevance):")
    print("=" * 80)
    for match in matches:
        player = players_map[match['id']]
        print(f"Player: {player['name']}")
        print(f"Similarity Score: {match['similarity']:.4f}")
        print(f"Position: {player['position']}")
        
        # Generate a brief explanation of why this player matched
        explain_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a hockey expert. Briefly explain in 1-2 sentences why this player biography matches the user's query."},
                {"role": "user", "content": f"Query: {query}\nPlayer Info:\nName: {player['name']}\nPosition: {player['position']}\nBiography: {player.get('biography', 'No biography available')}\n\nWhy is this player relevant to the query?"}
            ]
        )
        print(f"Match Explanation: {explain_response.choices[0].message.content}")
        print("-" * 80)
    
    # Continue with generating the detailed answer...
    context = "Here are some hockey player biographies:\n\n"
    for player in players_response.data:
        context += f"Player: {player['name']}\n"
        context += f"Position: {player['position']}\n"
        
    
    # Generate answer using OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a hockey expert. Answer the question based only on the information provided in the context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    
    return response.choices[0].message.content

def main():
    print("Hockey Player Information System")
    print("--------------------------------")
    
    while True:
        query = input("\nAsk a question about hockey players (or 'exit' to quit): ")
        
        if query.lower() == 'exit':
            break
            
        answer = answer_question(query)
      

if _name_ == "_main_":
    main()
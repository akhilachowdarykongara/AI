import os
from dotenv import load_dotenv
from supabase import create_client
import openai

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(_file_))
env_path = os.path.join(script_dir, '.env')

# Load environment variables from the explicit path
load_dotenv(env_path)

# Debug: Print current working directory and .env file location
print(f"Current working directory: {os.getcwd()}")
print(f"Script directory: {script_dir}")
print(f"Looking for .env file in: {env_path}")
print(f"Does .env file exist? {os.path.exists(env_path)}")

# Set up clients
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

openai_api_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY loaded: {'Yes' if openai_api_key else 'No'}")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY must be set in .env file")
client = openai.OpenAI(api_key=openai_api_key)

# First, add the vector column if it doesn't exist
# This would typically be done in SQL:
# ALTER TABLE public.hockey_players
# ADD COLUMN bio_vector vector(1536);

def generate_and_store_embeddings():
    # Get all players
    response = supabase.table("hockey_players").select("*").execute()
    players = response.data
    
    print(f"Generating embeddings for {len(players)} players...")
    
    for player in players:
        # Generate embedding for biography
        embedding_response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=player["biography"]
        )
        embedding = embedding_response.data[0].embedding
        
        # Update player record with embedding
        supabase.table("hockey_players").update(
            {"bio_vector": embedding}
        ).eq("id", player["id"]).execute()
        
        print(f"Added embedding for {player['name']}")

if _name_ == "_main_":
    generate_and_store_embeddings()
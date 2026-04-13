import os
import sys
from datetime import datetime, timezone
# from dotenv import load_dotenv
from dotenv import load_dotenv
from supabase import create_client, Client

# load_dotenv() 
# ── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL  = os.environ.get("SUPABASE_URL")
SUPABASE_KEY  = os.environ.get("SUPABASE_ANON_KEY")

# Any existing table in your DB — just to run a SELECT against
PING_TABLE = os.environ.get("PING_TABLE", "your_table_name")

# ── Validation ────────────────────────────────────────────────────────────────
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: SUPABASE_URL and SUPABASE_ANON_KEY must be set.")
    sys.exit(1)

# ── Connect ───────────────────────────────────────────────────────────────────
try:
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"✅ Connected to Supabase: {SUPABASE_URL}")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    sys.exit(1)

# ── Ping: lightweight SELECT — no writes, no new tables ──────────────────────
def ping_database():
    try:
        response = (
            client.table(PING_TABLE)
            .select("*")
            .limit(1)
            .execute()
        )
        print(f"✅ SELECT success → DB is alive")
        return True

    except Exception as e:
        print(f"❌ DB operation failed: {e}")
        return False

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'─'*50}")
    print(f"  Supabase Keep-Alive Ping")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'─'*50}\n")

    success = ping_database()

    print(f"\n{'─'*50}")
    print(f"  Result: {'SUCCESS ✅' if success else 'FAILED ❌'}")
    print(f"{'─'*50}\n")

    sys.exit(0 if success else 1)
from dotenv import load_dotenv
import os

load_dotenv()

groq_key = os.environ.get("GROQ_API_KEY")
ls_key = os.environ.get("LANGSMITH_API_KEY")
ls_tracing = os.environ.get("LANGSMITH_TRACING")
ls_project = os.environ.get("LANGSMITH_PROJECT")

print(f"GROQ_API_KEY:      {'✅' if groq_key else '❌ НЕТ'} (длина: {len(groq_key) if groq_key else 0})")
print(f"LANGSMITH_API_KEY: {'✅' if ls_key else '❌ НЕТ'} (длина: {len(ls_key) if ls_key else 0})")
print(f"LANGSMITH_TRACING: {ls_tracing}")
print(f"LANGSMITH_PROJECT: {ls_project}")

if groq_key: print(f"GROQ префикс:      {groq_key[:7]}...")
if ls_key:   print(f"LANGSMITH префикс: {ls_key[:7]}...")
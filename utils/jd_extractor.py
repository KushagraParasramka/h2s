from docx import Document
from keybert import KeyBERT
import json


def read_docx(file_path):
    """
    Reads the Job Description DOCX file and returns its text content.
    """
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def extract_skills_section(jd_text):
    """
    Extracts the skills and requirements section from the Job Description
    to focus keyword extraction on relevant technical skills.
    """
    lines = jd_text.split("\n")
    relevant = []
    capture = False

    trigger_words = [
        "skills", "require", "experience", "must have", "need",
        "looking for", "what you", "qualification", "you absolutely",
        "you'd", "inventory", "technical", "things we"
    ]

    for line in lines:
        if any(t in line.lower() for t in trigger_words):
            capture = True
        if capture and line.strip():
            relevant.append(line)

    return "\n".join(relevant) if relevant else jd_text


def get_candidate_text(candidate):
    """
    Combines candidate profile information, work experience,
    and skills into a single searchable text string.
    """
    text_parts = []

    profile = candidate.get("profile", {})
    text_parts.append(profile.get("headline", ""))
    text_parts.append(profile.get("summary", ""))
    text_parts.append(profile.get("current_title", ""))

    for job in candidate.get("career_history", []):
        text_parts.append(job.get("title", ""))
        text_parts.append(job.get("description", ""))

    for skill in candidate.get("skills", []):
        text_parts.append(skill.get("name", ""))

    return " ".join(text_parts).lower()


# =====================================================
# STEP 1: READ JOB DESCRIPTION FILE
# =====================================================

jd_text = read_docx("public/job_description.docx")

print("\nReading Job Description...\n")


# =====================================================
# STEP 2: EXTRACT IMPORTANT KEYWORDS FROM JD
# =====================================================

# Extract only the skills/requirements section from the JD
skills_text = extract_skills_section(jd_text)

# Seed keywords help KeyBERT focus on important technical skills
seed_keywords = [
    "python", "machine learning", "deep learning", "nlp", "embeddings",
    "vector database", "retrieval", "ranking", "llm", "fine-tuning",
    "spark", "sql", "airflow", "aws", "gcp", "pytorch", "tensorflow",
    "transformer", "bert", "recommendation", "search", "a/b testing",
    "elasticsearch", "pinecone", "weaviate", "milvus", "faiss",
    "lora", "qlora", "peft", "xgboost", "production", "deployment",
    "evaluation", "ndcg", "mrr", "map", "inference", "distributed"
]

# Initialize KeyBERT model
kw_model = KeyBERT()

# Extract top keywords/keyphrases from the JD
keywords = kw_model.extract_keywords(
    skills_text,
    keyphrase_ngram_range=(1, 2),
    stop_words="english",
    top_n=30,
    seed_keywords=seed_keywords
)

# Remove company names, locations, and other irrelevant terms
BLOCKLIST = {
    "redrob", "redrob ai", "hyderabad", "pune", "noida", "delhi",
    "mumbai", "bengaluru", "bangalore", "india", "google", "meta",
    "career google", "career pure", "candidates hyderabad", "role jd",
    "pune noida", "noida pune", "hyderabad pune", "recruiting tech",
    "candidate ai", "ai native", "series", "hackathon", "work ai",
    "senior ai", "ai roles", "ai engineering", "ai engineer",
    "skills fit", "listed skills", "search roles"
}

# Keep only valid technical keywords
jd_keywords = [
    kw.lower() for kw, score in keywords
    if kw.lower() not in BLOCKLIST
]

print("Extracted JD Keywords:\n")
for keyword, score in keywords:
    if keyword.lower() not in BLOCKLIST:
        print(f"  {keyword:<35} {score:.4f}")

print(f"\nTotal keywords after filtering: {len(jd_keywords)}\n")


# =====================================================
# STEP 3: LOAD CANDIDATE DATA
# =====================================================

candidates = []

with open("public/candidates.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        candidates.append(json.loads(line))

print(f"Loaded {len(candidates)} candidates.\n")


# =====================================================
# STEP 4: CALCULATE MATCH SCORE FOR EACH CANDIDATE
# =====================================================

results = []

for candidate in candidates[:20]:

    # Convert candidate profile into searchable text
    candidate_text = get_candidate_text(candidate)

    matched_keywords = []

    # Find JD keywords present in candidate profile
    for keyword in jd_keywords:
        if keyword in candidate_text:
            matched_keywords.append(keyword)

    # Calculate percentage match score
    match_percentage = (
        len(matched_keywords) / len(jd_keywords)
    ) * 100 if jd_keywords else 0

    results.append({
        "candidate_id": candidate["candidate_id"],
        "score": round(match_percentage, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": list(
            set(jd_keywords) - set(matched_keywords)
        )
    })


# =====================================================
# STEP 5: SORT CANDIDATES BY MATCH SCORE
# =====================================================

results.sort(
    key=lambda candidate: candidate["score"],
    reverse=True
)


# =====================================================
# STEP 6: DISPLAY TOP MATCHING CANDIDATES
# =====================================================

print("\n========== TOP MATCHING CANDIDATES ==========\n")

for result in results[:10]:

    print(f"Candidate ID      : {result['candidate_id']}")
    print(f"Match Percentage  : {result['score']}%")

    print("\nMatched Keywords:")
    print(result["matched_keywords"])

    print("\nMissing Keywords:")
    print(result["missing_keywords"])

    print("\n" + "=" * 60 + "\n")


# =====================================================
# STEP 7: DISPLAY BEST MATCHING CANDIDATE
# =====================================================

best_candidate = results[0]

print("\n========== BEST MATCH ==========\n")

print(f"Candidate ID     : {best_candidate['candidate_id']}")
print(f"Match Percentage : {best_candidate['score']}%")

print("\nMatched Keywords:")
print(best_candidate["matched_keywords"])
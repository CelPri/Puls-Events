from datasets import Dataset
from ragas import evaluate

# métrique compatible anciennes versions
try:
    from ragas.metrics import answer_similarity
except ImportError:
    from ragas.metrics.similarity import answer_similarity

# embeddings RAGAS (pas LangChain)
from ragas.embeddings import HuggingFaceEmbeddings

from src.rag.chatbot import ask_rag


questions = [
    "Quels événements culturels ont lieu à Bordeaux ?",
    "Quels concerts ou événements de musique pop ont lieu à Bordeaux ?",
    "Quels événements sont prévus à Bordeaux le 10 décembre 2025 ?",
    "Qui a gagné la Coupe du monde de football ?"
]

ground_truths = [
    "De nombreux événements culturels ont lieu à Bordeaux, notamment des expositions, des spectacles vivants, des conférences et des ateliers artistiques tout au long de l’année.",
    "Aucun concert explicitement identifié comme de la musique pop n’est référencé dans les données OpenAgenda disponibles.",
    "Aucun événement ne débute exactement le 10 décembre 2025 à Bordeaux, mais plusieurs expositions et événements sont en cours à cette période.",
    "Cette question n’est pas liée aux événements culturels référencés dans la base OpenAgenda."
]


answers = [ask_rag(q) for q in questions]


dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "ground_truth": ground_truths,
})


embeddings = HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2"
)


results = evaluate(
    dataset=dataset,
    metrics=[answer_similarity],
    embeddings=embeddings,
)

print(results)

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset
from src.rag.chatbot import answer


def chunk_events(events):
    """
    Découpe les événements en chunks simples.
    Fonction testable unitairement.
    """
    chunks = []

    for event in events:
        if event.get("description"):
            chunks.append({
                "uid": event.get("uid"),
                "text": event.get("description")
            })

    return chunks

if __name__ == "__main__":

    # Questions RAGAS
    questions = [
        "Quels événements culturels ont lieu à Bordeaux ?",
        "Quels concerts ou événements de musique pop ont lieu à Bordeaux ?",
        "Quels événements sont prévus à Bordeaux le 10 décembre 2025 ?",
        "Qui a gagné la Coupe du monde de football ?"
    ]

    # Réponses humaines idéales (ground truth)
    ground_truths = [
        "De nombreux événements culturels ont lieu à Bordeaux, notamment des expositions, des spectacles vivants, des conférences et des ateliers artistiques tout au long de l’année.",
        "Aucun concert explicitement identifié comme de la musique pop n’est référencé dans les données OpenAgenda disponibles.",
        "Aucun événement ne débute exactement le 10 décembre 2025 à Bordeaux, mais plusieurs expositions et événements sont en cours à cette période.",
        "Cette question n’est pas liée aux événements culturels référencés dans la base OpenAgenda."
    ]

    # Générer les réponses du RAG
    answers = []
    for q in questions:
        result = answer(q)
        answers.append(result.content)

    # Dataset RAGAS
    data = {
        "question": questions,
        "answer": answers,
        "ground_truth": ground_truths,
        "contexts": [["événements culturels OpenAgenda"]] * len(questions)
    }

    dataset = Dataset.from_dict(data)

    # Évaluation RAGAS
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy]
    )

    print(results)

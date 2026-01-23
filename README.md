# 🎭 RAG Events - Système de Récupération d'Événements Culturels

**Un système de Retrieval-Augmented Generation (RAG) intelligent pour interroger les événements culturels de Bordeaux via OpenAgenda.**

---

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture du système](#architecture-du-système)
- [Schéma UML](#schéma-uml)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure des fichiers](#structure-des-fichiers)
- [API REST](#api-rest)
- [Pipeline de traitement](#pipeline-de-traitement)
- [Technologie](#technologie)
- [Tests et Évaluation](#tests-et-évaluation)
- [Contribution](#contribution)

---

## 👁️ Vue d'ensemble

**RAG Events** est un système intelligent qui combine la récupération d'informations vectorielles avec un modèle de langage (LLM) pour répondre à des questions naturelles sur les événements culturels à Bordeaux.

### Caractéristiques principales

✅ **Récupération intelligente** : Utilise FAISS pour rechercher les événements les plus pertinents  
✅ **Extraction de dates** : Analyse automatiquement les questions pour extraire les dates pertinentes  
✅ **Filtrage temporel** : Restreint les résultats aux événements spécifiés  
✅ **LLM Mistral** : Génère des réponses contextualisées et pertinentes  
✅ **API REST** : Interface HTTP facile à utiliser via FastAPI  
✅ **Évaluation RAGAS** : Mesure la fidélité et la pertinence des réponses  
✅ **Dockerisé** : Déploiement simplifié via Docker  

---

## 🏗️ Architecture du système

```
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION RAG EVENTS                         │
└─────────────────────────────────────────────────────────────────────┘

                        ┌─────────────────┐
                        │   UTILISATEUR   │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  FastAPI Server │
                        │  (/ask, /rebuild)
                        └────────┬────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
   ┌─────────────┐      ┌────────────────┐    ┌──────────────┐
   │   Question  │      │  Chatbot.py    │    │ FAISS Vector │
   │ Processing  │      │  (RAG Engine)  │◄───┤  Store Index │
   └─────────────┘      └────────┬───────┘    └──────────────┘
          │                      │
          │           ┌──────────▼──────────┐
          │           │ Date Extraction     │
          │           │ (LLM - Mistral)     │
          │           └──────────┬──────────┘
          │                      │
          │           ┌──────────▼──────────┐
          │           │ Document Filtering  │
          │           │ (By Date & Relevance)
          │           └──────────┬──────────┘
          │                      │
          └──────────────────────┼──────────┐
                                 │          │
                        ┌────────▼──────┐   │
                        │ Answer Gener. │   │
                        │ (LLM - Mistral)   │
                        └────────┬──────┘   │
                                 │          │
                        ┌────────▼──────────▼┐
                        │   JSON Response    │
                        │ {"answer": "..."}  │
                        └────────────────────┘
```

---

## 📊 Schéma UML

### Diagramme des classes

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE ORIENTÉE OBJET                       │
└──────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐
│        Event (Data Model)      │
├────────────────────────────────┤
│ - title: str                   │
│ - description: str             │
│ - start_date: datetime         │
│ - end_date: datetime           │
│ - source: str                  │
│ - uid: str                     │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────────────┐
│    EventChunk (For Vector Storage)     │
├────────────────────────────────────────┤
│ - text: str                            │
│ - uid: str                             │
│ - title: str                           │
│ - start_date: str                      │
│ - end_date: str                        │
│ - source: str                          │
│ - chunk_id: int                        │
└────────────┬───────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────┐
│    Document (LangChain Wrapper)                  │
├──────────────────────────────────────────────────┤
│ - page_content: str (chunk text)                 │
│ - metadata: dict (event info)                    │
│  └─ uid, title, start_date, end_date, source    │
└──────────────────────────────────────────────────┘


┌─────────────────────────────────┐
│      Retriever Module           │
├─────────────────────────────────┤
│ + retrieve_documents(query)     │
│   └─ Uses FAISS Index           │
│   └─ Returns: List[Document]    │
└─────────────────────────────────┘


┌─────────────────────────────────────────────────────────┐
│            Chatbot Module (RAG Engine)                  │
├─────────────────────────────────────────────────────────┤
│ - llm: ChatMistralAI                                    │
│ - date_prompt: ChatPromptTemplate                       │
│ - rag_prompt: ChatPromptTemplate                        │
├─────────────────────────────────────────────────────────┤
│ + answer(question: str) -> str                          │
│   1. Extract date from question (LLM)                   │
│   2. Retrieve documents from FAISS (k=500)              │
│   3. Filter by date if applicable                       │
│   4. Generate response with RAG prompt                  │
│   5. Return final answer                                │
└─────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────┐
│        FastAPI Server (Main Application)         │
├──────────────────────────────────────────────────┤
│ - app: FastAPI(title="RAG Events API")           │
├──────────────────────────────────────────────────┤
│ + POST /ask                                      │
│   Input: Question(question: str)                 │
│   Output: {answer: str}                          │
│                                                  │
│ + POST /rebuild                                  │
│   Rebuilds FAISS index from events_chunks.json   │
│   Output: {status: str}                          │
└──────────────────────────────────────────────────┘
```

### Diagramme de flux (Data Flow)

```
┌──────────────────────┐
│  OpenAgenda API      │
│  (fetch_openagenda)  │
└──────────┬───────────┘
           │
           │ GET /events (last 12 months)
           ▼
┌──────────────────────────────┐
│ Parse Events                 │
│ (parse_events)               │
│ Output: events.json          │
└──────────┬───────────────────┘
           │
           │ 200+ events
           ▼
┌──────────────────────────────┐
│ Chunk Events                 │
│ (chunk_events.py)            │
│ Splits large text chunks     │
│ Output: events_chunks.json   │
└──────────┬───────────────────┘
           │
           │ 1000+ chunks
           ▼
┌──────────────────────────────────────┐
│ Build FAISS Index                    │
│ (build_faiss.py)                     │
│ - Load chunks                        │
│ - Generate embeddings (HuggingFace)  │
│ - Create FAISS vector index          │
│ Output: faiss_index/                 │
└──────────┬───────────────────────────┘
           │
           ▼
┌───────────────────────────────┐
│   Vector Store Ready (FAISS)  │
│   ~/faiss_index/              │
└───────────────────────────────┘
           │
           │ (Loaded by Retriever)
           ▼
┌────────────────────────────────┐
│  API Request: /ask             │
│  {question: "..."}             │
└──────────┬─────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│ Chatbot.answer()                 │
│ 1. Date extraction (LLM)         │
│ 2. FAISS retrieval (k=500)       │
│ 3. Date filtering                │
│ 4. Context generation            │
│ 5. LLM answer generation         │
└──────────┬───────────────────────┘
           │
           ▼
┌────────────────────────────┐
│  API Response              │
│  {answer: "..."}           │
└────────────────────────────┘
```

### Diagramme des dépendances

```
┌─────────────────────────────────────────────────────┐
│              DÉPENDANCES PRINCIPALES                │
└─────────────────────────────────────────────────────┘

FastAPI (Web Framework)
    │
    └─► Pydantic (Data Validation)
    └─► Uvicorn (ASGI Server)


LangChain (RAG Framework)
    │
    ├─► LangChain-Mistral (LLM Integration)
    ├─► LangChain-Community (Vector Stores & Embeddings)
    │
    └─► FAISS (Vector Search)
        └─► HuggingFace Embeddings


Data Processing
    │
    ├─► Pandas (Data manipulation)
    ├─► Requests (HTTP calls)
    ├─► Python-dotenv (Environment variables)
    │
    └─► Mistral AI (LLM)


Evaluation
    │
    ├─► RAGAS (RAG Assessment)
    └─► Datasets (Dataset handling)


Infrastructure
    │
    ├─► Docker (Containerization)
    └─► Config Logger (Logging)
```

---

## 📦 Installation

### Prérequis

- **Python** 3.10+
- **pip** (gestionnaire de paquets)
- **Docker** (optionnel, pour la containerisation)

### Installation locale

1. **Clonez le projet**
```bash
cd "c:\Users\User\Desktop\Formation IA\Projet7"
```

2. **Créez un environnement virtuel**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Sur Windows (PowerShell)
# ou
.\.venv\Scripts\activate.bat   # Sur Windows (CMD)
# ou
source .venv/bin/activate      # Sur Linux/macOS
```

3. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurez les variables d'environnement** (voir Configuration)

---

## ⚙️ Configuration

### Variables d'environnement (.env)

Créez un fichier `.env` à la racine du projet :

```env
# Mistral AI API Key
MISTRAL_API_KEY=votre_clé_api_mistral

# OpenAgenda Configuration (optionnel, si modification)
OPENAGENDA_API_KEY=bb4beba0fed746f9a82473251c59085e
OPENAGENDA_AGENDA_UID=ville-de-bordeaux
```

### Fichiers de configuration

- **`config/logger.py`** : Configuration du logging
  - Format: `%(levelname)s - %(message)s`
  - Niveau: `logging.INFO`

---

## 🚀 Utilisation

### 1. Préparation des données

#### Étape 1 : Récupérer les événements OpenAgenda
```bash
python src/fetch_openagenda.py
```
Sortie : `data/events.json` (les 12 derniers mois)

#### Étape 2 : Découper les événements en chunks
```bash
python src/chunk_events.py
```
Sortie : `data/events_chunks.json` (textes découpés)

#### Étape 3 : Construire l'index FAISS
```bash
python src/build_faiss.py
```
Sortie : `faiss_index/` (index vectoriel)

### 2. Lancer l'API

```bash
python -m uvicorn api.main:app --reload
```

L'API sera disponible sur : **http://127.0.0.1:8000**

Documentation Swagger : **http://127.0.0.1:8000/docs**

### 3. Tester l'API

#### Exemple avec curl
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Quels événements culturels à Bordeaux ?"}'
```

#### Exemple avec Python (requests)
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "Quels événements culturels à Bordeaux ?"}
)

print(response.json())
# {"answer": "Les événements culturels disponibles incluent..."}
```

#### Exemple avec le script de test
```bash
python tests/api_test.py
```

### 4. Reconstruire l'index FAISS

Via l'API :
```bash
curl -X POST "http://127.0.0.1:8000/rebuild"
```

---

## 📁 Structure des fichiers

```
projet7/
├── README.md                          # Ce fichier
├── requirements.txt                   # Dépendances Python
├── Dockerfile                         # Configuration Docker
│
├── api/                               # Module API REST
│   └── main.py                        # Application FastAPI
│       ├── POST /ask                  # Poser une question
│       └── POST /rebuild              # Reconstruire l'index
│
├── src/                               # Module source
│   ├── fetch_openagenda.py            # Récupération des événements
│   ├── chunk_events.py                # Découpage en chunks
│   ├── build_faiss.py                 # Construction de l'index FAISS
│   │
│   └── rag/                           # Module RAG (Retrieval-Augmented Generation)
│       ├── chatbot.py                 # Moteur de réponse (2 prompts LLM)
│       │   ├── Date extraction prompt
│       │   └── RAG final prompt
│       └── retriever.py               # Recherche vectorielle FAISS
│
├── config/                            # Configuration
│   ├── __init__.py
│   └── logger.py                      # Système de logging
│
├── data/                              # Données
│   ├── events.json                    # Événements bruts (200+ items)
│   └── events_chunks.json             # Chunks pour embeddings (1000+ items)
│
├── faiss_index/                       # Index vectoriel FAISS
│   └── index.faiss                    # Fichier d'index
│
├── tests/                             # Tests
│   ├── api_test.py                    # Test API
│   └── evaluate_rag.py                # Évaluation RAGAS
│
└── .env                               # Variables d'environnement (à créer)
```

---

## 🔌 API REST

### Endpoint 1 : Poser une question

**`POST /ask`**

#### Request
```json
{
  "question": "Quels événements culturels à Bordeaux ?"
}
```

#### Response (200 OK)
```json
{
  "answer": "Les événements culturels à Bordeaux incluent des expositions, des concerts, des spectacles vivants, des conférences et des ateliers artistiques..."
}
```

#### Error (400 Bad Request)
```json
{
  "detail": "La question ne peut pas être vide."
}
```

### Endpoint 2 : Reconstruire l'index

**`POST /rebuild`**

Relance la construction complète de l'index FAISS.

#### Response (200 OK)
```json
{
  "status": "FAISS index rebuilt"
}
```

### Endpoint 3 : Documentation API (Swagger UI)

**`GET /docs`**

Accédez à la documentation interactive Swagger.

---

## 🔄 Pipeline de traitement

### Phase 1 : Extraction des données (One-time)

```
OpenAgenda API
    ↓
fetch_openagenda.py
    • Récupère les événements du dernier an
    • Filtre par agenda UID
    • Parse les métadonnées (titre, description, dates)
    ↓
events.json (environ 200 événements)
```

**Fonction principale** : `get_events()` → `parse_events()` → JSON

### Phase 2 : Préparation vectorielle (One-time)

```
events.json
    ↓
chunk_events.py
    • Divise les descriptions longues en chunks
    • Préserve les métadonnées (dates, source)
    • Génère chunk_id unique
    ↓
events_chunks.json (environ 1000+ chunks)
```

**Logique** : Chunks chevauchants pour meilleure contexte (voir code)

### Phase 3 : Indexation vectorielle (One-time)

```
events_chunks.json
    ↓
build_faiss.py
    • Charge les chunks
    • Génère embeddings via HuggingFace (all-MiniLM-L6-v2)
    • Crée un index FAISS (vector search)
    • Sauvegarde localement
    ↓
faiss_index/ (binary format)
```

**Modèle d'embeddings** : `sentence-transformers/all-MiniLM-L6-v2`

### Phase 4 : Inference (Runtime - À chaque question)

```
Question utilisateur
    ↓ (via API /ask)
    ↓
chatbot.answer(question)
    │
    ├─ 1. Date Extraction
    │  • Prompt LLM : Extrait année/mois de la question
    │  • Retour : {"year": "2026", "month": "08"} ou {}
    │
    ├─ 2. Retrieval (FAISS)
    │  • Cherche les 500 chunks les plus pertinents
    │  • Utilise similarity_search (cosine distance)
    │
    ├─ 3. Temporal Filtering
    │  • Si date extraite : filtre par date (start_date ≤ end ≤ end_date)
    │  • Retour : documents pertinents datés
    │
    └─ 4. Answer Generation
       • Combine contexte + question
       • Prompt LLM : "Réponds UNIQUEMENT à partir du contexte"
       • Retour : Réponse structurée
    ↓
Response JSON {"answer": "..."}
```

---

## 🛠️ Technologie

### Framework & Librairies

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Web Framework** | FastAPI | Latest |
| **ASGI Server** | Uvicorn | Latest |
| **RAG Framework** | LangChain | Latest |
| **LLM** | Mistral AI (mistral-small-latest) | - |
| **Vector DB** | FAISS (CPU) | Latest |
| **Embeddings** | HuggingFace Transformers | all-MiniLM-L6-v2 |
| **Data Processing** | Pandas | Latest |
| **HTTP** | Requests | Latest |
| **Evaluation** | RAGAS + Datasets | Latest |
| **Config** | python-dotenv | Latest |
| **Containerization** | Docker | Latest |

### Stack Technical

```
┌─────────────────────────────────┐
│   Frontend/Client               │
│   (HTTP Client, Swagger UI)     │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   FastAPI + Uvicorn             │
│   (Web Server)                  │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   LangChain RAG Engine          │
│   (Orchestration)               │
└────────────┬────────────────────┘
             │
    ┌────────┴─────────┐
    │                  │
┌───▼───┐        ┌─────▼──────┐
│ FAISS │        │ Mistral AI │
│Vector │        │   LLM      │
│ Store │        └────────────┘
└───────┘
```

---

## 🧪 Tests et Évaluation

### 1. Test d'API simple

**Fichier** : `tests/api_test.py`

```bash
python tests/api_test.py
```

**Test** :
```python
response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": "Quels événements culturels à Bordeaux ?"}
)
print(response.status_code)  # 200
print(response.json())       # {"answer": "..."}
```

### 2. Évaluation RAGAS

**Fichier** : `tests/evaluate_rag.py`

Évalue la qualité du RAG sur 4 questions de test :

```bash
python tests/evaluate_rag.py
```

**Métriques** :
- **Faithfulness** : Le RAG reste-t-il fidèle au contexte ?
- **Answer Relevancy** : Les réponses sont-elles pertinentes à la question ?

**Questions d'évaluation** :
1. "Quels événements culturels ont lieu à Bordeaux ?"
2. "Quels concerts ou événements de musique pop ?"
3. "Quels événements le 10 décembre 2025 ?"
4. "Qui a gagné la Coupe du monde ?" (test hors-domaine)

### 3. Test de recherche

**Fichier** : `test_search.py`

Teste la recherche vectorielle directe FAISS.

---

## 🐳 Docker

### Build l'image

```bash
docker build -t rag-events:latest .
```

### Lancer le conteneur

```bash
docker run -p 8000:8000 \
  -e MISTRAL_API_KEY=votre_clé \
  rag-events:latest
```

L'API sera disponible sur : **http://localhost:8000**

### Dockerfile

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Exemples d'utilisation

### Exemple 1 : Question simple

**Question** : "Quels événements culturels à Bordeaux ?"

**Processus** :
1. Aucune date trouvée dans la question
2. Retrieval de 500 chunks pertinents
3. Génération de réponse contextuelle

**Réponse attendue** :
```
"Les événements culturels à Bordeaux incluent des expositions d'art 
contemporain au CAPC, des spectacles vivants au Grand-Théâtre, 
des conférences et ateliers artistiques..."
```

### Exemple 2 : Question avec date

**Question** : "Quels événements en août 2026 à Bordeaux ?"

**Processus** :
1. LLM extrait : `{"year": "2026", "month": "08"}`
2. Retrieval de 500 chunks
3. Filtrage par date : `2026-08-01 ≤ event.date ≤ 2026-08-31`
4. Génération de réponse filtrée

**Réponse attendue** :
```
"Les événements prévus en août 2026 incluent..."
```

### Exemple 3 : Question hors-domaine

**Question** : "Qui a remporté la Coupe du monde ?"

**Processus** :
1. Aucun événement pertinent trouvé
2. Contexte vide
3. LLM répond : "Cette question n'est pas liée aux événements..."

**Réponse attendue** :
```
"Je ne dispose d'informations que sur les événements culturels à Bordeaux."
```

---

## 🤝 Contribution

Pour contribuer au projet :

1. **Fork** le repository
2. **Créez une branche** : `git checkout -b feature/ma-feature`
3. **Committez** : `git commit -m "Ajout de ma feature"`
4. **Push** : `git push origin feature/ma-feature`
5. **Ouvrez une Pull Request**

### Améliorations futures

- [ ] Support multi-langues (EN, ES, DE)
- [ ] Caching des embeddings
- [ ] Filtrage par catégorie d'événements
- [ ] Intégration avec d'autres agendas
- [ ] Authentification utilisateur
- [ ] Dashboard de monitoring
- [ ] Export PDF des réponses
- [ ] Support des images d'événements

---

## 📝 Notes techniques

### Optimisations possibles

1. **Cache FAISS** : Les embeddings sont calculés une seule fois
2. **Batch Processing** : Traiter plusieurs questions en parallèle
3. **Temporal Indexing** : Créer des sous-index par date
4. **Chunking Strategy** : Ajuster la taille des chunks
5. **Embedding Model** : Tester d'autres modèles (multilingual)

### Limitations actuelles

⚠️ **OpenAgenda** : Limité aux données de la Ville de Bordeaux  
⚠️ **FAISS CPU** : Plus lent que GPU (voir `faiss-gpu`)  
⚠️ **Modèle LLM** : Mistral Small (pas de modèle plus puissant ici)  
⚠️ **Contexte** : 500 chunks peut être important pour le contexte LLM  

---

## 📞 Support

Pour toute question ou problème :

1. Vérifiez les **issues** existantes
2. Consultez la documentation **LangChain** et **FastAPI**
3. Vérifiez les **logs** dans `config/logger.py`
4. Créez une **nouvelle issue** avec détails

---

## 📄 Licence

Ce projet est fourni à titre de démonstration éducatif dans le cadre de la formation IA.

---

## 🎓 Créé avec ❤️

Système de Retrieval-Augmented Generation pour les événements culturels de Bordeaux.  
Framework: **LangChain** | LLM: **Mistral AI** | Vector DB: **FAISS** | API: **FastAPI**

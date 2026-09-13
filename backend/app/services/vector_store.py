import json
import os

import faiss
import numpy as np


# ======================================================
# CONFIGURATION
# ======================================================

VECTOR_STORE_DIR = "vector_store"

INDEX_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "documents.index"
)

MAPPING_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "mapping.json"
)

# all-MiniLM-L6-v2 produces 384-dimensional embeddings
EMBEDDING_DIMENSION = 384


# ======================================================
# INITIALIZE VECTOR STORE DIRECTORY
# ======================================================

def ensure_vector_store_directory():
    """
    Create the vector store directory if it does not exist.
    """

    os.makedirs(
        VECTOR_STORE_DIR,
        exist_ok=True
    )


# ======================================================
# CREATE EMPTY FAISS INDEX
# ======================================================

def create_empty_index():
    """
    Create a new FAISS index.

    IndexFlatL2 uses Euclidean distance.
    """

    return faiss.IndexFlatL2(
        EMBEDDING_DIMENSION
    )


# ======================================================
# LOAD FAISS INDEX
# ======================================================

def load_index():
    """
    Load the existing FAISS index.

    If no index exists, create a new one.
    """

    ensure_vector_store_directory()

    if not os.path.exists(INDEX_PATH):

        print(
            "FAISS index does not exist. "
            "Creating a new index."
        )

        return create_empty_index()

    index = faiss.read_index(
        INDEX_PATH
    )

    # Verify embedding dimension
    if index.d != EMBEDDING_DIMENSION:

        raise ValueError(
            f"FAISS index dimension is "
            f"{index.d}, but expected "
            f"{EMBEDDING_DIMENSION}."
        )

    return index


# ======================================================
# SAVE FAISS INDEX
# ======================================================

def save_index(index):
    """
    Save the FAISS index to disk.
    """

    ensure_vector_store_directory()

    faiss.write_index(
        index,
        INDEX_PATH
    )


# ======================================================
# LOAD MAPPING
# ======================================================

def load_mapping():
    """
    Load FAISS position -> PostgreSQL chunk ID mapping.

    The mapping is stored as a dictionary:

    {
        "0": 101,
        "1": 102,
        "2": 103
    }

    where:

        FAISS position 0 -> chunk ID 101
        FAISS position 1 -> chunk ID 102
        FAISS position 2 -> chunk ID 103
    """

    ensure_vector_store_directory()

    if not os.path.exists(MAPPING_PATH):

        return {}

    try:

        with open(
            MAPPING_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            mapping = json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        print(
            "Warning: Could not read mapping.json. "
            "Starting with an empty mapping."
        )

        return {}

    # ------------------------------------------
    # Normal dictionary format
    # ------------------------------------------

    if isinstance(mapping, dict):

        return mapping

    # ------------------------------------------
    # Backward compatibility:
    # if the old mapping was a list,
    # convert it into a dictionary.
    # ------------------------------------------

    if isinstance(mapping, list):

        converted_mapping = {}

        for index, chunk_id in enumerate(mapping):

            converted_mapping[str(index)] = chunk_id

        return converted_mapping

    raise ValueError(
        "Invalid mapping.json format. "
        "Expected a dictionary or list."
    )


# ======================================================
# SAVE MAPPING
# ======================================================

def save_mapping(mapping):
    """
    Save the FAISS position -> chunk ID mapping.
    """

    ensure_vector_store_directory()

    with open(
        MAPPING_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            mapping,
            file,
            indent=2
        )


# ======================================================
# ADD EMBEDDINGS TO FAISS
# ======================================================

def add_embeddings_to_faiss(
    embeddings,
    chunk_ids
):
    """
    Add embeddings to the FAISS index and update
    the FAISS-position -> PostgreSQL chunk-ID mapping.

    Parameters
    ----------
    embeddings:
        NumPy array or list of embedding vectors.

    chunk_ids:
        PostgreSQL document chunk IDs corresponding
        to the embeddings.
    """

    # ------------------------------------------
    # Validate input
    # ------------------------------------------

    if embeddings is None:

        raise ValueError(
            "Embeddings cannot be None."
        )

    if chunk_ids is None:

        raise ValueError(
            "chunk_ids cannot be None."
        )

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )

    # ------------------------------------------
    # Handle single embedding
    # ------------------------------------------

    if embeddings.ndim == 1:

        embeddings = embeddings.reshape(
            1,
            -1
        )

    # ------------------------------------------
    # Validate dimensions
    # ------------------------------------------

    if embeddings.ndim != 2:

        raise ValueError(
            "Embeddings must be a 2-dimensional array."
        )

    if embeddings.shape[1] != EMBEDDING_DIMENSION:

        raise ValueError(
            f"Embedding dimension is "
            f"{embeddings.shape[1]}, expected "
            f"{EMBEDDING_DIMENSION}."
        )

    # ------------------------------------------
    # Validate number of embeddings
    # ------------------------------------------

    if len(embeddings) != len(chunk_ids):

        raise ValueError(
            f"Number of embeddings "
            f"({len(embeddings)}) does not match "
            f"number of chunk IDs "
            f"({len(chunk_ids)})."
        )

    if len(embeddings) == 0:

        print(
            "No embeddings to add."
        )

        return {
            "added": 0,
            "total_vectors": 0
        }

    # ------------------------------------------
    # Load index
    # ------------------------------------------

    index = load_index()

    # ------------------------------------------
    # Load mapping
    # ------------------------------------------

    mapping = load_mapping()

    # ------------------------------------------
    # Current FAISS vector count
    # ------------------------------------------

    start_position = index.ntotal

    print(
        f"FAISS vectors before adding: "
        f"{start_position}"
    )

    # ------------------------------------------
    # Add embeddings
    # ------------------------------------------

    index.add(
        embeddings
    )

    # ------------------------------------------
    # Update mapping
    #
    # IMPORTANT:
    # mapping is a dictionary, so we do NOT use
    # mapping.append().
    # ------------------------------------------

    for offset, chunk_id in enumerate(
        chunk_ids
    ):

        faiss_position = (
            start_position +
            offset
        )

        mapping[
            str(faiss_position)
        ] = int(chunk_id)

    # ------------------------------------------
    # Verify mapping size
    # ------------------------------------------

    if len(mapping) < index.ntotal:

        raise RuntimeError(
            "FAISS index and mapping are inconsistent. "
            f"Index contains {index.ntotal} vectors, "
            f"but mapping contains {len(mapping)} entries."
        )

    # ------------------------------------------
    # Save everything
    # ------------------------------------------

    save_index(
        index
    )

    save_mapping(
        mapping
    )

    print(
        f"Added {len(embeddings)} embeddings "
        f"to FAISS."
    )

    print(
        f"FAISS vectors after adding: "
        f"{index.ntotal}"
    )

    return {
        "added": len(embeddings),
        "total_vectors": index.ntotal
    }


# ======================================================
# SEARCH FAISS
# ======================================================

def search_faiss(
    query_embedding,
    top_k: int = 5
):
    """
    Search the FAISS vector store.

    Returns:

    [
        {
            "chunk_id": 123,
            "distance": 0.42
        },
        ...
    ]
    """

    if top_k <= 0:

        raise ValueError(
            "top_k must be greater than 0."
        )

    # ------------------------------------------
    # Convert query embedding
    # ------------------------------------------

    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32
    )

    # ------------------------------------------
    # Handle one-dimensional embedding
    # ------------------------------------------

    if query_embedding.ndim == 1:

        query_embedding = query_embedding.reshape(
            1,
            -1
        )

    # ------------------------------------------
    # Validate dimensions
    # ------------------------------------------

    if query_embedding.shape[1] != EMBEDDING_DIMENSION:

        raise ValueError(
            f"Query embedding dimension is "
            f"{query_embedding.shape[1]}, expected "
            f"{EMBEDDING_DIMENSION}."
        )

    # ------------------------------------------
    # Load index
    # ------------------------------------------

    index = load_index()

    # ------------------------------------------
    # Empty index
    # ------------------------------------------

    if index.ntotal == 0:

        return []

    # ------------------------------------------
    # Load mapping
    # ------------------------------------------

    mapping = load_mapping()

    # ------------------------------------------
    # Search
    # ------------------------------------------

    actual_top_k = min(
        top_k,
        index.ntotal
    )

    distances, indices = index.search(
        query_embedding,
        actual_top_k
    )

    results = []

    for distance, faiss_index in zip(
        distances[0],
        indices[0]
    ):

        # FAISS can return -1 when no result exists
        if faiss_index < 0:
            continue

        # --------------------------------------
        # Get chunk ID
        # --------------------------------------

        chunk_id = mapping.get(
            str(int(faiss_index))
        )

        # Backward compatibility for mappings
        # that may contain integer keys.
        if chunk_id is None:

            chunk_id = mapping.get(
                int(faiss_index)
            )

        if chunk_id is None:

            print(
                f"Warning: No mapping found for "
                f"FAISS position {faiss_index}."
            )

            continue

        results.append(
            {
                "chunk_id": int(chunk_id),
                "distance": float(distance)
            }
        )

    return results


# ======================================================
# GET VECTOR STORE INFORMATION
# ======================================================

def get_vector_store_info():
    """
    Return information about the FAISS vector store.
    """

    index = load_index()

    mapping = load_mapping()

    return {
        "index_path": INDEX_PATH,
        "mapping_path": MAPPING_PATH,
        "embedding_dimension": EMBEDDING_DIMENSION,
        "total_vectors": index.ntotal,
        "total_mappings": len(mapping),
        "consistent": (
            index.ntotal == len(mapping)
        )
    }
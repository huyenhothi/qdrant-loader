import threading
import spacy
from spacy.cli import download
import logging

logger = logging.getLogger(__name__)

_SPACY_MODELS: dict[str, "spacy.Language"] = {}
_SPACY_LOCK = threading.Lock()


def get_spacy_model(model_name: str):
    """
    Load spaCy model once per process per model_name.
    Thread-safe.
    """
    if model_name in _SPACY_MODELS:
        return _SPACY_MODELS[model_name]

    with _SPACY_LOCK:
        # Double-check to avoid race
        if model_name in _SPACY_MODELS:
            return _SPACY_MODELS[model_name]

        try:
            nlp = spacy.load(model_name)
        except OSError:
            logger.info(f"Downloading spaCy model {model_name}...")
            download(model_name)
            nlp = spacy.load(model_name)

        # Optimize pipeline: disable parser only
        if "parser" in nlp.pipe_names:
            essential_pipes = [p for p in nlp.pipe_names if p != "parser"]
            nlp.select_pipes(enable=essential_pipes)

        _SPACY_MODELS[model_name] = nlp
        logger.info(
            "Loaded spaCy model %s (id=%s)", model_name, id(nlp)
        )
        return nlp

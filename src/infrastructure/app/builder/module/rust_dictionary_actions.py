from enum import Enum

class rust_dictionary_actions(Enum):
    APP: str = "rust-dictionary"
    RESOLVE: str = 'resolve'
    ADD_WORD: str = 'add-word'
    REMOVE_WORD: str = 'remove-word'
    NEW_CLUE: str = 'new-clue'
    UPDATE_SCORE: str = 'update-score'
    RESOLVE_SCORE: str = 'resolve-score'
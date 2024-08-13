import pytest
from app.services.data_service import get_super_wv, create_word_vector
import scipy

def test_get_super_wv():    
    # Act
    word_vector = get_super_wv()

    # Assert
    assert isinstance(word_vector, scipy.sparse._csr.csr_matrix)  # check that the output is a list


def test_create_word_vector():
    # Arrange
    keywords = ["this", "is", "an", "example"]

    # Act
    word_vector = create_word_vector(keywords)

    # Assert
    assert isinstance(word_vector, scipy.sparse._csr.csr_matrix)  # check that the output is a list

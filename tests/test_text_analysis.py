import pytest
from app.services.text_analysis import generate_keywords

def test_generate_keywords():
    # Arrange
    text = "This is a test sentence for keyword extraction."

    # Act
    keywords = generate_keywords(text)

    # Assert
    assert isinstance(keywords, list)
    assert all(isinstance(kw, str) for kw in keywords)
    assert "this" in keywords
    assert "test" in keywords
    assert "sentence" in keywords
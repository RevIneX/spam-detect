import pytest
from app.ml_service import spam_detector

def test_model_loaded():
    assert spam_detector.classifier is not None
    assert spam_detector.model_name is not None

def test_predict_spam():
    result = spam_detector.predict("Click here to claim your free iPhone 15 and win a $1000 gift card immediately!")
    assert "result" in result
    assert "score" in result
    assert result["result"] in ["SPAM", "HAM"]
    assert 0 <= result["score"] <= 1

def test_predict_ham():
    result = spam_detector.predict("Ayo bruh! how a y doing today?")
    assert "result" in result
    assert "score" in result
    assert isinstance(result["score"], float)

def test_predict_empty_string():
    result = spam_detector.predict("")
    assert result is not None

def test_predict_short_text():
    result = spam_detector.predict("Hi")
    assert result is not None
    assert "result" in result

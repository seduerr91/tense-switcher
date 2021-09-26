from __future__ import unicode_literals, print_function
import persuasion_service
import pytest

persuasion = persuasion_service.PERSUASION()

def test_correct_transformation_3_nouns():
    original = "Phil, Bob and Tom are not going to the school and they have fun doing this."
    to_tense = 'past'
    expected = "Phil, Bob and Tom were not going to the school and they had fun doing this."
    result = persuasion.transformer(original, to_tense)

    assert result == expected

def test_correct_transformation_1_nouns():
    original = "Phil is not going to the school."
    to_tense = 'past'
    expected = "Phil was not going to the school."
    result = persuasion.transformer(original, to_tense)

    assert result == expected

def test_future_tense():
    original = "Phil is not going to the school."
    to_tense = 'future'
    expected = "Phil will be not going to the school."
    result = persuasion.transformer(original, to_tense)

    assert result == expected
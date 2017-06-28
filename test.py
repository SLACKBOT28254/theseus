import theseus
from StringIO import StringIO

def true_is_true():
    assert true == true





def test_is_greeting_accurately_recognised():
    assert theseus.is_a_greeting('hi okay soo this is good') == True
    assert theseus.is_a_greeting('okay soo this is good') == False
    assert theseus.is_a_greeting('okay soo HI this is good') == True
    assert theseus.is_a_greeting('okay soo hellothis is good') == False
    assert theseus.is_a_greeting('okay HEY is good') == True
    assert theseus.is_a_greeting('yoyo') == False
    assert theseus.is_a_greeting('yo') == True

def test_opening_hours_questions_accurately_recognises_opening_hours_query():
    assert theseus.opening_hours_questions('What are your opening hours?') == True
    assert theseus.opening_hours_questions('okay soo this is good') == False
    assert theseus.opening_hours_questions('okay soo hi this is good') == False
    assert theseus.opening_hours_questions('When are you open?') == True
    assert theseus.opening_hours_questions('okay soo hellothis is good') == False
    assert theseus.opening_hours_questions('What time can I call until?') == True
    assert theseus.opening_hours_questions('okay hey hey is good') == False
    assert theseus.opening_hours_questions('yoyo') == False
    assert theseus.opening_hours_questions('Opening times') == True


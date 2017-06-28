import theseus
from StringIO import StringIO

def true_is_true():
    assert true == true

def test_logged_events_returns_expected_test():
    expected_output = "--NEW EVENT LOG--\n\nUSER: U60S6CM3Q\nCHANNEL: None\nTYPE: presence_change\nTEXT: None"
    out = StringIO()
    event = {u'type': u'presence_change', u'user':u'U60S6CM3Q', u'presence': u'active'}

    theseus.log_event(event, out=out)
    real_output = out.getvalue().strip()

def test_is_greeting_accurately_recognises_greeting():
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

def test_likely_loans_questions_accurately_recognises_likely_loans_query():
    assert theseus.likely_loans_queries('okay soo this is good') == False
    assert theseus.likely_loans_queries("Who are likely loans?") == True
    assert theseus.likely_loans_queries("okay hi this is excellent") == False
    assert theseus.likely_loans_queries("What is likely loans?") == True
    assert theseus.likely_loans_queries("okay hey this is really good") == False
    

def test_oakbrook_finance_questions_recognises_oakbrook_finance_query():
    assert theseus.oakbrook_finance_query("what is oakbrook?") == True
    assert theseus.oakbrook_finance_query("what is finance?") == False
    assert theseus.oakbrook_finance_query("what is oakbrook finance?") == True
    assert theseus.oakbrook_finance_query("what is this company?") == False
    assert theseus.oakbrook_finance_query("Who is oakbrook finance?") == True
    assert theseus.oakbrook_finance_query("Hey this is finance") == False
    assert theseus.oakbrook_finance_query("Who is Oakbrook?") == True
    assert theseus.oakbrook_finance_query("Oakbrook Finance") == True

def test_loan_questions_recognises_loan_query():
    assert theseus.min_and_max_loan_query("What is the minimum loan?") == True
    assert theseus.min_and_max_loan_query("Loan range") == False
    assert theseus.min_and_max_loan_query("How much can I borrow?") == True
    assert theseus.min_and_max_loan_query("hey is this loans") == False
    assert theseus.min_and_max_loan_query("What is the maximum loan?") == True
    assert theseus.min_and_max_loan_query("Likely loans") == False
    assert theseus.min_and_max_loan_query("How much can I loan?") == True
    assert theseus.min_and_max_loan_query("Hello is this loan") == False
    assert theseus.min_and_max_loan_query("How much can I loan?") == True


def test_arrangement_fee_questions_recognises_arrangement_fee_query():
    assert theseus.arrangement_fee_query("Do you charge an arrangement fee?") == True
    assert theseus.arrangement_fee_query("Hello admit this") == False
    assert theseus.arrangement_fee_query("Is there an arrangement fee?") == True
    assert theseus.arrangement_fee_query("Can this be arranged?") == False
    assert theseus.arrangement_fee_query("Arrangement fee") == True
    assert theseus.arrangement_fee_query("Admin fee") == True
    assert theseus.arrangement_fee_query("Will I be charged for admin?") == True
   
    

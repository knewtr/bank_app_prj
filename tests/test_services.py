from src.services import bank_investment


def test_bank_investment(operation_list):
    assert bank_investment("2018-02", operation_list, 50) == 15.0
    assert bank_investment("2019-01", operation_list, 50) == 54.0
    assert bank_investment("2019-03", operation_list, 50) == 0.0
from characteristic_parameters._helpers import all_equal


def test_all_equal():

    # Arrange
    list_to_be_tested_true = [2, 2, 2, 2]
    list_to_be_tested_false = [1,2,3,1]

    # Act & Assert
    assert all_equal(list_to_be_tested_true)
    assert not all_equal(list_to_be_tested_false)

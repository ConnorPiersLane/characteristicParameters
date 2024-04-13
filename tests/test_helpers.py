from characteristicParameters._helpers import all_are_close


def test_all_are_close():
    # Arrange
    list_to_be_tested_true = [2, 2, 2, 2]
    list_to_be_tested_false = [1, 2, 3, 1]

    # Act & Assert
    assert all_are_close(list_to_be_tested_true)
    assert not all_are_close(list_to_be_tested_false)

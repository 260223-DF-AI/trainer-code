import pytest
from src.functions import Functions

@pytest.fixture
def func():
    return Functions()


class TestMoreFunctions:
    
    def test_add(self, func):
        # ARRANGE - SETUP
            # setup resource, predict your outcome
        expected = 20
        #func = Functions()

        # ACT - DO THE THING
        actual = func.add(10, 10)

        # ASSERT - VERIFY
        # asserting (actual) == (expected)
          
        assert actual == expected

        assert (func.add(10, 10)) == (20)
        assert func.add(-1, 1) == 0
        #now!
        assert func.add(0, 0) == 0 
    
    def test_division(self, func):
        # Arrange
        #func = Functions()

        # Act & Assert
        with pytest.raises(ValueError):
            func.divide(10, 0)


    
    def test_division(self, func):
        # Arrange
        #func = Functions()
        expected = 10
        actual = func.divide(10, 0)
        # Act & Assert
        assert (actual) == (expected)
    

import pytest
from src.functions import Functions

@pytest.fixture
def func():
    return Functions()


class TestFunctions:
    
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
    


    @pytest.mark.parametrize("a, b, expected", [
        (2, 2, 0),
        (3, 2, 1),
        (4, 2, 2),
        (5, 2, 3),
        (0, -2, 2),
        (2, 4, -2),
        (-1, -1, 0)
    ])
    def test_subtract(self, func, a, b, expected):
        # Arrange
        # parameterized and fixtured!

        # Act
        actual = func.subtract(a, b)

        # Assert
        assert actual == expected

    @pytest.mark.parametrize("n, expected", [
        (0, False),
        (1, True),
        (2, False),
        (3, True),
        (4, False),
        (10, False)
    ])
    def test_is_odd(self, func, n, expected):
        # Arrange
        # Act
        actual = func.is_odd(n)
        # Assert
        assert actual == expected




        '''
        
        
        Happy Path           ||           Unhappy Path
                            boundry case
                                                        edge case
        
        '''
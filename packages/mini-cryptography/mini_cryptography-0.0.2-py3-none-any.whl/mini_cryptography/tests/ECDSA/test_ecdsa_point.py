from mini_cryptography.ecdsa import Point, Field

def test_to_array_type():
    point = Point(1, 1)
    assert isinstance(point.to_array(), list)

def test_to_array_value():
    point = Point(1, 1)
    array = point.to_array()
    print([1, 1])
    
    assert array == [1, 1]

def test_point_equality():
    point1 = Point(1, 1)
    point2 = Point(1, 1)

    assert point1 == point2

def test_point_equality_not_equals():
    point = Point(1, 1)
    field = Field(1, 1, 1, 1, point)

    assert NotImplemented is point.__eq__(field)

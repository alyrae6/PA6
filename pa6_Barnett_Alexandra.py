####################################################################
# PA6
# Alexandra Barnett
#
# This program implements an unsorted map in which each key is
# associated with a list.
####################################################################


class MapBase:
    """Base class for map structures."""

    class _Item:
        """Stores one key-value pair."""

        __slots__ = "_key", "_value"

        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key


class UnsortedTableMap(MapBase):
    """Map implementation using an unsorted Python list."""

    def __init__(self):
        self._table = []

    def __getitem__(self, key):
        for item in self._table:
            if key == item._key:
                return item._value

        raise KeyError("Key not found: " + str(key))

    def __setitem__(self, key, value):
        for item in self._table:
            if key == item._key:
                item._value = value
                return

        self._table.append(self._Item(key, value))

    def __delitem__(self, key):
        for index in range(len(self._table)):
            if key == self._table[index]._key:
                self._table.pop(index)
                return

        raise KeyError("Key not found: " + str(key))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key


class UnsortedMapOfLists(UnsortedTableMap):
    """An unsorted map whose values are lists."""

    def __getitem__(self, position):
        # We check whether position is a tuple because a tuple contains
        # both a key and an index. A regular key returns the entire list.
        if not isinstance(position, tuple):
            return super().__getitem__(position)

        key, index = position
        values = super().__getitem__(key)

        if index >= len(values) or index < -len(values):
            raise IndexError(
                "Index "
                + str(index)
                + " is outside the list associated with key "
                + str(key)
            )

        return values[index]

    def __setitem__(self, position, value):
        # If no index is supplied, store the complete list as the value.
        if not isinstance(position, tuple):
            super().__setitem__(position, value)
            return

        key, index = position

        try:
            values = super().__getitem__(key)

            if index < -len(values):
                raise IndexError(
                    "Index "
                    + str(index)
                    + " is outside the list associated with key "
                    + str(key)
                )

            if index < len(values):
                values[index] = value

            elif index == len(values):
                values.append(value)

            else:
                raise IndexError(
                    "Index "
                    + str(index)
                    + " is outside the list associated with key "
                    + str(key)
                )

        except KeyError:
            if index != 0:
                raise IndexError(
                    "The first element for a new key must use index 0."
                )

            super().__setitem__(key, [value])

    def __delitem__(self, position):
        """
        Delete one element when a key and index are given.
        Delete the complete list when only a key is given.
        """

        if not isinstance(position, tuple):
            super().__delitem__(position)
            return

        key, index = position
        values = super().__getitem__(key)

        if index >= len(values) or index < -len(values):
            raise IndexError(
                "Index "
                + str(index)
                + " is outside the list associated with key "
                + str(key)
            )

        del values[index]


def swap_arrays(my_map, first_key, second_key):
    """Swap the complete lists associated with two keys."""

    first_array = my_map[first_key]
    second_array = my_map[second_key]

    my_map[first_key] = second_array
    my_map[second_key] = first_array


def main():
    """Test all required assignment operations."""

    my_map = UnsortedMapOfLists()

    # Test __setitem__ with keys and indexes.
    my_map["a", 0] = 5
    my_map["a", 0] = 50
    my_map["a", 1] = 60

    my_map["b", 0] = 2

    # Test storing an entire list.
    my_map["d"] = [10, 20, 30]

    print("1. Original lists")
    print("a =", my_map["a"])
    print("b =", my_map["b"])
    print("d =", my_map["d"])

    # Test __getitem__ with an index.
    print()
    print("2. Elements reached by index")
    print('my_map["a", 0] =', my_map["a", 0])
    print('my_map["a", 1] =', my_map["a", 1])

    # Test deleting one element.
    del my_map["a", 0]

    print()
    print("3. After deleting index 0 from a")
    print("a =", my_map["a"])

    # Test the swap function.
    swap_arrays(my_map, "a", "d")

    print()
    print("4. After swapping a and d")
    print("a =", my_map["a"])
    print("d =", my_map["d"])

    # Test deleting an entire list.
    del my_map["b"]

    print()
    print("5. After deleting the entire list associated with b")

    try:
        print("b =", my_map["b"])

    except KeyError:
        print("Key b was deleted successfully.")

    print()
    print("All tests completed successfully.")


if __name__ == "__main__":
    main()
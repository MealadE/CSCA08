"""Assignment 2 functions."""

from copy import deepcopy

# Examples to use in doctests:
THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]

# Used to compare floats in doctests:
# If the difference between the expected return value and the actual return
# value is less than EPSILON, we will consider the test passed.
EPSILON = 0.005


# We provide a full docstring for this function as an example.
def compare_elevations_within_row(elevation_map: list[list[int]], map_row: int,
                                  level: int) -> list[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """
    new = [0, 0, 0]
    sublist = elevation_map[map_row]
    for item in sublist:
        if item < level:
            new[0] = new[0] + 1
        if item == level:
            new[1] = new[1] + 1
        if item > level:
            new[2] = new[2] + 1
    return new


# We provide a partial doctest in this function as an example of
# testing a function that modifies its input. Note the use of deepcopy
# to create a copy of the nested list to use in the function call. We
# do this to make sure that different doctests do not affect each
# other.


def update_elevation(elevation_map: list[list[int]], start: list[int],
                     stop: list[int], delta: int) -> None:
    """Modify elevation_map with each cell between start and stop
    changed by delta.

    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = deepcopy(FOUR_BY_FOUR)
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]

    """
    elevation_map[stop[0]][stop[1]] += delta
    while start != stop:
        if start[0] == stop[0]:
            elevation_map[start[0]][start[1]] += delta
            start = [start[0], start[1] + 1]
        elif start[1] == stop[1]:
            elevation_map[start[0]][start[1]] += delta
            start = [start[0] + 1, start[1]]


# We provide a partial doctest in this function as an example of
# testing a function that returns a float. Note the use of abs and
# EPSILON to check if two floats are "close enough". We do this to
# deal with inevitable errors that arise in floating point arithmetic.


def get_average_elevation(elevation_map: list[list[int]]) -> float:
    """Return the average elevation across all cells in
    elevation_map.

    >>> abs(get_average_elevation(UNIQUE_3X3) - 5.0) < EPSILON
    True
    >>> abs(get_average_elevation(FOUR_BY_FOUR) - 3.8125) < EPSILON
    True
    """
    total = 0
    counter = 0
    for item in elevation_map:
        for num in item:
            total += num
            counter += 1
    return total / counter


def find_peak(elevation_map: list[list[int]]) -> list[int]:
    """Return the cell of the highest elevation point in
    elevation_map.

    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(UNIQUE_4X4)
    [0, 3]
    """
    new = []
    cell = []
    for item in elevation_map:
        new.append(max(item))
    highest = max(new)
    for index in range(len(elevation_map)):
        if highest in elevation_map[index]:
            cell.append(index)
    for item2 in elevation_map:
        for index1 in range(len(item2)):
            if item2[index1] == highest:
                cell.append(index1)
    return cell


def is_sink(elevation_map: list[list[int]], cell: list[int]) -> bool:
    """Return True iff cell is a sink in elevation_map.

    >>> is_sink(THREE_BY_THREE, [0, 0])
    True
    >>> is_sink(FOUR_BY_FOUR, [0, 1])
    False
    >>> is_sink(UNIQUE_3X3, [2, 0])
    True
    >>> is_sink(UNIQUE_4X4, [2, 1])
    False
    """
    if is_valid_cell(cell, len(elevation_map)):
        adjacent = get_adjacent_cells(cell, len(elevation_map))
        values = []
        values.append(elevation_map[cell[0]][cell[1]])
        for item in adjacent:
            values.append(
                elevation_map[item[0]][item[1]])
        if min(values) == elevation_map[cell[0]][cell[1]]:
            return True
    return False


def find_local_sink(elevation_map: list[list[int]],
                    cell: list[int]) -> list[int]:
    """Return the cell that is a sink that is adjacent or is cell
    in elevation_map.

    >>> find_local_sink(UNIQUE_3X3, [1, 1])
    [0, 0]
    >>> find_local_sink(UNIQUE_4X4, [2, 1])
    [2, 0]
    >>> find_local_sink(UNIQUE_4X4, [3, 3])
    [2, 2]
    """
    local_sink = cell
    adjacent = get_adjacent_cells(cell, len(elevation_map))
    for item in adjacent:
        if elevation_map[item[0]][item[1]] < \
                elevation_map[local_sink[0]][local_sink[1]]:
            local_sink = item
    return local_sink


def can_hike_to(elevation_map: list[list[int]], start: list[int],
                dest: list[int], supplies: int) -> bool:
    """Return True iff able to reach dest from start in
    elevation_map with supplies available.

    >>> can_hike_to(THREE_BY_THREE, [2, 2], [1, 1], 5)
    True
    >>> can_hike_to(FOUR_BY_FOUR, [3, 3], [2, 1], 8)
    False
    >>> can_hike_to(FOUR_BY_FOUR, [3, 3], [1, 1], 7)
    True
    >>> can_hike_to(UNIQUE_3X3, [2, 1], [0, 1], 7)
    False
    >>> can_hike_to(UNIQUE_4X4, [3, 2], [1, 0], 17)
    True
    """
    while supplies >= 0:
        elevate_west = elevation_map[start[0]][start[1] - 1]
        elevate_north = elevation_map[start[0] - 1][start[1]]
        elevate_start = elevation_map[start[0]][start[1]]
        if start == dest:
            return True
        if abs(elevate_north - elevate_start) <= abs(elevate_west -
                                                     elevate_start) \
                and start[0] != dest[0] and start[1] != dest[1]:
            supplies -= abs(elevate_north - elevate_start)
            start = [start[0] - 1, start[1]]
        elif abs(elevate_west - elevate_start) < abs(elevate_north -
                                                     elevate_start) \
                and start[0] != dest[0] and start[1] != dest[1]:
            supplies -= abs(elevate_west - elevate_start)
            start = [start[0], start[1] - 1]
        elif start[1] == dest[1]:
            supplies -= abs(elevate_north - elevate_start)
            start = [start[0] - 1, start[1]]
        elif start[0] == dest[0]:
            supplies -= abs(elevate_west - elevate_start)
            start = [start[0], start[1] - 1]
    return False


def get_lower_resolution(elevation_map: list[list[int]]) -> list[list[int]]:
    """Return elevation_map as a new map with a decreased
    number of elevation points.

    >>> get_lower_resolution(FOUR_BY_FOUR)
    [[3, 4], [4, 3]]
    >>> get_lower_resolution(UNIQUE_4X4)
    [[7, 12], [9, 12]]
    >>> get_lower_resolution(UNIQUE_3X3)
    [[5, 5], [4, 6]]
    >>> get_lower_resolution(THREE_BY_THREE)
    [[3, 3], [7, 9]]
    """
    lower_res = []
    for index in range(len(elevation_map)):
        if index % 2 == 0:
            new_list = []
            for index1 in range(len(elevation_map[index])):
                new = 0
                number = 0
                if index1 % 2 == 0:
                    possible_cell = [[index, index1], [index + 1, index1],
                                     [index, index1 + 1],
                                     [index + 1, index1 + 1]]
                    for item in possible_cell:
                        if is_valid_cell(item, len(elevation_map)):
                            new += elevation_map[item[0]][item[1]]
                            number += 1
                    new_list.append(new // number)
            lower_res.append(new_list)
    return lower_res


# SUGGESTED HELPER FUNCTIONS #################################################
# These functions are not required in the assignment. However, we believe it is
# a great idea to define these functions and use them as helpers in the
# required functions.

def is_valid_cell(cell: list[int], dimension: int) -> bool:
    """Return True if and only if cell is a valid cell in an elevation map
    of dimensions dimension x dimension.

    Precondition: cell is a list of length 2.`

    >>> is_valid_cell([1, 1], 2)
    True
    >>> is_valid_cell([0, 2], 2)
    False

    """
    for item in cell:
        if item < 0:
            return False
        if item >= dimension:
            return False
    return True


def is_cell_lower(elevation_map: list[list[int]], cell_1: list[int],
                  cell_2: list[int]) -> bool:
    """Return True iff cell_1 has a lower elevation than cell_2.

    Precondition: elevation_map is a valid elevation map
                  cell_1 and cell_2 are valid cells in elevation_map

    >>> map = [[0, 1], [2, 3]]
    >>> is_cell_lower(map, [0, 0], [1, 1])
    True
    >>> is_cell_lower(map, [1, 1], [0, 0])
    False

    """
    return elevation_map[cell_1[0]][cell_1[1]] \
        < elevation_map[cell_2[0]][cell_2[1]]


def get_adjacent_cells(cell: list[int], dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell in an elevation map with
    dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.

    >>> adjacent_cells = get_adjacent_cells([1, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    >>> adjacent_cells = get_adjacent_cells([1, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]]

    """
    all_cells = [
        [cell[0] - 1, cell[1] - 1],
        [cell[0] - 1, cell[1]],
        [cell[0] - 1, cell[1] + 1],
        [cell[0], cell[1] - 1],
        [cell[0], cell[1] + 1],
        [cell[0] + 1, cell[1] - 1],
        [cell[0] + 1, cell[1]],
        [cell[0] + 1, cell[1] + 1]
    ]
    ans = []
    for item in all_cells:
        if is_valid_cell(item, dimension):
            ans.append(item)
    return ans


if __name__ == '__main__':
    import doctest

    doctest.testmod()

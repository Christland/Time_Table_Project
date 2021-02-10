import math
import pprint
import random

from sklearn.utils import shuffle

from _shared import NotEnoughRooms
from features.periods.service import get_periods
from features.rooms.service import get_rooms

from .services import get_exam_search
from features.rooms.distance_services import get_distance_between_rooms

# Function that updates the room capacity after extracting the number of rooms to be used for a particular exam
def __update_room_capacity(room, capacity):
    return {**room, 'size': capacity}


def get_index_max_room_size(room_data):
    """Function that gets room from room date with largest capacity

    Arguments:
       room date [list] -- get rooms with multiple room data columns

    Returns:
       room data with maximum room capacity
     """

    capacities = [room['size'] for room in room_data]

    return capacities.index(max(capacities))
def get_room_index_from_ls(rooms, index_returned):
    print('search_item,', index_returned)
    for id, room in enumerate(rooms):
        if room['roomName'] == index_returned:
            return id

def  get_next_room_to_be_allocated_index(updated_room, room_allocated):
    
    if len(room_allocated) == 0:
        max_room_index = get_index_max_room_size(updated_room)
        return max_room_index
    else:
        last_room_index = len(room_allocated) - 1
        room_in_vicinity = [room for room in updated_room if (get_distance_between_rooms(room_allocated[last_room_index]['roomName'], room['roomName']))[0] == 0.0]
        if len(room_in_vicinity) > 0:
            index_of_greatest =  get_index_max_room_size(room_in_vicinity)
            return get_room_index_from_ls(updated_room, room_in_vicinity[index_of_greatest]['roomName'])
        else:
            return get_index_max_room_size(updated_room)


def room_compute(current_student_size, room_data, room_allocated=None):
    """Function that calculates the rooms to be used by the enrolled students for an exams
       It assigns the room with maximum seats first. After room has been assigned it is removed from the room data list

    Arguments:
        current_student_size int -- students enrolled for an exam
        room_data [list] -- rooms available for a particular period

    Returns:
       room_allocated [list] -- room data for rooms assigned to pacrticular enrollment
       updated_room [list] -- room  name with remaining seats if any after assignment
     """
   
    if len(room_data) == 0:
        raise NotEnoughRooms

    room_allocated = room_allocated or []
    updated_room = room_data.copy()
    max_room_index = get_next_room_to_be_allocated_index(updated_room, room_allocated)
    # print(' room after', room_data[max_room_index])
    room_capacity = room_data[max_room_index]['size']
    remainder = room_capacity - current_student_size

    if remainder < 0:
        room_allocated.append(updated_room[max_room_index])
        updated_room.pop(max_room_index)
        
        return room_compute(abs(remainder), updated_room.copy(), room_allocated)

    elif remainder > 0:
        updated_room[max_room_index] = __update_room_capacity(updated_room[max_room_index], remainder)

        room_allocated.append(__update_room_capacity(updated_room[max_room_index], room_capacity - remainder))
        
        return room_allocated, updated_room
    else:
        room_allocated.append(updated_room[max_room_index])
        updated_room.pop(max_room_index)
        
        return room_allocated, updated_room
    


def period_room_allocation(periods, rooms):
    """Function that returns an assignment of rooms available for a list of period
        

    Arguments:
        periods [list] -- students enrolled for an exam
        rooms [list] -- rooms available for a particular period

    Returns:
       period_room [dict] -- room period assignment
     """
    period_room = {}
    periods = list(periods)
    room_arr = list(rooms)

    for period_id, _ in periods:
        room_data = room_arr.copy()
        random.shuffle(room_data)
        period_room[period_id] = room_data
    return period_room


if __name__ == "__main__":
    T1 = [('A110', 200), ('RMA', 102), ('RMB', 103)]
    # print(type(T1))
    # room_allocated = []
    # room_compute(300, T1, room_allocated)

    # print(room)
    # print(result)
    # periods = get_period()
    from main import app
    with app.app_context():
        rooms = get_index_max_room_size(get_rooms())
    # period_room_allocation(periods, rooms)

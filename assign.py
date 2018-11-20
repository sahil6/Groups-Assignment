#!/bin/env python3

"""
    Before coming up with the below mentioned solution
    we thought of other algorithms apart from search
    which can solve this problem. We considered the
    following algorithms but couldn't get the optimal result
    in short time. We are also sharing those attempts in different files
    We thought this could be a type of assignment and transportation problem
    Hence thought of Hungarian Algorithm but could not establish this as Hungarian Problem.
    Also analysed against the stable marriage problem, it looked variation of that too.
    Also Googled about high dimensional assignment and transportation algorithm but then discarded
    thinking it makes the problem more complicated.
    Monte Carlo was also considered for short while but didn't get time to spend more time using that algorithm
    At last came back to search algorithm, implemented using the priority queue taking the minutes as cost.
"""



import random
import queue
import sys

# Inputs fom the command line
input_file = sys.argv[1]
k = int(sys.argv[2])
cost_like_student_not_in_group = int(sys.argv[3])
cost_dislike_student_in_group = int(sys.argv[4])

# Declaring Constants
max_students_allowed_in_each_group = 3
like_people_preference = "like_people_preference"
dislike_people_preference = "dislike_people_preference"
group_size_preference = "group_size_preference"
username_key = "username"
show_no_preference = "_"

# reading the file
with open(input_file) as file:
    input_data = file.readlines()

# list to store user names of all the users
all_user_name_list = []

# Dictionary to story the computed group costs
computed_dict = {}


# Pre-processing the data for the further use
input_data = [x.strip() for x in input_data]
student_choices = []
user_names = []

for detail in input_data:
    split_detail = detail.split(" ")
    student_choices.append({
        username_key: split_detail[0],
        group_size_preference: split_detail[1],
        like_people_preference: split_detail[2].split(","),
        dislike_people_preference: split_detail[3].split(",")
    })
    user_names.append([split_detail[0]])


def get_liking_list(username):
    """
        @Description:
            Function to get the list of users this username likes
        @Parameters:
            username : username of the student for which we want to know the students he wants(likes) in his group.
        @Returns:
            liking_list : <list> List of usernames a student likes eg: [djcran, gbedi]
    """

    return [item[like_people_preference] for item in student_choices if item[username_key] == username][0]


def get_dislike_list(username):
    """
        @Description:
            Function to get the list of users this username dislikes or doesn't want in his/her group
        @Parameters:
            username : username of the student for which we want to know the students he doesn't wants(dislikes) in his group.
        @Returns:
            disliking_list : <list> List of username a student dislikes eg: [tvstan, gbedi]
    """

    return [item[dislike_people_preference] for item in student_choices if item[username_key] == username][0]



def get_number_of_students(username):
    """
        @Description:
           Function to get the size of group that is preferred by this user.
        @Parameters:
            username : username of the student for which we want to know the group size preference
        @Returns:
            number : Represents the number of students particular user wants in his group
    """

    return [item[group_size_preference] for item in student_choices if item[username_key] == username][0]


def get_number_of_people_cost(username, group_list):
    """
        @Description:
            Get cost for this user in the group, taking only his group size preference into consideration
        @Parameters:
            username : username of the student for which we want to know the group size cost
            group_list: <list> the list that represents one group. eg: [djcra, gbedi]
        @Returns:
            cost : returns the cost for given user in the given group based on his group size preference
    """

    number = int(get_number_of_students(username))
    if number == 0:
        return 0
    cost = 0 if number == len(group_list) or number == 0 else 1
    return cost


# Get cost for this user in group for the students he wants in his/her group preference
def get_liking_cost(username, group_list):
    """
       @Description:
           Get cost for this user in the group, taking only his group liking preference into consideration
       @Parameters:
           username : username of the student for which we want to know the liking cost
           group_list: <list> the list that represents one group. eg: [djcra, gbedi]
       @Returns:
           cost : returns the cost for given user in the given group based on his liking preferences
    """

    not_included = 0
    like_list = get_liking_list(username)

    if like_list[0] == show_no_preference:
        return 0

    for like in like_list:
        if like not in group_list:
            not_included = not_included + 1

    cost = not_included * cost_like_student_not_in_group

    return cost


def get_disliking_cost(username, group_list):

    """
      @Description:
          Get cost for this user in the group, taking only his disliking preference into consideration
      @Parameters:
          username : username of the student for which we want to know the disliking cost
          group_list: <list> the list that represents one group. eg: [djcra, gbedi]
      @Returns:
          cost : returns the cost(number of minutes) for given user in the given group based on his disliking preferences
    """

    included = 0
    dislike_list = get_dislike_list(username)

    if dislike_list[0] == show_no_preference:
        return 0

    for dislike in dislike_list:
        for student in group_list:
            if dislike == student:
                included = included + 1
    cost = included * cost_dislike_student_in_group

    return cost


def get_group_cost(group_list):

    """
      @Description:
          Get cost for the group taking all the preferences into consideration
      @Parameters:
          group_list: <list> the list that represents one group. eg: [djcra, gbedi]
      @Returns:
          cost : returns the cost(number of minutes) for the group considering all the preferences of each member
    """

    total_cost = 0

    for student in group_list:

        size_cost = get_number_of_people_cost(student, group_list)
        dislike_cost = get_disliking_cost(student, group_list)
        like_cost = get_liking_cost(student, group_list)

        cost = size_cost + dislike_cost + like_cost
        total_cost = total_cost + cost

    return total_cost + k # Here we are adding k because each groups costs k


def students_like_each_other(group):
    """
       @Description:
           To know if there is any person who likes other student
       @Parameters:
           group: <list> the list that represents one group. eg: [djcran, gbedi]
       @Returns:
           True if there is at least  one student who like another student in group
    """

    like_cost = sys.maxsize

    if len(group) > 1:
        for item in group:
            if get_liking_cost(item, group) == 0:
                like_cost = 0
        if like_cost == 0:
            return True
    else:
        return False


def students_do_not_dislike_each_other(group):

    """
       @Description:
           To know if there is any person who dislikes other student
       @Parameters:
           group: <list> the list that represents one group. eg: [djcran, gbedi]
       @Returns:
           True if there is at least  one student who dislikes another student in group
    """

    dislike_cost = sys.maxsize

    if len(group) > 1:
        for item in group:
            if get_disliking_cost(item, group) == 0:
                dislike_cost = 0
        if dislike_cost == 0:
            return True
    else:
        return False



def get_group_size_cost(group):

    """
       @Description:
           To know the group size cost for the complete group, adding for all students in the group
       @Parameters:
           group: <list> the list that represents one group. eg: [djcran, gbedi]
       @Returns:
           Cost that represents the cost of whole group taking group size preferences of all students into consideration
    """

    group_size_cost = 0
    for item in group:
            group_size_cost = group_size_cost + get_number_of_people_cost(item, group)
    return group_size_cost


def get_state_cost(group_state):

    """
       @Description:
           To know the cost of whole state taking all the costs into consideration for all the groups in the state
       @Parameters:
           group_state: [[]] List of lists having all the groups of the state.
           Eg: [['jbedi,gbedi'],['djcran,rkjain']] This is one state having two groups
       @Returns:
           Cost that represents the cost of whole state taking preferences of all students in all the groups in the state
    """
    state_cost = 0

    for item in group_state:
        cost = computed_dict[str(item)] if str(item) in computed_dict else get_group_cost(item)
        state_cost = state_cost + cost
        computed_dict[str(item)] = cost

    return state_cost


def priority_successor_for_liking(original_list):

    """
       @Description:
           Returns the desired successor for the input state'
       @Parameters:
           original_list: represents a state from which we want to find all the successors
       @Returns:
           succ_list [[]]: returns the list of lists of all the successor state for the given state.
    """

    succ_list = []
    for i in range(0, len(original_list) - 1):
        for j in range(1, len(original_list) - 1):
            if original_list[i] != original_list[j]:
                # grouping the users in one group if they satisfy the condition
                group = list(set(original_list[i]) | set(original_list[j]))
                if len(group) <= max_students_allowed_in_each_group:
                    if students_like_each_other(group) and students_do_not_dislike_each_other(group):
                        new_list = original_list.copy()
                        new_list.remove(original_list[i])
                        new_list.remove(original_list[j])
                        new_list.append(group)
                        succ_list.append(new_list)
    return succ_list


def print_output(state):
    """
       @Description:
           Function to print the state in desired format
       @Parameters:
           state: Represents the state which we want to print
       @Returns:
          None
    """
    for item in state:
        for user in item:
            sys.stdout.write(user + " ")
            sys.stdout.flush()
        print("")


def priority_successor(state):
    """
       @Description:
           Successor function
       @Parameters:
           state: Represents the state which we want to print
       @Returns:
          All successor state for the given state
    """
    from_liking = priority_successor_for_liking(state)
    return from_liking


def solve_priority(beginning):
    """
       @Description:
           Function to start our search, using the priority queue for the search
       @Parameters:
           beginning: The starting state of the program, all students in different group
       @Returns:
          state: our desirable state
          min: the cost of the state
    """
    min = sys.maxsize
    fringe = queue.PriorityQueue()
    starting_state_cost = get_state_cost(beginning)
    fringe.put((starting_state_cost, beginning))

    while not fringe.empty():
        next_state_tuple = fringe.get()
        next_state = list(next_state_tuple[1])
        for s in priority_successor(next_state):
            state_cost = get_state_cost(s)
            # pushing the state with lesser cost. trying to minimize the cost here
            if state_cost < min:
                min = state_cost
                state = s
                fringe.put((get_state_cost(s), s))
    return state,min


# Taking different input variations for the state to get the optimal result.
start_state = user_names
for i in range(0,10):
    min = sys.maxsize
    if i % 2 == 0:
        random.shuffle(start_state)
    else:
        start_state = sorted(start_state)
    state_value, min_value = solve_priority(start_state)
    if min_value < min:
        min = min_value
        state = state_value

print_output(state)
print(min)

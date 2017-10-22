from RateApp.models import Rate, Teacher, Subject

# Function to get arr from two lists
def create_two_dem_arr(list_a, list_b):
    arr = [[0 for x in range(2)] for y in range(len(list_a))]
    i = 0
    for users in arr:
        users[1] = list_a[i]
        users[0] = list_b[i]
        i = i + 1
    return arr


# Function to get all objects off class
def get_objects_as_matrix(cls, name, name2=None, additional=None):
    objects = cls.objects.all().values_list(name, flat=True)
    if name2:
        objects2 = cls.objects.all().values_list(name2, flat=True)
    if additional:
        objects_additional = cls.objects.all().values_list(additional, flat=True)
    matrix = [[0 for x in range(2)] for y in range(len(objects))]
    x = 0
    y = 0
    for x in range(len(matrix[x])):
        matrix[x][y] = cls.objects.values_list(name, flat=True)[x]
        if name2:
            matrix[x][y + 1] = objects2[x]
        if name2 and additional:
            matrix[x][y + 1] = objects2[x] + " " + objects_additional[x]
        else:
            matrix[x][y + 1] = objects[x]
        x = x + 1
    return matrix


def get_average(id, type):

    if type == 'subject':
        how_interesting = Rate.objects.filter(subject_id=id).values_list('how_interesting', flat=True)
        how_easy = Rate.objects.filter(subject_id=id).values_list('how_interesting', flat=True)
        how_interesting_av = sum(how_interesting)/len(how_interesting)
        how_easy_av = int(sum(how_easy) / len(how_easy))
        return how_interesting_av, how_easy_av
    else :
        how_interesting = Rate.objects.filter(leader_id=id).values_list('how_interesting', flat=True)
        how_easy = Rate.objects.filter(leader_id=id).values_list('how_interesting', flat=True)
        how_interesting_av = sum(how_interesting)/len(how_interesting)
        how_easy_av = int(sum(how_easy) / len(how_easy))
        return how_interesting_av, how_easy_av


"""Functions to parse a file containing student data."""


def all_houses(filename):
    """Return a set of all house names in the given file.

    For example:
      >>> unique_houses('cohort_data.txt')
      {"Dumbledore's Army", 'Gryffindor', ..., 'Slytherin'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    # We use a single underscore (_) as variable names below.
    # This is a way to say, "Hey don't worry about this variable
    # because we'll never use it --- we only care about `house`.
    #
    # Python doesn't handle underscores in a special way or anything ---
    # it's still just a variable name.

    return {house for _, house, *_ in all_data(filename) if house}


def students_by_cohort(filename, cohort="All"):
    """Return a list of students' full names by cohort.

    Names are sorted in alphabetical order. If a cohort isn't
    given, return a list of all students. For example:
      >>> students_by_cohort('cohort_data.txt')
      ['Adrian Pucey', 'Alicia Spinnet', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Fall 2015')
      ['Angelina Johnson', 'Cho Chang', ..., 'Terence Higgs', 'Theodore Nott']

      >>> students_by_cohort('cohort_data.txt', cohort='Winter 2016')
      ['Adrian Pucey', 'Andrew Kirke', ..., 'Roger Davies', 'Susan Bones']

      >>> students_by_cohort('cohort_data.txt', cohort='Spring 2016')
      ['Cormac McLaggen', 'Demelza Robins', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Summer 2016')
      ['Alicia Spinnet', 'Dean Thomas', ..., 'Terry Boot', 'Vincent Crabbe']

    Arguments:
      - filename (str): the path to a data file
      - cohort (str): optional, the name of a cohort

    Return:
      - list[list]: a list of lists
    """

    # We have a pretty difficult to understand, compound conditional
    # expression inside of the for-loop below. It's good to avoid
    # writing compound conditional expressions that aren't immediately
    # understandable.
    #
    # We should attempt to tell a better "story" with our code. What
    # we *want* to express is that, if `cohort` == `"All"`, then return
    # all the students. Otherwise, filter the students by cohort.
    #
    # The problem is that instructors and ghosts are all mixed in with
    # students. Let's tackle this problem *before* we filter (or not filter)
    # the students by cohort.

    # Create a list of students' full names and cohort names
    student_data = [
        (fullname, cohort_name)
        for fullname, _, _, cohort_name in all_data(filename)
        if cohort_name not in ("I", "G")  # Filter out instructors, ghosts
    ]

    if cohort == "All":
        return sorted([fullname for fullname, _ in student_data])
    else:
        return sorted(
            [
                fullname
                for fullname, cohort_name in student_data
                if cohort_name == cohort
            ]
        )


def all_names_by_house(filename):
    """Return a list that contains rosters for all houses, ghosts, instructors.

    Rosters appear in this order:
    - Dumbledore's Army
    - Gryffindor
    - Hufflepuff
    - Ravenclaw
    - Slytherin
    - Ghosts
    - Instructors

    Each roster is a list of names sorted in alphabetical order.

    For example:
      >>> rosters = hogwarts_by_house('cohort_data.txt')
      >>> len(rosters)
      7

      >>> rosters[0]
      ['Alicia Spinnet', ..., 'Theodore Nott']
      >>> rosters[-1]
      ['Filius Flitwick', ..., 'Severus Snape']

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[list]: a list of lists
    """

    dumbledores_army = []
    gryffindor = []
    hufflepuff = []
    ravenclaw = []
    slytherin = []
    ghosts = []
    instructors = []

    for fullname, house, _, cohort_name in all_data(filename):
        # Sometimes it makes code easier for someone else to read
        # and understand if we take care of the weird edge case
        # of ghosts and instructors first before taking care
        # of the normal case.
        if not house:
            if cohort_name == "G":
                ghosts.append(fullname)
            elif cohort_name == "I":
                instructors.append(fullname)

        if house == "Dumbledore's Army":
            dumbledores_army.append(fullname)
        elif house == "Gryffindor":
            gryffindor.append(fullname)
        elif house == "Hufflepuff":
            hufflepuff.append(fullname)
        elif house == "Ravenclaw":
            ravenclaw.append(fullname)
        elif house == "Slytherin":
            slytherin.append(fullname)

    return [
        sorted(dumbledores_army),
        sorted(gryffindor),
        sorted(hufflepuff),
        sorted(ravenclaw),
        sorted(slytherin),
        sorted(ghosts),
        sorted(instructors),
    ]


def all_data(filename):
    """Return all the data in a file.

    Each line in the file is a tuple of (full_name, house, adviser, cohort)

    Iterate over the data to create a big list of tuples that individually
    hold all the data for each person. (full_name, house, adviser, cohort)

    For example:
      >>> all_student_data('cohort_data.txt')
      [('Harry Potter', 'Gryffindor', 'McGonagall', 'Fall 2015'), ..., ]

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[tuple]: a list of tuples
    """
    with open(filename) as cohort_data:

        # `line.rstrip().split("|")` returns a list. A more semantic data
        # structure to use to represent rows of data is a tuple. So, let's
        # actually have this function return a list of tuples instead of
        # a list of lists.

        data = [tuple(line.rstrip().split("|")) for line in cohort_data]

    # Here, `rest` means "the rest of the data"
    return [(f"{first} {last}", *rest) for first, last, *rest in data]


def get_cohort_for(filename, name):
    """Given someone's name, return the cohort they belong to.

    Return None if the person doesn't exist. For example:
      >>> get_cohort_for('cohort_data.txt', 'Harry Potter')
      'Fall 2015'

      >>> get_cohort_for('cohort_data.txt', 'Hannah Abbott')
      'Winter 2016'

      >>> get_cohort_for('cohort_data.txt', 'Balloonicorn')
      None

    Arguments:
      - filename (str): the path to a data file
      - name (str): a person's full name

    Return:
      - str: the person's cohort or None
    """

    for full_name, _, _, cohort_name in all_data(filename):
        if full_name == name:
            return cohort_name


def find_duped_last_names(filename):
    """Return a set of duplicated last names that exist in the data.

    For example:
      >>> find_name_duplicates('cohort_data.txt')
      {'Creevey', 'Weasley', 'Patil'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    dupes = set()

    seen_names = set()
    for first, last, *_ in read_cohort_data(filename):
        if last in seen_names:
            dupes.add(last)

        seen_names.add(last)

    return dupes


# Helper function that returns a student's house


def get_house_for(filename, name):
    """Return house of student with `name`."""

    for fullname, house, *_ in all_data(filename):
        if fullname == name:
            return house


def get_housemates_for(filename, name):
    """Return a set of housemates for the given student.

    Given a student's name, return a list of their housemates. Housemates are
    students who belong to the same house and were in the same cohort as the
    given student.

    For example:
    >>> get_housemates_for('cohort_data.txt', 'Hermione Granger')
    {'Angelina Johnson', ..., 'Seamus Finnigan'}
    """

    target_cohort = get_cohort_for(filename, name)
    target_house = get_house_for(filename, name)

    return {
        full_name
        for full_name, house, _, cohort_name in all_data(filename)
        if full_name != name
        and house == target_house
        and cohort_name == target_cohort
    }


##############################################################################
# END OF MAIN EXERCISE.  Yay!  You did it! You Rock!
#

if __name__ == "__main__":
    import doctest

    result = doctest.testfile(
        "doctests.py",
        report=False,
        optionflags=(doctest.REPORT_ONLY_FIRST_FAILURE),
    )
    doctest.master.summarize(1)
    if result.failed == 0:
        print("ALL TESTS PASSED")


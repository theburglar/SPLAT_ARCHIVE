"""Solutions to the Inheritance tutorial questions."""


__copyright__ = "Copyright 2018, University of Queensland"



class Student(object) :
    """Simple model of a university student"""
    def __init__(self, name, student_num):
        """
        Parameters:
            name (str): The student's name in "first_name last_name" format.
            student_num (str): The student's unique student id number.
        """
        self._name = name
        self._student_num = student_num
        self._enrolments = []  # list of tuples (course code, tuition fee)

    def get_name(self) :
        """(str) Returns the name of the student "first_name last_name"."""
        return self._name

    def get_student_num(self) :
        """(str) Returns the students student number."""
        return self._student_num

    def enrol(self, course_code, fee) :
        """Enrol in a course, at a given fee.

        Parameters:
            course_code (str): Unique course code in which Student is enrolling.
            fee (int): The fee for taking this course (in whole dollar amount).

        Preconditions:
            fee > 0
        """
        self._enrolments.append((course_code, fee))

    def get_enrolments(self) :
        """list<(str, in)> Return a list of courses the student is enrolled in."""
        return self._enrolments

    def calculate_fees(self) :
        """Compute the total tuition fees for the student.
        
        Return:
            int: Total tuition fees for this Student.
        """
        total = 0
        for course_code, fee in self._enrolments :
            total += fee
        return total


class CollegeStudent(Student) :
    """Simple model for a student living in college."""
    def __init__(self, name, student_num, college_name, college_fee) :
        """
        Parameters:
            name (str): The student's name in "first_name last_name" format.
            student_num (str): The student's unique student id number.
            college_name (str): Name of the college providing accommodation.
            college_fee (int): Fee for living in the college in whole dollars.
        """
        # First initialize this instance of CollegeStudent as a Student with
        # the appropriate name and student number (student_num).
        super().__init__(name, student_num)

        # Keep a reference to the college name and college fee for this
        # CollegeStudent
        self._college_name = college_name
        self._college_fee = college_fee

    def get_college(self) :
        """(str) Returns the name of the college that this CollegeStudent
        belongs to.
        """
        return self._college_name

    def calculate_fees(self) :
        """(int) Returns the total fees for this CollegeStudent in dollars."""

        # ---------------------------------------------------------------------
        # For this method, we need to calculate the sum of the CollegeStudent's
        # tuition fees (i.e. for courses) and their college fee (i.e. for
        # staying in their college).
        # 
        # We can calculate the tuition fees by utilizing the calculate_fees
        # method of the Student class which CollegeStudent extends, and the
        # college fee is stored in ._college_fee
        # ---------------------------------------------------------------------

        # Calculate the student fees by calling the calculate_fees method of
        # Student on this instance of CollegeStudent (i.e. self)
        tuition_fees = Student.calculate_fees(self)

        # Return the sum of the tuition fees and the college fee
        return tuition_fees + self._college_fee


def task1() :
    """
    Convenience method to group all code relating to task 1.
    """
    fred = CollegeStudent("Fred", 43214321, "St. Leo's", 18000)
    print("Fred's college is", fred.get_college())
    print("Fees before enrolling:", fred.calculate_fees())
    fred.enrol('CSSE1001', 1000)
    fred.enrol('LAWS1000', 1300)
    print("Fees after enrolling:", fred.calculate_fees())


###############################################################################


from html.parser import HTMLParser
import urllib
import urllib.request
import pprint

class LinkParser1(HTMLParser) :
    """Class for obtaining links from HTML code."""

    def __init__(self) :
        """Creates a LinkParser object to parse hyperlinks from HTML text."""
        # First initialise this instance of LinkParser as a HTMLParser, since it
        # directly inherits from HTMLParser.
        super().__init__()

    def handle_starttag(self, tag, attrs) :
        """Handles the start tag of every HTML element parsed by this object.

        This initial version of this method will output each tag and its
        corresponding attributes to the console.

        Parameters:
            tag (str): Name of the tag being processed (lower case).
            attrs (list[tuple(str, str)]): The tag's attributes.
                Attributes are stored as ('name', 'value').
        """
        print(tag, attrs)
        # ---------------------------------------------------------------------
        # From the output of the above code, it can be seen that this method is
        # called for the start tag of each HTML element found by the parser,
        # with the name of the tag (tag), and a list of tuples of the
        # attributes of the tag, with each tuple having two elements, the first
        # being the name of the attribute, and the second being the
        # corresponding value.
        # i.e. [(attr1_name, attr1_value), (attr2_name, attr2_value), ...]
        # ---------------------------------------------------------------------

    def get_urls(self) :
        pass


class LinkParser2(HTMLParser) :
    """Class for obtaining links from HTML code."""

    def __init__(self) :
        """Creates a LinkParser object to parse hyperlinks from HTML text."""
        # First initialise this instance of LinkParser as a HTMLParser, since
        # it directly inherits from HTMLParser.
        super().__init__()

        # Keep a list of all the urls found in the files parsed by this
        # instance of LinkParser.
        self._urls = []

    def handle_starttag(self, tag, attrs) :
        """Handles the start tag of every HTML element parsed by this object.

        This version of this method will only output the anchor's ('a') link
        attribute to the console.

        Parameters:
            tag (str): Name of the tag being processed (lower case).
            attrs (list[tuple(str, str)]): The tag's attributes.
                Attributes are stored as ('name', 'value').
        """
        # Considering the output from step 1 (i.e. LinkParser1), we will need
        # to iterate over each attribute and only print out the values for the
        # attributes with the name 'href', and only for 'a' tags.
        if tag == 'a' :
            for name, value in attrs :
                if name == 'href' :
                    print(value)

        # ---------------------------------------------------------------------
        # An alternative way would be to return early for all non-'a' tags,
        # transforming the above code to:
        # ---------------------------------------------------------------------
        #
        # if tag != 'a' :
        #     return
        #
        # for name, value in attrs :
        #     if name == 'href' :
        #         print(value)
        #
        # ---------------------------------------------------------------------


        # ---------------------------------------------------------------------
        # Now it is fair to assume that there will be no duplicate attributes,
        # i.e. a certain attribute should only occur for a given tag once. In
        # the case of duplicates, the above code will output all values for
        # the href attribute. If we say that we assume that there will only be
        # a single occurrence of the href attribute for a given tag, and that
        # in the case of duplicates we will only consider the last one, we can
        # simplify this code by converting the list of attributes into a
        # dictionary first. i.e.
        # ---------------------------------------------------------------------
        #
        # if tag != 'a' :
        #     return
        #
        # attrs = dict(attrs)
        # # Use get in case there is no href attribute
        # print attrs.get('href')
        #
        # ---------------------------------------------------------------------


    def get_urls(self) :
        pass


class LinkParser(HTMLParser) :
    """Class for obtaining links from HTML code."""

    def __init__(self) :
        """Creates a LinkParser object to parse hyperlinks from HTML text."""
        # First initialise this instance of LinkParser as a HTMLParser, since it
        # directly inherits from HTMLParser.
        super().__init__()

        # Keep a list of all the URLs found in the files parsed by this
        # instance of LinkParser.
        self._urls = []

    def handle_starttag(self, tag, attrs) :
        """Handles the start tag of every HTML element parsed by this object.

        This version of this method stores all of the links found in anchor tags.

        Parameters:
            tag (str): Name of the tag being processed (lower case).
            attrs (list[tuple(str, str)]): The tag's attributes.
                Attributes are stored as ('name', 'value').
        """
        # Using the code from step 2 (i.e. LinkParser2), we need to add the URL
        # of each link we encounter to the list of URLs, rather than printing
        # it out.
        if tag != 'a':
            return

        attrs = dict(attrs)
        # Use get in case there is no href attribute
        href = attrs.get('href')
        # Ensure that we only add a url if the href attribute exists
        if href != None :
            self._urls.append(href)

    def get_urls(self) :
        """(list<str>) Returns a list of URLs found by this LinkParser."""
        return self._urls


def find_links(url) :
    """Return a list of links from the given Web page.

    Return:
        (list[str]): List of all links found at the given URL.
    """
    # Open the webpage and read the HTML text
    fd = urllib.request.urlopen(url)
    text = fd.read()
    fd.close()

    # Create a parser instance and feed it the text
    parser = LinkParser()
    parser.feed(str(text)) # Need to use str as feed returns a bytes type;
                           # str() will convert to string of html as required.

    return parser.get_urls()


def task2() :
    """Convenience method to group all code relating to task 2."""
    url = 'http://www.itee.uq.edu.au/'
    # Use the pretty print module to make the output a bit more readable.
    # See https://docs.python.org/3.6/library/pprint.html
    pprint.pprint(find_links(url))


###############################################################################


# This code will only be executed if the code is run (F5 or from terminal)
# and not imported.
if __name__ == '__main__' :
    task1()
    print('\n' + '-'*70 + '\n')
    task2()

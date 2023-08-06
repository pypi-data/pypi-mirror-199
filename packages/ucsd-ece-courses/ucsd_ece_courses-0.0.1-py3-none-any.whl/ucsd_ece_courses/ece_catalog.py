from difflib import get_close_matches
import re
from bs4 import BeautifulSoup
import requests

class ECECatalog:
    '''
    Class for scraping, organizing, and filtering UCSD ECE Department's course catalog webpage.

    Attributes
    ----------

    Private:

        __course_catalog : dict, dictionary of course catalog indexed by course number

    Public:

        course_url : str, the URL to UCSD ECE Department's course catalog webpage
        course_numbers : list, a list of all UCSD ECE course numbers
        course_titles : list, a list of all UCSD ECE course titles

    Methods
    -------

    Private:

        __get_catalog : method that populates the __course_catalog dictionary
        __course_aliases : method that finds a valid closely matched course number given an alias

    Public:

        course_title : method that returns the title of a course provided its alias
        course_credit : method that returns the credits offered for the course provided its alias
        course_summary : method that returns the summary of a course provided its alias
        course_prerequisite : method that returns the prerequisite(s) of a course provided its alias
    '''

    def __init__(self) -> None:
        '''
        Creates a new instance of ECECatalog
        '''

        self.course_url = 'https://catalog.ucsd.edu/courses/ECE.html'
        self.__course_catalog = {}

        self.__get_catalog()

        self.course_numbers = list(self.__course_catalog.keys())
        self.course_titles = list(course['title'] for course in self.__course_catalog.values())
    
    def __get_catalog(self) -> None:
        '''
        Method that populates the __course_catalog dictionary

        :return: None
        '''

        course_html = requests.get(self.course_url).text
        soup = BeautifulSoup(course_html, 'html.parser')
        clean = re.compile('<.*?>')

        raw_course_titles = soup.find_all(class_='course-name')
        raw_course_descriptions = soup.find_all(class_='course-descriptions')

        # Filter for number, title, credits, summary, and prerequisites
        for course, description in zip(raw_course_titles, raw_course_descriptions):
            course = re.sub(clean, '', str(course))
            description = re.sub(clean, '', str(description))

            # Number
            number = course[:course.find('.')]
            number = re.findall('\d+', number)[0]

            # Title
            title = course[course.find('. '):course.find('(')]
            title = title[2:].strip()

            # Credits
            credit = course[course.find('('):]
            credit = re.sub(r'()', '', credit)

            # Summary and prerequisites
            prerequisite = description.find('Prerequisites:')
            if prerequisite != -1:
                summary = description[:prerequisite].strip()
                prerequisite = description[prerequisite:].replace('Prerequisites: ', '')
                prerequisite = prerequisite.capitalize()

            else:
                summary = description
                prerequisite = None

            temp = {number: {
                'title': title,
                'credit': credit,
                'summary': summary,
                'prerequisite': prerequisite,
            }}

            self.__course_catalog.update(temp)
            
    def __course_aliases(self, course: str) -> str:
        '''
        Method that finds a valid closely matched course number given an alias

        :param course: course alias
        :return: closest matched course number from alias
        '''     

        course = re.findall('\d+', course)[0]

        try:
            alias = get_close_matches(course, self.__course_catalog.keys())[0]
            alias = alias if alias in course else False
            assert alias
        except (IndexError, AssertionError):
            raise AssertionError('Course does not exist')

        return alias

    def course_title(self, course: str) -> str:
        '''
        Method that returns the title of a course provided its alias

        :param course: course alias
        :return: title of course
        '''

        assert isinstance(course, str), 'Argument must be string type'

        course = self.__course_aliases(course)

        return self.__course_catalog[course]['title']

    def course_credit(self, course: str) -> str:
        '''
        Method that returns the credits offered for the course provided its alias

        :param course: course alias
        :return: credits offered for the course
        '''

        assert isinstance(course, str), 'Argument must be string type'

        course = self.__course_aliases(course)
        
        return self.__course_catalog[course]['credit']
    
    def course_summary(self, course: str) -> str:
        '''
        Method that returns the summary of a course provided its alias

        :param course: course alias
        :return: summary of the course
        '''
            
        assert isinstance(course, str), 'Argument must be string type'

        course = self.__course_aliases(course)
        
        return self.__course_catalog[course]['summary']
    
    def course_prerequisite(self, course: str) -> str:
        '''
        Method that returns the prerequisite(s) of a course provided its alias

        :param course: course alias
        :return: prerequisite of the course
        '''

        assert isinstance(course, str), 'Argument must be string type'

        course = self.__course_aliases(course)
        
        return self.__course_catalog[course]['prerequisite']
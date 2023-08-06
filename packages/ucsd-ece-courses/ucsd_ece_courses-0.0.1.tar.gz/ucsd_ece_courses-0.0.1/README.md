# ucsd-ece-courses

A neat package to scrape, organize, and filter for UCSD ECE Department's course catalog. Under construction!

Developed by Kendrick Nguyen, who is currently experimenting with packaging.

## Installation

```python
pip3 install ucsd_ece_courses
```

## Examples of How To Use

Get course descriptions

```python
from ucsd_ece_courses import ECECatalog

catalog = ECECatalog()

# Get ECE 5 courage descriptions, try also 'ece 5', 'ece_5', '5', etc.
course = 'ece_5'
print(catalog.course_title(course))
print(catalog.course_credit(course))
print(catalog.course_summary(course))
print(catalog.course_prerequisite(course))
```

Get all course numbers and titles

```python
from ucsd_ece_courses import ECECatalog

catalog = ECECatalog()

# Get all course numbers and titles
print(catalog.course_numbers)
print(catalog.course_titles)
```
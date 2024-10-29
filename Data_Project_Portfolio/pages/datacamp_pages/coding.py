from pages.datacamp_pages.functions import *

hotels = search_hotels("NYC", radius=10, ratings="4")
print(hotels)  # This will print the list of hotel names
This program scrapes images using beatifulsoup.
Finds a "Next Page" button at the bottom of a page and continues scraping until it reaches a user defined limit.
Saves images as 0.jpg,1.jpg,2.jpg etc
Checkpoints are saved as "checkpoint.txt" which contains an initialization URL, the next URL up to scrape, the total number of photos downloaded throughout all runs, and the number of photos to download next time the script is run.

Downloads images into a subfolder

# Using an old Nook for bus times and weather

A little project to put back into use an unused Barnes and Noble Nook that had been sitting in a drawer for years.

Goal was to show when the next few buses will be arriving at the bus stop at the top of our road. 

Then also included some info on weather - ideally wanted to show the likelyhood of rain that day (this part still needs some work).

Project involved:
- working out how to break into the nook
- rooting the nook so that I could display my own content
- working out how to display a web page as a proxy for content display
- working out how to install as a display (battery life not quite good enough for the number of updates I was wanting- once per minute)

This project by Edent was really helpful in working out how to get everything working:
https://shkspr.mobi/blog/2020/02/turn-an-old-ereader-into-an-information-screen-nook-str/ 

End result was:

- Python script runs from crontab once per minute to generate a webpage - bus.py
- This page is being served by a RPi on the same network as the nook
- The nook then calls this html page and uses "electic sign" to save as screensaver
- Screensaver is set to update once a minute
- I request weather data once an hour to reduce api calls to openweather.org
- I bought a cheap picture frame, removed glass, created cardboard surround, cut notch for cable and taped it all together

## bus.py
The script running on the RPi

## bus_test.html
The starting part of me calling the tfl api to generate bus data for my location

## test.html
Working out some display parameters for the nook
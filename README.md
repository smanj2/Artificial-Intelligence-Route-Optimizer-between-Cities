# B551 Assignment 1: Searching
##### Submission by Sri Harsha Manjunath - srmanj@iu.edu; Vijayalaxmi Bhimrao Maigur - vbmaigur@iu.edu; Disha Talreja - dtalreja@iu.edu
###### Fall 2019

## Part 2: Road trip!
Besides baseball, McDonald's, and reality TV, few things are as canonically American as hopping in the car for an old-fashioned road trip. We've prepared a dataset of major highway segments of the United States
(and parts of southern Canada and northern Mexico), including highway names, distances, and speed limits;
you can visualize this as a graph with nodes as towns and highway segments as edges. We've also prepared
a dataset of cities and towns with corresponding latitude-longitude positions.
between pairs of cities given by the user. Your program should be run on the command line like this:
```
./route.py [start-city] [end-city] [cost-function]
```
where:
* start-city and end-city are the cities we need a route between.
* cost-function is one of:
  * **segments** tries to find a route with the fewest number of "turns" (i.e. edges of the graph)
  * **distance** tries to find a route with the shortest total distance
  * **time** tries to find the fastest route, for a car that always travels at the speed limit
  * **mpg** tries to find the most economical route, for a car that always travels at the speed limit and
whose mileage per gallon (MPG) is a function of its velocity (in miles per hour), as follows:
MPG(v) = 400 v/150 (1 - v/150)4

The output of your program should be a nicely-formatted, human-readable list of directions, including travel times, distances, intermediate cities, and highway names, similar to what Google Maps or another site might produce. In addition, the last line of output should have the following machine-readable output about the route your code found:
```
[total-segments] [total-miles] [total-hours] [total-gas-gallons] [start-city] [city-1] [city-2] ... [end-city]
```

Please be careful to follow these interface requirements so that we can test your code properly. For instance, the last line of output might be:
```
3 51 1.0795 1.9552 Bloomington,_Indiana Martinsville,_Indiana Jct_I-465_&_IN_37_S,_Indiana Indianapolis,_Indiana
```
Like any real-world dataset, our road network has mistakes and inconsistencies; in the example above, for example, the third city visited is a highway intersection instead of the name of a town. Some of these "towns" will not have latitude-longitude coordinates in the cities dataset; you should design your code to still work well in the face of these problems.

## Solution 
#### Search Abstraction
##### 1. Set of States S
The set of states S, can be defined as all cities in the road-segments.txt that has interconnected neighbors, such that one can visit a city using one of its neighbors

##### 2. Successor Function
The successor function used in this problem returns every adjacent neighbor for a given city along with the following metrics for each neighbor
* distance
* speed limit
* Highway name
* Time to reach
* mpg achieved by travelling

##### 3. Initial State
The start city specified by the user

##### 4. Goal State:
To find the optimal route between a start and destination city, based on the optimization metric specifed by the user. If no solution is found, then to return `Inf`

##### 4. Cost:
The cost will depend on the metric chosen for optimization
* Segments - Number of edges in the path
* Distance - Total miles in the path
* Time - Total time taken to travel
* MPG - Total Miles per Gallon associated with the path

#### Approach
The implementation follows a greedy approach for most of the metrics, where it chooses the least expensive neighbor at every step. Although greedy algorithms are not always optimal, or even complete, the nature of this problem allows us to find solutions pretty quickly most of the times, since the algorithm mimics choices made in the real world.

Most often than not, we choose the least expensive path when driving between 2 cities

The implementation also uses a visited structure to record the cities that have been encountered in the path to avoid going in loops

For optimizing on segments, the implementation follows a breadth first search method.

#### Alternative approaches considered
Since we had the GPS coordinates available from the `city-gps.txt` we initially tried the A* algorithm with a straight line heuristic.
* Where the straight line distance between 2 cities was derived using the haversine function.
* This distance in turn formed the heuristic for the A* algorithm
* For cases where a city did not have a GPS coordinate, we used the next neighboring city that had a GPS co-ordinate. Since straight line distance just need to give a rough intuition (heuristic) as to in which direction a city lied, we felt this was appropriate

This implementation was abandoned since the other method provided satisfactory, if not better, results

##### Assumptions
* **Important callout**  - 'mpg' implementation as instructed by the pdf, says to `"Find the most economical route, for a car that always travels at the speed limit and
whose mileage per gallon (MPG) is a function of its velocity."`
  * We assume "most economical" means the cheapest (in terms of fuel), and hence the least amount of gallons consumed. Entity optimized here being gallons
  * We have not considered the maximum `mpg` for each city
* The difference between the two being, "More bang for your buck" v/s "Number of bucks" and we choose to have fewer "number of bucks" go towards fuel rather than "most bang for your buck."

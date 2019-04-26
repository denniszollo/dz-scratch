import math
def meters_per_deg(lat):
  m1 = 111132.92;     # latitude calculation term 1
  m2 = -559.82;       # latitude calculation term 2
  m3 = 1.175;         # latitude calculation term 3
  m4 = -0.0023;       # latitude calculation term 4
  p1 = 111412.84;     # longitude calculation term 1
  p2 = -93.5;         # longitude calculation term 2
  p3 = 0.118;         # longitude calculation term 3

  # Calculate the length of a degree of latitude and longitude in meters
  latlen = m1 + (m2 * math.cos(2 * lat)) + (m3 * math.cos(4 * lat)) + \
          (m4 * math.cos(6 * lat));
  longlen = (p1 * math.cos(lat)) + (p2 * math.cos(3 * lat)) + \
              (p3 * math.cos(5 * lat));
  return (latlen, longlen)


# The londiff is the difference between the leftmost longitude line and 
# the rightmost longitude line in the scale from the screenshot
londiff = 122.2380325 - 122.2380305
# same for the latdiff
latdiff = 37.798565 - 37.798585

(latperdeg, lonperdeg) = meters_per_deg(37.798565)

print "lon_diff is {0}".format(lonperdeg * londiff)
print "lat_diff is {0}".format(latperdeg * latdiff)


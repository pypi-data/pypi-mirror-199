import math


def calculate_distance(latlon1, latlon2):
    lat_dist = math.radians(latlon1[0] - latlon2[0])
    lon_dist = math.radians(latlon1[1] - latlon2[1])
    lat1_rad = math.radians(latlon1[0])
    lat2_rad = math.radians(latlon2[0])
    angle_sin2 = math.sin(lat_dist/2)**2 + math.sin(lon_dist/2)**2*math.cos(lat1_rad)*math.cos(lat2_rad)
    dist_rad = 2 * math.asin(math.sqrt(angle_sin2))
    return dist_rad * 6371


def get_distances(lats1, lns1, lats2, lns2):
     dists = []
     for lat1, lon1, lat2, lon2 in zip(lats1, lns1, lats2, lns2):
         dist = calculate_distance((lat1, lon1), (lat2, lon2))
         dists.append(dist)
     return dists
    

def caculate_closest_point(point, points):
    dists = [calculate_distance(point, p) for p in points] 
    return points[dists.index(min(dists))]

# table = pd.read_excel(r"/Users/xuzhoufeng/SynologyDrive/项目/迁地与就地保护评价/biotracks2.xlsx")

# xzqh = pd.read_excel(r"/Users/xuzhoufeng/OneDrive/PDP/ipybd/ipybd/lib/xzqh.xlsx")
points = [(lat, lon) for lat, lon in zip(xzqh['Lat'], xzqh['Lng'])]

distances = []
for lat, lng in zip(table['decimalLatitude'], table['decimalLongitude']):
    if lat is None:
        distances.append(None)
        continue
    near_point = caculate_closest_point((lat, lng), points)
    dist = calculate_distance((lat, lng), near_point)
    distances.append(dist)

table['dist'] = pd.Series(distances)
table.to_excel(r"~/Downloads/dists.xlsx")
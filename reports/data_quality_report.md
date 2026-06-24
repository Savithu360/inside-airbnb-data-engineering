# Day 1 Data Quality Report

Generated at: 2026-06-24 20:46:54

Selected city: Stockholm, Sweden

## Raw Files Used

- listings: `C:/Users/Savithu/Documents/inside-airbnb-data-engineering/data/raw/listings.csv.gz` (found)
- calendar: `C:/Users/Savithu/Documents/inside-airbnb-data-engineering/data/raw/calendar.csv.gz` (found)
- reviews: `C:/Users/Savithu/Documents/inside-airbnb-data-engineering/data/raw/reviews.csv.gz` (found)
- neighbourhoods: `C:/Users/Savithu/Documents/inside-airbnb-data-engineering/data/raw/neighbourhoods.csv` (found)

## Dataset Summary

| Dataset | Raw rows | Raw columns | Clean rows | Clean columns | Raw duplicates | Clean duplicates |
|---|---:|---:|---:|---:|---:|---:|
| listings | 4955 | 79 | 4955 | 32 | 0 | 0 |
| calendar | 1808575 | 7 | 1808575 | 8 | 0 | 0 |
| reviews | 161036 | 6 | 161036 | 6 | 0 | 0 |
| neighbourhoods | 14 | 2 | 14 | 2 | 0 | 0 |

## Schema Summary: listings

| Column | Data type |
|---|---|
| id | int64 |
| listing_url | str |
| scrape_id | int64 |
| last_scraped | str |
| source | str |
| name | str |
| description | str |
| neighborhood_overview | str |
| picture_url | str |
| host_id | int64 |
| host_url | str |
| host_name | str |
| host_since | str |
| host_location | str |
| host_about | str |
| host_response_time | str |
| host_response_rate | str |
| host_acceptance_rate | str |
| host_is_superhost | str |
| host_thumbnail_url | str |
| host_picture_url | str |
| host_neighbourhood | str |
| host_listings_count | float64 |
| host_total_listings_count | float64 |
| host_verifications | str |
| host_has_profile_pic | str |
| host_identity_verified | str |
| neighbourhood | str |
| neighbourhood_cleansed | str |
| neighbourhood_group_cleansed | float64 |
| latitude | float64 |
| longitude | float64 |
| property_type | str |
| room_type | str |
| accommodates | int64 |
| bathrooms | float64 |
| bathrooms_text | str |
| bedrooms | float64 |
| beds | float64 |
| amenities | str |
| price | str |
| minimum_nights | int64 |
| maximum_nights | int64 |
| minimum_minimum_nights | float64 |
| maximum_minimum_nights | float64 |
| minimum_maximum_nights | float64 |
| maximum_maximum_nights | float64 |
| minimum_nights_avg_ntm | float64 |
| maximum_nights_avg_ntm | float64 |
| calendar_updated | float64 |
| has_availability | str |
| availability_30 | int64 |
| availability_60 | int64 |
| availability_90 | int64 |
| availability_365 | int64 |
| calendar_last_scraped | str |
| number_of_reviews | int64 |
| number_of_reviews_ltm | int64 |
| number_of_reviews_l30d | int64 |
| availability_eoy | int64 |
| number_of_reviews_ly | int64 |
| estimated_occupancy_l365d | int64 |
| estimated_revenue_l365d | float64 |
| first_review | str |
| last_review | str |
| review_scores_rating | float64 |
| review_scores_accuracy | float64 |
| review_scores_cleanliness | float64 |
| review_scores_checkin | float64 |
| review_scores_communication | float64 |
| review_scores_location | float64 |
| review_scores_value | float64 |
| license | float64 |
| instant_bookable | str |
| calculated_host_listings_count | int64 |
| calculated_host_listings_count_entire_homes | int64 |
| calculated_host_listings_count_private_rooms | int64 |
| calculated_host_listings_count_shared_rooms | int64 |
| reviews_per_month | float64 |

## Missing Value Summary: listings

| Column | Null count | Null percentage |
|---|---:|---:|
| neighbourhood_group_cleansed | 4955 | 100.0% |
| calendar_updated | 4955 | 100.0% |
| license | 4955 | 100.0% |
| host_neighbourhood | 3585 | 72.35% |
| neighborhood_overview | 3175 | 64.08% |
| neighbourhood | 3175 | 64.08% |
| host_about | 2713 | 54.75% |
| beds | 1767 | 35.66% |
| bathrooms | 1766 | 35.64% |
| price | 1765 | 35.62% |
| estimated_revenue_l365d | 1765 | 35.62% |
| host_response_time | 1576 | 31.81% |
| host_response_rate | 1576 | 31.81% |
| host_acceptance_rate | 1154 | 23.29% |
| host_location | 940 | 18.97% |
| review_scores_checkin | 870 | 17.56% |
| review_scores_communication | 870 | 17.56% |
| review_scores_location | 870 | 17.56% |
| review_scores_value | 870 | 17.56% |
| first_review | 869 | 17.54% |
| last_review | 869 | 17.54% |
| review_scores_rating | 869 | 17.54% |
| review_scores_accuracy | 869 | 17.54% |
| review_scores_cleanliness | 869 | 17.54% |
| reviews_per_month | 869 | 17.54% |
| bedrooms | 258 | 5.21% |
| description | 192 | 3.87% |
| has_availability | 184 | 3.71% |
| host_is_superhost | 28 | 0.57% |
| bathrooms_text | 8 | 0.16% |
| host_name | 4 | 0.08% |
| host_since | 4 | 0.08% |
| host_thumbnail_url | 4 | 0.08% |
| host_picture_url | 4 | 0.08% |
| host_listings_count | 4 | 0.08% |
| host_total_listings_count | 4 | 0.08% |
| host_verifications | 4 | 0.08% |
| host_has_profile_pic | 4 | 0.08% |
| host_identity_verified | 4 | 0.08% |
| minimum_minimum_nights | 3 | 0.06% |
| maximum_minimum_nights | 3 | 0.06% |
| minimum_maximum_nights | 3 | 0.06% |
| maximum_maximum_nights | 3 | 0.06% |
| id | 0 | 0.0% |
| listing_url | 0 | 0.0% |
| scrape_id | 0 | 0.0% |
| last_scraped | 0 | 0.0% |
| source | 0 | 0.0% |
| name | 0 | 0.0% |
| picture_url | 0 | 0.0% |
| host_id | 0 | 0.0% |
| host_url | 0 | 0.0% |
| neighbourhood_cleansed | 0 | 0.0% |
| latitude | 0 | 0.0% |
| longitude | 0 | 0.0% |
| property_type | 0 | 0.0% |
| room_type | 0 | 0.0% |
| accommodates | 0 | 0.0% |
| amenities | 0 | 0.0% |
| minimum_nights | 0 | 0.0% |
| maximum_nights | 0 | 0.0% |
| minimum_nights_avg_ntm | 0 | 0.0% |
| maximum_nights_avg_ntm | 0 | 0.0% |
| availability_30 | 0 | 0.0% |
| availability_60 | 0 | 0.0% |
| availability_90 | 0 | 0.0% |
| availability_365 | 0 | 0.0% |
| calendar_last_scraped | 0 | 0.0% |
| number_of_reviews | 0 | 0.0% |
| number_of_reviews_ltm | 0 | 0.0% |
| number_of_reviews_l30d | 0 | 0.0% |
| availability_eoy | 0 | 0.0% |
| number_of_reviews_ly | 0 | 0.0% |
| estimated_occupancy_l365d | 0 | 0.0% |
| instant_bookable | 0 | 0.0% |
| calculated_host_listings_count | 0 | 0.0% |
| calculated_host_listings_count_entire_homes | 0 | 0.0% |
| calculated_host_listings_count_private_rooms | 0 | 0.0% |
| calculated_host_listings_count_shared_rooms | 0 | 0.0% |

## Sample Values: listings

| Column | Sample values |
|---|---|
| id | 164448, 220851, 238411 |
| listing_url | https://www.airbnb.com/rooms/164448, https://www.airbnb.com/rooms/220851, https://www.airbnb.com/rooms/238411 |
| scrape_id | 20250929042406, 20250929042406, 20250929042406 |
| last_scraped | 2025-09-29, 2025-09-29, 2025-09-29 |
| source | city scrape, city scrape, city scrape |
| name | Double room in central Stockholm with Wi-Fi, One room in appartement, Cozy apartment in central Stockholm |
| description | I am renting out a nice double room on the top floor in a large duplex apartment in the center of Stockholm at Södermalm. Close to metro and bus and walking distance to most of the sights., Welcome!, I am renting out a nice single room on the top floor in a large duplex apartment in the center of Stockholm at Södermalm. (See my other ad if you would like to have a double room).<br /><br />Close to public transportation, old town, restaurants and bars. |
| neighborhood_overview | Many restaurangs wery close and walkingdistance To city., Restaurants, cafés, museums, art galleries, parks, shops etc. All things that make for a vibrant neighborhood are here!, Södermalm, often shortened to "Söder", is a district in central Stockholm. It covers the large island of the same name (formerly called "Åsön"). With a population of 99,685 (December 2008) it is one of the most densely populated districts of Scandinavia. Although Södermalm usually is considered an island, water to both its north and south does not flow freely but passes through locks.<br /><br />My apartment is next to Slussen subway and from here you can easy access hole Stockholm with public transport. <br /><br />Gamla Stan (old town) is just 3-5 min walk from my door, its a must for first visit to Stockholm. In Gamla Stan you find the Royal Palace, just around 5-6 min walk from my door. <br /><br />The area around Slussen (Götgatan, Götstreet) have many cool bars, café and good shopping. <br /><br />Just 2-3 min from my apartment you find a nice park (Mariatorget) that is fantastic a nice summer day. Several other parks is reach easy with walking. |
| picture_url | https://a0.muscache.com/pictures/f56d8d10-a7fa-44d9-b521-b7a577abf327.jpg, https://a0.muscache.com/pictures/2085606/7a706118_original.jpg, https://a0.muscache.com/pictures/2806060/7fc681f0_original.jpg |
| host_id | 784312, 412283, 1250232 |
| host_url | https://www.airbnb.com/users/show/784312, https://www.airbnb.com/users/show/412283, https://www.airbnb.com/users/show/1250232 |
| host_name | Li, Fredric, Mia |
| host_since | 2011-07-06, 2011-02-27, 2011-10-05 |
| host_location | Stockholm, Sweden, Stockholm, Sweden, Stockholm, Sweden |
| host_about | I am a recently retired lady, who has two rooms spare for rent and enjoys having tourists over., I am into arts yoga meditation design life relaxation love music , I am from Stockholm. I'm passionate about traveling and meeting people from other cultures. My favorite country is Italy! I know my city very well and am always happy to share my knowledge - just ask! |
| host_response_time | within an hour, a few days or more, within a few hours |
| host_response_rate | 100%, 0%, 100% |
| host_acceptance_rate | 100%, 23%, 0% |
| host_is_superhost | t, f, f |
| host_thumbnail_url | https://a0.muscache.com/im/users/784312/profile_pic/1314897997/original.jpg?aki_policy=profile_small, https://a0.muscache.com/im/pictures/user/e0c057ab-8506-4226-8ed6-109de8c6fc4e.jpg?aki_policy=profile_small, https://a0.muscache.com/im/users/1250232/profile_pic/1321297318/original.jpg?aki_policy=profile_small |
| host_picture_url | https://a0.muscache.com/im/users/784312/profile_pic/1314897997/original.jpg?aki_policy=profile_x_medium, https://a0.muscache.com/im/pictures/user/e0c057ab-8506-4226-8ed6-109de8c6fc4e.jpg?aki_policy=profile_x_medium, https://a0.muscache.com/im/users/1250232/profile_pic/1321297318/original.jpg?aki_policy=profile_x_medium |
| host_neighbourhood | Södermalm, Kungsholmen, Norrmalm |
| host_listings_count | 2.0, 2.0, 1.0 |
| host_total_listings_count | 2.0, 4.0, 1.0 |
| host_verifications | ['email', 'phone'], ['email', 'phone'], ['email', 'phone'] |
| host_has_profile_pic | t, t, t |
| host_identity_verified | t, t, t |
| neighbourhood | Stockholm, Stockholm County, Sweden, Stockholm, Stockholm County, Sweden, Stockholm, Stockholm County, Sweden |
| neighbourhood_cleansed | Södermalms, Kungsholmens, Norrmalms |
| neighbourhood_group_cleansed |  |

## Numeric Summary: listings

### id
- count: 4955.0
- mean: 6.984012811875928e+17
- std: 5.666998193367076e+17
- min: 164448.0
- 25%: 37308075.0
- 50%: 8.745691968785348e+17
- 75%: 1.181722686879964e+18
- max: 1.5197165869784622e+18

### scrape_id
- count: 4955.0
- mean: 20250929042406.0
- std: 0.0
- min: 20250929042406.0
- 25%: 20250929042406.0
- 50%: 20250929042406.0
- 75%: 20250929042406.0
- max: 20250929042406.0

### host_id
- count: 4955.0
- mean: 197842933.08
- std: 207142048.52
- min: 4457.0
- 25%: 24493620.5
- 50%: 100332605.0
- 75%: 359514031.0
- max: 720534628.0

### host_listings_count
- count: 4951.0
- mean: 7.07
- std: 30.42
- min: 1.0
- 25%: 1.0
- 50%: 1.0
- 75%: 2.0
- max: 1456.0

### host_total_listings_count
- count: 4951.0
- mean: 12.56
- std: 133.11
- min: 1.0
- 25%: 1.0
- 50%: 2.0
- 75%: 4.0
- max: 8775.0

### neighbourhood_group_cleansed
- count: 0.0
- mean: nan
- std: nan
- min: nan
- 25%: nan
- 50%: nan
- 75%: nan
- max: nan

### latitude
- count: 4955.0
- mean: 59.32
- std: 0.03
- min: 59.23
- 25%: 59.3
- 50%: 59.32
- 75%: 59.34
- max: 59.42

### longitude
- count: 4955.0
- mean: 18.03
- std: 0.07
- min: 17.77
- 25%: 18.0
- 50%: 18.05
- 75%: 18.08
- max: 18.19

### accommodates
- count: 4955.0
- mean: 3.5
- std: 2.02
- min: 1.0
- 25%: 2.0
- 50%: 3.0
- 75%: 4.0
- max: 16.0

### bathrooms
- count: 3189.0
- mean: 1.29
- std: 1.09
- min: 0.0
- 25%: 1.0
- 50%: 1.0
- 75%: 1.5
- max: 50.0

### bedrooms
- count: 4697.0
- mean: 1.72
- std: 1.39
- min: 0.0
- 25%: 1.0
- 50%: 1.0
- 75%: 2.0
- max: 50.0

### beds
- count: 3188.0
- mean: 2.16
- std: 1.83
- min: 0.0
- 25%: 1.0
- 50%: 2.0
- 75%: 3.0
- max: 50.0

### minimum_nights
- count: 4955.0
- mean: 7.13
- std: 24.81
- min: 1.0
- 25%: 1.0
- 50%: 3.0
- 75%: 5.0
- max: 500.0

### maximum_nights
- count: 4955.0
- mean: 305.05
- std: 363.93
- min: 1.0
- 25%: 25.0
- 50%: 180.0
- 75%: 365.0
- max: 1125.0

### minimum_minimum_nights
- count: 4952.0
- mean: 6.62
- std: 23.92
- min: 1.0
- 25%: 1.0
- 50%: 2.0
- 75%: 4.0
- max: 500.0

### maximum_minimum_nights
- count: 4952.0
- mean: 7.91
- std: 32.07
- min: 1.0
- 25%: 2.0
- 50%: 3.0
- 75%: 5.0
- max: 999.0

### minimum_maximum_nights
- count: 4952.0
- mean: 394.9
- std: 430.12
- min: 1.0
- 25%: 28.0
- 50%: 365.0
- 75%: 385.0
- max: 1125.0

### maximum_maximum_nights
- count: 4952.0
- mean: 402.94
- std: 431.37
- min: 1.0
- 25%: 30.0
- 50%: 365.0
- 75%: 730.0
- max: 1125.0

### minimum_nights_avg_ntm
- count: 4955.0
- mean: 7.22
- std: 24.54
- min: 1.0
- 25%: 2.0
- 50%: 3.0
- 75%: 5.0
- max: 500.0

### maximum_nights_avg_ntm
- count: 4955.0
- mean: 398.47
- std: 429.37
- min: 1.0
- 25%: 30.0
- 50%: 365.0
- 75%: 651.5
- max: 1125.0

### calendar_updated
- count: 0.0
- mean: nan
- std: nan
- min: nan
- 25%: nan
- 50%: nan
- 75%: nan
- max: nan

### availability_30
- count: 4955.0
- mean: 8.47
- std: 10.84
- min: 0.0
- 25%: 0.0
- 50%: 1.0
- 75%: 16.0
- max: 30.0

### availability_60
- count: 4955.0
- mean: 20.31
- std: 23.12
- min: 0.0
- 25%: 0.0
- 50%: 8.0
- 75%: 43.0
- max: 60.0

### availability_90
- count: 4955.0
- mean: 32.96
- std: 35.47
- min: 0.0
- 25%: 0.0
- 50%: 15.0
- 75%: 69.0
- max: 90.0

### availability_365
- count: 4955.0
- mean: 139.37
- std: 140.44
- min: 0.0
- 25%: 0.0
- 50%: 86.0
- 75%: 276.0
- max: 365.0

### number_of_reviews
- count: 4955.0
- mean: 32.5
- std: 72.97
- min: 0.0
- 25%: 1.5
- 50%: 8.0
- 75%: 27.5
- max: 1239.0

### number_of_reviews_ltm
- count: 4955.0
- mean: 8.87
- std: 19.53
- min: 0.0
- 25%: 0.0
- 50%: 2.0
- 75%: 8.0
- max: 436.0

### number_of_reviews_l30d
- count: 4955.0
- mean: 0.81
- std: 1.91
- min: 0.0
- 25%: 0.0
- 50%: 0.0
- 75%: 1.0
- max: 31.0

### availability_eoy
- count: 4955.0
- mean: 34.5
- std: 36.85
- min: 0.0
- 25%: 0.0
- 50%: 17.0
- 75%: 71.0
- max: 94.0

### number_of_reviews_ly
- count: 4955.0
- mean: 7.43
- std: 21.63
- min: 0.0
- 25%: 0.0
- 50%: 1.0
- 75%: 5.0
- max: 714.0

### estimated_occupancy_l365d
- count: 4955.0
- mean: 50.58
- std: 78.68
- min: 0.0
- 25%: 0.0
- 50%: 12.0
- 75%: 60.0
- max: 255.0

### estimated_revenue_l365d
- count: 3190.0
- mean: 103075.29
- std: 455930.79
- min: 0.0
- 25%: 0.0
- 50%: 35595.0
- 75%: 126000.0
- max: 23565780.0

### review_scores_rating
- count: 4086.0
- mean: 4.81
- std: 0.34
- min: 1.0
- 25%: 4.75
- 50%: 4.91
- 75%: 5.0
- max: 5.0

### review_scores_accuracy
- count: 4086.0
- mean: 4.81
- std: 0.33
- min: 1.0
- 25%: 4.75
- 50%: 4.9
- 75%: 5.0
- max: 5.0

### review_scores_cleanliness
- count: 4086.0
- mean: 4.74
- std: 0.39
- min: 1.0
- 25%: 4.67
- 50%: 4.86
- 75%: 5.0
- max: 5.0

### review_scores_checkin
- count: 4085.0
- mean: 4.86
- std: 0.3
- min: 1.0
- 25%: 4.84
- 50%: 4.95
- 75%: 5.0
- max: 5.0

### review_scores_communication
- count: 4085.0
- mean: 4.87
- std: 0.31
- min: 1.0
- 25%: 4.86
- 50%: 4.98
- 75%: 5.0
- max: 5.0

### review_scores_location
- count: 4085.0
- mean: 4.81
- std: 0.31
- min: 1.0
- 25%: 4.75
- 50%: 4.9
- 75%: 5.0
- max: 5.0

### review_scores_value
- count: 4085.0
- mean: 4.72
- std: 0.37
- min: 1.0
- 25%: 4.64
- 50%: 4.8
- 75%: 4.95
- max: 5.0

### license
- count: 0.0
- mean: nan
- std: nan
- min: nan
- 25%: nan
- 50%: nan
- 75%: nan
- max: nan

### calculated_host_listings_count
- count: 4955.0
- mean: 4.62
- std: 9.95
- min: 1.0
- 25%: 1.0
- 50%: 1.0
- 75%: 2.0
- max: 51.0

### calculated_host_listings_count_entire_homes
- count: 4955.0
- mean: 4.04
- std: 9.93
- min: 0.0
- 25%: 1.0
- 50%: 1.0
- 75%: 1.0
- max: 51.0

### calculated_host_listings_count_private_rooms
- count: 4955.0
- mean: 0.53
- std: 1.95
- min: 0.0
- 25%: 0.0
- 50%: 0.0
- 75%: 0.0
- max: 21.0

### calculated_host_listings_count_shared_rooms
- count: 4955.0
- mean: 0.04
- std: 0.43
- min: 0.0
- 25%: 0.0
- 50%: 0.0
- 75%: 0.0
- max: 6.0

### reviews_per_month
- count: 4086.0
- mean: 1.28
- std: 2.16
- min: 0.01
- 25%: 0.18
- 50%: 0.5
- 75%: 1.54
- max: 52.34


## Schema Summary: calendar

| Column | Data type |
|---|---|
| listing_id | int64 |
| date | str |
| available | str |
| price | float64 |
| adjusted_price | float64 |
| minimum_nights | int64 |
| maximum_nights | int64 |

## Missing Value Summary: calendar

| Column | Null count | Null percentage |
|---|---:|---:|
| price | 1808575 | 100.0% |
| adjusted_price | 1808575 | 100.0% |
| listing_id | 0 | 0.0% |
| date | 0 | 0.0% |
| available | 0 | 0.0% |
| minimum_nights | 0 | 0.0% |
| maximum_nights | 0 | 0.0% |

## Sample Values: calendar

| Column | Sample values |
|---|---|
| listing_id | 164448, 164448, 164448 |
| date | 2025-09-29, 2025-09-30, 2025-10-01 |
| available | t, t, t |
| price |  |
| adjusted_price |  |
| minimum_nights | 2, 2, 2 |
| maximum_nights | 120, 120, 120 |

## Numeric Summary: calendar

### listing_id
- count: 1808575.0
- mean: 6.984012811875931e+17
- std: 5.6664278846200186e+17
- min: 164448.0
- 25%: 37301374.0
- 50%: 8.745691968785348e+17
- 75%: 1.1817848205683418e+18
- max: 1.5197165869784622e+18

### price
- count: 0.0
- mean: nan
- std: nan
- min: nan
- 25%: nan
- 50%: nan
- 75%: nan
- max: nan

### adjusted_price
- count: 0.0
- mean: nan
- std: nan
- min: nan
- 25%: nan
- 50%: nan
- 75%: nan
- max: nan

### minimum_nights
- count: 1808575.0
- mean: 7.22
- std: 25.19
- min: 1.0
- 25%: 2.0
- 50%: 3.0
- 75%: 5.0
- max: 999.0

### maximum_nights
- count: 1808575.0
- mean: 398.47
- std: 430.59
- min: 1.0
- 25%: 30.0
- 50%: 365.0
- 75%: 700.0
- max: 1125.0


## Schema Summary: reviews

| Column | Data type |
|---|---|
| listing_id | int64 |
| id | int64 |
| date | str |
| reviewer_id | int64 |
| reviewer_name | str |
| comments | str |

## Missing Value Summary: reviews

| Column | Null count | Null percentage |
|---|---:|---:|
| comments | 16 | 0.01% |
| listing_id | 0 | 0.0% |
| id | 0 | 0.0% |
| date | 0 | 0.0% |
| reviewer_id | 0 | 0.0% |
| reviewer_name | 0 | 0.0% |

## Sample Values: reviews

| Column | Sample values |
|---|---|
| listing_id | 164448, 164448, 164448 |
| id | 407660, 451097, 472271 |
| date | 2011-07-30, 2011-08-16, 2011-08-24 |
| reviewer_id | 870312, 901633, 894674 |
| reviewer_name | Fred, Julien, Liliana |
| comments | great fun at lidia's. she had the power adapter i needed. (try getting that at a hotel). and advice on stockholm. bright top floor and a quirky cork light switch worth the visit alone., Great centrally located room, very nice facilities. Everything was clean and tidy. I can only recommend this., Lidia is a very nice person. Very good plase to stay for visit Stockolm.  |

## Numeric Summary: reviews

### listing_id
- count: 161036.0
- mean: 3.5072735100952774e+17
- std: 4.8855143598737197e+17
- min: 164448.0
- 25%: 20586254.5
- 50%: 40867254.0
- 75%: 8.221292860531889e+17
- max: 1.5154439258602015e+18

### id
- count: 161036.0
- mean: 8.417460407352202e+17
- std: 5.3517287991977395e+17
- min: 407660.0
- 25%: 4.4761719565398854e+17
- 50%: 9.738125651358162e+17
- 75%: 1.2846953951421652e+18
- max: 1.5203040671279493e+18

### reviewer_id
- count: 161036.0
- mean: 196015899.52
- std: 188702942.33
- min: 81.0
- 25%: 37200480.25
- 50%: 126485896.0
- 75%: 331294138.5
- max: 720536090.0


## Schema Summary: neighbourhoods

| Column | Data type |
|---|---|
| neighbourhood_group | float64 |
| neighbourhood | str |

## Missing Value Summary: neighbourhoods

| Column | Null count | Null percentage |
|---|---:|---:|
| neighbourhood_group | 14 | 100.0% |
| neighbourhood | 0 | 0.0% |

## Sample Values: neighbourhoods

| Column | Sample values |
|---|---|
| neighbourhood_group |  |
| neighbourhood | Älvsjö, Bromma, Enskede-Årsta-Vantörs |

## Numeric Summary: neighbourhoods

### neighbourhood_group
- count: 0.0
- mean: nan
- std: nan
- min: nan
- 25%: nan
- 50%: nan
- 75%: nan
- max: nan


## Duplicate Summary

| Dataset | Duplicate rows in raw data | Duplicate rows after cleaning |
|---|---:|---:|
| listings | 0 | 0 |
| calendar | 0 | 0 |
| reviews | 0 | 0 |
| neighbourhoods | 0 | 0 |

## Validation Checks

- listings: 4955 rows available after cleaning.
- calendar: 1808575 rows available after cleaning.
- reviews: 161036 rows available after cleaning.
- neighbourhoods: 14 rows available after cleaning.
- listings: invalid latitude values flagged: 0.
- listings: invalid longitude values flagged: 0.
- listings: invalid listing prices flagged: 0.
- calendar: invalid calendar prices flagged: 0.
- calendar: raw `price` and `adjusted_price` are 100.0% missing, so calendar pricing analysis is not available from this Stockholm source file.
- reviews: rows with unparseable or missing review dates: 0.
- date fields are converted with invalid parses set to null for later review.

## Cleaning Actions Performed

### listings
- Converted price to numeric.
- Removed percent signs and converted host_response_rate to numeric.
- Removed percent signs and converted host_acceptance_rate to numeric.
- Converted host_is_superhost from t/f to boolean.
- Converted instant_bookable from t/f to boolean.
- Converted host_since to datetime.
- Converted first_review to datetime.
- Converted last_review to datetime.
- Flagged listing prices less than or equal to zero.

### calendar
- Converted date to datetime.
- Converted available from t/f to boolean.
- Converted price to numeric.
- Converted adjusted_price to numeric.
- Flagged calendar prices less than or equal to zero.

### reviews
- Renamed id to review_id.
- Converted date to datetime.

### neighbourhoods
- Cleaned neighbourhood column names.

## Assumptions

- Raw files are the Stockholm Inside Airbnb CSV files placed in `data/raw`.
- Currency fields are assumed to represent listing prices in the source dataset's currency format.
- Percentage fields are stored as numeric values from 0 to 100 after removing `%`.
- Rows are retained during Day 1 cleaning; invalid values are flagged instead of dropped.

## Limitations

- Day 1 focuses on familiarization, profiling, cleaning, and storage only.
- The Stockholm calendar dataset contains 100% missing values for price and adjusted_price in the raw source file. Therefore, calendar-based pricing analysis such as monthly price trends and weekday vs weekend price comparison cannot be performed using calendar data. Calendar data will be used for availability analysis only, while pricing analysis will use the listings dataset price field.
- Text fields such as review comments and amenities are not deeply parsed yet.
- No feature engineering, modeling, orchestration, or dashboarding is included yet.

## Next Steps for Day 2

- Explore relationships between listings, calendar availability, reviews, and neighbourhoods.
- Use `listings_clean.price` for pricing analysis.
- Use `calendar_clean` only for availability analysis.
- Do not plan calendar-based price analysis unless a future dataset version includes calendar prices.
- Add focused visualizations for listing price, availability, room type, and review patterns.
- Decide on analysis-ready features for later ML without training a model yet.
- Add lightweight tests for key cleaning functions.

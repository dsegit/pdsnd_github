import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# define possible analyses options
cities = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days   = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    finding_city = True
    while finding_city: 
        
        # get user input
        try:
            city = input("""
            \n\nWhich city do you want to analyze? Your possible choices:\n
             - 'chicago'\n
             - 'new york city'\n
             - 'washington'
             """).lower()
        except Exception as e:
            print("The following error occurred: {}".format(e))    
        
        # check whether one of the predefined cities was found, if so exit loop
        if city in cities:
            print("Thanks, we'll run the analyses for city: '{}'.\n".format(city))
            finding_city = False
        else:
            print("Your entered city '{}' appears not to exist. Try another city.\n".format(city))
        

    # get user input for month (all, january, february, ... , june)
    finding_month = True
    while finding_month:

        # get user input
        try:
            month = input("""
            \n\nWhich month do you want to analyze? Your possible choices:\n
             - all\n
             - january\n
             - february\n
             - march\n
             - april\n
             - may\n
             - june
             """).lower()
        except Exception as e:
            print("The following error occurred: {}".format(e))    
        
        # check whether one of the predefined months was found, if so exit loop
        if month in months:
            print("Thanks, we'll run the analyses for month: '{}'.\n".format(month))
            finding_month = False
        else:
            print("Your entered month '{}' appears not to exist. Try another month.\n".format(month))
    
    
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    finding_day = True
    while finding_day:

        # get user input
        try:
            day = input("""
            \n\nWhich day do you want to analyze? Your possible choices:\n
             - all\n 
             - monday\n 
             - tuesday\n 
             - wednesday\n 
             - thursday\n 
             - friday\n 
             - saturday\n 
             - sunday
             """).lower()
        except Exception as e:
            print("The following error occurred: {}".format(e))    

        # check whether one of the predefined days was found, if so exit loop
        if day in days:
            print("Thanks, we'll run the analyses for day: '{}'.\n".format(day))
            finding_day = False
        else:
            print("Your entered day '{}' appears not to exist. Try another day.\n".format(month))
    
        
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    filepath = CITY_DATA[city]
    df = pd.read_csv(filepath)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], format="%Y-%m-%d %H:%M:%S")

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name() # source: https://stackoverflow.com/questions/8380389/how-to-get-day-name-from-datetime (last accessed, July 28, 2022, 15:33)
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("\nMost popular month: ", popular_month, "\n")

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("\nMost popular day: ", popular_day, "\n")

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost popular hour: ", popular_hour, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts()
    print("\nMost popular start station: ", popular_start_station, " (count: ", popular_start_station_count[popular_start_station],")\n")

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts()
    print("\nMost popular end station: ", popular_end_station, " (count: ", popular_end_station_count[popular_end_station], ")\n")

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " - " + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    popular_trip_count = df['Trip'].value_counts()
    print("\nMost popular trip: ", popular_trip, " (count: ", popular_trip_count[popular_trip], ")\n")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal Travel Time: ", round(total_travel_time, 2), " sec.\n") # source: https://realpython.com/python-rounding/, last accessed: July 28, 2022, 16:04

    # display mean travel time
    total_travel_time = df['Trip Duration'].mean()
    print("\nMean Travel Time:  ", round(total_travel_time, 2), " sec.\n") # source: https://realpython.com/python-rounding/, last accessed: July 28, 2022, 16:04

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.head(): # source: https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/, last accessed: July 28, 2022, 16:14
        counts_user_types = df['User Type'].value_counts()
        print("\nCounts of User Types:\n", counts_user_types.to_string(), "\n") # source: https://dtuto.com/questions/7164/index.html, last accessed: July 28, 2022, 15:52

    # Display counts of gender
    if 'Gender' in df.head(): # source: https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/, last accessed: July 28, 2022, 16:14
        counts_gender = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", counts_gender.to_string(), "\n") # source: https://dtuto.com/questions/7164/index.html, last accessed: July 28, 2022, 15:52

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.head(): # source: https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/, last accessed: July 28, 2022, 16:14
        yob_earlierst = int(df['Birth Year'].min())
        yob_mostrecent = int(df['Birth Year'].max())
        yob_mostcommon = int(df['Birth Year'].mode()[0])
        print("\nYear of Birth (Earliest): ",    yob_earlierst, 
              "\nYear of Birth (Most Recent): ", yob_mostrecent, 
            "\nYear of Birth (Most Common): ", yob_mostcommon,"\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# define function to show raw data
def get_rawdata(df):
    showing_rawdata = True
    while showing_rawdata:
        # get user input
        try:
            usr_show_rawdata = input("""
            \n\nWould you like to see the raw data (first five rows)? Enter 'yes' or 'no'.\n
            """).lower()
        except Exception as e:
            print("The following error occurred: {}".format(e))    
        
        # check whether one of the predefined answer was found, if so exit loop
        if usr_show_rawdata == 'yes':
            
            # inquire for more data
            getting_more_rawdata = True
            idx = 0 
            while getting_more_rawdata: 

                # provide data
                print(df.iloc[idx:(idx+5)])
                idx += 5

                # get user input
                try:
                    usr_more_rawdata = input("""
                    \n\nWould you like to see 5 additional rows of data? Enter 'yes' or 'no'.\n
                    """).lower()
                except Exception as e:
                    print("The following error occurred: {}".format(e))    

                if usr_more_rawdata == 'yes':
                    print("Sure, we'll be glad to provide an additional 5 rows of data.\n")
                elif usr_more_rawdata == 'no':
                    showing_rawdata = False
                    getting_more_rawdata = False
                else:
                    print("Your entered answer '{}' appears not to exist. Try another answer.\n".format(usr_more_rawdata))
        elif usr_show_rawdata == 'no':
            showing_rawdata = False
        else:
            print("Your entered answer '{}' appears not to exist. Try another answer.\n".format(showing_rawdata))
    



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_rawdata(df)

        restart = input("""\nWould you like to restart? Enter 'yes' or 'no'.\n""")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def validate_input(user_input, valid):
    """
    function to validate user input 
        arguments:
        (str) user_input - user inpit to be validated 
        (list) valid - viald values of user input

        return:
        (str) user input - either city , month or day
    """
    while user_input.lower() not in valid:
        print("please inter a valid input")
        user_input= input()

    return user_input.lower()


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
    city = input("please select the city to filter by (chicago, new york city, washington)\n")
    city = validate_input(city,["chicago", "new york city", "washington"])

    filter_by = input("Would you like to filter the data by month, day, or not at all (Enter : none)?\n")    
    filter_by = validate_input(filter_by,["month","day","none"])

    # get user input for month (all, january, february, ... , june)
    month = "all"
    if filter_by == "month":
        month = input("please select the month to filter by (january, february, march, april, may, or june)\n")
        month = validate_input(month,["january", "february", "march", "april", "may", "june"])  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = "all"
    if filter_by == "day":
        day= input("please select the day to filter by (monday, tuesday, wednesday, thursday, friday, saturday, or sunday)\n")
        day = validate_input(day,["monday", "tuesday", "wednesday", "thursday", "friday", "saturday","sunday"])

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("the most common month is :\t", months[df['month'].mode()[0]-1])
    print("the count :               \t", max(df['month'].value_counts()),'\n')

    # display the most common day of week
    print("the most common day is :\t", df['day_of_week'].mode()[0])
    print("the count :             \t", max(df['day_of_week'].value_counts()),'\n')

    # display the most common start hour
    df['hour'] =df['Start Time'].dt.hour
    print("the most common hour is :\t", df['hour'].mode()[0])
    print("the count :             \t", max(df['hour'].value_counts()),'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("the most common start station is :\t", df['Start Station'].mode()[0])
    print("the count :                       \t", max(df['Start Station'].value_counts()),'\n')    

    # display most commonly used end station
    print("the most common end station is :\t", df['End Station'].mode()[0])
    print("the count :                     \t", max(df['End Station'].value_counts()),'\n')  

    # display most frequent combination of start station and end station trip
    common_route= df[['Start Station','End Station']].value_counts() 
    print(common_route.head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time is :    \t",total_time,"  sec \n")

    # display mean travel time
    mean_time = df['Trip Duration'].mean().round(2)
    print("the mean travel time is :\t",mean_time,"  sec \n")

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("the braekdown of Users:","\n",user_types,"\n")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types= df['Gender'].value_counts()
        print("the braekdown of Gender:","\n",gender_types,"\n")
    else:
        print("\nThere is no gender records for this city")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        old_year= int(min(df["Birth Year"]))
        print("The oldest user have Birth Year of:  \t",old_year,'\n')

        young_year= int(max(df["Birth Year"]))
        print("The youngest user have Birth Year of:\t",young_year,'\n')

        popular_year= int(df['Birth Year'].mode()[0])
        print('The most popular year of birth is :  \t',popular_year,"\n")

    else:
        print("\nThere is nno Birth Year records for this city")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_record(df):
    """Displays Users records """
    
    view_record = input("Would you like to view some users row records (Enter : y for YES and n for NO)?\n")    
    view_record = validate_input(view_record,["y","n"])

    while view_record =="y":
        print(df.sample(n=5))
        view_record = input("Would you like to view some users row records (Enter : y for YES and n for NO)?\n")    
        view_record = validate_input(view_record,["y","n"])
    
    print("Thank you for using our program, we hope you get useful inights from the Datsets")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_record(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
§
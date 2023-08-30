import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
def convert_seconds(seconds):
    # this function converts a number of seconds into days, hours, minutes and seconds

    # calculate the number of whole days in the time period
    num_days = seconds // (24 * 60 * 60)
    
    # find out how many seconds remaining to allocate among hours, minutes and seconds
    secs_to_allocate = seconds - (num_days * 24 * 60 * 60)
    
    # calculate the number of hours in the remaining time period
    num_hours = secs_to_allocate // (60 * 60)
    
    # find out how many seconds remaining to allocate among minutes and seconds
    secs_to_allocate = secs_to_allocate - (num_hours * 60 *60)
    
    # calculate the number of minutes in the remaining time period  
    num_minutes = secs_to_allocate // 60
    
    # find out how many seconds remaining
    rem_seconds = secs_to_allocate - (num_minutes *60)
    
    return num_days, num_hours, num_minutes, int(rem_seconds)


def generator_from_dataframe(df):
    for raw_data_row in df.iterrows():
        yield raw_data_row


def display_raw_data(df):
    # this function displays raw data in five-row chunks, including the column headings each time
    
    # ask the user whether raw data should be displayed
    while True:
        # validate input
        raw_choice = input('Would you like to see some raw data? Please enter yes or no (case-insensitive): ').lower()
        if raw_choice in ['yes', 'no']:
            break
        else:
            print('Invalid input. Please try again.')
            
    if raw_choice == 'yes':
        # call generator function
        generator = generator_from_dataframe(df)
        # initialise variables
        count = 0
        keep_printing = 'yes'
        while keep_printing == 'yes':
            # this loop needs to exit if the generator runs out of rows to yield
            try:
                for row in generator:
                    print(row)
                    count += 1
                    if count == 5:
                        while True:
                            # test whether the user wants to see more rows
                            keep_printing = input('Would you like to see five more rows? Please enter yes or no (case-insensitive): ').lower()
                            # validate input
                            if keep_printing in ['yes', 'no']:
                                break
                            else:
                                print('Invalid input. Please try again.')
                        count = 0
                        break
            except:
                print('No more raw data left to display!')
                break


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
    while True:
        city = input('Enter a city: Chicago, New York City or Washington (case-insensitive): ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            # handle invalid input appropriately
            print('Invalid input. Please try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter a month: all, jan, feb, mar, apr, may, jun (case-insensitive): ').lower()
        if month in ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']:
            break
        else:
            # handle invalid input appropriately
            print('Invalid input. Please try again.')
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter a day: all, mon, tue, wed, thu, fri, sat, sun (case-insensitive): ').lower()
        if day in ['all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
            full_days = {'all':'all', 'mon':'Monday', 'tue':'Tuesday', 'wed':'Wednesday', 'thu':'Thursday', 'fri':'Friday', 'sat':'Saturday', 'sun':'Sunday'}
            day = full_days[day]
            break
        else:
            # handle invalid input appropriately
            print('Invalid input. Please try again.')
    
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
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
    
        # filter dataframe by month
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        
        # filter dataframe by day        
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    
    # obtain full name of month for display
    full_months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
    most_common_month = full_months[most_common_month]
    print('The most common month is {}'.format(most_common_month))

    # display the most common day of week
    most_common_dotw = df['day_of_week'].mode()[0]
    print('The most common day of the week is {}'.format(most_common_dotw))

    # display the most common start hour
    most_common_sh = df['hour'].mode()[0]
    print('The most common start hour is {}'.format(most_common_sh))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_stst = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}'.format(most_common_stst))

    # display most commonly used end station
    most_common_endst = df['End Station'].mode()[0]
    print('The most commonly used end station is {}'.format(most_common_endst))

    # display most frequent combination of start station and end station trip
    # create new column concatenating station names into a string (including 'and')    
    df['station_combo'] = df['Start Station'] + ' and ' + df['End Station']  
    most_common_combo = df['station_combo'].mode()[0]
    print('The most frequent combination of start and end stations is {}'.format(most_common_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # obtain total travel time in seconds
    total_travel_time = df['Trip Duration'].sum()
    
    # call convert_seconds function and return days, hours, minutes and seconds for display
    num_days, num_hours, num_minutes, remaining_seconds = convert_seconds(total_travel_time)
    print('The total travel time is {} days, {} hours, {} minutes and {} seconds'.format(num_days, num_hours, num_minutes, remaining_seconds))  
    
    # display mean travel time
    # obtain mean travel time in seconds
    mean_travel_time = df['Trip Duration'].mean()

    # call convert_seconds function and return days, hours, minutes and seconds for display
    num_days, num_hours, num_minutes, remaining_seconds = convert_seconds(int(mean_travel_time))
    print('The mean travel time is {} days, {} hours, {} minutes and {} seconds'.format(num_days, num_hours, num_minutes, remaining_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Counts of user type are as follows: \n{}'.format(user_type_counts.to_string()))

    # Display counts of gender
    
    # compare city against list of cities for which gender data are available
    if city in ['chicago', 'new york city']:
        # calculate counts
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender are as follows: \n{}'.format(gender_counts.to_string()))
    else:
        print('Gender data not available')

    # Display earliest, most recent, and most common year of birth
    # compare city against list of cities for which birth year data are available 
    if city in ['chicago', 'new york city']:
        # calculate stats
        earliest_by = int(df['Birth Year'].min())
        most_recent_by = int(df['Birth Year'].max())
        most_common_by = int(df['Birth Year'].mode()[0])
        print('The earliest birth year among users is: {}'.format(earliest_by))
        print('The most recent birth year among users is: {}'.format(most_recent_by))
        print('The most common birth year among users is: {}'.format(most_common_by))

    else:
        print('Birth date data not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # use get_filters function to obtain user data on city, month and day of the week of interest
        city, month, day = get_filters()
        # load selected data into a dataframe
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

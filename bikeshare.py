#Reference links
# https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html


import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_choices = ['chicago','new york city','washington']

month_choices = ['all','january','february','march','april','may','june']

day_choices = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """


    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    city_input = ''

    while city_input.lower() not in city_choices:
        city_input = input("Which city would you like to see data for: Chicago, New York City, or Washington?\n").lower()
        if city_input in city_choices:
            city = city_input
        else:
            print("Your entry is not a valid input. Please input either chicago, new york city or washington.\n")


    month_input = ''

    while month_input.lower() not in month_choices:
        month_input = input("Which month would you like to see data for: (all, January, February,... June)?\n").lower()
        if month_input in month_choices:
            month = month_input
        else:
            print("Your entry is not a valid input. Please input either 'all' or January, February,... June.\n")


    day_input = ''

    while day_input.lower() not in day_choices:
        day_input = input("Please enter a day(all, monday, tuesday, ... sunday)\n").lower()
        if day_input in day_choices:
            day = day_input
        else:
            print("Your entry is not a valid input. Please input either 'all' or monday, tuesday, ... sunday.\n")

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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most popular days and times for trips."""

    start_time = time.time()


    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is {}".format(popular_month))


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is {}".format(popular_day))


    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most common start hour is {}".format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station {}".format(popular_start_station))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(popular_end_station))


    # display most frequent combination of start station and end station trip
    popular_start_end_station = df[['Start Station','End Station']].mode().loc[0]
    print("The most frequent combination of start station and end station trip are {} and {}".format(popular_start_end_station[0],popular_start_end_station[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print("The total travel time is {}".format(tot_travel_time))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {}".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Type Counts:\n{}".format(user_types))


    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['User Type'].value_counts()
        print("Gender Counts:\n{}".format(gender_types))
    else:
        print("Gender stats cannot be calculated because Gender does not appear in dataset")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
           earliest_birth_year = df['Birth Year'].min()
           most_recent_birth_year = df['Birth Year'].max()
           popular_birth_year = df['Birth Year'].mode()[0]
           print("The earliest birth year is: {}\nThe most recent birth year is: {}\nThe most common birth year is: {}".format(earliest_birth_year,most_recent_birth_year,popular_birth_year))
    else:
        print("Birth Year stats cannot be calculated because Birth Year does not appear in dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_raw_data(df):
    """Prompts user if they want to view raw data and displays raw data if yes."""
     
    print(df.head())

    line_counter = 0

    while True:
          display_raw = input("Would you like to view the next 5 lines of raw data (yes or no)?\n").lower()

          if display_raw == 'yes':
            line_counter = line_counter + 5
            print(df.iloc[line_counter:line_counter + 5])
          else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
          display_raw = input("Would you like to view the first 5 lines of raw data (yes or no)?\n").lower()
          if display_raw != 'yes':
            break
          display_raw_data(df)
          break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

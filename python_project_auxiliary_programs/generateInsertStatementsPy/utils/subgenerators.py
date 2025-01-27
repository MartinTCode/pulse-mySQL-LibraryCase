# utils/subgenerators.py
import random, os
from datetime import datetime, timedelta
from typing import List, Dict
#import 3rd party module to visualize tables:
from tabulate import tabulate

# source: https://en.wiktionary.org/wiki/Appendix:Swedish_given_names#The_most_common_given_names_in_Sweden_1890_-_2008
_names_male = ["Alexander", "Alf", "Allan", "Anders", "Andreas", "Anton", "Arne", "Arvid", "Axel", "Bengt", "Bertil", "Birger", "Björn", "Bo", "Bror", "Börje", "Carl", "Christer", "Christian", "Daniel", "David", "Einar", "Emanuel", "Emil", "Eric", "Erik", "Ernst", "Evert", "Folke", "Fredrik", "Georg", "Gunnar", "Gustaf", "Gustav", "Göran", "Gösta", "Hans", "Harald", "Harry", "Henrik", "Henry", "Håkan", "Ingemar", "Ingvar", "Ivar", "Jan", "Johan", "Johannes", "John", "Jonas", "Karl", "Kent", "Kjell", "Knut", "Kurt", "Lars", "Leif", "Lennart", "Magnus", "Marcus", "Martin", "Mats", "Mattias", "Michael", "Mikael", "Niklas", "Nils", "Olof", "Olov", "Oskar", "Ove", "Patrik", "Per", "Peter", "Ragnar", "Robert", "Roger", "Roland", "Rolf", "Rune", "Sebastian", "Simon", "Stefan", "Sten", "Stig", "Sven", "Thomas", "Tobias", "Tomas", "Tommy", "Torsten", "Ulf", "Valdemar", "Vilhelm", "William", "Åke"]
_names_female = ["Agneta", "Alice", "Amanda", "Anette", "Anita", "Ann", "Anna", "Annika", "Astrid", "Barbro", "Berit", "Birgit", "Birgitta", "Britt", "Camilla", "Carina", "Caroline", "Cecilia", "Charlotta", "Christina", "Edit", "Elin", "Elisabet", "Elisabeth", "Elsa", "Emma", "Ester", "Eva", "Greta", "Gun", "Gunborg", "Gunhild", "Gunilla", "Gunvor", "Hanna", "Helena", "Ida", "Inga", "Ingeborg", "Ingegerd", "Ingegärd", "Inger", "Ingrid", "Irene", "Jenny", "Johanna", "Julia", "Karin", "Karolina", "Katarina", "Kerstin", "Kristina", "Lena", "Linda", "Linnea", "Linnéa", "Lisa", "Louise", "Maj", "Malin", "Margareta", "Margit", "Maria", "Marie", "Matilda", "Monica", "Märta", "Rut", "Sara", "Signe", "Siv", "Sofia", "Sonja", "Susanne", "Svea", "Therese", "Ulla", "Ulrika", "Viktoria", "Viola", "Yvonne", "Åsa"]
_names = _names_male + _names_female
# source: https://en.wiktionary.org/wiki/Category:Swedish_surnames
_surnames = ["Abrahamsson", "Adamsberg", "Ahlman", "Alexandersson", "Alfvén", "Andersson", "André", "Andreasson", "Apell", "Arvidsson", "Ask", "Axelsson", "Backlund", "Backman", "Backström", "Bengtsson", "Berg", "Berggren", "Berglund", "Bergman", "Bergqvist", "Bergstrand", "Bergström", "Bergvall", "Bernadotte", "Berzelius", "Bildt", "Birgersson", "Björk", "Björklund", "Björkman", "Björn", "Blom", "Blomqvist", "Blomstrand", "Bolund", "Borg", "Boström", "Brovall", "Burman", "Bååth", "Bäcklund", "Bäckström", "Börjeson", "Carlsson", "Cederström", "Cronström", "Dahl", "Dahlberg", "Dahlbäck", "Dahlström", "Danielsson", "Davidsson", "Ehrling", "Ek", "Ekberg", "Ekdahl", "Ekelöf", "Ekerlid", "Ekholm", "Eklund", "Eklöf", "Ekström", "Eliasson", "Engberg", "Englund", "Engström", "Ericsson", "Eriksson", "Erlandsson", "Erlund", "Fagerlund", "Fallström", "Fjäll", "Fontelius", "Forsberg", "Forsman", "Forssell", "Fransson", "Fredriksson", "Friman", "Frisk", "Glad", "Grafström", "Granestrand", "Grönholm", "Grönroos", "Gucci", "Gunnarsson", "Gustafsson", "Gustavsson", "Göransson", "Hammare", "Hammarskjöld", "Hansson", "Haverling", "Hedborg", "Hedenskog", "Hedlund", "Hedman", "Helander", "Helenius", "Helin", "Hellström", "Henriksson", "Hermansson", "Hjelmqvist", "Holm", "Holmberg", "Holmgren", "Holmquist", "Holmström", "Hulth", "Hyltenstam", "Håkansson", "Hård", "Högberg", "Höglund", "Höxter", "Isaksson", "Ishizaki", "Ivarsson", "Jacobsson", "Jakobsson", "Jansson", "Johansson", "Johnson", "Johnsson", "Jonasson", "Jonsson", "Josefsson", "Jäderberg", "Jönsson", "Karlsson", "Kindstrand", "Kjellander", "Kjellberg", "Kjellström", "Kristersson", "Kvist", "Kvisth", "Kwist", "Lagerkvist", "Lagerlöf", "Larsdotter", "Larsson", "Leander", "Lenné", "Lind", "Lindberg", "Lindblad", "Lindblom", "Lindelöf", "Lindén", "Lindfors", "Lindgren", "Lindholm", "Lindqvist", "Lindroos", "Lindström", "Linnaeus", "Linné", "Ljungberg", "Ljungqvist", "Lundberg", "Lundgren", "Lundh", "Lundin", "Lundqvist", "Lundström", "Löfgren", "Magnusson", "Malin", "Malmquist", "Malmström", "Mankell", "Markström", "Martinsson", "Matsson", "Mattsson", "Månsson", "Mårtensson", "Nilsson", "Nobel", "Nobelius", "Norberg", "Nordin", "Nordquist", "Nordqvist", "Nordström", "Norén", "Nyberg", "Nylund", "Nyman", "Nyström", "Nåjde", "Olofsson", "Olsson", "Palm", "Palme", "Palmquist", "Palmqvist", "Parkstad", "Pehrson", "Pehrsson", "Person", "Persson", "Petersson", "Pettersson", "Pourmokhtari", "Quist", "Quisth", "Qvist", "Qvisth", "Qwist", "Rangström", "Rask", "Renström", "Ribbing", "Ringberg", "Roos", "Ros", "Rosberg", "Rosengren", "Rosenqvist", "Rothschild", "Rudbeck", "Rudolfsson", "Rydberg", "Rydbäck", "Rydkvist", "Rydqvist", "Rydstedt", "Rydström", "Rydvall", "Ryttberg", "Råberg", "Rådström", "Sahlin", "Saleh", "Samuelsson", "Sandberg", "Sandelin", "Sandell", "Sandström", "Schyman", "Sellström", "Sievert", "Sirén", "Sjöberg", "Sjöblom", "Sjögren", "Sjökvist", "Sjölund", "Sjöquist", "Sjöqvist", "Skarsgård", "Skog", "Skoglund", "Snellman", "Spahandelin", "Spjuth", "Spångberg", "Stare", "Staxäng", "Stenqvist", "Stenström", "Strand", "Strid", "Ström", "Strömberg", "Ståhl", "Ståhlbrand", "Sundberg", "Sundkvist", "Sundqvist", "Sundström", "Svanstedt", "Svanström", "Svedberg", "Svensson", "Svinhufvud", "Säfström", "Söder", "Söderberg", "Södergren", "Söderström", "Thunberg", "Thörnqvist", "Torvalds", "Tunberg", "Tungel", "Tungelfelt", "Tvilling", "Wahlroos", "Wahlström", "Wallander", "Wallin", "Westerberg", "Westerlund", "Westman", "Wickman", "Widforss", "Wiktorin", "Åberg", "Ågren", "Åhlström", "Åkerblom", "Åkerlund", "Åkerman", "Åkerström", "Åkesson", "Ångström", "Åslund", "Åström", "Ärlig", "Öberg", "Östberg", "Österberg", "Österman", "Östlund", "Östman"]

def _shuffle_list(l_ints: List[int]) -> List[int]:
    return random.sample(l_ints, len(l_ints))

def tabulate_print(l_dict2tabulate: List[Dict], table_name: str, context_str: str) -> None:
    header2print = "\n" + table_name + "  -  " + context_str
    print(header2print)
    print(tabulate(l_dict2tabulate, headers="keys"))

# TODO: this could be done a lot cleaner... old code from string handling and not dict handling.
def value_for_grupp_bokning_reference(grupp_bokning_ids, bookings_added_per_groupb, grupp_bokning_n):
    #global bookings_added_per_groupb
    #global l_values_generated_gbokning_ref
    shouldHaveGroup = random.randint(0, 1)# radomly decide if to assign NULL or to a group foreign ID.
    if shouldHaveGroup:
        if bookings_added_per_groupb[grupp_bokning_ids-1] < grupp_bokning_n:
            bookings_added_per_groupb[grupp_bokning_ids-1] += 1
            return grupp_bokning_ids, bookings_added_per_groupb
        else: 
            return "NULL", bookings_added_per_groupb  # if it is filled return NULL.
    else: 
        return "NULL", bookings_added_per_groupb  

def update_middag_dict_on_bookings(l_middag_dicts, l_bokning_dicts):
    for middag_dict in l_middag_dicts: 
        for bokning_dict in l_bokning_dicts:
            if bokning_dict['grupp_bokning_id'] == middag_dict['grupp_bokning_id']:
                checkin_f_b = bokning_dict['datum_incheck']
                checkout_f_b = bokning_dict['datum_utcheck']
                delta_timedelta = checkout_f_b - checkin_f_b # store the difference between the two
                random_delta_s = random.randint(0, int(delta_timedelta.total_seconds())) # random seconds within interval.
                random_timestamp_interval = checkin_f_b + timedelta(seconds=random_delta_s)
                middag_dict['datum'] = random_timestamp_interval
                break # no need to check more in bokning dict now that we found our match

# update bokning_dicts with factura dict AND update faktura_dicts.
    # functions like this: 
    """ Check: if a booking has a group booking then it updates factura with that group booking ID  << UPDATES FAKTURA * 
                        AND saves (list: l_factura_id_w_gb) which factura_id has a group booking assigned to it.
                else sets factura_id to an factura_id in bokning that doesn't (EXIST IN list: l_factura_id_w_gb)
                    have a group_booking assigned to it in a factura entity. """
def update_bokning_and_faktura_for_grupp_bokning(l_bokning_dicts: List[Dict], l_faktura_dicts: List[Dict]) -> None:
        # NOTE: faktura_id in bokning_dict is always "NULL" before this function call
        # NOTE: grupp_bokning_ID in faktura_dict is always "NULL" before this function call
        l_factura_id_w_gb = [] # store which factura IDs have a group booking assigned
        l_factura_id_wo_gb_taken = [] # store which factura IDs have been used for faktura without group bookings as to not duplicate
        for bokning_dict in l_bokning_dicts:
            # update factura_dict with the right group_id
            if bokning_dict['grupp_bokning_id'] != 'NULL':
                for faktura_dict in l_faktura_dicts:
                    if faktura_dict['grupp_bokning_id'] == 'NULL':
                        faktura_dict['grupp_bokning_id'] = bokning_dict['grupp_bokning_id']
                        l_factura_id_w_gb.append(faktura_dict['faktura_id']) #save this as to not assign it for booking without group.
                        break # break out of for loop since we now found what we were looking for.
        # update bokning_dict with non group booking assigned faktura_id when the booking isn't a group booking:
        # we need a new for loop for this to make sure the list is fully populated first:
        for bokning_dict in l_bokning_dicts:
            # update bokning_dict with the right faktura_id
            if bokning_dict['grupp_bokning_id'] == 'NULL':
                for faktura_dict in l_faktura_dicts:
                    if (
                        faktura_dict['faktura_id'] not in l_factura_id_w_gb
                        and 
                        faktura_dict['faktura_id'] not in l_factura_id_wo_gb_taken
                        ):
                        bokning_dict['faktura_id'] = faktura_dict['faktura_id']
                        l_factura_id_wo_gb_taken.append(bokning_dict['faktura_id'])

                        break # break out of for loop since we now found what we were looking for.

def update_faktura_for_erbjudande_id(l_faktura_dicts: List[Dict], fakt_w_erb_n: int):
    count_erbjudande = 0 # also works as index!
    max_w_erbjudande = len(l_faktura_dicts) - fakt_w_erb_n
    l_faktura_ids = [item['faktura_id'] for item in l_faktura_dicts]
    # random_order_ids = _shuffle_list(l_faktura_ids) # shuffle them around to make it random!
    while count_erbjudande < max_w_erbjudande:
        for faktura in l_faktura_dicts:
            random_f_id = l_faktura_ids[count_erbjudande]
            if (faktura['erbjudande_id'] != 'NULL' and
            count_erbjudande < max_w_erbjudande and
            faktura['faktura_id'] == random_f_id):
                faktura['erbjudande_id'] = 'NULL'
                count_erbjudande += 1

#region check dates and make sure they're right:

# Helper function to generate a random datetime within a given range
def _random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime between `start` and `end`."""
    time_delta = end - start
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

# Helper function to calculate the difference in days between two dates
def _days_between(startd, endd) -> int:
    """Calculate the number of days between two dates."""
    # Check if date1 and date2 are strings, and convert to datetime if necessary
    if isinstance(startd, str):
        startd = datetime.strptime(startd, "%Y-%m-%d")
    if isinstance(endd, str):
        endd = datetime.strptime(endd, "%Y-%m-%d")
    
    return abs((endd - startd).days)

# Validation function to ensure generated dates follow the rules
def _validate_dates(max_days_between: int,erbjudande: Dict, pris: Dict, bokning: Dict, middag: Dict) -> bool:
    """Ensure generated dates are valid according to your rules."""
    # Check the offer period
    if not (erbjudande['start_datum'] <= bokning['bokning_datum'] <= erbjudande['slut_datum']):
        return False
    if not (1 < _days_between(erbjudande['start_datum'], erbjudande['slut_datum']) <= max_days_between):
            return False
    # Check the price period
    if not (pris['start_datum'] <= bokning['bokning_datum'] < pris['slut_datum']):
        return False
    if not (1 < _days_between(pris['start_datum'], pris['slut_datum']) <= max_days_between):
            return False
    # Check booking and check-in/out dates
    if not (bokning['bokning_datum'] <= bokning['datum_incheck'] < bokning['datum_utcheck']):
        return False
    if not (1 < _days_between(bokning['bokning_datum'], bokning['datum_incheck']) <= max_days_between):
            return False
    # Check if the dinner date is within the check-in and check-out dates
    if not (bokning['datum_incheck'] <= middag['datum'] <= bokning['datum_utcheck']):
        return False
    if not (1 <= _days_between(middag['datum'], bokning['datum_utcheck']) <=max_days_between):
            return False
    
    return True

# Function to update date ranges for lists of dictionaries
def update_date_range(
    lower_limit: datetime, 
    upper_limit: datetime, 
    max_days_between: datetime,
    l_erbjudande_dict: List[Dict], 
    l_bokning_dict: List[Dict], 
    l_pris_dict: List[Dict], 
    l_middag_dict: List[Dict]
) -> None:
    """
    Updates the dates for the lists of dictionaries according to the specified rules:
    
    1. Erbjudande_t-start <= bokning_t-bookingDate <= erbjudande_t-slut
    2. Pris_t-start <= bokning_t-bookingDate < pris_t-slut
    3. Bokning_t-bokning_datum <= bokning_t-checkin_date < bokning_t-checkout_date
    4. Bokning_t-checkin_date <= middag_t-datum <= bokning_t-checkout_date
    """
    # Iterate over the lists safely, ensuring that shorter lists do not cause index errors
    for i in range(max(len(l_erbjudande_dict), len(l_bokning_dict), len(l_pris_dict), len(l_middag_dict))):
        # Safely get elements from each list, defaulting to empty dictionaries if out of range
        erbjudande = l_erbjudande_dict[i] if i < len(l_erbjudande_dict) else {}
        bokning = l_bokning_dict[i] if i < len(l_bokning_dict) else {}
        pris = l_pris_dict[i] if i < len(l_pris_dict) else {}
        middag = l_middag_dict[i] if i < len(l_middag_dict) else {}

        # Keep generating valid dates until all conditions are satisfied
        while True:
            # Generate random dates within the valid range
            erbjudande['start_datum'] = _random_date(lower_limit, upper_limit)
            erbjudande['slut_datum'] = _random_date(erbjudande['start_datum'], upper_limit)
            
            pris['start_datum'] = _random_date(erbjudande['start_datum'], erbjudande['slut_datum'])
            pris['slut_datum'] = _random_date(pris['start_datum'], erbjudande['slut_datum'])
            
            bokning['bokning_datum'], bokning['datum_incheck'], bokning['datum_utcheck'] = (
                generate_random_3interval_defined_interval(pris['start_datum'], pris['slut_datum'], max_days_between))
            #bokning['bokning_datum'] = _random_date(lower_limit, upper_limit)
            #bokning['datum_incheck'] = _random_date(lower_limit, upper_limit)
            #bokning['datum_utcheck'] = _random_date(lower_limit, upper_limit)
            
            middag['datum'] = _random_date(bokning['datum_incheck'], bokning['datum_utcheck'])
            
            # Validate the generated dates
            if _validate_dates(max_days_between, erbjudande, pris, bokning, middag):
                #bokning['datum_incheck'] = conv_timestamp2date(bokning, 'datum_incheck')
                #bokning['datum_utcheck'] = conv_timestamp2date(bokning, 'datum_utcheck')
                # above is done later on.
                break

        # Update the lists with the newly generated dates
        if i < len(l_erbjudande_dict):
            l_erbjudande_dict[i] = erbjudande
        if i < len(l_bokning_dict):
            l_bokning_dict[i] = bokning
        if i < len(l_pris_dict):
            l_pris_dict[i] = pris
        if i < len(l_middag_dict):
            l_middag_dict[i] = middag

def change_key_name_in_l(dict_l: List[Dict], old_key_n: str, new_key_n: str) -> None:
    for my_dict in dict_l:
        my_dict[new_key_n] = my_dict.pop(old_key_n)

#endregion 

def conv_timestamp2datetime_l(l_x_dict: List[Dict], key_name: str) -> None:
    for dict in l_x_dict:
        dict[key_name] = dict[key_name].replace(microsecond=0)

def conv_timestamp2date_l(l_x_dict: List[Dict], key_name: str) -> None:
    for dict in l_x_dict:
        dict[key_name] = dict[key_name].date()

def conv_timestamp2date(given_dict: Dict, key_name: str) -> Dict:
    return given_dict[key_name].date()


def name_surname_generator() -> tuple[str, str]:
    name = random.choice(_names)  # First names
    surname = random.choice(_surnames)  # Last names
    return name, surname

def generate_checked_in_or_out() -> tuple[str, str]:
    b_checked_in = random.choice(["FALSE", "TRUE"])
    if b_checked_in == "FALSE":
        b_checked_out = "TRUE"
    else:
        b_checked_out = "FALSE"
    return b_checked_in, b_checked_out

def generate_random_timestamp(start_date: datetime, end_date: datetime) -> datetime:
     # to convert to timedelta, add minimum amount to it.
    first = True # to enter while loop
    random_timestamp = start_date # just to have the value pre defined.
    # only return when it randomly has made a date withing given range!
    while ((random_timestamp < start_date or random_timestamp > end_date) or first):
        # take away while-loop entry condition:
        if first: first = False
        # get number of days in difference
        end_days_f_start = (end_date - start_date).days
        # Generate a random number of days between 0 and end_days_f_start, viz. enddate.
        random_days = random.randint(0, int(end_days_f_start))
        # Generate random time (hours, minutes, seconds, microseconds)
        # total number of seconds in a day: 24 * 60 * 60
        random_seconds_in_day = random.randint(0, 24 * 60 * 60)
        # Calculate the random timestamp by adding random_days and random time to start_date
        random_timestamp = start_date + timedelta(days=random_days, seconds=random_seconds_in_day)
    # Return the random timestamp
    return random_timestamp

def generate_triple_random_interval(start_datetime: datetime, end_datetime: datetime, max_days: int) -> tuple[datetime, datetime, datetime]:
    # Ensure the initial range is valid and adjust it if necessary
    total_days = (end_datetime - start_datetime).days

    if total_days > max_days:
        # If the range is greater than max_days, truncate the end_datetime
        end_datetime = start_datetime + timedelta(days=max_days)

    # Recalculate the total days after adjustment
    total_days = (end_datetime - start_datetime).days

    # Generate random lowest datetime
    lowest_value = start_datetime + timedelta(days=random.randint(0, total_days - max_days))

    # Generate middle value such that it is valid
    max_middle_offset = min(max_days, total_days - (lowest_value - start_datetime).days)
    if max_middle_offset <= 0:
        raise ValueError("Unable to generate a valid middle value; please check the date range.")

    middle_value = lowest_value + timedelta(days=random.randint(1, max_middle_offset))

    # Generate highest value within the max_days limit
    max_highest_offset = min(max_days, total_days - (middle_value - start_datetime).days)
    if max_highest_offset <= 0:
        raise ValueError("Unable to generate a valid highest value; please check the date range.")

    highest_value = middle_value + timedelta(days=random.randint(1, max_highest_offset))

    return lowest_value, middle_value, highest_value

def generate_random_interval_timestamp(start_datetime: datetime, end_datetime: datetime) -> tuple[datetime, datetime]:
    r_start_dt = generate_random_timestamp(start_datetime, end_datetime) # to predefine
    r_end_dt = generate_random_timestamp(r_start_dt, end_datetime) # to predefine

    return r_start_dt, r_end_dt

def generate_random_interval_defined_interval(start_datetime: datetime, end_datetime: datetime, max_days: int) -> tuple[datetime, datetime]:
    gives_diff_days = (end_datetime - start_datetime).days # to predefine
    while(gives_diff_days > max_days):
        start_datetime, end_datetime= generate_random_interval_timestamp(start_datetime, end_datetime)
        gives_diff_days = (end_datetime - start_datetime).days
    return start_datetime, end_datetime

#region for three!
def generate_random_3interval_timestamp(start_datetime: datetime, end_datetime: datetime) -> tuple[datetime, datetime, datetime]:
    r_start_dt = generate_random_timestamp(start_datetime, end_datetime) # to predefine
    r_middle_dt = generate_random_timestamp(r_start_dt, end_datetime) # to predefine
    r_end_dt = generate_random_timestamp(r_middle_dt, end_datetime) # to predefine
    return r_start_dt, r_middle_dt, r_end_dt

def generate_random_3interval_defined_interval(start_datetime: datetime, end_datetime: datetime, max_days: int) -> tuple[datetime, datetime, datetime]:
    first = True # to enter loop.
    gives_diff_days1 = (end_datetime - start_datetime).days # to predefine
    gives_diff_days2 = (end_datetime - start_datetime).days # to predefine
    while((gives_diff_days1 > max_days or gives_diff_days2 > max_days) or first):
        if first: first = False # stop using entry condition
        start_datetime, middle_datetime, end_datetime= generate_random_3interval_timestamp(start_datetime, end_datetime)
        gives_diff_days1 = (middle_datetime - start_datetime).days
        gives_diff_days2 = (end_datetime- middle_datetime).days
    return start_datetime, middle_datetime, end_datetime
#endregion

def generate_random_interval_defined_interval_date(start_datetime: datetime, end_datetime: datetime, max_days: int) -> tuple[datetime, datetime]:
    start_d, end_d = generate_random_interval_defined_interval(start_datetime, end_datetime, max_days)
    return start_d.date(), end_d.date()


def generate_random_interval_date(start_datetime: datetime, end_datetime: datetime) -> tuple[datetime, datetime]:
    r_s_dt, r_e_dt = generate_random_interval_timestamp(start_datetime, end_datetime)
    return r_s_dt.date(), r_e_dt.date()

# Generate random date between today and a future date within a certain range (e.g., 30 days from today)
def generate_random_date(start_datetime: datetime, end_datetime: datetime) -> datetime:
    random_time = generate_random_timestamp(start_datetime, end_datetime)
    # parse string to a date datetime object
    # return a random number of days, viz DATE
    return datetime.strptime(random_time, "%Y-%m-%d")

# e.g. input = 100.11, 500, 2
# e.g. output = 432.11
def generate_random_decimal_pricesum(l_limit, u_limit, n_of_dec_places: int) -> float:
    random_value = random.uniform(l_limit, u_limit)
    return round(random_value, n_of_dec_places)

# generate price intervalls for each room based on it's roop type
def price_intervalls_per_room_type(room_type_id: str) -> float:
    if room_type_id == "enkelrum":
        return round(random.uniform(400.0, 550.0), 2)
    if room_type_id == "dubbelrum":
        return round(random.uniform(600.0, 950.0), 2)
    if room_type_id == "familjerum":
        return round(random.uniform(1000.0, 1400.0), 2)

# write string to a created output directory with date and time of runtime as part of it's name.
def write_to_file(filename: str, queries: str) -> None:
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"output_{current_time}"
    
    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the folder in the parent directory
    full_folder_path = os.path.join(parent_directory, folder_name)
    os.makedirs(full_folder_path, exist_ok=True)
    
    full_path = os.path.join(folder_name, filename)
    print(str(full_path))
    
    with open(full_path, 'w', encoding='utf-8') as file:
        for query in queries:
            file.write(query + '\n')
    
    print(f"Data written to {full_path}")
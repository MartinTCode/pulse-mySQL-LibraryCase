#region import statements
import random
import math
import time # to keep track of runtime since many heavy while loops...
from datetime import datetime
# import our own modules from utils child directory.
from utils import dict_to_sql_insert_str # converts dictionary to sql formatted string
from utils import name_surname_generator, generate_checked_in_or_out, generate_random_timestamp, generate_random_decimal_pricesum, tabulate_print
from utils import write_to_file, price_intervalls_per_room_type
from utils import update_middag_dict_on_bookings, update_bokning_and_faktura_for_grupp_bokning, update_faktura_for_erbjudande_id
from utils import value_for_grupp_bokning_reference # old code, should be updated one time...
from utils import update_date_range
from utils import conv_timestamp2datetime_l, conv_timestamp2date_l, change_key_name_in_l
from utils import generate_random_interval_timestamp, generate_random_interval_defined_interval
#endregion


#region global variables
# number of testcases viz. input statements per table
g_numberOfRooms = 49
# number of "grupp_bokningar" FIXME: cascades badly, need to revise. faktura needs to have enough field values for both gbokning and bokning.
g_grupp_bokning_n = 3
# percentage of bookings that should be group bookings: TODO: deprecated?
#p_gr_b = 0.50
# number of bookings per group booking TODO: deprecated?
#bookings_per_groupb = math.floor(round((numberOfRooms)*p_gr_b)/grupp_bokning_n) # percent of the booking divided by number of group bookings rounded down.

# Store the generated primary key values for foreign key references
g_personal_ids = []
g_erbjudande_ids = []
g_faktura_ids = []
g_rum_ids = []
g_rum_typ_ids = []  # Has predefined room types
g_kund_ids = []
g_huvud_gast_ids = []
g_rum_pris_ids = []
g_grupp_bokning_ids = []
g_erbjudande_ids = []
g_middag_ids = []
g_forsaljning_ids = []
g_bokning_ids = []

# fixed length list of number of bookings assigned to each group booking
boknings_added_per_groupb = [0] * g_grupp_bokning_n

# a start date so we don't have different ones everywhere:
g_set_start_datetime = datetime(2023, 10, 16, 00, 00, 00) 
g_set_end_datetime = datetime(2025, 10, 16, 23, 59, 59)
g_set_days_intervall = 30

# make a dictionary for number of rooms:
g_n_r_dict = {
    'enkelrum_max': 15,
    'enkelrum_i': 0,
    'dubbelrum_max': 30,
    'dubbelrum_i': 0,
    'familjerum_max': 4,
    'familjerum_i': 0
}
#function to give the right rum_typ_id to rum table:
def g_assign_rum_typ() -> str:
    # we need to remember between runs:
    global g_n_r_dict
    # We'll break out of this when a correct room is choosen:
    while (True):
        choosen_rt = random.choice(g_rum_typ_ids)
        if choosen_rt == "enkelrum":
            if g_n_r_dict['enkelrum_i'] < g_n_r_dict['enkelrum_max']:
                g_n_r_dict['enkelrum_i'] += 1
                break
        elif choosen_rt == "dubbelrum":
            if g_n_r_dict['dubbelrum_i'] < g_n_r_dict['dubbelrum_max']:
                g_n_r_dict['dubbelrum_i'] += 1
                break
        elif choosen_rt == "familjerum":
            if g_n_r_dict['familjerum_i'] < g_n_r_dict['familjerum_max']:
                g_n_r_dict['familjerum_i'] += 1
                break
    return choosen_rt



#endregion
#FIXME: Fel i testdata: inbokning och utbokning kan vara samma dag.
#FIXME: Fel i testdata. Det finns flera aktuella rumpris för enkelrum. 
# Måste antingen göra så att personalen manuellt väljer pris, 
# eller fixa testdatan så att inte rumpris med samma rumtyp får överlappa i tid

#region DICTIONARY GENERATORS
# to make data accesible but still editable in case of foreign key conflicts etc.

# ID is not auto increment here: has to be manually assigned.
def generate_rum_typ_dict(p_id):
    max_antal_personer = 1 if p_id == "enkelrum" else 2 if p_id == "dubbelrum" else 4 if p_id == "familjerum" else 0
    rum_typ_dict = {
        'rum_typ_id': p_id,
        'max_antal_personer': max_antal_personer
    }
    return rum_typ_dict

def generate_erbjudande_dict(p_id):
    # Generate random erbjudande values
    start_datum, slut_datum = generate_random_interval_defined_interval(g_set_start_datetime, g_set_end_datetime, 90)  # Get random dates
    erbjudande_dict = {
        #NOTE:  discount to work by fixed deduction since this is test data. Normally this would be manually entered and used manually as well.
        #random.choice(rum_typ_ids),  # Room type ID must be "enkelrum", "familjerum", or "dubbelrum"
        'erbjudande_id': p_id,
        'prisavdrag': round(random.uniform(100.0, 300.0), 2),  # Price per X deduction
        'villkor': 'PLACEHOLDER villkor',  # Placeholder condition
        'start_datum': start_datum,  
        'slut_datum': slut_datum  
    }
    return erbjudande_dict

def generate_personal_dict(p_id):
    # Generate random personal values
    name, surname = name_surname_generator()
    personal_dict = {
        'personal_id': p_id,
        'fornamn': name,
        'efternamn': surname,
        'roll': random.choice(['Receptionist', 'Manager', 'Cleaner'])  
    }
    return personal_dict

def generate_kund_dict(p_id):
    # Generate random values for the kund dictionary
    name, surname = name_surname_generator()
    kund_dict = {
        'kund_id': p_id,
        'fornamn': name,
        'efternamn': surname, 
        'mejl_address': '{}@example.com'.format(random.randint(1000, 9999)),  
        'telefon_nummer': '+46{}'.format(random.randint(700000000, 799999999))  
    }
    return kund_dict

def generate_huvud_gast_dict(p_id):
    # Generate random values for the huvud_gast dictionary
    name, surname = name_surname_generator()
    huvud_gast_dict = {
        'huvud_gast_id': p_id,
        'fornamn': name,  
        'efternamn': surname, 
        'mejl_address': '{}@example.com'.format(random.randint(1000, 9999)),  
        'telefon_nummer': '+46{}'.format(random.randint(700000000, 799999999))  
    }
    return huvud_gast_dict

# foreign keys used: rum_typ_ids, personal_ids
def generate_rum_dict(p_id, fki):
    # Generate random values for the rum dictionary
    b_check_in, b_check_out = generate_checked_in_or_out() # gives either true of false on either one.
    rum_dict = {
        'rum_id': p_id,
        'rum_typ_id': g_assign_rum_typ(),  # Room type ID (e.g., "enkelrum", "familjerum", "dubbelrum")
        #'personal_id': random.choice(g_personal_ids),  # Personal ID must exist in 'personal'
        'personal_id': g_personal_ids[fki % len(g_personal_ids)],  # Personal ID must exist in 'personal'
        'checked_in': b_check_in,  # Checked in (0 or 1)
        'checked_out': b_check_out,  # Checked out (0 or 1)
        'vaningsplan': random.randint(1,5)
    }
    return rum_dict

# foreign keys used: rum_typ_ids
def generate_rum_pris_dict(p_id, fki):
    rum_typ_id = g_rum_typ_ids[fki % len(g_rum_typ_ids)]
    pris_per_natt = price_intervalls_per_room_type(rum_typ_id)  
    pris_start_datum, pris_slut_datum = generate_random_interval_defined_interval(g_set_start_datetime, g_set_end_datetime, 90) 
    
    rum_pris_dict = {
        'rum_pris_id': p_id,
        'rum_typ_id': rum_typ_id,  
        'pris_per_natt': pris_per_natt,  
        'start_datum': pris_start_datum,  
        'slut_datum': pris_slut_datum  
    }
    
    return rum_pris_dict

# foreign keys used: grupp_bokning_ids
def generate_middag_dict(p_id, fki):
    middag_dict = {
        'middag_id': p_id,
        'grupp_bokning_id': g_grupp_bokning_ids[fki % len(g_grupp_bokning_ids)],  # always has to have grupp_bokning_id to exist
        'antal_personer': random.randint(1, 10),  
        'datum': "NULL"  # Placeholder for date of the meal, updated later since dependent on bookings
    }
    return middag_dict

# foreign keys used: personal_ids
def generate_faktura_dict(p_id, fki):
    # FIXME: 
    #faktura['status']=
    """jämföra mot today ==> enkelt.
    pågående:
    jämföra mot today ==> enkelt.
    betald:
    jämföra mot today ==> enkelt.
    obetald:
    inte ha med. """
    faktura_dict = {
        'faktura_id': p_id,
        'personal_id': random.choice(g_personal_ids),  
        'erbjudande_id': g_erbjudande_ids[fki % len(g_erbjudande_ids)],
        'status': random.choice(['pagaende', 'betald', 'kommande']), # correct one is set manually
        'grupp_bokning_id': "NULL"  # updated later via main, depends on grupp_bokning
    }
    return faktura_dict

# foreign keys used: rum_id, personal_id, faktura_id
def generate_forsaljning_dict(p_id, fki):
    summa = generate_random_decimal_pricesum(50,500,2)
    datum = generate_random_timestamp(g_set_start_datetime, g_set_end_datetime)
    
    forsaljning_dict = {
        'forsaljning_id': p_id,
        'rum_id': g_rum_ids[fki % len(g_rum_ids)],
        'personal_id': random.choice(g_personal_ids),
        'faktura_id': g_faktura_ids[fki % len(g_faktura_ids)],
        'summa': summa,
        'datum': datum
    }
    return forsaljning_dict

# foreign keys used: rum_ids, kund_ids, huvud_gast_ids, personal_ids, grupp_bokning_ids
# bokning_datum kan vara i framtiden relativt checkin_date, känns inte rätt, fixas senare i update dictionaries
def generate_bokning_dict(p_id, fki, g_grupp_bokning_n):
    global boknings_added_per_groupb
    # Get random dates within 1 month
    checkin_date, checkout_date = generate_random_interval_defined_interval(g_set_start_datetime, g_set_end_datetime, g_set_days_intervall)  
    # Returns null or fk_grupp_bokning and updates global list. 
    grupp_bokning_assigned_value, boknings_added_per_groupb_updated = value_for_grupp_bokning_reference(
        g_grupp_bokning_ids[fki % len(g_grupp_bokning_ids)], boknings_added_per_groupb, g_grupp_bokning_n)  
    boknings_added_per_groupb = boknings_added_per_groupb_updated 
    bokning_timestamp = generate_random_timestamp(g_set_start_datetime, g_set_end_datetime) 
    bokning_dict = {
        'bokning_id': p_id,
        'rum_id': g_rum_ids[fki % len(g_rum_ids)],  
        'kund_id': g_kund_ids[fki % len(g_kund_ids)],  
        'huvud_gast_id': g_huvud_gast_ids[fki % len(g_huvud_gast_ids)],  
        'personal_id': random.choice(g_personal_ids),  
        'rum_pris_id': g_rum_pris_ids[fki % len(g_rum_pris_ids)],  
        'grupp_bokning_id': grupp_bokning_assigned_value,  # Group booking ID, either an ID or NULL
        'faktura_id': "NULL",  # Placeholder for faktura ID, fixed later, either ID or NULL, is NULL when group id has ID.
        'datum_incheck': checkin_date,  # Randomized check-in date
        'datum_utcheck': checkout_date,  # Randomized check-out date
        'bokning_datum': bokning_timestamp,  # Booking date, randomly generated
        'antal_gaster': random.randint(1, 4)  # Number of guests
    }
    return bokning_dict

def generate_grupp_bokning_dict(p_id):
    grupp_bokning_dict = {
        'grupp_bokning_id': p_id,
        # 'personal_id': random.choice(personal_ids) 
    }
    return grupp_bokning_dict
#endregion

#region INSERT STATEMENT STRING GENERATOR:::

# INPUTS:
#   table_name: name of table for insert statement
#   dict: the dictionary to be converted to an SQL insert statement
#   b_p_key_auto_increment: boolean, if the primary key is auto increment --> true; otherwise --> false.
def generate_insert_statement(table_name, dict, b_p_key_auto_increment):
    return dict_to_sql_insert_str(table_name, dict, b_p_key_auto_increment)

#endregion

def update_status_in_dict(l_data_dict):
    # Check which boolean value is True and assign the key name as a string
    for data_dict in l_data_dict:
        if data_dict['checkat_in'] == "TRUE":
            data_dict['status'] = 'checkat_in'
        elif data_dict['checkat_ut'] == "TRUE":
            data_dict['status'] = 'checkat_ut'
        else:
            data_dict['status'] = 'unknown'  # Optional: handle cases where both are False or missing
        # Delete the original boolean keys
        del data_dict['checkat_in']
        del data_dict['checkat_ut']

#


# made all dict functions 
def main():
    # start tracking runtime:
    start_time = time.time()
    # global values with IDs so we can keep track of foreign IDs etc.
    global g_personal_ids, g_erbjudande_ids, g_faktura_ids, g_rum_ids, g_kund_ids, g_huvud_gast_ids, g_rum_pris_ids
    global g_middag_ids, g_forsaljning_ids, g_bokning_ids, g_rum_typ_ids, g_grupp_bokning_ids

    #region number of entities per entity-type, based on NumberOfRooms
    rum_typ_n = 3 # hardcoded as per specification to 3.
    erbjudande_n = math.floor(g_numberOfRooms/4) # 25% of number of rooms.
    personal_n = math.floor(g_numberOfRooms/4) # 25% of number of rooms.
    huvud_gast_n = g_numberOfRooms # same as number of rooms, since same in number of bookings.
    kund_n = g_numberOfRooms # NOTE: for now keep the same, see if break or not.
    rum_pris_n = math.floor(g_numberOfRooms/4) # 25% of rooms.
    rum_n = g_numberOfRooms # same as number of rooms.
    faktura_n = g_numberOfRooms # same as number of rooms.
    #grupp_bokning_n = grupp_boking_n  # has different amount, see global value at start. 
    middag_n = g_grupp_bokning_n*2 # we thinks it's resonable that every group has two dinners. 
    forsaljning_n = math.floor(g_numberOfRooms/4) # 25 % of number of rooms: only 25% of guests buy stuff and put on room bill.
    booking_n = g_numberOfRooms # same as number of rooms.
    #endregion

    #region number of certain fields occurances
    fakt_w_erb_n = math.floor(faktura_n/4) # 25 % of number of faktura: only 25% of guests will get discounts.


    #region generate all autoincrement primary ids as ref for foreign key etc.
    g_rum_typ_ids = ["enkelrum", "dubbelrum", "familjerum"] #  predefined
    g_erbjudande_ids = list(range(1, erbjudande_n+1)) 
    g_personal_ids = list(range(1, personal_n+1)) 
    g_huvud_gast_ids = list(range(1, huvud_gast_n+1)) 
    g_kund_ids = list(range(1, kund_n+1)) 
    g_rum_pris_ids = list(range(1, rum_pris_n+1)) 
    g_rum_ids = list(range(1, rum_n+1)) 
    g_faktura_ids = list(range(1, faktura_n+1)) 
    g_grupp_bokning_ids = list(range(1, g_grupp_bokning_n+1))
    g_middag_ids = list(range(1, middag_n+1)) 
    g_forsaljning_ids = list(range(1, forsaljning_n+1)) 
    g_bokning_ids = list(range(1, booking_n+1)) 
    #endregion

    #region Generate all the dictionaries and tabulate the results to visualize them:

    l_rum_typ_dicts = [generate_rum_typ_dict(g_rum_typ_ids[i]) for i in range(rum_typ_n)]
    tabulate_print(l_rum_typ_dicts, "rum_typ", "pre_processing")
    l_erbjudande_dicts = [generate_erbjudande_dict(g_erbjudande_ids[i]) for i in range(erbjudande_n)]
    tabulate_print(l_erbjudande_dicts, "erbjudande", "pre_processing")
    l_personal_dicts = [generate_personal_dict(g_personal_ids[i]) for i in range(personal_n)]
    tabulate_print(l_personal_dicts, "personal", "pre_processing")
    l_huvud_gast_dicts = [generate_huvud_gast_dict(g_huvud_gast_ids[i]) for i in range(huvud_gast_n)]
    tabulate_print(l_huvud_gast_dicts, "huvud_gast", "pre_processing")
    l_kund_dicts = [generate_kund_dict(g_kund_ids[i]) for i in range(kund_n)]
    tabulate_print(l_kund_dicts, "kund", "pre_processing")
    l_rum_pris_dicts = [generate_rum_pris_dict(g_rum_pris_ids[i], i) for i in range(rum_pris_n)]
    tabulate_print(l_rum_pris_dicts, "rum_pris_typ", "pre_processing")
    l_rum_dicts  = [generate_rum_dict(g_rum_ids[i], i) for i in range(rum_n)]
    tabulate_print(l_rum_dicts, "rum", "pre_processing")
    l_faktura_dicts = [generate_faktura_dict(g_faktura_ids[i], i) for i in range(faktura_n)]
    tabulate_print(l_faktura_dicts, "faktura", "pre_processing")
    l_grupp_bokning_dicts = [generate_grupp_bokning_dict(g_grupp_bokning_ids[i]) for i in range(g_grupp_bokning_n)]
    tabulate_print(l_grupp_bokning_dicts, "grupp_bokning", "pre_processing")
    l_middag_dicts = [generate_middag_dict(g_middag_ids[i], i) for i in range(middag_n)]
    tabulate_print(l_middag_dicts, "middag", "pre_processing")
    l_forsaljning_dicts = [generate_forsaljning_dict(g_forsaljning_ids[i], i) for i in range(forsaljning_n)]
    tabulate_print(l_forsaljning_dicts, "forsaljning", "pre_processing")
    l_bokning_dicts = [generate_bokning_dict(g_bokning_ids[i], i, g_grupp_bokning_n) for i in range(booking_n)]
    tabulate_print(l_bokning_dicts, "bokning", "pre_processing")
    #endregion


    #region TODO: update dictionaries with values:
    # FIXME: breaks date range functon for booking in regards to incheckning and utcheckning
    # FIXME: status: checkat_in eller checkat_ut verkar vara arbiträrt assignerat. Slumpat?

    # update middag with date for dinner based on bookings:
    update_middag_dict_on_bookings(l_middag_dicts, l_bokning_dicts)
    tabulate_print(l_middag_dicts, "middag", "after: update_middag_dict_on_bookings")

    # update bokning_dicts with factura dict AND update faktura_dicts.
    # functions like this:
    """ Check: if a booking has a group booking then it sets factura_id to NULL in bokning << UPDATES BOOKING *
                    AND updates factura with that group booking ID  << UPDATES FAKTURA * 
                        AND saves (list: l_factura_id_w_gb) which factura_id has a group booking assigned to it.
                else sets factura_id to an factura_id in bokning that doesn't (EXIST IN list: l_factura_id_w_gb)
                    have a group_booking assigned to it in a factura entity. """
    update_bokning_and_faktura_for_grupp_bokning(l_bokning_dicts, l_faktura_dicts)
    tabulate_print(l_faktura_dicts, "faktura", "update_bokning_and_faktura_for_grupp_bokning")
    tabulate_print(l_bokning_dicts, "bokning", "update_bokning_and_faktura_for_grupp_bokning")

    # update erbjudande_id in faktura so that it will reflect the amount we want:
    update_faktura_for_erbjudande_id(l_faktura_dicts, fakt_w_erb_n)
    tabulate_print(l_faktura_dicts, "faktura", "update_faktura_for_erbjudande_id")

    # make sure dates are within a good range, #TODO: doesn't take FK and PM into regard, so might come out mixed anyhow. >.<
    update_date_range(g_set_start_datetime, g_set_end_datetime, g_set_days_intervall, l_erbjudande_dicts, l_bokning_dicts, l_rum_pris_dicts, l_middag_dicts)
    tabulate_print(l_erbjudande_dicts, "erbjudande", "update_date_range")
    tabulate_print(l_rum_pris_dicts, "rum_pris", "update_date_range")
    tabulate_print(l_bokning_dicts, "bokning", "update_date_range")
    tabulate_print(l_middag_dicts, "middag", "update_date_range")

    # change format for dates!
    # erbjudande:
    conv_timestamp2datetime_l(l_erbjudande_dicts, "start_datum")
    conv_timestamp2datetime_l(l_erbjudande_dicts, "slut_datum")
    # försäljning
    conv_timestamp2datetime_l(l_forsaljning_dicts, "datum")
    # bokning
    conv_timestamp2date_l(l_bokning_dicts, "datum_incheck")
    conv_timestamp2date_l(l_bokning_dicts, "datum_utcheck")
    conv_timestamp2datetime_l(l_bokning_dicts, "bokning_datum")
    # rum_pris
    conv_timestamp2datetime_l(l_rum_pris_dicts, "start_datum")
    conv_timestamp2datetime_l(l_rum_pris_dicts, "slut_datum")
    # middag
    conv_timestamp2datetime_l(l_middag_dicts, "datum")

    # change key name for certain dictionaries.
    # erbjudande start_datum -> start_datum_tid
    change_key_name_in_l(l_erbjudande_dicts, "start_datum", "start")
    # erbjudande slut_datum -> datum_datum_tid
    change_key_name_in_l(l_erbjudande_dicts, "slut_datum", "slut")
    # middag datum -> datum_tid
    # bokning datum -> datum_tid
    # rum_pris start_datum -> start_datum_tid
    change_key_name_in_l(l_rum_pris_dicts, "start_datum", "start")
    # rum_pris slut_datum -> slut_datum_tid
    change_key_name_in_l(l_rum_pris_dicts, "slut_datum", "slut")
    # forsaljning datum -> datum_tid
    # bokning datum_incheck --> incheckning
    change_key_name_in_l(l_bokning_dicts, "datum_incheck", "incheckning")
    # bokning datum_utcheck -> utcheckning
    change_key_name_in_l(l_bokning_dicts, "datum_utcheck", "utcheckning") 
    # rum checked_in -> incheckad
    change_key_name_in_l(l_rum_dicts, "checked_in", "checkat_in")
    # rum checked_out -> utcheckad
    change_key_name_in_l(l_rum_dicts, "checked_out", "checkat_ut")
    # now we use status instead for rooms!:
    update_status_in_dict(l_rum_dicts)
    #pop personal_id from gruppbokning:
    #done at start. commented it out.

    #pop id from faktura:
    for d in l_faktura_dicts:
        del d['grupp_bokning_id']

    #endregion

    #region tabulate final version before conversion to sql query stings
    tabulate_print(l_rum_typ_dicts, "rum_typ", "final")
    tabulate_print(l_erbjudande_dicts, "erbjudande", "final")
    tabulate_print(l_personal_dicts, "personal", "final")
    tabulate_print(l_huvud_gast_dicts, "huvud_gast", "final")
    tabulate_print(l_kund_dicts, "kund", "final")
    tabulate_print(l_rum_pris_dicts, "rum_pris", "final")
    tabulate_print(l_rum_dicts, "rum", "final")
    tabulate_print(l_faktura_dicts, "faktura", "final")
    tabulate_print(l_grupp_bokning_dicts, "grupp_bokning", "final")
    tabulate_print(l_middag_dicts, "middag", "final")
    tabulate_print(l_forsaljning_dicts, "forsaljning", "final")
    tabulate_print(l_bokning_dicts, "bokning", "final")
    #endregion

    #region create strings with all the sql queries for write to file!
    
    # generate room_type queries
    rum_typ_queries = [generate_insert_statement("rum_typ", l_rum_typ_dicts[i], False) for i in range(rum_typ_n)]

    # Generate 'erbjudande' queries.
    erbjudande_queries = [generate_insert_statement("erbjudande", l_erbjudande_dicts[i], True) for i in range(erbjudande_n)]

    # Generate 'personal' queries
    personal_queries = [generate_insert_statement("personal", l_personal_dicts[i], True) for i in range(personal_n)]

    # Generate 'huvud_gast' queries 
    huvud_gast_queries = [generate_insert_statement("huvud_gast", l_huvud_gast_dicts[i], True) for i in range(huvud_gast_n)]

    # Generate 'kund' queries 
    kund_queries = [generate_insert_statement("kund", l_kund_dicts[i], True) for i in range(kund_n)]

    # Generate 'rum_pris' queries 
    rum_pris_queries = [generate_insert_statement("rum_pris", l_rum_pris_dicts[i], True) for i in range(rum_pris_n)]

    # Generate 'rum' queries 
    rum_queries = [generate_insert_statement("rum", l_rum_dicts[i], True) for i in range(rum_n)]

    # Generate 'faktura' queries 
    faktura_queries = [generate_insert_statement("faktura", l_faktura_dicts[i], True) for i in range(faktura_n)]

    # Generate 'grupp_bokning' queries 
    grupp_bokning_queries = [generate_insert_statement("grupp_bokning", l_grupp_bokning_dicts[i], True) for i in range(g_grupp_bokning_n)]

    # generate middag queries
    middag_queries = [generate_insert_statement("middag", l_middag_dicts[i], True) for i in range(middag_n)]

    # generate forsaljning queries
    forsaljning_queries = [generate_insert_statement("forsaljning", l_forsaljning_dicts[i], True) for i in range(forsaljning_n)]

    # Generate booking queries
    bokning_queries = [generate_insert_statement("bokning", l_bokning_dicts[i], True) for i in range(booking_n)]

    #endregion

    #region Write to text files

    write_to_file('1_rum_typ_inserts.txt', rum_typ_queries)
    write_to_file('2_erbjudande_inserts.txt', erbjudande_queries)
    write_to_file('3_personal_inserts.txt', personal_queries)
    write_to_file('4_huvud_gast_inserts.txt', huvud_gast_queries)
    write_to_file('5_kund_inserts.txt', kund_queries)
    write_to_file('6_rum_pris_inserts.txt', rum_pris_queries)
    write_to_file('7_rum_inserts.txt', rum_queries)
    write_to_file('8_grupp_bokning_inserts.txt', grupp_bokning_queries)
    write_to_file('9_faktura_inserts.txt', faktura_queries)
    write_to_file('10_middag_inserts.txt', middag_queries)
    write_to_file('11_forsaljning_inserts.txt', forsaljning_queries)
    write_to_file('12_bokning_inserts.txt', bokning_queries)

    #endregion

    #runtime finished, print to terminal:
    end_time = time.time()
    runtime = end_time - start_time
    r_minutes = int(runtime // 60) # int nmr of mins
    r_seconds = int(runtime % 60)
    print(f"\nProgram runtime:\t{r_minutes:02d} minutes and {r_seconds:02d} seconds.")
    runtimestr = (f"\nProgram runtime:\t{r_minutes:02d} minutes and {r_seconds:02d} seconds.")
    write_to_file('0_runtime.txt', runtimestr)
    
if __name__ == '__main__':
    main()

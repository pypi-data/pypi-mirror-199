import psycopg

_create_bidding_data_table = """
    CREATE TABLE bidding_data (
        interval_datetime timestamp,
        duid text,
        bidband int4,
        onhour bool,
        bidprice float4,
        bidvolume float4,
        bidvolumeadjusted float4,
        PRIMARY KEY(interval_datetime, duid, bidband)
    );
"""

_create_demand_data_table = """
    CREATE TABLE demand_data (
        settlementdate timestamp,
        regionid text,
        totaldemand float8,
        rrp float8,
        PRIMARY KEY(settlementdate, regionid)
    );
"""

_create_duid_info_table = """
    CREATE TABLE duid_info (
        duid text PRIMARY KEY,
        region text,
        "fuel source - descriptor" text,
        "dispatch type" text,
        "technology type - descriptor" text,
        "unit type" text,
        "station name" text
    );
"""

_create_price_bins_table = """
    CREATE TABLE price_bins (
        bin_name text PRIMARY KEY,
        lower_edge float8,
        upper_edge float8
    );
"""

_create_unit_dispatch_table = """
    CREATE TABLE unit_dispatch (
        interval_datetime timestamp,
        duid text,
        onhour bool,
        availability float4,
        totalcleared float4,
        finalmw float4,
        asbidrampupmaxavail float4,
        asbidrampdownminavail float4,
        rampupmaxavail float4,
        rampdownminavail float4,
        pasaavailability float4,
        maxavail float4,
        PRIMARY KEY (interval_datetime, duid)
    );
"""

_create_distinct_unit_types_function = """
    CREATE OR REPLACE FUNCTION distinct_unit_types_v3(dispatch_type text, regions text[])
      RETURNS TABLE ("unit type" text)
      LANGUAGE plpgsql AS
    $func$
    BEGIN

      RETURN QUERY SELECT DISTINCT t."unit type" from duid_info t where t."dispatch type" = dispatch_type and region = ANY(regions);

    END
    $func$;
    """


_create_aggregate_bids_function = """
    CREATE OR REPLACE FUNCTION aggregate_bids_v2(regions text[], start_datetime timestamp, end_datetime timestamp, resolution text, dispatch_type text, adjusted text, tech_types text[])
      RETURNS TABLE (interval_datetime timestamp, bin_name text, bidvolume float4)
      LANGUAGE plpgsql AS
    $func$
      DECLARE hourly_filter text;
      DECLARE bidvolume_col text;
    BEGIN

      DROP TABLE IF EXISTS filtered_regions;
      DROP TABLE IF EXISTS filtered_duid_info;
      DROP TABLE IF EXISTS return_table;

      IF array_length(tech_types, 1) > 0 THEN
        CREATE TEMP TABLE filtered_duid_info ON COMMIT DROP as
        SELECT * FROM duid_info d WHERE d."unit type" = ANY(tech_types);
      ELSE
        CREATE TEMP TABLE filtered_duid_info ON COMMIT DROP as
        SELECT * FROM duid_info d;
      END IF;

      CREATE TEMP TABLE filtered_regions ON COMMIT DROP AS
      SELECT * FROM filtered_duid_info WHERE region = ANY(regions) and "dispatch type" = dispatch_type;

      IF resolution = 'hourly' THEN
        hourly_filter:= ' onhour = true and';
      ELSE
        hourly_filter:= '';
      END IF;

      IF adjusted = 'adjusted' THEN
        bidvolume_col:= 'bidvolumeadjusted';
      ELSE
        bidvolume_col:= 'bidvolume';
      END IF;

      EXECUTE format($$CREATE TEMP TABLE return_table ON COMMIT DROP as SELECT t.interval_datetime, t.bin_name, SUM(t.bidvolume) as bidvolume FROM
                          ((SELECT b.interval_datetime, b.bidprice, b.%s as bidvolume FROM bidding_data b WHERE%s b.interval_datetime > (timestamp '%s') and b.interval_datetime <= (timestamp '%s')
                            and b.duid IN (SELECT duid FROM filtered_regions)) a
                          LEFT JOIN price_bins p ON a.bidprice >= p.lower_edge AND a.bidprice < p.upper_edge) t
                        group by t.interval_datetime, t.bin_name;$$,
                      bidvolume_col, hourly_filter, start_datetime, end_datetime);

      RETURN QUERY SELECT * FROM return_table;

    END
    $func$;
    """

_create_aggregate_dispatch_data_function = """
    CREATE OR REPLACE FUNCTION aggregate_dispatch_data_v2(column_name text, regions text[], start_datetime timestamp, end_datetime timestamp, resolution text, dispatch_type text, tech_types text[])
      RETURNS TABLE (interval_datetime timestamp, columnvalues float4)
      LANGUAGE plpgsql AS
    $func$

      DECLARE extra_col text;

    BEGIN

      DROP TABLE IF EXISTS filtered_duid_info;
      DROP TABLE IF EXISTS filtered_regions;
      DROP TABLE IF EXISTS time_filtered_dispatch;
      DROP TABLE IF EXISTS region_filtered_dispatch;
      DROP TABLE IF EXISTS return_data;

      IF array_length(tech_types, 1) > 0 THEN
        CREATE TEMP TABLE filtered_duid_info ON COMMIT DROP as
        SELECT * FROM duid_info d WHERE d."unit type" = ANY(tech_types);
      ELSE
        CREATE TEMP TABLE filtered_duid_info ON COMMIT DROP as
        SELECT * FROM duid_info d;
      END IF;

      CREATE TEMP TABLE filtered_regions ON COMMIT DROP AS
      SELECT * FROM filtered_duid_info WHERE region = ANY(regions) and "dispatch type" = dispatch_type;

      IF column_name = 'asbidrampupmaxavail' THEN
        extra_col:= ', d.maxavail';
      ELSIF column_name = 'rampupmaxavail' THEN
        extra_col:= ', d.availability';
      ELSE
        extra_col:= '';
      END IF;

      IF resolution = 'hourly' THEN
        EXECUTE format($$CREATE TEMP TABLE time_filtered_dispatch ON COMMIT DROP as
                        SELECT d.interval_datetime, d.duid, d.%s as columnvalue %s
                          FROM unit_dispatch d WHERE onhour = true AND d.interval_datetime > (timestamp '%s') and d.interval_datetime <= (timestamp '%s');$$, column_name, extra_col, start_datetime, end_datetime);
      ELSE
        EXECUTE format($$CREATE TEMP TABLE time_filtered_dispatch ON COMMIT DROP as
                        SELECT d.interval_datetime, d.duid, d.%s as columnvalue %s
                          FROM unit_dispatch d WHERE d.interval_datetime > (timestamp '%s') and d.interval_datetime <= (timestamp '%s');$$, column_name, extra_col, start_datetime, end_datetime);
      END IF;

      CREATE TEMP TABLE region_filtered_dispatch ON COMMIT DROP as
      SELECT * FROM time_filtered_dispatch WHERE duid IN (SELECT duid FROM filtered_regions);

      IF column_name = 'asbidrampupmaxavail' THEN
        UPDATE region_filtered_dispatch d SET columnvalue = d.maxavail WHERE d.columnvalue > d.maxavail;
      ELSIF column_name = 'asbidrampdownminavail' THEN
        UPDATE region_filtered_dispatch d SET columnvalue = 0  WHERE d.columnvalue < 0;
      ELSIF column_name = 'rampupmaxavail' THEN
        UPDATE region_filtered_dispatch d SET columnvalue = d.availability WHERE d.columnvalue > d.availability;
      ELSIF column_name = 'rampdownminavail' THEN
        UPDATE region_filtered_dispatch d SET columnvalue = 0 WHERE d.columnvalue < 0;
      END IF;

      CREATE TEMP TABLE return_data ON COMMIT DROP AS SELECT d.interval_datetime, sum(d.columnvalue) as column_value
        FROM region_filtered_dispatch d group by d.interval_datetime;

      RETURN QUERY SELECT * FROM return_data;

    END
    $func$;
"""

_create_get_bids_by_unit_function = """
    CREATE OR REPLACE FUNCTION get_bids_by_unit_v2(duids text[], start_datetime timestamp, end_datetime timestamp, resolution text, adjusted text)
      RETURNS TABLE (interval_datetime timestamp, duid text, bidband int, bidvolume float4, bidprice float4)
      LANGUAGE plpgsql AS
    $func$
    BEGIN

      -- set temp_buffers = 10000;

      DROP TABLE IF EXISTS time_filtered_bids;
      DROP TABLE IF EXISTS correct_volume_column;

      IF resolution = 'hourly' THEN
        CREATE TEMP TABLE time_filtered_bids ON COMMIT DROP as
        SELECT * FROM bidding_data b WHERE onhour
                                       AND b.interval_datetime > start_datetime
                                       and b.interval_datetime <= end_datetime
                                       and b.duid = ANY(duids);
      ELSE
       CREATE TEMP TABLE time_filtered_bids ON COMMIT DROP as
        SELECT * FROM bidding_data b WHERE b.interval_datetime > start_datetime
                                       and b.interval_datetime <= end_datetime
                                       and b.duid = ANY(duids);
      END IF;

      IF adjusted = 'adjusted' THEN
        CREATE TEMP TABLE correct_volume_column ON COMMIT DROP as
        SELECT t.interval_datetime, t.duid, t.bidband, t.bidvolumeadjusted as bidvolume, t.bidprice
          FROM time_filtered_bids t;
      ELSE
        CREATE TEMP TABLE correct_volume_column ON COMMIT DROP as
        SELECT t.interval_datetime, t.duid, t.bidband, t.bidvolume, t.bidprice FROM time_filtered_bids t;
      END IF;

      RETURN QUERY SELECT b.interval_datetime, b.duid, b.bidband, b.bidvolume, b.bidprice FROM correct_volume_column b;

    END
    $func$;
"""

_create_aggregate_dispatch_data_duids_function = """
    CREATE OR REPLACE FUNCTION aggregate_dispatch_data_duids_v2(column_name text,duids text[], start_datetime timestamp, end_datetime timestamp, resolution text)
    RETURNS TABLE (interval_datetime timestamp, columnvalues float4)
      LANGUAGE plpgsql AS
    $func$
    BEGIN

      DROP TABLE IF EXISTS filtered_dispatch;
      DROP TABLE IF EXISTS return_data;

      IF resolution = 'hourly' THEN
        CREATE TEMP TABLE filtered_dispatch ON COMMIT DROP as
        SELECT * FROM unit_dispatch d WHERE onhour = true
                                        AND d.interval_datetime > start_datetime
                                        and d.interval_datetime <= end_datetime
                                        and d.duid = ANY(duids);
      ELSE
       CREATE TEMP TABLE filtered_dispatch ON COMMIT DROP as
        SELECT * FROM unit_dispatch d WHERE d.interval_datetime > start_datetime
                                        and d.interval_datetime <= end_datetime
                                        and d.duid = ANY(duids);
      END IF;

      UPDATE filtered_dispatch d SET asbidrampupmaxavail = d.maxavail WHERE d.asbidrampupmaxavail > d.maxavail;
      UPDATE filtered_dispatch d SET asbidrampdownminavail = 0  WHERE d.asbidrampdownminavail < 0;

      UPDATE filtered_dispatch d SET rampupmaxavail = d.availability WHERE d.rampupmaxavail > d.maxavail;
      UPDATE filtered_dispatch d SET rampdownminavail = 0 WHERE d.rampdownminavail < 0;

      EXECUTE format('CREATE TEMP TABLE return_data ON COMMIT DROP AS SELECT d.interval_datetime,
                      SUM(d.%I) as columnvalues
                      FROM filtered_dispatch d group by d.interval_datetime;', column_name);

      RETURN QUERY SELECT * FROM return_data;

    END
    $func$;
    """

_create_get_duids_for_stations = """
    CREATE OR REPLACE FUNCTION get_duids_for_stations(stations text[])
      RETURNS TABLE (duid text)
      LANGUAGE plpgsql AS
    $func$

    BEGIN

      RETURN QUERY SELECT d.duid FROM duid_info d WHERE d."station name" = ANY(stations) ;

    END
    $func$;
    """

_create_get_duids_and_stations_function = """
    CREATE OR REPLACE FUNCTION get_duids_and_staions_in_regions_and_time_window_v2(regions text[], start_datetime timestamp, end_datetime timestamp, dispatch_type text, tech_types text[])
      RETURNS TABLE (duid text, "station name" text)
      LANGUAGE plpgsql AS
    $func$

      DECLARE available_duids text[];

    BEGIN

      DROP TABLE IF EXISTS time_filtered_bids;
      DROP TABLE IF EXISTS filtered_duid_info;

      CREATE TEMP TABLE time_filtered_bids ON COMMIT DROP as
      SELECT DISTINCT b.duid FROM bidding_data b WHERE onhour = true
                                                   and b.interval_datetime > start_datetime
                                                   and b.interval_datetime <= end_datetime;

      IF array_length(tech_types, 1) > 0 THEN
        CREATE TEMP TABLE filtered_duid_info ON COMMIT DROP as
        SELECT * FROM duid_info d WHERE d."unit type" = ANY(tech_types) and "dispatch type" = dispatch_type
                                        and region = ANY(regions);
      ELSE
        CREATE TEMP TABLE filtered_duid_info ON COMMIT DROP as
        SELECT * FROM duid_info d WHERE "dispatch type" = dispatch_type and region = ANY(regions);
      END IF;

      RETURN QUERY SELECT d.duid, d."station name" FROM filtered_duid_info d WHERE d.duid IN (SELECT t.duid from time_filtered_bids t);

    END
    $func$;
    """

_create_aggregate_prices_function = """
    CREATE OR REPLACE FUNCTION aggregate_prices(regions text[], start_datetime timestamp, end_datetime timestamp)
      RETURNS TABLE (settlementdate timestamp, price float)
      LANGUAGE plpgsql AS
    $func$
    BEGIN

      DROP TABLE IF EXISTS time_filtered_price;

      CREATE TEMP TABLE time_filtered_price ON COMMIT DROP as
      SELECT b.settlementdate, b.regionid, b.totaldemand, b.rrp FROM demand_data b WHERE b.settlementdate > start_datetime and b.settlementdate <= end_datetime and regionid = ANY(regions);

      RETURN QUERY SELECT b.settlementdate, sum(b.rrp*b.totaldemand)/sum(b.totaldemand) as vwap FROM time_filtered_price b GROUP BY b.settlementdate;

    END
    $func$;
    """

_create_aggregate_demand_function = """
    CREATE OR REPLACE FUNCTION aggregate_demand(regions text[], start_datetime timestamp, end_datetime timestamp)
      RETURNS TABLE (settlementdate timestamp, totaldemand float)
      LANGUAGE plpgsql AS
    $func$
    BEGIN

      DROP TABLE IF EXISTS time_filtered_demand;

      CREATE TEMP TABLE time_filtered_demand ON COMMIT DROP as
      SELECT b.settlementdate, b.regionid, b.totaldemand FROM demand_data b
        WHERE b.settlementdate > start_datetime and b.settlementdate <= end_datetime and regionid = ANY(regions);

      RETURN QUERY SELECT b.settlementdate, sum(b.totaldemand) as totaldemand
                      FROM time_filtered_demand b GROUP BY b.settlementdate;

    END
    $func$;
    """

_create_table_statements = [
    _create_bidding_data_table,
    _create_demand_data_table,
    _create_duid_info_table,
    _create_price_bins_table,
    _create_unit_dispatch_table,
]

_create_function_statements = [
    _create_aggregate_bids_function,
    _create_aggregate_dispatch_data_function,
    _create_distinct_unit_types_function,
    _create_get_bids_by_unit_function,
    _create_get_duids_for_stations,
    _create_get_duids_and_stations_function,
    _create_aggregate_prices_function,
    _create_aggregate_dispatch_data_duids_function,
    _create_aggregate_demand_function,
]


def create_db_tables(connection_string):
    """
    Creates the tables needed to store data in a PostgresSQL database. This function
    should be run after creating an empty database, then functions in the
    :py:mod:`nem_bidding_dashboard.populate_postgres_db` can be used to add data to the database.

    Examples:

    >>> from nem_bidding_dashboard import postgres_helpers

    >>> con_string = postgres_helpers.build_connection_string(
    ... hostname='localhost',
    ... dbname='bidding_dashboard_db',
    ... username='bidding_dashboard_maintainer',
    ... password='1234abcd',
    ... port=5433)

    >>> create_db_tables(con_string)

    Args:
        connection_string: str for connecting to PostgresSQL database, the function :py:func:`nem_bidding_dashboard.postgres_helpers.build_connection_string`
            can be used to build a properly formated connection string, or alternative any string that matches the
            format allowed by `PostgresSQL <https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING>`_
            can be used

    """
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            for statement in _create_table_statements:
                cur.execute(statement)
            conn.commit()


def create_db_functions(connection_string):
    """
    Creates the functions needed to retreive data in a PostgresSQL database. This function
    should be run after creating an empty database, then functions in the
    :py:mod:`nem_bidding_dashboard.populate_postgres_db` can be used to add data to the database.

    Examples:

    >>> from nem_bidding_dashboard import postgres_helpers

    >>> con_string = postgres_helpers.build_connection_string(
    ... hostname='localhost',
    ... dbname='bidding_dashboard_db',
    ... username='bidding_dashboard_maintainer',
    ... password='1234abcd',
    ... port=5433)

    >>> create_db_functions(con_string)

    Args:
        connection_string: str for connecting to PostgresSQL database, the function :py:func:`nem_bidding_dashboard.postgres_helpers.build_connection_string`
            can be used to build a properly formated connection string, or alternative any string that matches the
            format allowed by `PostgresSQL <https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING>`_
            can be used

    """
    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            for statement in _create_function_statements:
                cur.execute(statement)
            conn.commit()

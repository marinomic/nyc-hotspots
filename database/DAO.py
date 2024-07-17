from database.DB_connect import DBConnect
from model.location import Location


class DAO():

    @staticmethod
    def getAllProviders():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select distinct Provider 
        from nyc_wifi_hotspot_locations
        order by Provider
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row['Provider'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(provider):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct location
            from nyc_wifi_hotspot_locations 
            where Provider = %s
            """

        cursor.execute(query, (provider,))

        for row in cursor:
            result.append(row['location'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(provider):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT n1.Location as n1Loc, n2.Location as n2Loc, avg(n1.Latitude) as n1Lat, avg(n1.Longitude) as n1Long, avg(n2.Latitude) as n2Lat, avg(n2.Longitude) as n2Long
                    FROM nyc_wifi_hotspot_locations n1 , nyc_wifi_hotspot_locations n2 
                    WHERE n1.Provider = n2.Provider 
                    and n1.Provider = %s
                    and n1.Location < n2.Location 
                    GROUP by n1.Location, n2.Location
                """

        cursor.execute(query, (provider,))

        for row in cursor:
            loc1 = Location(row['n1Loc'], row['n1Lat'], row['n1Long'])
            loc2 = Location(row['n2Loc'], row['n2Lat'], row['n2Long'])
            result.append((loc1, loc2))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllObjLocationForProvider(provider):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select Location , avg(Latitude) as lat , avg(Longitude) as lon	 
                from nyc_wifi_hotspot_locations
                where Provider = %s
                group by Location 
                order by Location asc 
                """

        cursor.execute(query, (provider,))

        for row in cursor:
            result.append(Location(row['Location'], row['lat'], row['lon']))

        cursor.close()
        conn.close()
        return result

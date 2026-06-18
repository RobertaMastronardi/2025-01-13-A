from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction
from model.nodo import Node


class DAO():

    @staticmethod
    def get_all_localizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct c.Localization 
                        from classification c 
                        order by c.Localization desc
                        """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select i.*, g1.Chromosome as chr1, g2.Chromosome as chr2
                        from classification c1, classification c2, interactions i, genes g1, genes g2
                        where c1.Localization=c2.Localization and c1.Localization =%s and c1.GeneID =i.GeneID1 and c2.GeneID =i.GeneID2 
                        and c1.GeneID <>c2.GeneID and c1.GeneID =g1.GeneID and c2.GeneID =g2.GeneID 
                        group by i.GeneID1 , i.GeneID2 """
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append((row["GeneID1"],row["GeneID2"], row["chr1"], row["chr2"]))

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_nodes(localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select c.*, g.Essential 
                           from classification c, genes g 
                           where  c.GeneID =g.GeneID and c.Localization = %s
                           group by c.GeneID  """
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append(Node(row["GeneID"], row ["Localization"],row["Essential"]))

            cursor.close()
            cnx.close()
        return result

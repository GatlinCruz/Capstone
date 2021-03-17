from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from pathlib import Path


class App:

    def __init__(self, uri, username, pw):
        """
        The constructor for the App object
        :param uri: The uri that is being used
        :param username: The username that is used to gain access to the database
        :param pw: The password that is used to gain access to the database
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, pw))

    def close(self):
        """
        Cooses the driver object connection
        :return: None
        """
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        """
        Calls the static method _create_and_return_friendship to add nodes and their link
        :param person1_name: The first node
        :param person2_name: The second node
        :return: None
        """
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        """
        This method creates two nodes in the database and a link between them
        :param tx: The tx object used to run the command
        :param person1_name: The first node
        :param person2_name: The second node
        :return: The result from the call
        """
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:O]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        """
        Calls the static method _find_and_return_person to find a node
        :param person_name: The node that is being searched for
        :return: None
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        """
        Finds a node in the database if it exists
        :param tx: The tx object used to run the command
        :param person_name: The node that is being searched for
        :return: The node if it exists
        """
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]

    @staticmethod
    def _create_and_return_node(tx, node, graph_name):
        """
        Creates a node to the database
        :param tx: The tx object used to run the command
        :param node: The node object that's being added
        :return: The result from the function call
        """
        query = ("CREATE (p1:" + str(graph_name) + "{ name: $node }) RETURN p1")

        return tx.run(query, node=node, graph_name=graph_name).single()

    def create_node(self, person1_name, graph_name):
        """
        Calls the static method _create_and_return to add a single node
        :param graph_name: the name of the graph
        :param person1_name: The name of the node
        :return: The result from the function call
        """
        with self.driver.session() as session:
            return session.write_transaction(self._create_and_return_node, person1_name, graph_name)

    @staticmethod
    def _create_and_return_links_db(tx, node1, node2, graph_name):
        """
        Creates the links between the nodes
        :param tx: the object that runs the query
        :param node1: the starting node in the link
        :param node2: the ending node in the link
        :return: the result of the function call
        """

        return tx.run("MATCH (a:{}), (b:{}) WHERE a.name = '{}' AND b.name = '{}'CREATE (a)-[r:PORT]->(b)RETURN "
                      "type(r)".format(graph_name, graph_name, node1, node2))

    def create_links_db(self, node1, node2, graph_name):
        """
        Calls _create_and_return_links_db method
        :param graph_name: the name of the graph
        :param node1: the starting node in the link
        :param node2: the ending node in the link
        :return: the result of the function call
        """
        with self.driver.session() as session:
            return session.write_transaction(self._create_and_return_links_db, node1, node2, graph_name)

    def create_csv(self, filename):
        """
        Calls the static method _create_csv to export the csv file
        :param filename: The name of the file
        :return: The result from the function call
        """
        with self.driver.session() as session:
            return session.write_transaction(self._create_and_return_csv, filename)

    @staticmethod
    def _create_and_return_csv(tx, filename):
        """
        Creates the links between the nodes
        :param tx: the object that runs the query
        :param filename: the name of the file
        :return: the result of the function call
        """

        path = str(Path.home()) + "/Desktop/" + str(filename) + ".csv"
        return tx.run("CALL apoc.export.csv.all($path, {})", path=path).single()


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    bolt_url = "neo4j://localhost:7687"  # %%BOLT_URL_PLACEHOLDER%%
    user = "neo4j"
    password = "mininet"
    app = App(bolt_url, user, password)
    app.create_friendship("Alice", "David")
    app.find_person("Alice")
    app.close()

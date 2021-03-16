query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:O]->(p2) "
            "RETURN p1, p2"
        )
print(query)
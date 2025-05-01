# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "kuzu",
# ]
# ///
import kuzu

# Create an empty on-disk database and connect to it
db = kuzu.Database("./demo_db")
conn = kuzu.Connection(db)
# Create a graph with a node label and a property
try:
    conn.execute(
        """
        DROP TABLE IF EXISTS ActedIn;
        DROP TABLE IF EXISTS Movie;
        DROP TABLE IF EXISTS Person;
        CREATE NODE TABLE IF NOT EXISTS Movie (name STRING, PRIMARY KEY(name));
        CREATE NODE TABLE IF NOT EXISTS Person (name STRING, birthDate STRING, PRIMARY KEY(name));
        CREATE REL TABLE IF NOT EXISTS ActedIn (FROM Person TO Movie);
        CREATE (:Person {name: 'Al Pacino', birthDate: '1940-04-25'});
        CREATE (:Person {name: 'Robert De Nero', birthDate: '1943-08-17'});
        CREATE (:Movie {name: 'The Godfather: Part II'});
        MATCH (p:Person), (m:Movie) WHERE p.name = 'Al Pacino' AND m.name = 'The Godfather: Part II' CREATE (p)-[:ActedIn]->(m);
        MATCH (p:Person), (m:Movie) WHERE p.name = 'Robert De Nero' AND m.name = 'The Godfather: Part II' CREATE (p)-[:ActedIn]->(m);
        """
    )
except Exception as e:
    print(f"Error executing graph operations: {str(e)}")
# Execute Cypher query
response = conn.execute(
    """
    MATCH (a)
    RETURN a.name AS name 
    """
)
while response.has_next():
    print(response.get_next())
conn.close()
db.close()
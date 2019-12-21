from ariadne import ObjectType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

import pydgraph

# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql("""
    type Query {
        entities: [Entity]!,
        animals: [Animal]!,
        users: [User]!
    }

    type Mutate {
        createAnimal(id: ID!, 
        species: String!, 
        breed: [String!], 
        ownedBy: String!, 
        createdBy: String!): createAnimalResponse
    }

    type CreateAnimalResponse {
        status: Boolean!,
        error: Error,
        animal: Animal
    }

    type Animal {
        id: ID!, 
        species: String!, 
        breed: [String!], 
        ownedBy: Entity!, 
        createdBy: User!
    }

    type Entity {
        id: ID!,
        entityClassification: String!,
        companyName: String!
    }

    type User {
        id: ID!,
        phoneNumber: Int!
        firstName: String,
        lastName: String
    }
""")


# Creating dgraph schema, as-required, by pydgraph
client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)

def set_schema(client):
    schema = """
    id: [uid] @index(exact) .
    companyName: string .
    firstName: string .
    lastName: string .
    entityClassification: string .
    phoneNumber: int
    createdBy: [uid] @reverse .
    ownedBy: [uid] @reverse .
    entityId: [uid] @index(exact) .
    species: string .
    breed: string .

    type User {
        id
        firstName
        lastName
    }
    
    type Entity {
        id
        companyName
        entityClassification
    }

    type Animal {
        id
        species
        breed
        ownedBy
        createdBy
    }
    """
    return client.alter(pydgraph.Operation(schema=schema))




def resolve_createAnimal(_, info, animalType, ownedBy, createdBy):
    request = info.context["request"]
    txn = client.txn()

    try:

    
    user = auth.authenticate(username, password)
    if user:
        auth.login(request, user)
        return {"status": True, "user": user}
    return {"status": False, "error": "Invalid username or password"}

# Map resolver functions to Query fields using QueryType
query = QueryType()

# Resolvers are simple python functions
@query.field("people")
def resolve_people(*_):
    return [
        {"firstName": "John", "lastName": "Doe", "age": 21},
        {"firstName": "Bob", "lastName": "Boberson", "age": 24},
    ]


# Map resolver functions to custom type fields using ObjectType
person = ObjectType("Person")

@person.field("fullName")
def resolve_person_fullname(person, *_):
    return "%s %s" % (person["firstName"], person["lastName"])

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, query, person)

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema, debug=True)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/nounsdao/nouns-subgraph")

# Create the query string and variables required for the request.
query = """
    {
  nouns(first: 1000, orderBy: id) {
    id,
    owner,
    votes {
        proposal {
            id,
            proposer,
            targets,
            proposalThreshold,
            quorumVotes,
            forVotes,
            againstVotes,
            abstainVotes,
            description,
            status,
            votes

        },
        supportDetailed
    }
  }
}
"""
# Synchronous request
data = client.execute(query=query)

# For noun in data["data"]["nouns"] get each ['votes'] ['proposal'] and add them all to a list
proposals = []
for noun in data["data"]["nouns"]:
    for vote in noun["votes"]:
        proposals.append(vote["proposal"])
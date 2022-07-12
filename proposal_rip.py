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


proposals_df = pd.DataFrame(proposals)
# Replace all "\n" with " " in the description column
proposals_df["description"] = proposals_df["description"].str.replace("\n", " ")
# each row of ['proposer'] is a dictionary {'id':'...'}, so we need to just keep the 'id'
proposals_df["proposer"] = proposals_df["proposer"].apply(lambda x: x["id"])
# drop duplicates
proposals_df = proposals_df.loc[proposals_df.astype(str).drop_duplicates().index]


# Create a new dataframe then loop through all rows and for each row loop through all 'votes'
# Each vote that has a 'reason' we will append a new row to the new dataframe
# The new dataframe will have the columns 'proposal_id','quorumVotes','forVotes','againstVotes', 'abstainVotes','description','status','voter id','voter support','votes','reason'

reasons_df = pd.DataFrame()
for index, row in proposals_df.iterrows():
    for vote in row["votes"]:
        if vote["reason"] is not None:
            if vote['support']:
                # append using concat to add a new row to the dataframe into the correct columns saying "I support this proposal"
                reasons_df = pd.concat([reasons_df, pd.DataFrame([[row["id"], row["quorumVotes"], row["forVotes"], row["againstVotes"], row["abstainVotes"],"# Proposal: " + row["description"], row["status"], vote["id"], vote["support"], vote["votes"],"## I support this proposal: " + vote["reason"] + "## END"]])], ignore_index=True)
            else:
                # append using concat to add a new row to the dataframe into the correct columns saying "I do not support this proposal"
                reasons_df = pd.concat([reasons_df, pd.DataFrame([[row["id"], row["quorumVotes"], row["forVotes"], row["againstVotes"], row["abstainVotes"],"# Proposal: " + row["description"], row["status"], vote["id"], vote["support"], vote["votes"],"## I do not support this proposal: " + vote["reason"] + "## END"]])], ignore_index=True)

# rename the columns
reasons_df.columns = ['proposal_id','quorumVotes','forVotes','againstVotes', 'abstainVotes','description','status','voter id','voter support','votes','reason']



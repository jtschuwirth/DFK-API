import requests

graph_url = "https://api.defikingdoms.com/graphql"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

def getHeroes(address):
    query = """
        query($owner: String) {
            heroes(where: {
                owner: $owner
            }) {
                profession
                id
            }
        }
    """

    variables = {
        "owner": address
    }
    response = requests.post(graph_url, json={"query":query, "variables": variables}, headers=headers)
    return response.json()["data"]["heroes"]
    
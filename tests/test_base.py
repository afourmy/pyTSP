def test_pytsp(client):
    assert client.get('/').status_code == 200
    for algorithm in (
        'nearest_neighbor',
        'nearest_insertion',
        'farthest_insertion',
        'cheapest_insertion',
        'pairwise_exchange',
        'node_insertion',
        'edge_insertion',
        'ILP_solver'
    ):
        client.post('/' + algorithm)

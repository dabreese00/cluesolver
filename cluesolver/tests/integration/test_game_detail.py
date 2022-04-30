def test_nonexistent_game_returns_404(app, client):
    games_path = '/games'
    r = client.get(games_path + '/idontexist')
    assert r.status_code == 404

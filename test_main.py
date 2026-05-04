from fastapi.testclient import TestClient
import pytest
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def reset_database():
    main.games.clear()
    main.next_id = 1

def execute_graphql(query: str):
    return client.post("/graphql", json={"query":query})

def test_home():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message":"Games GraphQL API with Pydantic active!"}

def test_should_create_game_successfully():
    query = """
    mutation {
        createGame(game: {
            title: "Pokemon Pearl",
            genre: "RPG",
            completed: true
        }) {
            id
            title
            genre
            completed
        }
    }
    """
    
    response = execute_graphql(query)
    
    assert response.status_code == 200
    
    body = response.json()
    data = body["data"]["createGame"]
    
    assert data["id"] == 1
    assert data["title"] == "Pokemon Pearl"
    assert data["genre"] == "RPG"
    assert data["completed"] is True

def test_should_list_games():
    create_query = """
    mutation {
        createGame(game: {
            title: "Stardew Valley",
            genre: "Farm RPG",
            completed: false
        }) {
            id
        }
    }
    """
    
    execute_graphql(create_query)
    
    list_query = """
    query {
        allGames {
            id
            title
            genre
            completed
        }
    }
    """
    response = execute_graphql(list_query)

    assert response.status_code == 200
    
    data = response.json()["data"]["allGames"]
    
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Stardew Valley"
    assert data[0]["genre"] == "Farm RPG"
    assert data[0]["completed"] is False

def test_should_list_games():
    create_query = """
    mutation {
        createGame(game: {
            title: "Castlevania",
            genre: "Action",
            completed: true
        }) {
            id
        }
    }
    """
    
    execute_graphql(create_query)
    
    get_query = """
    query {
        gameById(gameId: 1) {
            id
            title
            genre
            completed
        }
    }
    """
    response = execute_graphql(get_query)

    assert response.status_code == 200
    
    data = response.json()["data"]["gameById"]
    

    assert data["id"] == 1
    assert data["title"] == "Castlevania"
    assert data["genre"] == "Action"
    assert data["completed"] is True

def test_should_list_games():
    query = """
    query {
        gameById(gameId: 999) {
            id
            title
            genre
            completed
        }
    }
    """
    response = execute_graphql(query)

    assert response.status_code == 200
    data = response.json()["data"]["gameById"] is None

def test_should_update_game_successfully():
    create_query = """
    mutation {
        createGame(game: {
            title: "Pokemon Diamond",
            genre: "RPG",
            completed: false
        }) {
            id
        }
    }
    """
    
    execute_graphql(create_query)
    
    update_query = """
    mutation {
        updateGame(
            gameId:1,
            game: {
                title: "Pokemon HeartGold",
                genre: "RPG",
                completed: true
        }) {
            id
            title
            genre
            completed
        }
    }
    """
    
    response = execute_graphql(update_query)
    
    assert response.status_code == 200
    
    data = response.json()["data"]["updateGame"]
    
    assert data["id"] == 1
    assert data["title"] == "Pokemon HeartGold"
    assert data["genre"] == "RPG"
    assert data["completed"] is True

def test_should_return_none_when_updating_game_that_does_not_exist():
    query = """
    mutation {
        updateGame(
            gameId:999,
            game: {
                title: "Pokemon HeartGold",
                genre: "RPG",
                completed: true
        }) {
            id
            title
            genre
            completed
        }
    }
    """
    
    response = execute_graphql(query)
    
    assert response.status_code == 200
    assert response.json()["data"]["updateGame"] is None

def test_should_delete_game_successfully():
    create_query = """
    mutation {
        createGame(game: {
            title: "Dungeon Meshi",
            genre: "Fantasy",
            completed: false
        }) {
            id
        }
    }
    """

    execute_graphql(create_query)

    delete_query = """
    mutation {
        deleteGame(gameId: 1)
    }
    """

    response = execute_graphql(delete_query)

    assert response.status_code == 200
    assert response.json()["data"]["deleteGame"] is True


def test_should_return_false_when_deleting_game_that_does_not_exist():
    query = """
    mutation {
        deleteGame(gameId: 999)
    }
    """

    response = execute_graphql(query)

    assert response.status_code == 200
    assert response.json()["data"]["deleteGame"] is False


def test_should_return_error_when_title_is_invalid():
    query = """
    mutation {
        createGame(game: {
            title: "A",
            genre: "RPG",
            completed: true
        }) {
            id
            title
            genre
            completed
        }
    }
    """

    response = execute_graphql(query)

    assert response.status_code == 200

    body = response.json()

    print(body)
    assert "errors" in body
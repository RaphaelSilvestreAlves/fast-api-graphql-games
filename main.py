from typing import Optional

import strawberry
from fastapi import FastAPI
from pydantic import BaseModel, Field
from strawberry.fastapi import GraphQLRouter

next_id = 1


class GameModel(BaseModel):
    id: int
    title: str = Field(..., min_length=1)
    genre: str = Field(..., min_length=1)
    completed: bool = False


games: list[GameModel] = []


@strawberry.type
class Game:
    id: int
    title: str
    genre: str
    completed: bool

@strawberry.input
class GameInput:
    title: str
    genre: str
    completed: bool = False


def to_graphql_game(game: GameModel) -> Game:
    return Game(
        id=game.id,
        title=game.title,
        genre=game.genre,
        completed=game.completed,
    )


@strawberry.type
class Query:
    @strawberry.field
    def all_games(self) -> list[Game]:
        return [to_graphql_game(game) for game in games]
    
    @strawberry.field
    def game_by_id(self, game_id: int) -> Optional[Game]:
        for game in games:
            if game.id == game_id:
                return to_graphql_game(game)
            
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_game(self, game: GameInput) -> Game:
        global next_id
        
        new_game = GameModel(
            id=next_id,
            title=game.title,
            genre=game.genre,
            completed=game.completed
        )
        
        games.append(new_game)
        next_id += 1
        
        return to_graphql_game(new_game)

    @strawberry.mutation
    def update_game(self, game_id: int, game: GameInput) -> Optional[Game]:
        for index, existing_game in enumerate(games):
            if existing_game.id == game_id:
                updated_game = GameModel(
                    id=existing_game.id,
                    title=game.title,
                    genre=game.genre,
                    completed=game.completed,
                )
                games[index] = updated_game
                
                return to_graphql_game(updated_game)
        
        return None
    
    @strawberry.mutation
    def delete_game(self, game_id: int) -> bool:
        for game in games:
            if game.id == game_id:
                games.remove(game)
                return True
        
        return False

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def home():
    return {"message":"Games GraphQL API active"}

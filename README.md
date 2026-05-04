# FastAPI GraphQL Games

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![GraphQL](https://img.shields.io/badge/GraphQL-Endpoint-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Strawberry](https://img.shields.io/badge/Strawberry-GraphQL-FF4785?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

A simple games API built with **FastAPI**, **GraphQL**, **Strawberry**, and **Pydantic**.

This project is meant to practice the main GraphQL concepts: `schema`, `type`, `query`, `mutation`, and `input`, using an in-memory list as storage.

## Project Idea

This API allows you to:

- create games
- list all games
- find a game by id
- update a game
- delete a game

Instead of creating several REST routes, this project uses a single GraphQL endpoint:

```txt
/graphql
```

Through this endpoint, the client chooses which operation to run and which fields should be returned.

## Technologies

- **FastAPI**: creates the web application.
- **Strawberry**: adds GraphQL support to Python.
- **GraphQL**: defines how the client queries and changes data.
- **Pydantic**: validates data before saving it in the application.
- **Pytest**: tests the API behavior.

## Main Concepts

### GraphQL

GraphQL is a way to build APIs where the client asks for exactly the data it needs.

In a REST API, there are usually several routes. In GraphQL, there is usually one main route, and the operation sent by the client defines what should happen.

### Schema

The schema is the API contract.

It defines which operations exist, which parameters they receive, and which type of data they return.

If something is not in the schema, the client cannot request it.

### Type

A `type` describes the shape of data that the API can return.

In this project, `Game` represents a game. It defines that a game has `id`, `title`, `genre`, and `completed`.

### Query

Query is used to read data.

In this project, the queries are:

- `allGames`: lists all games
- `gameById`: finds a game by id

A query should only read data, not change it.

### Mutation

Mutation is used to change data.

In this project, the mutations are:

- `createGame`: creates a game
- `updateGame`: updates a game
- `deleteGame`: deletes a game

A mutation is used when an operation creates, edits, or removes information.

### Input

Input defines the shape of data sent to a mutation.

In this project, `GameInput` defines the data required to create or update a game.

### Pydantic

Pydantic validates the internal application data.

In this project, `GameModel` makes sure that:

- `id` is an integer
- `title` has at least 2 characters
- `genre` has at least 2 characters
- `completed` is a boolean value

This means a game is validated before it is saved in the list.

## Installation

Create and activate a virtual environment, if you want:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install fastapi strawberry-graphql pydantic uvicorn pytest
```

## How to Run

Run:

```bash
uvicorn main:app --reload
```

Then open:

```txt
http://127.0.0.1:8000
```

GraphQL endpoint:

```txt
http://127.0.0.1:8000/graphql
```

## Quick Examples

Create a game:

```graphql
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
```

List games:

```graphql
query {
  allGames {
    id
    title
    genre
    completed
  }
}
```

Find by id:

```graphql
query {
  gameById(gameId: 1) {
    id
    title
    genre
    completed
  }
}
```

Update a game:

```graphql
mutation {
  updateGame(
    gameId: 1,
    game: {
      title: "Pokemon HeartGold",
      genre: "RPG",
      completed: true
    }
  ) {
    id
    title
    genre
    completed
  }
}
```

Delete a game:

```graphql
mutation {
  deleteGame(gameId: 1)
}
```

## How to Run the Tests

Run:

```bash
pytest
```

The tests check game creation, listing, search, update, deletion, and invalid data validation.

## Project Mental Model

```txt
Client
  |
  v
/graphql
  |
  v
Strawberry reads the query or mutation
  |
  v
Pydantic validates the data
  |
  v
The games list stores games in memory
  |
  v
GraphQL returns only the requested fields
```

## Note

The data is stored only in memory.

If the server restarts, the games list becomes empty again.

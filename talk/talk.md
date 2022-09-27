# My Project - Creating a Web Browsable database for Weightlifitng in New Zealand

---

## The Problem

- The results for Weightlifting in New Zealand are not web browsable.

- (What is Weightlifting?)

- Inspired by other sports in their statistics (e.g. Cricket) and ability to tell a story.

- Also inspired by Australia's Weightlifting website along with.

- Personal motivation: build a end-to-end project to learn, challenge myself, and showcase to future employers.

- Nerds lift heavy weights too.

---

## The Approach

- Basic CRUD

- REST API to a database

- Django Rest Framework + PostgreSQL

- React with Typescript and TailwindCSS

---

## The Architecture:

```

        PostgresSQL DB
              |
              |
           DRF API
             / \
            /   \
           /     \
        React   Wrapper

```

---

## The Backend

Django Rest Framework

urls.py -> views.py -> HTML template

urls.py (routers) -> views.py (viewset) -> serailizers.py -> json Data

models.py -> SQL -> PostgreSQL Database

ORM - Object Relational Mapper

---

## The Frontend

React Typescript TailwindCSS

API Endpoints -> React TS -> HTML | TailwindCSS

Important libraries:

- React Query
- React Table

---

## Problem #1

How to organise data?

Competition Model -> Session Model -> Lift Model
|
^
Athlete Model

Constraints:

- Competition has many sessions. Sessions can have many lifts.
- Only one session instance can be in one competition.
- An athlete's lift can only be in one session for one competition.

---

## Problem #2

How to validate lifts?

Rules:

1. A lift is a 'good lift', a 'no lift', or a 'did not attempt'.
2. An athlete attempts 3 lifts per lift type.
3. If the lift is a 'good lift', the next weight must be at least one kg greater.
4. If the lift is a 'no lift', the next weight can be the same.
5. If lift was not attempted, then the weight does not matter.

E.g.
Correct: +100 -105 +105
Incorrect: -100 +95 -

---

## Problem #3

How to come up with placings? - Complex

Placings can be determined by the lifts numbers and don't need to be inputted.

Rules:

1. The person with the highest total wins
2. If totals are equal, it's the person who gets to the total first
   a. smallest clean and jerk
   b. least lottery number

---

## Problem #4

Turning PDFs and Excel into form API can understand

Jupyter Notebooks -> (AWS Textract) -> pandas -> API Wrapper

---

## Wrapper for API

How to access data for some fun analytics!

---

## Putting it all together

Show the project!

---

## Challenges

- Fun
- Struggle
- Make an MVP!
- Am I doing it right?
  e.g. Lift model validation
  e.g. React code

---

## Future

- Present at a meetup
- Show to Weightliting New Zealand

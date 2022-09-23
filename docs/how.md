# How It Works

## Overview

The API consists of three models: `Athlete`, `Competition`, and `Lift`

## Determining the Junior/Youth/Senior

The API is able to determine if a athlete at the time of the competition date start if they are Youth, Junior and/or Senior.

## Design choices

### Female before Male ordering

Generally, competitions lift with female first following by males.

The subject of gender can be particularly sensitive. So a choice was made to detach gender from athletes, and instead

### Data Protection

The only data available is the athlete's name, birth year (to determine age grading) and their competitions lifts.

### Grading

Grading is determined by looking at the lifts for the current year and determining the best grade from these lifts.


## Roadmap

- Include volunteers on the competition results

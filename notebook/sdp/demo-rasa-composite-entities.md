## intent:affirm
- yes
- yep
- yeah
- indeed
- that's right
- ok
- great
- right, thank you
- correct
- great choice
- sounds really good

## intent:goodbye
- bye
- goodbye
- good bye
- stop
- end
- farewell
- Bye bye
- have a good one

## intent:greet
- hey
- howdy
- hey there
- hello
- hi
- good morning
- good evening
- dear sir

## intent:chitchat
- What's your name?
- What can I call you?
- How's the weather?
- Is it too hot outside?

## intent:book_flight
- i'm looking for a flight
- I want to book a flight
- i'm looking for a flight to [Berlin]{"entity": "location", "role": "to"}
- show me flights from [Amsterdam]{"entity": "location", "role": "from"}
- show me flights to [London]{"entity": "location", "role": "to"}
- i am looking for a flight from [SF]{"entity": "location", "value": "San Fransisco", "role": "from"} to [New York]{"entity": "location", "role": "to"}
- search for flights
- from [Madrid]{"entity": "location", "role": "from"} to [Munich]{"entity": "location", "role": "to"}
- any flight to [Liverpool]{"entity": "location", "role": "to"}

## intent:order_pizza
- i want a [large]{"entity": "size", "group": "1"} pizza with [tomato]{"entity": "topping", "group": "1"} and a [small]{"entity": "size", "group": "2"} pizza with [bacon]{"entity": "topping", "group": "2"}
- one [large]{"entity": "size", "group": "1"} with [pepperoni]{"entity": "topping", "group": "1"} and a [medium]{"entity": "size", "group": "2"} with [mushrooms]{"entity": "topping", "group": "2"}
- I would like a [medium]{"entity": "size", "group": "1"} standard pizza and a [medium]{"entity": "size", "group": "2"} pizza with [extra cheese]{"entity": "topping", "group": "2"}
- [large]{"entity": "size", "group": "1"} with [onions]{"entity": "topping", "group": "1"} and [small]{"entity": "size", "group": "2"} with [olives]{"entity": "topping", "group": "2"}
- a pizza with [onions]{"entity": "topping", "group": "1"} in [medium]{"entity": "size", "group": "1"} and one with [mushrooms]{"entity": "topping", "group": "2"} in [small]{"entity": "size", "group": "2"} please
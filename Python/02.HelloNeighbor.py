people = []
myself = {
    "name": "YourName",
    "city": "YourCity",
    "state": "YourState",
}
people.append(myself)
neighbor = {
    "name": "YourNeighborName",
    "city": "YourNeighborCity",
    "state": "YourNeighborState"
}
people.append(neighbor)

print("Hello")
for person in people:
    print(f"{person['name']} from {person['city']}, {person['state']}")
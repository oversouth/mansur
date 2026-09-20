from fastapi import FastAPI
app = FastAPI()
localdb: dict[str, dict[str, str]] = {}

@app.get("/HelloWorld")
def helloworld():
    return "Hello World"

@app.post("/new_user")
def new_user(info: dict):
    name = info.get("name")
    pwd = info.get("password")

    if not name or not pwd:
        return {"error": "name and password are required"}

    # Указан encoding='utf-8' для исправления предупреждения W1514
    with open(f"{name}.txt", "w", encoding="utf-8") as file:
        file.write(f"name {name}\npassword {pwd}")

    localdb[name] = {"name": name, "password": pwd}

    return {"message": "user created"}

@app.post("/whoami")
def whoami(info: dict):
    name = info.get("name")

    if not name:
        return {"error": "name is required"}

    userprofile = localdb.get(name)

    if userprofile:
        return userprofile

    return {"error": "user not found"}

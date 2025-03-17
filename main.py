from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import httpx
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

SECRET_KEY = os.getenv("SECRET_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")
MEDIA_URL = os.getenv("MEDIA_URL")

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session",
)



@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login route: Authenticates user and stores JWT token in Redis
@app.post("/login")
async def login(request: Request):
    print("Login endpoint reached")  # Add this line
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    print (f"I WILL CALL {BACKEND_URL}/token")
    # Send login credentials to external auth backend
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        # Extract JWT token from the response
        jwt_token = response.json()["access_token"]

        # Store JWT token in Redis
        request.session["auth_token"] = jwt_token  # Use username as key (you may choose a different key strategy)

        # Redirect to the clients page
        return RedirectResponse(url="/clients", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials. Try again."})


@app.get("/clients", response_class=HTMLResponse)
async def get_clients(request: Request):
    # Retrieve username from session to get the JWT token from Redis
    jwt_token = request.session.get("auth_token")
    if not jwt_token:
        return RedirectResponse(url="/login")

    # Use JWT token to fetch the user's clients from the backend
    headers = {"Authorization": f"Bearer {jwt_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/clients", headers=headers)

    # Process the clients data if the response is successful
    if response.status_code == 200:
        clients_data = response.json()
        return templates.TemplateResponse("clients.html", {"request": request, "clients": clients_data})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve clients data")


@app.get("/clients/{client_id}/orders", response_class=HTMLResponse)
async def get_client_orders(request: Request, client_id: str):
    # Retrieve JWT token from session
    jwt_token = request.session.get("auth_token")
    if not jwt_token:
        return RedirectResponse(url="/login")

    # Use JWT token to fetch the client's orders from the backend
    headers = {"Authorization": f"Bearer {jwt_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/clients/{client_id}/orders", headers=headers)

    # Process the orders data if the response is successful
    if response.status_code == 200:
        orders_data = response.json()
        return templates.TemplateResponse("client_orders.html", {"request": request, "orders": orders_data, "media_url": MEDIA_URL})
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve orders data")


@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})
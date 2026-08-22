from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")

    if request.url.path.startswith("/product"):
        if not token:
            return RedirectResponse("/login")

    response = await call_next(request)

    return response

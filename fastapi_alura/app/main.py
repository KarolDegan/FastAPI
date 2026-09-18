from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from rotas.cliente import router as clientes_router

app = FastAPI(
    title="Techlog Solutions API",
    description="CRM para Techlog Solutions",
    version="1.0.0",
)

app.include_router(clientes_router)

#usando somente um decorador do FastAPI, podemos fazer com que uma determinada função seja acessível pela rede
@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.get("/front", response_class=HTMLResponse)
async def front_page():
    html_content = """
        <html>
            <head>
                <title>Techlog Solutions</title>
            </head>
            <body>
                <h1>🔪 Techlog Solutions</h1>
                <p>Sistema de Gestão de Ordens de Serviço</p>
                <p>Status: <strong>Operacional</strong></p>
            </body>
        </html>
    """
    return html_content
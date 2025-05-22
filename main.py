from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from algo import floyd_warshall, ShortestPathResult

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def is_infinite(value):
    try:
        return value == float('inf')
    except Exception:
        return False

templates.env.tests['infinite'] = is_infinite

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("path_form.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request, graph_data: str = Form(...)):
    try:
        graph = {}
        rows = graph_data.strip().splitlines()
        for i, row in enumerate(rows):
            cols = row.split()
            graph[str(i)] = {}
            for j in range(len(cols)):
                value = cols[j].strip()
                if value == "999":
                    graph[str(i)][str(j)] = float('inf')
                else:
                    graph[str(i)][str(j)] = float(value)

        result: ShortestPathResult = floyd_warshall(graph)
        return templates.TemplateResponse(
            "path_result.html",
            {"request": request, "result": result}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": f"Ошибка обработки: {e}"}
        )
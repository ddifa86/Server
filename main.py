from fastapi import FastAPI
from routers.HoldAPI import router as hold_router
from routers.UserAPI import router as user_router

from routers.CragAPI import router as crag_router
from routers.RouteAPI import router as route_router
from routers.RouteHoldAPI import router as routehold_router

from routers.ClimbingDetailAPI import router as ClimbingDetail_router
from routers.ClimbingHistoryAPI import router as Climbing_router


app = FastAPI() 

app.include_router(hold_router)
app.include_router(user_router)

app.include_router(crag_router)
app.include_router(route_router)
app.include_router(routehold_router)
app.include_router(ClimbingDetail_router)
app.include_router(Climbing_router)

 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
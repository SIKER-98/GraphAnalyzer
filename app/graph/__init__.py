def register_routes(app):
    from .controller import router as graph_router

    app.include_router(graph_router)
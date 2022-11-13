def register_routes(app):
    from .controller import router as node_router

    app.include_router(node_router)

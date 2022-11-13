def register_routes(app):
    from .controller import router as relations_router

    app.include_router(relations_router)

def register_routes(app):
    from .controller import router as user_router
    app.include_router(user_router)


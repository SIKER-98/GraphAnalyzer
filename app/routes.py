def register_routes(app):
    from .users import register_routes as attach_user
    from .graph import register_routes as attach_graph
    from .nodes import register_routes as attach_nodes
    from .relations import register_routes as attach_relations

    # add routes
    attach_user(app)
    attach_graph(app)
    attach_nodes(app)
    attach_relations(app)

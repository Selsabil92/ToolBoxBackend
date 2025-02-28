# Gestion des erreurs et sécurité 
def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Not Found"}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {"message": "Internal Server Error"}, 500

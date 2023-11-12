from quart import Quart, render_template, request, redirect, url_for, session
from quart_schema import QuartSchema
from api.project import project_blue
from api.tags import tag_blue



app = Quart(__name__)
app.register_blueprint(project_blue)
app.register_blueprint(tag_blue)
QuartSchema(app)

if __name__ == '__main__':
    app.run(debug=True)
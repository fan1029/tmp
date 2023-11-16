from quart import Quart, render_template, request, redirect, url_for, session, Response
from quart_schema import QuartSchema
from api.project import project_blue
from api.tags import tag_blue
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin='*')
app.register_blueprint(project_blue)
app.register_blueprint(tag_blue)
QuartSchema(app)


@app.before_request
async def handle_options():
    if request.method == 'OPTIONS':
        return Response(status=200)


# 解决跨域问题


if __name__ == '__main__':
    from plugins import importPlugins
    importPlugins()
    app.run( port=5000, debug=True)

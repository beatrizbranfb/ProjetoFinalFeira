from bottle import Bottle, template, request
import socketio


class Application:

    def __init__(self):
        self.pages = {
            'index': self.helper,
            'products': self.products,
        }

        self.app = Bottle()
        self.sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
        self.setup_websocket_events()

        self.wsgi_app = socketio.WSGIApp(self.sio, self.app)


    def render_page(self, template_name, **kwargs):
        kwargs['user_id'] = request.session.get('user_id')
        kwargs['is_admin'] = request.session.get('role') == 'admin'
        return template(template_name, **kwargs)

    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()

    def helper(self):
        return template('app/views/index.html')

    def products(self):
        return template('app/views/cliente_produto.html')

    def setup_websocket_events(self):
        @self.sio.event
        async def connect(sid, environ):
            print(f"Cliente Conectado: {sid}")
            self.sio.emit('connected', {'data': 'Connected'}, room=sid)

        @self.sio.event
        async def disconnect(sid):
            print(f"Cliente Desconectado: {sid}")

        
    def emit_product_update(self, product_data):
        print(f"Emitindo atualização de produto: {product_data}")
        self.sio.emit('product_update', product_data)

    def emit_order_update(self, order_data):
        print(f"Emitindo atualização de pedido: {order_data}")
        self.sio.emit('order_status_update', order_data)

app_renderer = Application()

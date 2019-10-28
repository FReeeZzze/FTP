from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

authorizer = DummyAuthorizer()

authorizer.add_user('freeezzz', 'qwerty', 'ftp', perm='elradfmwMT')
authorizer.add_user("user", "12345", "ftp", perm="elradfmw")
authorizer.add_user('anonymous', '', 'ftp', perm="elr", msg_login="Login successful.", msg_quit="Goodbye.")
handler = FTPHandler
handler.log_prefix = '@ [%(username)s] IP: %(remote_ip)s:%(remote_port)s'
handler.authorizer = authorizer
#address = ("127.0.0.1", 21)
address = ('0.0.0.0', 21)
ftpd = FTPServer(address, handler)
ftpd.serve_forever()


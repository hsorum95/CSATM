from pytm.pytm import TM, Server, Datastore, Dataflow, Boundary, Actor, Data, Classification

tm = TM("Simple threat model")
tm.description = "a simple threat model of a website serving static content"
Web_User = Boundary("Web/User trust boundary")
user = Actor("Web user")
web = Server("Web Server")
web.OS = "CentOS"
web.isHardened = True
web.inBoundary = Web_User

user_to_web = Dataflow(user, web, "Get Request")
web_to_user = Dataflow(web, user, "Sends HTML-file")
tm.process()
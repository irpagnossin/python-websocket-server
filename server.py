from websocket_server import WebsocketServer
import json

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    msg = json.loads(message)

    incoming_action = str(msg['action'])

    if incoming_action == 'USER_SAYS':
        server.send_message_to_all(message)

    elif incoming_action == "SIGN_IN":

        new_user = {
            'username': str(msg['user']),
            'room': str(msg['room'])
        }

        outgoing_socket_message = {
            'action': "USER_IN",
            'message': str(msg['message']),
            'room': str(msg['room']),
            'user': str(msg['user'])
        }
        print "avisando outros: %s" % json.dumps(outgoing_socket_message)
        server.send_message_to_all(json.dumps(outgoing_socket_message))



    elif incoming_action == "SIGN_OUT":

        outgoing_socket_message = {
            'action': "USER_OUT",
            'message': "",
            'room': msg['room'],
            'user': msg['user']
        }

        server.send_message_to_all(json.dumps(outgoing_socket_message))
        client_left(client, server)

        print json.dumps(outgoing_socket_message)

    elif incoming_action == "REQUEST_USERS":

        outgoing_socket_message = {
            'action': "ALL_USERS",
            'message': 'user1,user2,user3',
            'room': "",
            'user': ""
        }
        print "Informando usuarios existentes: %s" % json.dumps(outgoing_socket_message)
        server.send_message(client, json.dumps(outgoing_socket_message))
        pass

    else:
        print "I don't know what you mean!"

    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

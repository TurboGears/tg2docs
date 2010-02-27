.. _realtimeintro:

Real-time TurboGears Introduction
=================================

This tutorial will describe how to set up an introductory "real time chat"
application using the `Orbited`_ framework and TurboGears.  Real-time
web-sites are capable of far more than simple chat applications, but
chat is the common "Hello World" of real-time developers.

.. warning::

    You should already be fairly familiar with TurboGears, Javascript and
    JQuery before you begin this tutorial.

.. note::

    The setup described here is *not* a production-ready real-time-web
    solution. MorbidQ is not a production Message Queue Server, and indeed
    most production solutions would want to use a more robust and efficient
    protocol such as AMQP.  Currently AMQP protocols for Javascript are
    "in development".  This document is intended to let you get started
    with real-time-web development before you graduate to more mature
    technologies.

Setup
-----

You will need to have a running TurboGears :ref:`virtualenv` to follow along
in this tutorial.  We recommend the :ref:`downloadinstall` if possible.

Architectural Overview
~~~~~~~~~~~~~~~~~~~~~~

* `Orbited`_ -- a server process which provides "web socket proxying" support
  as well as Javascript client-side implementations for supported
  protocols.
* `MorbidQ`_ -- a simple (non-scalable) STOMP message queue for developers,
  its primary advantage is that the message queue is built into the Orbited
  server, so a simple config setting will enable and configure it
* TurboGears -- serves the HTML widget which references the Orbited Javascript.
  TurboGears does not connect to the MorbidQ service in this project, but
  sending STOMP messages to the server *can* be implemented.

Software Install
~~~~~~~~~~~~~~~~

Orbited provides a "web socket" mechanism that allows Javascript code
to connect to (defined) servers to recieve messages.  The networking
protocol spoken by the Javascript code can be any implemented TCP protocol.
The following are the protocols *commonly* used with Orbited:

* `STOMP`_, a simple streaming text format we will use here
* `XMPP`_, such as spoken by jabberd
* `IRC`_, an older protocol for internet chat

Orbited's model means that with a simple Javascript plugin which speaks a
given protocol, your Javascript code can be connected to any server and
port on the Internet (with the proper Orbited configuration).

To install the Orbited framework in your VirtualEnv we need to install the
Orbited 0.7.10+ and `Twisted`_ 9.0+ packages.  This will also pull in the
morbidq package.

.. code-block:: bash

    (tgenv)$ easy_install twisted orbited

MorbidQ
~~~~~~~

MorbidQ provides an easily configured message broker/queue which is not intended
for large-scale production use. It uses the simple STOMP protocol.
If you want to stick with STOMP as you scale up, you can explore the
`other STOMP servers available`_.

.. note::

    There are (far) faster message queue engines than Morbid, but most of them use
    the AMQP binary protocol.  There is an experimental AMQP implementation for
    Javascript available in `Kamaloka-js`_.  It is suggested that you become
    comfortable with real-time-web programming before switching to a full-featured
    Queue server.

To configure MorbidQ and Orbited, you need a config file.  Something like the
following, which we will save as "chat.ini" in our "rtchat" project's
directory.

.. code-block:: ini

    [listen]
    # this is the server which provides the socket-proxy for javascript
    http://:9000
    # the following enables the MorbidQ STOMP Message Queue
    stomp://:61613

    [access]
    # allow incoming HTTP requests on port 9000 to connect to
    # localhost:61613 (i.e. the MorbidQ STOMP server)
    # The * refers to the
    * -> localhost:61613

    [global]
    session.ping_interval = 20

You can now run Orbited with the embedded MorbidQ queue with the following
command:

.. code-block:: ini

    (tg2env)$ orbited --config=chat.ini

You should see messages telling you that Orbited/MorbidQ is listening on the
defined ports.  You can hit CTRL-C to stop the server, though we'll want to
use it in a moment, so you'll likely want to leave it running and start
another console.

Chat View (HTML)
----------------

We are going to be very simplistic with our chat widget in our first attempt.
We'll simply dump the text which is sent to the server into a div node.  The
view looks like this:

.. code-block:: html

    <?python
    # we pull some values out of TurboGears config-file, with defaults
    # for our tutorial settings.
    from simplejson import dumps as d
    orbited_server = config.get( 'orbited_server', 'localhost' )
    orbited_port = config.get( 'orbited_port', 9000 )
    stomp_server = config.get( 'stomp_server', 'localhost' )
    stomp_port = config.get( 'stomp_port', 61613 )
    orbited_files = 'http://%s:%s/static'%( orbited_server, orbited_port )
    ?>
      <div id="chat">
        <h2>Real-time Chat</h2>
        <div class="chat-trace">
        </div>
        <div class="chat-entry">
            Chat:
            <input class="chatter" />
            <button class="chat-trigger">Send</button>
        </div>
      </div>

Orbited/STOMP Javascript Setup
------------------------------

We are going to use JQuery for our javascript framework.  Here we use the
Google javascript APIs version of the library:

.. code-block:: html

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>

The JSON javascript library provides for safe JSON parsing, that is, it
actually parses the JSON data rather than doing an unsafe "eval" on the
code.  We linked it into our "public" directory above.

.. code-block:: html

    <script type="text/javascript" src="${orbited_files}/JSON.js"></script>

The Orbited javascript library implements the "proxied socket" mechanism
which connects to the Orbited server we started above.  We'll use Orbited's
proxy-socket to connect to the MorbidQ server via STOMP.  We configure the
Orbited client *before* we import the STOMP client library as the STOMP
client library references "TCPSocket" as seen here.

.. code-block:: html

    <script type="text/javascript" src="${orbited_files}/Orbited.js"></script>
    <script type="text/javascript">
        // This line is required to allow our chat server and this
        // page to operate on different ports...
        document.domain = document.domain;
        // Establish the port and server for the Orbited server
        Orbited.settings.port = 9000;
        Orbited.settings.hostname = ${simplejson.dumps( chat_server )};
        // Enable streaming operation
        Orbited.settings.streaming = true;
        // This object is referenced by stomp.js
        TCPSocket = Orbited.TCPSocket;
    </script>
    <script type="text/javascript" src="${orbited_files}/protocols/stomp/stomp.js"></script>

The Chat Client
----------------

The chat client we show here is extremely simplistic.  It is intended to show
you the minimum required to get messages flowing across the MorbidQ server.

.. code-block:: html

    <script type="text/javascript">
        var add_message = function( text ) {
            var node = $('<div class="chat-message"></div>');
            node.append( text );
            $('.chat-trace').append( node );
        };
        $(document).ready( function() {
            stomp = new STOMPClient();
            stomp.onconnectedframe = function(frame) {
                stomp.subscribe( "/topic/chat" );
            };
            stomp.onmessageframe = function( frame ) {
                add_message( frame.body );
            };
            stomp.connect(${d(stomp_server)},${d(stomp_port)} );
            $('.chat-entry .chat-trigger').click( function() {
                var chatter = $('.chat-entry .chatter');
                var value = chatter.attr( 'value' );
                if (value.length) {
                    stomp.send( value, "/topic/chat" );
                    chatter.attr( 'value', '' );
                }
            });
        });
    </script>

Testing and Revision
---------------------

You should now be able to start your TurboGears server, browse to
http://localhost:8080 and start chatting.  Your messages should show up
in the chat-trace DIV as you enter them.

You will immediately notice problems with the chat system, some obvious
enhancements:

* messages should include the user's chosen nickname
* the "enter" key should be hooked to send chat messages
* it would be nice to log the messages on the server
* you would normally use JSON.stringify() and JSON.parse() to send JSON
  structured messages
* you *likely* want to implement *some* form of security

There are a number of callbacks of the STOMP object that you may wish to
override to perform basic configuration and the like:

* stomp.onopen( ) -- called on initialization of the STOMP connection
* stomp.onclose( code ) -- connection was lost with an error-code
  describing the reason
* stomp.onerrorframe( frame ) -- error-describing frame was recieved
  * frame.body contains the payload
* stomp.onconnectframe( frame ) -- called when the connection to the server
  has been set up
* stomp.onmessageframe( frame ) -- a (normal) message was received from
  the server, frame.body is normally a JSON payload, but can be whatever
  the sender has put into the body

The methods to control the STOMP object are:

* stomp.reset( ) -- force the STOMP connection to reset/reconnect
* stomp.connect( server, port ) -- connect to the given address
* stomp.send( payload, channel ) -- send the given payload to the
  given channel
* stomp.subscribe( channel ) -- subscribe to messages sent to a given
  channel (onmessageframe( frame) will begin getting called).

What's Next?
------------

.. toctree::
   :maxdepth: 1

   moksha

.. note::

    The code on this page is loosely based on `Django, Orbited, Stomp and Co.`_

.. _`Kamaloka-js`: https://fedorahosted.org/kamaloka-js/
.. _`other STOMP servers available`: http://www.morbidq.com/
.. _`Orbited`: http://orbited.org/
.. _`MorbidQ`: http://www.morbidq.com/
.. _`STOMP`: http://stomp.codehaus.org/
.. _`XMPP`: http://xmpp.org/
.. _`IRC`: http://en.wikipedia.org/wiki/Internet_Relay_Chat
.. _`Twisted`: http://www.twistedmatrix.com/
.. _`Django, Orbited, Stomp and Co.`: http://mischneider.net/?p=125

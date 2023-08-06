# imports?
import inspect
import hashlib
import pprint
import sys
import traceback
import os
import lzma
import base64

try:
    import dill as pickle

except ModuleNotFoundError:
    import pickle

def test():
    """just needed to test that the program is running"""
    print("Hello... World?")

class subscriber:
    """Subscriber object for pubsub"""
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback
        self.sid = topic + chr(0) + hashlib.md5(pickle.dumps(callback)).hexdigest()

class pubsub:
    """Publish/Subscribe model"""
    def __init__(self):
        # cache of listeners
        self.cache = {}

    def publish(self, topic, args=[], kwargs={}, cache=None):
        """Publish to a channel, run all callbacks listed with args and kwargs as list/dict. Returns a list of return values, newest subbed to oldest."""
        # Slashes are tiered, e.g subscribing to foo/bar/baz will callback when foo or foo/bar or foo/bar/baz are published.

        try:
            # retrieve listeners
            subs = self.cache[topic]

        except KeyError:
            return

        returns = []
        for subber in subs:
            # callback listeners
            returns.append(subber.callback(*args, **kwargs))

        return returns

    def subscribe(self, topic, callback):
        """Subscribe to a topic"""

        try:
            # retrieve listeners
            subs = self.cache[topic]

        except KeyError:
            self.cache[topic] = []
            subs = self.cache[topic]

        subber = subscriber(topic, callback)
        subs.insert(0, subber)
        return subber.sid

    def unsubscribe(self, sid):
        """Unsubscribe to topic with SID generated from crutil.pubsub().subscribe()"""
        # split into topic/callback hash
        sidl = sid.split(chr(0))

        try:
            # retrieve listeners
            subs = self.cache[sidl[0]]

        except KeyError:
            raise KeyError("Topic of unsubscribed callback not found")

        # unsubscribe stuff
        for i, subber in enumerate(subs):
            if subber.sid == sid:
                del self.cache[sidl[0]][i]
                break

    def clear(self):
        """say bye bye to your cache"""
        self.cache = {} # bye bye

    def view(self):
        """PPrints the cache tree"""
        pprint.pprint(self.cache, indent=4)

def find_args(func):
    """Attempt to list all arguments of a callable function"""
    try:
        return list(
            map(
                str,
                str(
                    inspect.signature(
                        func
                    )
                )[1:-1].split(
                    ", "
                )
            )
        )

    except ValueError:
        # couldn't find signature
        return None

class recursion:
    """
    A recursion context manager.
    Be careful when using this, settings a recursionlimit
    too high can literally crash python. To use, do
    with crutil.recursion(69420):
        print("lalala")

    Warning, you can cause Python to segfault if recursion limit
    is set too high.
    """
    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)

class Defer(object):
    """Defers functions to the end of a function/context manager."""
    def __init__(self, f=None):
        self.tb = traceback

        if f == None:
            self.exits, self.args, self.kwargs = [], [], []

        elif callable(f):
            self.function = f

        else:
            raise TypeError("Defer requires a function")

    def __call__(self, *args, **kwargs):

        import sys

        exits, aargs, akwargs = [], [], []

        def ddefer(f, *args, **kwargs):
            if callable(f):
                exits.append(f)
                aargs.append(args)
                akwargs.append(kwargs)

            else:
                raise TypeError(f"Object {f} cannot be deferred.")

        err = False
        try:
            out = self.function(defer=ddefer, *args, **kwargs)

        except:
           sys.stderr.write(self.tb.format_exc())
           err = True

        for i in range(0, len(exits)):
            exits[i](*aargs[i], **(akwargs[i]))

        if err:
            sys.exit()

    def __enter__(self):
        return self.fdefer

    def fdefer(self, f, *args, **kwargs):
        if callable(f):
            self.exits.append(f)
            self.args.append(args)
            self.kwargs.append(kwargs)

        else:
            raise TypeError(f"Object {f} cannot be deferred.")

    def __exit__(self, type, value, traceback):
        trace = self.tb.format_exc()
        err = False

        if not trace.startswith("None"):
            sys.stderr.write(self.tb.format_exc())
            err = True

        temp = self.exits[::-1]
        for i in range(0, len(temp)):
            try:
                args, kwargs, curf = self.args[i], self.kwargs[i], temp[i]

                if args:
                    if kwargs:
                        curf(*args, **kwargs)

                    else:
                        curf(*args)

                else:
                    if kwargs:
                        curf(**kwargs)

                    else:
                        curf()

            except:
                sys.stderr.write(self.tb.format_exc())
                err = True

        if err:
            sys.exit()

class suppress:
    """Suppress messages being printed from stdout or stdeerr in this context manager."""
    def __init__(self):
        self.old_stderr = sys.stderr

    def __enter__(self, err=False):
        self.old_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

        if not err:
            self.old_stderr = sys.stderr
            sys.stderr = open(os.devnull, "w")

    def __exit__(self, type, value, tb):
        sys.stdout.close()
        sys.stdout = self.old_stdout

        sys.stderr.close()
        sys.stderr = self.old_stderr

def blob(inf, outf="blob.py"):
    """Blobify files into a python file for easy pyinstallering and stuff"""
    with open(inf, "rb") as f:
        with open(outf, "w") as g:
            g.write(
                "import lzma,base64;data=lzma.decompress(base64.a85decode(\""
                + base64.a85encode(
                    lzma.compress(
                        f.read()
                    )
                ).decode(
                    "utf"
                ).replace(
                    "\\",
                    "{"
                ).replace(
                    "\"",
                    "}"
                )
                + "\".replace(\"{\", \"\\\\\").replace(\"}\", \"\\\"\").encode(\"utf\")))\n"
                + """def unblob(outf):
\tglobal data
\twith open(outf, "wb") as f:
\t\tf.write(data)"""
            )

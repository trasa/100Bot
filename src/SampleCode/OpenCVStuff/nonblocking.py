
import Queue
import time
import threading
import weakref

def nonblocking(f, blocking_return=None, sleep_time=0.01):
  """
  Wrap a callable which returns an iter so that it no longer blocks.

  The wrapped iterator returns blocking_return while callable f is
  blocking.  The callable f is called in a background thread.  If the
  wrapped iterator is deleted, then the iterator returned by f is
  deleted also and the background thread is terminated.
  """
  def g(*args, **kwargs):
    f_iter = f(*args, **kwargs)
    g_iter = None
    def run():
      while True:
        g_obj = g_iter()
        if g_obj is None:
          return
        if g_obj.q.qsize() == 0:
          try:
            f_next = f_iter.next()
          except Exception, e:
            g_obj.exc = e
            return
          g_obj.q.put(f_next)
        else:
          del g_obj
          time.sleep(sleep_time)
    class Iter:
      def __init__(self):
        self.q = Queue.Queue()
        self.exc = None
        self.thread = threading.Thread(target=run)
        self.thread.setDaemon(True)
      def next(self):
        if self.exc is not None:
          raise self.exc
        try:
          return self.q.get_nowait()
        except Queue.Empty:
          return blocking_return
      def __iter__(self):
        return self

    obj = Iter()
    g_iter = weakref.ref(obj)
    obj.thread.start()
    try:
      return obj
    finally:
      del obj
  return g

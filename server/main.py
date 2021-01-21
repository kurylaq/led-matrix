import time
from connection_manager import ConnectionManagerProcess
from multiprocessing import Pipe

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = ConnectionManagerProcess(child_conn)
    try:
        p.start()

        time.sleep(4)
        parent_conn.send(("not that", ))
        # parent_conn.send(("stop", ))

        p.join()

    except KeyboardInterrupt:
        # parent_conn.send(("stop", ))
        parent_conn.close()

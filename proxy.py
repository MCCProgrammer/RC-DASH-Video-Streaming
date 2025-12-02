import sys
import threading
import queue
import requests
import socket


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 proxy.py baseURL movieName track")
        sys.exit(1)

    base_url = sys.argv[1].rstrip('/')
    movie_name = sys.argv[2]
    try:
        track_num = int(sys.argv[3])
    except ValueError:
        print("track must be an integer")
        sys.exit(2)

    manifest_url = f"{base_url}/{movie_name}/manifest.txt"
    try:
        resp = requests.get(manifest_url)
        resp.raise_for_status()
        manifest = resp.text.splitlines()
    except Exception as e:
        print(f"Error downloading/parsing manifest.txt: {e}")
        sys.exit(3)

    num_tracks = int(manifest[1])
    if not (0 <= track_num < num_tracks):
        print(f"Invalid track number: {track_num}")
        sys.exit(4)

    i = 2
    for t in range(track_num):
        seg_count = int(manifest[i+4])
        i += 5 + seg_count
    file_name = manifest[i]
    seg_count = int(manifest[i+4])
    segments = []
    for j in range(seg_count):
        offset, nbytes = manifest[i+5+j].split()
        segments.append((int(offset), int(nbytes)))
    track_url = f"{base_url}/{movie_name}/{file_name}"

    sock = socket.socket()
    print("Connecting to player at localhost:8000...")
    sock.connect(('127.0.0.1', 8000))
    print("Connected to player.")
    conn_file = sock.makefile('wb')

    buf_q = queue.Queue(maxsize=10)

    def producer():
        try:
            for offset, nbytes in segments:
                headers = {'Range': f'bytes={offset}-{offset + nbytes - 1}'}
                resp = requests.get(track_url, headers=headers)
                resp.raise_for_status()
                buf_q.put(resp.content)
        finally:
            buf_q.put(None) 

    def consumer():
        try:
            while True:
                chunk = buf_q.get()
                if chunk is None:
                    break
                conn_file.write(chunk)
                conn_file.flush()
        finally:
            try:
                conn_file.close()
            except:
                pass

    prod_thread = threading.Thread(target=producer)
    cons_thread = threading.Thread(target=consumer)
    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()
    sock.close()
    print("Done streaming.")

if __name__ == "__main__":
    main()

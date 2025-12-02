import sys
import requests
import time


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 programB.py serverURL movieName resultsFileName")
        sys.exit(1)

    server_url = sys.argv[1].rstrip('/')
    movie_name = sys.argv[2]
    results_filename = sys.argv[3]

    manifest_url = f"{server_url}/{movie_name}/manifest.txt"
    try:
        resp = requests.get(manifest_url)
        resp.raise_for_status()
        manifest = resp.text.splitlines()
    except Exception as e:
        print(f"Error downloading/parsing manifest.txt: {e}")
        sys.exit(2)

    if len(manifest) < 2:
        print("Malformed manifest.txt")
        sys.exit(3)

    num_tracks = int(manifest[1])
    i = 2
    results = []
    for t in range(num_tracks):
        file_name = manifest[i]
        codec = manifest[i+1] 
        bit_rate = manifest[i+2]
        duration = manifest[i+3]
        seg_count = int(manifest[i+4])
        segments = []
        for j in range(seg_count):
            offset, nbytes = manifest[i+5+j].split()
            segments.append( (int(offset), int(nbytes)) )

        with open(file_name, 'wb'):
            pass  

        track_url = f"{server_url}/{movie_name}/{file_name}"
        start_time = time.time()
        total_bytes = 0
        for seg_num, (offset, nbytes) in enumerate(segments):
            print(f"Downloading: Track {t}, Segment {seg_num+1}/{seg_count}, Offset {offset}, Size {nbytes}")
            range_header = {'Range': f'bytes={offset}-{offset + nbytes - 1}'}
            try:
                seg_resp = requests.get(track_url, headers=range_header)
                seg_resp.raise_for_status()
                total_bytes += len(seg_resp.content)
                with open(file_name, 'ab') as out_file:
                    out_file.write(seg_resp.content)
            except Exception as e:
                print(f"Error downloading segment offset={offset} len={nbytes}: {e}")
                sys.exit(4)
        elapsed = time.time() - start_time
        rate = total_bytes / elapsed if elapsed > 0 else 0
        print(f"Track {t}: elapsed time = {elapsed:.2f}s, download rate = {rate:.2f} bytes/s")
        results.append((elapsed, rate))
        i += 5 + seg_count

    with open(results_filename, 'w') as f:
        for tup in results:
            f.write(f"{tup[0]}\n{tup[1]}\n")

if __name__ == "__main__":
    main()

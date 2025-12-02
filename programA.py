import sys
import requests

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 programA.py serverURL movieName resultsFileName")
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
    sizes = []
    num_segments = 0
    i = 2
    for t in range(num_tracks):
        file_name = manifest[i]
        codec = manifest[i+1]
        bit_rate = manifest[i+2]
        duration = manifest[i+3]
        seg_count = int(manifest[i+4])
        if t == 0:
            num_segments = seg_count
        segment_sizes = [int(manifest[i+5+j].split()[1]) for j in range(seg_count)]
        total_size = sum(segment_sizes)
        sizes.append(total_size)
        i += 5 + seg_count

    with open(results_filename, 'w') as f:
        f.write(f"{num_tracks}\n")
        f.write(f"{num_segments}\n")
        for s in sizes:
            f.write(f"{s}\n")

if __name__ == "__main__":
    main()

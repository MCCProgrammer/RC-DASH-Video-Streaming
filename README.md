# 🎬 DASH Video Streaming — Computer Networks

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-1f2328?style=flat-square&logo=python&logoColor=white">
  <img alt="Course" src="https://img.shields.io/badge/Course-Computer%20Networks%20(RC)-1f2328?style=flat-square">
  <img alt="Year" src="https://img.shields.io/badge/2025%2F26-3rd%20year%2C%201st%20semester-1f2328?style=flat-square">
</p>

Assignment 4 of *Redes de Computadores* (Computer Networks), Computer Science degree at **NOVA School of Science and Technology (FCT NOVA)**.

## About

Video streaming over HTTP with **DASH** (Dynamic Adaptive Streaming over HTTP), where each movie is stored in several **tracks** of different quality, split into segments described by a `manifest.txt`.

- **`programA.py`** — reads a movie's manifest and works out the number of tracks, segments and total size of each track.
- **`programB.py`** — downloads every track segment by segment using **HTTP partial requests** (`Range` headers) and measures the download time and throughput of each.
- **`proxy.py`** — sits between a content server and a video player: it fetches the segments of the chosen track with range requests in a **producer thread**, queues them, and streams them to the player over a TCP socket.

## Running it

Needs Python 3 with `requests`, a content server with the movies (provided by the course) and a player such as mplayer or VLC.

```bash
pip install requests
python3 programA.py http://<server>/ coco results-a.txt
python3 programB.py http://<server>/ coco results-b.txt
python3 proxy.py http://<server>/ coco 2      # stream track 2 to the player on port 8000
```

## What I learned

- How adaptive streaming works: tracks, segments and manifests
- HTTP partial content requests and measuring throughput
- The producer/consumer pattern with threads and a queue

## Authors

- **Miguel Carmo** ([@MCCProgrammer](https://github.com/MCCProgrammer))
- **Tomás Ramos Alves** ([@Alvesss04](https://github.com/Alvesss04))

---

<sub>The assignment statement is not included in this repository, as it belongs to the course's teaching staff. This is a student project shared for portfolio purposes.</sub>

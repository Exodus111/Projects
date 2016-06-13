import libtorrent as lt
import time

ses = lt.session()
ses.listen_on(6881, 6891)

e = lt.bdecode(open("test.torrent", "rb").read())
info = lt.torrent_info(e)

params = {save_path: ".",
          storage_mode: lt.storage_mode_t.storage_mode_sparse,
          ti: info}

h = ses.add_torrent(params)

while not h.is_seed():
    s = h.status()
    state_str = ["quedued", "checking", "downloading metadata", "downloading", "finished", "seeding", "allocating"]
    print "{} complete (down: {} kb/s up: {} kB/s peers: {}) {}".format(s.progress*100, s.download_rate/1000, s.upload_rate/1000, s.num_peers, state_str[s.state])
    time.sleep(1)